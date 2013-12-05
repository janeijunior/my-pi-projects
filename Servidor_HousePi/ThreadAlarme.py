import thread
import threading
import time
import RPi.GPIO as GPIO 
import EnviaEmail
import Servidor

class ThreadAlarme(threading.Thread):
    def __init__(self, threadID, name, counter, aMcp):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.__stop_thread_event = threading.Event()
       
        @property
        def setMcp():
            self.mcp = aMcp
            
    def stop(self):
        self.mcp.output(10, 0)
        self.__stop_thread_event.set()
    def run(self):            
        while not self.__stop_thread_event.isSet(): 
            input0 = GPIO.input(17) 
            input1 = GPIO.input(18) 
            input2 = GPIO.input(27) 
            input3 = GPIO.input(22) 
            input4 = GPIO.input(23) 
            input5 = GPIO.input(24) 
            input6 = GPIO.input(25) 
            input7 = GPIO.input(4)
            
            if (input0 == 1): 
                print("sensor 0 Normal")
            else:
                print("Sendor 0 Violado!")
                #self.mcp.output(10, 1)
                #time.sleep(5) 
                self.mcp.output(10, 0)
                EnviaEmail.EnviarEmail()
                
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
            
            time.sleep(0.05)
