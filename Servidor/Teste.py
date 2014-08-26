#!/usr/bin/env python

import sys
import thread
import threading
import socket
import sys
import xml.etree.ElementTree as ET

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2342)
    sock.connect(server_address)
    lerDados(sock)
        
def lerDados(sock):
    while True:
        try:
            with open('/dev/tty1', 'r') as tty:
                RFID_input = tty.readline().rstrip()
                
                print "RFID: {0}".format(RFID_input)
                enviarComando(sock, RFID)
                
                tty.close()
        except:
            print "Erro ao abrir o arquivo."

def enviarComando(sock, RFID):
    root = Element("RFID")
    xmlstr = ET.tostring(root) + "\n"       
    sock.send(xmlstr)
            
main()

