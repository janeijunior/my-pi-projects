#!/usr/bin/env python
        
import time
        
import pigpio
        
GPIO_ON=17
GPIO_OFF=22

pigpio.start()

pigpio.set_mode(GPIO_ON, pigpio.OUTPUT)
pigpio.set_mode(GPIO_OFF, pigpio.OUTPUT)

##num_array=('i', [1,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0]) ##84358
    
Pulse_len=350
f1=[]

f1.append(pigpio.pulse(GPIO_ON,GPIO_OFF,Pulse_len*1))
f1.append(pigpio.pulse(GPIO_OFF,GPIO_ON,Pulse_len*1))
f1.append(pigpio.pulse(GPIO_ON,GPIO_OFF,Pulse_len*1))
f1.append(pigpio.pulse(GPIO_OFF,GPIO_ON,Pulse_len*2))
f1.append(pigpio.pulse(GPIO_ON,GPIO_OFF,Pulse_len*1))
f1.append(pigpio.pulse(GPIO_OFF,GPIO_ON,Pulse_len*2))
f1.append(pigpio.pulse(GPIO_ON,GPIO_OFF,Pulse_len*2))
f1.append(pigpio.pulse(GPIO_OFF,GPIO_ON,Pulse_len*4))
f1.append(pigpio.pulse(GPIO_ON,GPIO_OFF,Pulse_len*2))
f1.append(pigpio.pulse(GPIO_OFF,GPIO_ON,Pulse_len*1))

pigpio.wave_clear()

pigpio.wave_add_generic(f1)

pigpio.wave_tx_repeat()

time.sleep(10)

pigpio.wave_tx_stop()

pigpio.stop()