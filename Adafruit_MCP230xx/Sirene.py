from Adafruit_I2C import Adafruit_I2C 
import smbus 
import time 
#import spidev 
from Adafruit_MCP230xx import * 

OUTPUT = 0 
INPUT = 1 

if __name__ == '__main__':
    # Use busnum = 0 for older Raspberry Pi's (pre 512MB) 
    mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
    # Use busnum = 1 for new Raspberry Pi's (512MB) 
    # Set pins 10, 11 and 12 to output (you can set pins 0..15 this way) 
    mcp.config(10, OUTPUT) 
    mcp.config(11, OUTPUT) 
    mcp.config(12, OUTPUT) 
    # Python speed test on output 0 toggling at max speed 
    
    #while (True): 
        #mcp.output(Pin,State) 
    mcp.output(10, 1) # Pin 10 High 
    mcp.output(11, 1) # Pin 11 High 
    mcp.output(12, 1) # Pin 12 High 
    time.sleep(1.2) 
    mcp.output(10, 0) # Pin 10 High 
    mcp.output(11, 0) # Pin 11 High 
    mcp.output(12, 0)