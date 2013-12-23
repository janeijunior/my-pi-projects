#!/usr/bin/python
#-*- coding: utf-8 -*-

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
SIRENE = 10

orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(orig)
tcp.listen(1)

#Conexao com o banco de dados MySQL
conBanco = MySQLdb.connect(host="localhost", user="root", passwd="batistello", db="HousePi")

#variavel para controle do alarme
threadAlarme = None

#variavel para controle da funcao panico do alarme
panicoAlarme = False

#Le os arquivos da pasta passada como parametro
arquivos = os.listdir(os.path.expanduser('/home/pi/HousePi/Musicas/'))

for arquivo in arquivos:
   print arquivo

listaReles = [];

#Configura todos os pinos necessarios para o envio de comandos 
def configurarReles():
    print "Configurando reles..."

    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Rele")

    rows = cursor.fetchall()

    for row in rows:
        rele = Rele.Rele(id = row["Id"], numeroGPIO = row["NumeroGPIO"], status = row["Status"], nome = row["Nome"])        
        listaReles.insert(row["Id"], rele)

    listaReles[12].ligar()

#inicializa o alarme
def configurarAlarme():
    global threadAlarme
    threadAlarme = ThreadAlarme.ThreadAlarme(conBanco = conBanco, sirene = listaReles[SIRENE])

#função para validar o usuario e a senha, se nao estiverem certos desconecta!
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
    try:
        resultado = SensorDHT.lerTemperaturaHumidade()    
        root = Element("TemperaturaHumidade")
        dados = Element("Dados", Temperatura=resultado[0], Humidade=resultado[1])
        root.append(dados)
        
        print "Temperatura: ", resultado[0], " Humidade: ", resultado[1]
        
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)    
    except:
        print "Erro ao obter a temperatura e humidade."
        con.send("Erro\n")
        
#liga ou desliga o alarme
def controlarAlarme(root):
    acao = root.find("Acao").text
    
    global threadAlarme
    
    if acao == "Ligar":
        if threadAlarme.ligado == False:
            configurarAlarme()
            threadAlarme.start() 
            print "Alarme ativado."
    else:
        threadAlarme.stop()
        print "Alarme desativado."
        
    
#liga ou desliga a funcao panico do alarme
def controlarFuncaoPanico(root):
    acao = root.find("Acao").text
    
    global panicoAlarme
    
    if acao == "Ligar":
        listaReles[SIRENE].ligar()
        panicoAlarme = True
    else:
        listaReles[SIRENE].desligar()
        panicoAlarme = False

#funcao que envia as configuracoes dos reles e status
def enviarConfiguracaoStatus():
    root = Element("Reles")
    
    for i in range(0, 10):
        root.append(Element("Rele" + str(i), Status=str(listaReles[i].status), Nome=listaReles[i].nome))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que envia o status do alarme
def enviarConfiguracaoStatus():
    root = Element("Alarme")
    
    root.append(Element("SensorAlarme", Status=str(threadAlarme.status), Ligado=str(int(threadAlarme.ligado))))
    root.append(Element("PanicoAlarme", Ligado=str(int(panicoLigado))))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#cliente conectado, verifica os comandos recebidos
def conectado(con, cliente):    
    while True:
        msg = con.recv(1024)
        comando = msg[2:len(msg)]
     
        if not msg: 
            break
        
        print cliente, "Comando recebido: " + comando
                  
        
        if len(comando) > 0:
            try:
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
                elif root.tag == "StatusRele":
                    enviarConfiguracaoStatus()
                elif root.tag == "StatusAlarme":
            except:
                print "Erro"
                con.send("Erro\n")
                
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

configurarReles()
configurarAlarme()

#inicia a transmisao do video/webcam
os.system('mjpg-streamer/mjpg-streamer.sh start')

print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"

#para fechar o programa
def signal_handler(signal, frame):
    print "\nEncerrando aplicativo..."
    listaReles[12].desligar()
    os.system('mjpg-streamer/mjpg-streamer.sh stop')
    tcp.close;
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))
    
tcp.close()
