import time 
import RPi.GPIO as GPIO 
import Adafruit_MCP230xx

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17,GPIO.IN) #GPIO0 
GPIO.setup(18,GPIO.IN) #GPIO1 
GPIO.setup(27,GPIO.IN) #GPIO2 
GPIO.setup(22,GPIO.IN) #GPIO3 
GPIO.setup(23,GPIO.IN) #gpio4 
GPIO.setup(24,GPIO.IN) #GPIO5 
GPIO.setup(25,GPIO.IN) #GPIO6 
GPIO.setup(4,GPIO.IN) #GPIO7 

print 'Start' #initialise a previous input variable to 0 (assume button not pressed last) 
prev_input0 = 0 


mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

mcp.config(10, mcp.OUTPUT)


while True: 
    #take a reading 
    #print("Lendo sensores...")
    
    input0 = GPIO.input(17) 
    input1 = GPIO.input(18) 
    input2 = GPIO.input(27) 
    input3 = GPIO.input(22) 
    input4 = GPIO.input(23) 
    input5 = GPIO.input(24) 
    input6 = GPIO.input(25) 
    input7 = GPIO.input(4)
    
    #if the last reading was low and this one high, print 
    if (input0 == 1): 
        print("sensor 0 Normal")
    else:
        print("Sendor 0 Violado!")
        mcp.output(10, 1)
        time.sleep(5) 
        mcp.output(10, 0)
        
    if (input1 == 1): 
        print("sensor1") 
    if (input2 == 1): 
        print("sensor2") 
    if (input3 == 1): 
        print("sensor3") 
    if (input4 == 1):
        print("sensor4") 
    if (input5 == 1): 
        print("sensor5") 
    if (input6 == 1): 
        print("sensor6") 
    if (input7 == 1): 
        print("sensor7")
    #slight pause to debounce 
    time.sleep(0.05)