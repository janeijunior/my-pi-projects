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
			
			vTTransmiter = threading.Thread(target=fTransmiter, args=(outPin,))
			vTTransmiter.daemon = True
			vTTransmiter.start()
			
			vTReceiver.join()
			vTTransmiter.join()
	

def fReceiver(inPin):
	t=time()
	ps=None
	st = ''
	while True:
		s = inPin.value
		sleep(0.05)
		if ps!=s:
			if s:
				d = round(time()-t, 1)
				if d == 0.1:
					st += '0'
				elif d == 0.2:
					st += '1'
				else:
					if len(st)>0:
						print(chr(int(st, 2)), end='')
						st = ''
				t=time()
			ps = s
			

def fTransmiter(outPin):
	while True:
		print ('\nWrite something:')
		i = input()
		print ('\nSending. Please wait...\n')
		t=time()
		fSendText(outPin, i)
		print ('\n\nSent = Receive!', '('+str(round(time()-t, 2))+' sec)')

def fTransmiter_Send(outPin, n=0):
	outPin.value=1
	sleep(0.05)
	outPin.value=0
	sleep(0.05)
	if n==1:
		sleep(0.1)
	elif n==-1:
		sleep(0.2)

def fSendText(outPin, s):
	for v in s:
		f = format(ord(v), 'b')
		for b in f:
			fTransmiter_Send(outPin, int(b))
		fTransmiter_Send(outPin, -1)
	fTransmiter_Send(outPin, -1)


if __name__ =='__main__':
	fMain()