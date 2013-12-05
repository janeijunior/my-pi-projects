import socket
import thread
import threading
import time
import Adafruit_MCP230xx
import RPi.GPIO as GPIO 
import os
import commands
import xml.dom.minidom
import ThreadAlarme
import MySQLdb

HOST = ''    # IP do Servidor (em branco = atual)
PORT = 5000  # Porta do Servidor

#Variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

#Conexao com o banco de dados MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="batistello", db="housepi")

# Posiciona o cursor
cursor = db.cursor()

#cursor.execute("SELECT * FROM usuario")
#numrows = int(cursor.rowcount)
#for row in cursor.fetchall():
#   print " ",row[0]," ",row[1]

def getMcp():
    return mcp

def ConfigurarReles():
    print "Configurando reles..."
    
    #Configura todos os pinos necessarios para o envio de comandos 
    for i in range(0, 15):
        mcp.config(i, mcp.OUTPUT)

def ConfigurarSensoresAlarme():
    print "Configurando sendores do alarme..."

    #Configura os pinos dos sensores de alarme para modo leitura
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(17,GPIO.IN) #GPIO0 
    GPIO.setup(18,GPIO.IN) #GPIO1 
    GPIO.setup(27,GPIO.IN) #GPIO2 
    GPIO.setup(22,GPIO.IN) #GPIO3 
    GPIO.setup(23,GPIO.IN) #gpio4 
    GPIO.setup(24,GPIO.IN) #GPIO5 
    GPIO.setup(25,GPIO.IN) #GPIO6 
    GPIO.setup(4,GPIO.IN)  #GPIO7 

def PegarXMLStatusReles():
    doc = xml.dom.minidom.Document()
    root = doc.createElement('Status')
    rele = doc.createElement('Reles')

    for i in range(0, 10):        
        if 1 == 1:
            rele.setAttribute('rele' + str(i), '1')
        else:
            rele.setAttribute('rele' + str(i), '0')
    
    doc.appendChild(root)
    root.appendChild(rele)
    
    return doc

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
                threadalarme = ThreadAlarme.ThreadAlarme(1, "Thread", 1)
                con.sendall("Alarme Ligado")
                threadalarme.start()
            elif comando[2] == "l" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh start')
            elif comando[2] == "l" and comando[3] == "r":
                os.system('mplayer http://p.mm.uol.com.br/metropolitana_alta')            
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
                threadalarme.stop()
            elif comando[2] == "d" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh stop') 
            elif comando[2] == "s" and comando[3] == "t":
                      
                doc = PegarXMLStatusReles()
                      
                print doc.toprettyxml()
            
                con.send(str(doc))
            
            con.send(comando)

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

ConfigurarReles()
ConfigurarSensoresAlarme()

print "Aguardando conexoes..."

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
