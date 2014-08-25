#!/usr/bin/env python

import sys
import thread
import threading

card = ['0007181175', '0008056554']

def main():
    thread = threading.Thread(None, self.lerDados, None, ())
    thread.start()
            
def lerDados(self):
    while True:
        try:
            with open('/dev/tty1', 'r') as tty:
                RFID_input = tty.readline().rstrip()
                
                if RFID_input in card:
                    print "Acesso Permitido: {0}".format(RFID_input)
                else:
                    print "Acesso Negado: {0}".format(RFID_input)
                
                tty.close()
        except:
            print "Erro ao abrir o arquivo."
            
main()

