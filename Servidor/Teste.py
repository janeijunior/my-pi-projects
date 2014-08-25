# python
import serial

s = serial.Serial(
    port='/dev/tty0',
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=3,
    xonxoff=0,
    rtscts=0,
    baudrate=2400
   )

while True:
    try:
        print s.readline()
    except:
        print "Erro"