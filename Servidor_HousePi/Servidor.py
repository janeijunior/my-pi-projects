#!/usr/bin/python

import socket
import thread
import threading
import time
import os
import commands
import xml.dom.minidom
import ThreadAlarme
import MySQLdb
import Rele
import Conexao

HOST = ''    # IP do Servidor (em branco = IP do sistema)
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
    
def configurarReles():
    print "Configurando reles..."
    
    #Configura todos os pinos necessarios para o envio de comandos 
    for i in range(0, 15):
        rele = Rele.Rele(numero = i, status = 0, nome = 'Rele ' + str(i))        
        listaReles.insert(i, rele)

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

#funcao para envio de dados
def enviarDados(con, msg):
    totalenviado = 0
    while totalenviado < socket.MSGLEN:
        sent = con.sock.send(msg[totalenviado:])
        if sent == 0:
            raise RuntimeError("Erro na conexao")
        totalenviado = totalenviado + sent

#funcao para receber dados
def receberDados(con):
    msg = ''
    while len(msg) < socket.MSGLEN:
        chunk = con.sock.recv(socket.MSGLEN-len(msg))
        if chunk == '':
            raise RuntimeError("Erro na conexao")
        msg = msg + chunk
    return msg

#funcao que monitora o recebimento de comandos pelo socket
def conectado(con, cliente):
    print 'Conectado: ', cliente
    
    while True:
        msg = receberDados(con)
        comando = msg.strip() 
     
        if not msg: 
            break
        
        print cliente, "Comando recebido: " + comando
                  
        
        if len(comando) > 0:
            #print "Mensagem recebida -> " + msg.strip()
        
            
            if comando[2] == "l" and str.isdigit(comando[3]) and int(comando[3]) < 10:                
                listaReles[int(comando[3])].ligar()
            elif comando[2] == "l" and comando[3] == "p":
                listaReles[10].ligar()
            elif comando[2] == "l" and comando[3] == "a": # Liga o Alarme
                threadAlarme = ThreadAlarme.ThreadAlarme(tempoDisparo = 5, enviarEmail = 1, usarSirene = 0)
                threadAlarme.start() 
                print "Alarme ativado."
            elif comando[2] == "l" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh start')
            elif comando[2] == "l" and comando[3] == "r":
                os.system('mplayer http://p.mm.uol.com.br/metropolitana_alta')            
            elif comando[2] == "d" and str.isdigit(comando[3]) and int(comando[3]) < 10:
                listaReles[int(comando[3])].desligar()
            elif comando[2] == "d" and comando[3] == "p": 
                listaReles[10].desligar()
            elif comando[2] == "d" and comando[3] == "a": # Desliga o alarme
                threadAlarme.stop()
                print "Alarme desativado."
            elif comando[2] == "d" and comando[3] == "c":
                os.system('mjpg-streamer/mjpg-streamer.sh stop') 
            elif comando[2] == "s" and comando[3] == "t":
                      
                doc = PegarXMLStatusReles()
                      
                print doc.toprettyxml()
            
            
            enviarDados(con, comando)

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(orig)
tcp.listen(1)

configurarReles()

print "Aguardando conexoes..."

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
