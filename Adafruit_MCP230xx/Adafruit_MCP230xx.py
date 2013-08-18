from Adafruit_I2C import Adafruit_I2C 

import smbus 
import time 
import spidev 
from Adafruit_MCP230xx import * 

OUTPUT = 0 
INPUT = 1 

if __name__ == '__main__': 
    # Use busnum = 0 for older Raspberry Pi's (pre 512MB) 
    mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16) 
    
    # Use busnum = 1 for new Raspberry Pi's (512MB) 
    # Set pins 0, 1 and 2 to output (you can set pins 0..15 this way) 
    
    mcp.config(0, OUTPUT) 
    mcp.config(1, OUTPUT) 
    mcp.config(2, OUTPUT) 
    mcp.config(3, OUTPUT) 
    mcp.config(4, OUTPUT) 
    mcp.config(5, OUTPUT) 
    mcp.config(6, OUTPUT) 
    mcp.config(7, OUTPUT) 
    mcp.config(8, OUTPUT) 
    mcp.config(9, OUTPUT) 
    
    # Set pin 3 to input with the pullup resistor enabled 
    # mcp.pullup(3, 1) 
    # Read pin 3 and display the results 
    # print "%d: %x" % (3, mcp.input(3) >> 3) 
    # Python speed test on output 0 toggling at max speed 
    
    while (True): #mcp.output(Pin,State) 
      mcp.output(1, 1) # Pin 0 High
      mcp.output(0, 1) # Pin 0 High 
      mcp.output(2, 1) # Pin 0 High 
      mcp.output(3, 1) # Pin 0 High 
      mcp.output(4, 1) # Pin 0 High 
      mcp.output(5, 1) # Pin 0 High 
      mcp.output(6, 1) # Pin 0 High 
      mcp.output(7, 1) # Pin 0 High 
      mcp.output(8, 1) # Pin 0 High 
      mcp.output(9, 1) # Pin 0 High 
      time.sleep(1.2) 
      mcp.output(1, 0) # Pin 1 Low 
      mcp.output(0, 0) # Pin 1 Low 
      mcp.output(2, 0) # Pin 0 High 
      mcp.output(3, 0) # Pin 0 High 
      mcp.output(4, 0) # Pin 0 High 
      mcp.output(5, 0) # Pin 0 High 
      mcp.output(6, 0) # Pin 0 High 
      mcp.output(7, 0) # Pin 0 High 
      mcp.output(8, 0) # Pin 0 High 
      mcp.output(9, 0) # Pin 0 High 
      time.sleep(1.2)