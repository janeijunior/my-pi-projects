import socket
import thread
import threading
import time
import Adafruit_MCP230xx
import RPi.GPIO as GPIO 
import os
import commands
import xml.dom.minidom

HOST = '192.168.5.125'  # IP do Servidor
PORT = 5000            # Porta do Servidor

mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)



def ConfigurarRelesEscrita
    print "Configurando reles para escrita..."
    
    mcp.config(0, mcp.OUTPUT)
    mcp.config(1, mcp.OUTPUT)
    mcp.config(2, mcp.OUTPUT)
    mcp.config(3, mcp.OUTPUT)
    mcp.config(4, mcp.OUTPUT)
    mcp.config(5, mcp.OUTPUT)
    mcp.config(6, mcp.OUTPUT)
    mcp.config(7, mcp.OUTPUT)
    mcp.config(8, mcp.OUTPUT)
    mcp.config(9, mcp.OUTPUT)  #Cooler

  def ConfigurarRelesLeitura:
    mcp.config(0, mcp.INPUT)
    mcp.config(1, mcp.INPUT)
    mcp.config(2, mcp.INPUT)
    mcp.config(3, mcp.INPUT)
    mcp.config(4, mcp.INPUT)
    mcp.config(5, mcp.INPUT)
    mcp.config(6, mcp.INPUT)
    mcp.config(7, mcp.INPUT)
    mcp.config(8, mcp.INPUT)
    mcp.config(9, mcp.INPUT)  #Cooler

mcp.config(10, mcp.OUTPUT) #Sirene Alarme

print "Configurando sendores do alarme..."

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17,GPIO.IN) #GPIO0 
GPIO.setup(18,GPIO.IN) #GPIO1 
GPIO.setup(27,GPIO.IN) #GPIO2 
GPIO.setup(22,GPIO.IN) #GPIO3 
GPIO.setup(23,GPIO.IN) #gpio4 
GPIO.setup(24,GPIO.IN) #GPIO5 
GPIO.setup(25,GPIO.IN) #GPIO6 
GPIO.setup(4,GPIO.IN) #GPIO7 

prev_input0 = 0 

print "Aguardando conexoes..."

class ThreadAlarme(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.__stop_thread_event = threading.Event()
    def stop(self):
        mcp.output(10, 0)
        self.__stop_thread_event.set()
    def run(self):        
        while not self.__stop_thread_event.isSet(): 
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
                print("Sendor 0 Violado!")
                mcp.output(10, 1)
                time.sleep(5) 
                mcp.output(10, 0)
                
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
            #slight pause to debounce 
            time.sleep(0.05)

def conectado(con, cliente):
    print 'Conectado: ', cliente

    while True:
        msg = con.recv(1024)
        comando = msg.strip() 
     
        if not msg: 
            break
        
        print cliente, "Comando recebido: " + comando
                  
        
        if len(comando) > 0:
            #print "Mensagem recebida -> " + msg.strip()
            
            if comando[2] == "l" and comando[3] == "0":
                mcp.output(0, 1)
            elif comando[2] == "l" and comando[3] == "1":
                mcp.output(1, 1)
            elif comando[2] == "l" and comando[3] == "2":
                mcp.output(2, 1)
            elif comando[2] == "l" and comando[3] == "3":
                mcp.output(3, 1)
            elif comando[2] == "l" and comando[3] == "4":
                mcp.output(4, 1)
            elif comando[2] == "l" and comando[3] == "5":
                mcp.output(5, 1)
            elif comando[2] == "l" and comando[3] == "6":
                mcp.output(6, 1)
            elif comando[2] == "l" and comando[3] == "7":
                mcp.output(7, 1)
            elif comando[2] == "l" and comando[3] == "8":
                mcp.output(8, 1)
            elif comando[2] == "l" and comando[3] == "9":
                mcp.output(9, 1)
            elif comando[2] == "l" and comando[3] == "p":
                mcp.output(10, 1)
            elif comando[2] == "l" and comando[3] == "a": # Liga o Alarme
                thread1 = ThreadAlarme(1, "Thread-1", 1)
                thread1.start()
            elif comando[2] == "l" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh start')                
            elif comando[2] == "d" and comando[3] == "0":
                mcp.output(0, 0)
            elif comando[2] == "d" and comando[3] == "1":
                mcp.output(1, 0)
            elif comando[2] == "d" and comando[3] == "2":
                mcp.output(2, 0)
            elif comando[2] == "d" and comando[3] == "3":
                mcp.output(3, 0)
            elif comando[2] == "d" and comando[3] == "4":
                mcp.output(4, 0)
            elif comando[2] == "d" and comando[3] == "5":
                mcp.output(5, 0)
            elif comando[2] == "d" and comando[3] == "6":
                mcp.output(6, 0)
            elif comando[2] == "d" and comando[3] == "7":
                mcp.output(7, 0)
            elif comando[2] == "d" and comando[3] == "8":
                mcp.output(8, 0)
            elif comando[2] == "d" and comando[3] == "9":
                mcp.output(9, 0)
            elif comando[2] == "d" and comando[3] == "p": 
                mcp.output(10, 0)
            elif comando[2] == "d" and comando[3] == "a": # Desliga o alarme
                thread1.stop()
            elif comando[2] == "d" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh stop') 
            elif comando[2] == "s" and comando[3] == "t":
                doc = xml.dom.minidom.Document()
                root = doc.createElement('Status')
                rele = doc.createElement('Rele')
                rele.setAttribute('rele1', mcp.input(0))
                rele.setAttribute('rele1', mcp.input(1))
                rele.setAttribute('rele1', mcp.input(2))
                rele.setAttribute('rele1', mcp.input(3))
                rele.setAttribute('rele1', mcp.input(4))
                rele.setAttribute('rele1', mcp.input(5))
                rele.setAttribute('rele1', mcp.input(6))
                rele.setAttribute('rele1', mcp.input(7))
                rele.setAttribute('rele1', mcp.input(8))
                rele.setAttribute('rele1', mcp.input(9))  
                
                doc.appendChild(root)
                root.appendChild(rele)
                
                print doc.toprettyxml()
                
                con.send(doc)
                
            #else:
            #    print "Comando invalido!"

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
