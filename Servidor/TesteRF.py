#!/usr/bin/env python
#----------------------------------------------------------------------------
# Simple set of classes to read and write packets over RF through a serial
# port.
#----------------------------------------------------------------------------
from sys import argv
from time import sleep
from struct import pack, unpack
from random import randint

# Make sure we have pyserial
try:
  import serial
except:
  print "This script requires the PySerial module. Please try ..."
  print "  pip install pyserial"
  exit(1)

# Defaults
MARKER     = 0xAA
BAUD_RATE  = 150
PORT_NAME  = "/dev/ttyS0"
WAIT_DELAY = 12.0 / BAUD_RATE

#----------------------------------------------------------------------------
# Helper functions
#----------------------------------------------------------------------------

# High bytes lookup table
CRC16_LOOKUP_HIGH = (
  0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
  0x81, 0x91, 0xA1, 0xB1, 0xC1, 0xD1, 0xE1, 0xF1
  )

# Low bytes lookup table
CRC16_LOOKUP_LOW = (
  0x00, 0x21, 0x42, 0x63, 0x84, 0xA5, 0xC6, 0xE7,
  0x08, 0x29, 0x4A, 0x6B, 0x8C, 0xAD, 0xCE, 0xEF
  )

def generateCRC(data, offset, size):
  """ Generate a 16 bit CCITT CRC value for a block of data
      See http://www.digitalnemesis.com/info/codesamples/embeddedcrc16/
  """
  crcLow = 0xFF
  crcHigh = 0xFF
  # Helper to update the CRC with another 4 bits
  def updateCRC(value, crcLow, crcHigh):
    # Extract the most significant 4 bits
    temp = (crcHigh >> 4) & 0x0F
    # XOR in the message data
    temp = temp ^ (value & 0x0F)
    # Shift the CRC left 4 bits
    crcHigh = ((crcHigh << 4) & 0xF0) | ((crcLow >> 4) & 0x0F)
    crcLow = (crcLow << 4) & 0xF0
    # XOR the table lookup results into the CRC
    crcHigh = crcHigh ^ CRC16_LOOKUP_HIGH[temp]
    crcLow = crcLow ^ CRC16_LOOKUP_LOW[temp]
    # Return the new low, high values
    return crcLow, crcHigh
  # Now process the data
  for index in range(size):
    crcLow, crcHigh = updateCRC((data[offset + index] >> 4) & 0x0F, crcLow, crcHigh)
    crcLow, crcHigh = updateCRC(data[offset + index] & 0x0F, crcLow, crcHigh)
  # All done
  return crcLow, crcHigh

#----------------------------------------------------------------------------
# Classes for communication
#----------------------------------------------------------------------------

class RF433:
  """ Class for RF433 communications
  """
  def __init__(self, port = PORT_NAME, baud = BAUD_RATE, timeout = WAIT_DELAY):
    self.serial = serial.Serial(port, baud, timeout = timeout)
    self.packet = list()

  def send(self, data, offset = 0, size = -1):
    """ Send a message
    """
    # Check the size
    if size < 0:
      size = len(data) - offset
    if size > 255:
      raise Exception("Data exceeds maximum packet length")
    # Build up the data packet
    packet = [ MARKER, MARKER, size, ]
    for index in range(size):
      packet.append(ord(data[index]) & 0xFF)
    # Generate the CRC for the packet
    crcLow, crcHigh = generateCRC(packet, 2, len(packet) - 2)
    # And append it
    packet.append(crcLow)
    packet.append(crcHigh)
    # Now send the packet
    packet = "".join([ chr(x) for x in packet ])
    self.serial.write(packet)
    return packet[2:]

  def read(self):
    """ Read a packet from the serial port.

      Returns a block of data representing a valid packet or None if no
      packet is available. The data returned is the entire packet including
      the one byte length header and the trailing 16 bit CRC.

      All the bytes of a packet must be sent within 1 byte length of each
      other (baud / 10) seconds. Any longer delay is considered an error.
    """
    # Start reading data
    while True:
      data = self.serial.read(1)
      if len(data) < 1:
        return None # Read timeout
      self.packet.append(ord(data[0]))
      # Look for the two markers to signify the start of a packet
      while len(self.packet) >= 3:
        # Skip forward to the first marker
        if self.packet[0] <> MARKER:
          self.packet = self.packet[1:]
          continue
        # Check for the second one
        if self.packet[1] <> MARKER:
          self.packet = self.packet[2:]
          continue
        # We potentially have a packet, check the length
        size = self.packet[2]
        if len(self.packet) >= (size + 5): # Allow for markers, length and CRC
          # Check the CRC for the packet
          crcLow, crcHigh = generateCRC(self.packet, 2, size + 1)
          if (crcLow <> self.packet[size + 3]) or (crcHigh <> self.packet[size + 4]):
            # Invalid, skip start byte and loop around
            print "Bad CRC - got %02x%02x, wanted %02x%02x" % (
              crcHigh, crcLow,
              self.packet[size + 4], self.packet[size + 3]
              )
            self.packet = self.packet[1:]
            continue
          # Found a packet, return it as a string (for unpacking)
          result = "".join([ chr(x) for x in self.packet[2:size + 5]])
          self.packet = self.packet[size + 5:]
          return result
        else:
          break # Not a valid self.packet, too short

#----------------------------------------------------------------------------
# Main program
#----------------------------------------------------------------------------

if __name__ == "__main__":
  # Dump everything we know about a packet
  def dumpPacket(packet):
    size, sequence = unpack(">BH", packet[:3])
    crcLow, crcHigh = unpack("BB", packet[-2:])
    return "%d,%d,%02x%02x,%s" % (
      size,
      sequence,
      crcHigh,
      crcLow,
      "".join([ "%02x" % ord(x) for x in packet ])
      )
  # Create a packet
  def createPacket(sequence):
    size = randint(0, 253) # Allow two bytes for sequence number
    packet = pack(">H", sequence)
    while len(packet) < size:
      packet = packet + chr(randint(0, 255))
    return packet
  # Main program
  if len(argv) <> 3:
    print "Usage:\n"
    print "       rf433.py port tx|rx"
    exit(1)
  # Set up communications
  rf433 = RF433(argv[1])
  if argv[2] == "tx":
    # Open the log file
    logfile = open("rf433_tx.log", "w+")
    for sequence in range(1000):
      packet = rf433.send(createPacket(sequence))
      sequence = sequence + 1
      print dumpPacket(packet)
      logfile.write("%s\n" % dumpPacket(packet))
      # Wait for the packet to be transmitted + up to 5 seconds
      delay = 12.0 / BAUD_RATE * len(packet) + 1.0 * randint(0, 5)
      print "Waiting for %4.2f seconds" % delay
      sleep(delay)
  elif argv[2] == "rx":
    # Open the log file
    logfile = open("rf433_rx.log", "w+")
    while True:
      packet = rf433.read()
      if packet is not None:
        print dumpPacket(packet)
        logfile.write("%s\n" % dumpPacket(packet))
  else:
    print "Unknown option '%s' - use 'tx' or 'rx'" % argv[2]
    exit(1)