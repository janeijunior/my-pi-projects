import serial

serial = serial.Serial("/dev/tty", baudrate=9600)

code = ''

while True:
        data = serial.readline()
        
        if data == '\r':
                print(code)
                code = ''
        else:
                code = code + data