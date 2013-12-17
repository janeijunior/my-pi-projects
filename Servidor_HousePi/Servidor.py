#!/usr/bin/python

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import socket
import thread
import threading
import time
import os
import commands
import ThreadAlarme
import MySQLdb
import Rele
import signal
import sys
import SensorDHT

HOST = ''    # IP do Servidor (em branco = IP do sistema)
PORT = 5000  # Porta do Servidor

orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(orig)
tcp.listen(1)

#Conexao com o banco de dados MySQL
conBanco = MySQLdb.connect(host="localhost", user="root", passwd="batistello", db="HousePi")

#Le os arquivos da pasta passada como parametro
arquivos = os.listdir(os.path.expanduser('/home/pi/HousePi/Musicas/'))

for arquivo in arquivos:
   print arquivo

listaReles = [];

def configurarReles():
    #Configura todos os pinos necessarios para o envio de comandos 
    print "Configurando reles..."

    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Rele")

    rows = cursor.fetchall()

    for row in rows:
        rele = Rele.Rele(id = row["Id"], numeroGPIO = row["NumeroGPIO"], status = row["Status"], nome = row["Nome"])        
        listaReles.insert(row["Id"], rele)

    listaReles[12].ligar()

#funcao para validar o usuario e a senha, se nao estiverem certos desconecta!
def efetuarLogin(root):
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select Usuario, Senha from Configuracao")
    
    row = cursor.fetchone()
    
    usuario = root.find("Usuario").text
    senha = root.find("Senha").text
    
    if row["Usuario"] == usuario and row["Senha"]  == senha:
        print "Conectado: ", cliente
        con.send("Logado\n")
    else:
        print "Usuario ou senha invalidos."
        con.send("NaoLogado\n")
        con.close
        thread.exit()

#liga ou desliga os reles/atuadores
def controlarRele(root):
    acao = root.find("Acao").text
    numero = root.find("Numero").text
    
    if acao == "Ligar":
        listaReles[int(numero)].ligar()
    else:
        listaReles[int(numero)].desligar()
        
#le o sensor de temperatura e humidade e envia os resultados
def enviarTemperaturaHumidade():    
    resultado = SensorDHT.lerTemperaturaHumidade()    
    root = Element("TemperaturaHumidade")
    dados = Element("Dados", Temperatura=resultado[0], Humidade=resultado[1])
    root.append(dados)
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)    

#liga ou desliga o alarme
def controlarAlarme(root):
    
#liga ou desliga a funcao panico do alarme
def controlarFuncaoPanico(root):
    

#cliente conectado, verifica os comandos recebidos
def conectado(con, cliente):    
    while True:
        msg = con.recv(1024)
        comando = msg[2:len(msg)]
     
        if not msg: 
            break
        
        print cliente, "Comando recebido: " + comando
                  
        
        if len(comando) > 0:
            #root = XML recebido/elemento principal
            root = ET.fromstring(comando)
        
            if root.tag == "Logar":
                efetuarLogin(root = root)
            elif root.tag == "Rele":
                controlarRele(root)
            elif root.tag == "Temperatura":
                enviarTemperaturaHumidade()
            elif root.tag == "Alarme":
                controlarAlarme(root)
            elif root.tag == "Panico":
                controlarFuncaoPanico(root)           
            
            
            #if comando[2] == "l" and str.isdigit(comando[3]) and int(comando[3]) < 10:
            #    listaReles[int(comando[3])].ligar()
            #elif comando[2] == "l" and comando[3] == "p":
            #    listaReles[10].ligar()
            #elif comando[2] == "l" and comando[3] == "a": # Liga o Alarme
            #    threadAlarme = ThreadAlarme.ThreadAlarme(conBanco = conBanco)
            #    threadAlarme.start() 
            #    print "Alarme ativado."
            #elif comando[2] == "l" and comando[3] == "c":
            #    os.system('mjpg-streamer/mjpg-streamer.sh start')
            #elif comando[2] == "l" and comando[3] == "r":
            #    os.system('mplayer http://p.mm.uol.com.br/metropolitana_alta')            
            #elif comando[2] == "d" and str.isdigit(comando[3]) and int(comando[3]) < 10:
            #    listaReles[int(comando[3])].desligar()
            #elif comando[2] == "d" and comando[3] == "p": 
            #    listaReles[10].desligar()
            #elif comando[2] == "d" and comando[3] == "a": # Desliga o alarme
            #    threadAlarme.stop()
            #    print "Alarme desativado."
            #elif comando[2] == "d" and comando[3] == "c":
            #    os.system('mjpg-streamer/mjpg-streamer.sh stop') 
            #elif comando[2] == "s" and comando[3] == "t":
            #          
            #    doc = PegarXMLStatusReles()
            #          
            #    print doc.toprettyxml()
            #    
            #    con.send(str(doc))
            
            #con.send(comando)

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

configurarReles()

#inicia a transmisao do video/webcam
os.system('mjpg-streamer/mjpg-streamer.sh start')

print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"

#para fechar o programa
def signal_handler(signal, frame):
    print "\nEncerrando aplicativo..."
    os.system('mjpg-streamer/mjpg-streamer.sh stop')
    tcp.close;
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))
    
tcp.close()
