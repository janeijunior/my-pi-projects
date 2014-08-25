# python
import serial

s = serial.Serial(
    '/dev/tty0',
    port=0,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=3,
    xonxoff=0,
    rtscts=0,
    baudrate=2400
   )

print s.readline()