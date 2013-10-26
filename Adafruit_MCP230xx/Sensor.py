import time 
import RPi.GPIO as GPIO 
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
        print("Sensor 0 violado!")
    
    if (input1 == 1): 
        print("sensor 1 Normal")
    else:
        print("Sensor 1 violado!")
    
    if (input2 == 1): 
        print("sensor 2 Normal") 
    else:
        print("Sensor 2 violado!")
        
    if (input3 == 1): 
        print("sensor 3 Normal") 
    else:
        print("Sensor 3 violado!")
    
    if (input4 == 1):
        print("sensor 4 Normal") 
    else:
        print("Sensor 4 violado!")
    
    if (input5 == 1): 
        print("sensor 5 Normal") 
    else:
        print("Sensor 5 violado!")
    
    if (input6 == 1): 
        print("sensor 6 Normal") 
    else:
        print("Sensor 6 violado!")
        
    if (input7 == 1): 
        print("sensor 7 Normal")
    else:
        print("Sensor 7 violado!")
    
    #slight pause to debounce 
    time.sleep(0.05)