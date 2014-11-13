from quick2wire.gpio import pi_header_1, In, Out, Rising, Falling, Both
from os import system
import threading
from time import sleep, time


def fMain():
    with pi_header_1.pin(7, direction=In) as inPin:
		with pi_header_1.pin(11, direction=Out) as outPin:
		
			vTReceiver = threading.Thread(target=fReceiver, args=(inPin,))
			vTReceiver.daemon = True
			vTReceiver.start()
			
			vTTransmitter = threading.Thread(target=fTransmiter, args=(outPin,))
			vTTransmitter.daemon = True
			vTTransmitter.start()
			
			vTReceiver.join()
			vTTransmitter.join()
	

def fReceiver(inPin):
	t=time()
	d=0
	ps=None
	st = ''
	str=''
	while True:
		s = inPin.value
		sleep(0.0005)
		if ps!=s:
			if s:
				d = round(time()-t, 3)
				if d < 0.02:
					st += '1'
				elif d >= 0.02 and d <= 0.03:
					st += '0'
				elif d > 0.03 and d < 0.2:
					if len(st)>0:
						str+=chr(int(st, 2))
						st = ''
				t=time()
			ps = s
		d2 = round(time()-t, 3)
		if d2 > 0.2 and str!='':
				print('\nReceived:\n'+str)
				str=''
			

def fTransmiter(outPin):
	while True:
		print ('\nWrite something:')
		i = input()
		if i=='':
			continue
		print ('\nSending. Please wait...\n')
		t=time()
		fSendText(outPin, i)
		print ('Sent in '+str(round(time()-t, 2))+' seconds')
		sleep(1)

def fTransmiter_Send(outPin, n=0):
	outPin.value=1
	sleep(0.005)
	outPin.value=0
	sleep(0.005)
	if n==0:
		sleep(0.01)
	elif n==-1:
		sleep(0.03)

def fSendText(outPin, s):
	b = bytes(s, 'utf-8')
	for v in b:
		f = format(v, 'b')#.zfill(8)
		for b in f:
			fTransmiter_Send(outPin, int(b))
		fTransmiter_Send(outPin, -1)
	fTransmiter_Send(outPin, -1)


if __name__ =='__main__':
	fMain()