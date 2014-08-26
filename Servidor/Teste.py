#!/usr/bin/env python

import sys
import thread
import threading
import socket
import sys
import Funcoes
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', int(int(Funcoes.lerConfiguracaoIni("Porta"))))
        sock.connect(server_address)
    except:
        print "Erro ao conectar no servidor."
        
    lerDados(sock)
        
def lerDados(sock):
    while True:
        try:
            with open('/dev/tty1', 'r') as tty:
                RFID_input = tty.readline().rstrip()
                
                print "RFID: {0}".format(RFID_input)
                enviarComando(sock, RFID_input)
                
                tty.close()
        except:
            print "Erro ao abrir o arquivo."

def enviarComando(sock, RFID):
    root = Element("RFID")
    cartao = Element("Cartao").text = RFID
    root.append(cartao)
    xmlstr = ET.tostring(root) + "\n"       
	
    print xmlstr
    
    try:
        sock.sendall(xmlstr)
    except:
        print "Erro ao enviar o RFID."
    
main()

