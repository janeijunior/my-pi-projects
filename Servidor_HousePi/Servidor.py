import socket
import thread
import threading
import time
import RPi.GPIO as GPIO 
import os
import commands
import xml.dom.minidom
import ThreadAlarme
import MySQLdb
import Rele

HOST = ''    # IP do Servidor (em branco = atual)
PORT = 5000  # Porta do Servidor

#Conexao com o banco de dados MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="batistello", db="housepi")

# Posiciona o cursor
cursor = db.cursor()

#cursor.execute("SELECT * FROM usuario")
#numrows = int(cursor.rowcount)
#for row in cursor.fetchall():
#   print " ",row[0]," ",row[1]

#Le os arquivos da pasta passada como parametro
arquivos = os.listdir(os.path.expanduser('/home/pi/HousePi/Musicas/'))

for arquivo in arquivos:
   print arquivo

listaReles = [];

def ConfigurarReles():
    print "Configurando reles..."
    
    #Configura todos os pinos necessarios para o envio de comandos 
    for i in range(0, 15):
        rele = Rele.Rele(numero = i, status = 0, nome = 'Rele ' + i)
        rele.configurar()
        
        listaReles.insert(i, rele)


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
        
            
            if comando[2] == "l" and int(comando[3]) < 10:                
                listaReles[int(comando[3])].ligar()
            elif comando[2] == "l" and comando[3] == "p":
                listaReles[10].ligar()
            elif comando[2] == "l" and comando[3] == "a": # Liga o Alarme
                threadalarme = ThreadAlarme.ThreadAlarme(1, "Thread", 1)
                con.sendall("Alarme Ligado")
                threadalarme.start()
            elif comando[2] == "l" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh start')
            elif comando[2] == "l" and comando[3] == "r":
                os.system('mplayer http://p.mm.uol.com.br/metropolitana_alta')            
            elif comando[2] == "d" and int(comando[3]) < 10:
                listaReles[0].desligar()
            elif comando[2] == "d" and comando[3] == "p": 
                listaReles[10].desligar()
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
