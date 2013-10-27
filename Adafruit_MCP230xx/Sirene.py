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
    # Set pins 10, 11 and 12 to output (you can set pins 0..15 this way) 
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
    mcp.config(10, OUTPUT)
    mcp.config(11, OUTPUT) 
    mcp.config(12, OUTPUT)
    mcp.config(13, OUTPUT)
    mcp.config(14, OUTPUT)
    mcp.config(15, OUTPUT)
    # Python speed test on output 0 toggling at max speed 
    
    #while (True): 
    #mcp.output(Pin,State) 
    print "LIGANDO"
    mcp.output(0, 1)
    mcp.output(1, 1)
    mcp.output(2, 1)
    mcp.output(3, 1)
    mcp.output(4, 1)
    mcp.output(5, 1)
    mcp.output(6, 1)
    mcp.output(7, 1)
    mcp.output(8, 1)
    mcp.output(9, 1)
    mcp.output(10, 1) # Pin 10 High 
    mcp.output(11, 1) # Pin 11 High 
    mcp.output(12, 1) # Pin 12 High 
    mcp.output(13, 1)
    mcp.output(14, 1)
    mcp.output(15, 1)
    time.sleep(5) 
    print "DESLIGANDO"
    mcp.output(0, 0)
    mcp.output(1, 0)
    mcp.output(2, 0)
    mcp.output(3, 0)
    mcp.output(4, 0)
    mcp.output(5, 0)
    mcp.output(6, 0)
    mcp.output(7, 0)
    mcp.output(8, 0)
    mcp.output(9, 0) # Pin 10 High 
    mcp.output(10, 0)
    mcp.output(11, 0) # Pin 11 High 
    mcp.output(12, 0)
    mcp.output(13, 0)
    mcp.output(14, 0)
    mcp.output(15, 0)