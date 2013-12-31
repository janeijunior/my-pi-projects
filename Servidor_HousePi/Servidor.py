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
import Alarme
import MySQLdb
import Rele
import signal
import sys
import SensorDHT
import Funcoes
import Agendamento
import ThreadAgendamento
import subprocess
import select

HOST = ''    # IP do Servidor (em branco = IP do sistema)
PORT = 5000  # Porta do Servidor
SIRENE = 10

orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(orig)
tcp.listen(1)

#variavel para controle do alarme
alarme = None

#variavel para controle do agendamento
threadAgendamento = None
listaAgendamento = []

#lista dos reles
listaReles = [];

#variavel para controle do subprocesso do mplayer do linux
controleMPlayer = None

#Configura todos os pinos necessarios para o envio de comandos 
def configurarReles():
    print "Configurando reles..."

    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Rele")

    rows = cursor.fetchall()

    for row in rows:
        rele = Rele.Rele(id = row["Id"], numeroGPIO = row["NumeroGPIO"], status = row["Status"], nome = row["Nome"])        
        listaReles.insert(row["Id"], rele)
    
    conBanco.close()

    listaReles[12].ligar()

#inicializa o alarme
def configurarAlarme():
    global alarme
    
    alarme = Alarme.Alarme(sirene=listaReles[SIRENE])

#inicializar thread do agendamento
def iniciarAgendamento():
    global threadAgendamento
    global listaAgendamento
    
    threadAgendamento = ThreadAgendamento.ThreadAgendamento(listaAgendamento)
    threadAgendamento.start() 
        
#carregar lista de agendamentos
def carregarListaAgendamento():
    print "Carregando agendamentos..."

    global alarme
    global listaAgendamento
    
    listaAgendamento = []

    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Agendamento where Ativo = 1")

    rows = cursor.fetchall()

    for row in rows:
        if int(row["EhAlarme"]) == 1:
            agendamento = Agendamento.Agendamento(id = row["Id"], nome = row["Nome"], 
                          dataHoraInicial = row["DataHoraInicial"], dataHoraFinal = row["DataHoraFinal"], 
                          alarme = alarme, rele = None, ativo = int(row["Ativo"]))        
        else:
            agendamento = Agendamento.Agendamento(id = row["Id"], nome = row["Nome"], 
                          dataHoraInicial = row["DataHoraInicial"], dataHoraFinal = row["DataHoraFinal"], 
                          alarme = None, rele = listaReles[int(row["IdRele"])], ativo = row["Ativo"])                
            
        listaAgendamento.insert(row["Id"], agendamento)
    
    conBanco.close()
    
        
#função para validar o usuario e a senha, se nao estiverem certos desconecta!
def efetuarLogin(root):
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select Usuario, Senha from Configuracao")
    
    row = cursor.fetchone()
    
    usuario = root.find("Usuario").text
    senha = root.find("Senha").text
    
    conBanco.close()
    
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
    
    con.send("Ok\n")
        
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
    
    global alarme
    
    if acao == "Ligar":
        if alarme.alarmeLigado == False:
            alarme.ligarAlarme() 
            print "Alarme ativado."
    else:
        alarme.desligarAlarme()
        print "Alarme desativado."
    
    con.send("Ok\n")
        
    
#liga ou desliga a funcao panico do alarme
def controlarFuncaoPanico(root):
    acao = root.find("Acao").text
    
    global alarme
    
    if acao == "Ligar":
        alarme.ligarPanicoAlarme()
    else:
        alarme.desligarPanicoAlarme()
    
    con.send("Ok\n")
    
#funcao que envia as configuracoes dos reles e status
def enviarConfiguracaoStatusRele():
    root = Element("Reles")
    
    for rele in listaReles:
        root.append(Element("Rele" + str(rele.id), Status=str(rele.status), Nome=rele.nome))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que envia o status do alarme
def enviarConfiguracaoStatusAlarme():
    root = Element("Alarme")
    
    global alarme
    
    root.append(Element("SensorAlarme", Status=str(alarme.getStatusAlarme()), Ligado=str(int(alarme.alarmeLigado))))
    root.append(Element("PanicoAlarme", Ligado=str(int(alarme.panicoAlarmeLigado))))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que insere um novo agendamento no banco de dados e alualiza a lista de agendamentos
def gravarAgendamento(root):
    
    global alarme
    
    #se for alarme = -1
    if root.find("Equipamento").text == "-1":
        agendamento = Agendamento.Agendamento(id = 0, nome = root.find("Nome").text, dataHoraInicial = 
                                              root.find("DataHoraInicial").text, dataHoraFinal = root.find("DataHoraFinal").text,
                                              alarme = alarme, rele = None, ativo = 1)
    else:
        agendamento = Agendamento.Agendamento(id = 0, nome = root.find("Nome").text, dataHoraInicial = 
                                              root.find("DataHoraInicial").text, dataHoraFinal = root.find("DataHoraFinal").text,
                                              alarme = None, rele = listaReles[int(root.find("Equipamento").text)], ativo = 1)        
    
    if agendamento.gravarRegistroBanco():
        con.send("Ok\n")
        
        #carrega os novos agendamentos
        carregarListaAgendamento()
        
        global threadAgendamento
        global listaAgendamento
        
        #passa a nova lista para a thread
        threadAgendamento.listaAgendamento = listaAgendamento
    else:
        con.send("Erro\n")

#funcao que retorna os agendamentos do servidor para o aplicativo movel
def enviarAgendamento():
    root = Element("EnviarAgendamento")
    
    #atualiza a lista de agendamentos
    carregarListaAgendamento()
    
    global listaAgendamento
    
    for agendamento in listaAgendamento:
        if agendamento.alarme == None:
            root.append(Element("Agendamento" + str(agendamento.id), Id=str(agendamento.id), Nome=agendamento.nome, 
                                DataHoraInicial=str(agendamento.dataHoraInicial), DataHoraFinal=str(agendamento.dataHoraFinal),
                                EhAlarme="0", IdRele=str(agendamento.rele.id), NomeRele=agendamento.rele.nome))   
        else:
            root.append(Element("Agendamento" + str(agendamento.id), Id=str(agendamento.id), Nome=agendamento.nome, 
                                DataHoraInicial=str(agendamento.dataHoraInicial), DataHoraFinal=str(agendamento.dataHoraFinal),
                                EhAlarme="1"))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que remove o agendamento da lita e do banco de dados conforme solicitado
def removerAgendamento(root):
    global threadAgendamento
    global listaAgendamento
    
    for agendamento in listaAgendamento:
        if agendamento.id == int(root.find("Id").text):
            if agendamento.removerRegistroBanco():
                con.send("Ok\n")
                
                #atualiza a lista de agendamentos
                carregarListaAgendamento()
                
                #passa a nova lista de agendamentos para a thread
                threadAgendamento.listaAgendamento = listaAgendamento
            
                break
            else:
                con.send("Erro\n")

#funcao para alterar o usuario e a senha
def alterarUsuarioSenha(root):
    try:
        usuario = root.find("Usuario").text
        senha = root.find("Senha").text
        
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'".format(novoUsuario = usuario, novaSenha = senha)
        print sql
        
        cursor.execute(sql)
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")
            
#funcao para renomear os reles atraves da aba de configuracoes
def alterarConfiguracaoRele(root):
    try:
        global listaReles
        
        for child in root:
            listaReles[int(child.get("Id"))].nome = str(child.get("Nome")) 
            listaReles[int(child.get("Id"))].gravarNomeBanco();
        
        con.send("Ok\n")
    except:
        con.send("Erro\n")
        
#funcao que grava a nova configuracao de email
def alterarConfiguracaoEmail(root):
    try:
        usuario = root.find("Usuario").text
        senha = root.find("Senha").text
        destinatario = root.find("Destinatario").text
        servidor = root.find("Servidor").text
        porta = root.find("Porta").text
                
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = '''update Configuracao 
                    set RemetenteEmail = '{novoUsuario}', 
                        SenhaEmail = '{novaSenha}',
                        DestinatarioEmail = '{novoDestinatario}',
                        ServidorSMTP = '{novoServidor}',
                        PortaSMTP = {novaPorta}'''.format(novoUsuario = usuario, novaSenha = senha, 
                                                          novoDestinatario = destinatario, novoServidor = servidor, novaPorta = porta)
        print sql
        
        cursor.execute(sql)
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")

#envia a configuracao atual de email para o solicitante
def enviarConfiguracaoEmail():
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Configuracao")

    row = cursor.fetchone()
    
    root = Element("EnviarConfiguracaoEmail")
    dados = Element("Dados", Usuario = str(row["RemetenteEmail"]), Senha = str(row["SenhaEmail"]), Destinatario = str(row["DestinatarioEmail"]),
                             Servidor = str(row["ServidorSMTP"]), Porta = str(row["PortaSMTP"]))
    root.append(dados)
    
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
    conBanco.close()

#funcao para enviar as configuracoes atuais do alarme
def enviarConfiguracaoAlarme():
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
    cursor.execute("select EnviarEmailAlarme, UsarSireneAlarme, TempoDisparoAlarme from Configuracao")
    row = cursor.fetchone()

    root = Element("EnviarConfiguracaoAlarme")
    root.append(Element("Geral", TempoDisparo=str(row["TempoDisparoAlarme"]), UsarSirene=str(row["UsarSireneAlarme"]), UsarEmail=str(row["EnviarEmailAlarme"])))

    cursor.execute("select Id, Nome, Ativo from SensorAlarme")
    rows = cursor.fetchall()
    
    sensores = Element("Sensores")
    
    for row in rows:
         sensores.append(Element("Sensor" + str(row["Id"]), Nome=str(row["Nome"]), Ativo=str(row["Ativo"])))
    
    root.append(sensores)
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
    conBanco.close()
        
#funcao para gravar as novas configuracoes do alarme
def alterarConfiguracaoAlarme(root):
    try:
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = '''update Configuracao 
                    set TempoDisparoAlarme = {tempo}, 
                        UsarSireneAlarme = {usarSirene},
                        EnviarEmailAlarme = {usarEmail}'''.format(tempo = int(root.find("TempoDisparo").text), usarSirene = int(root.find("UsarSirene").text), usarEmail = int(root.find("UsarEmail").text))
        print sql
        cursor.execute(sql)
        
        sensores = root.find("Sensores")
        
        for child in sensores:
            sql = '''update SensorAlarme set Nome = '{novoNome}', Ativo = {ativo} where Id = {idSensor}'''.format(novoNome = child.get("Nome"), ativo = int(child.get("Ativo")), idSensor = int(child.get("Id")))
            print sql
            cursor.execute(sql)
        
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")

#envia a lista de musicas de uma pasta pre determinada
def enviarListaMusica():
    #Le os arquivos da pasta passada como parametro
    arquivos = os.listdir(os.path.expanduser('/home/pi/HousePi/Musicas/'))

    root = Element("EnviarListaMusica")

    for arquivo in arquivos:
        root.append(Element("Musicas", Nome=str(arquivo)))
    
    xmlstr = ET.tostring(root) + "\n"  
    con.send(xmlstr)

#remove e cria um novo arquivo de pipe para controle do mplayer
def iniciarSomAmbiente():
    os.system("rm /home/pi/HousePi/mplayer_control")
    os.system("mkfifo /home/pi/HousePi/mplayer_control")

#controla o mplayer do linux
def controlarSomAmbiente(root):
    global controleMPlayer
    
    comando = str(root.find("Comando").text)
    valor = str(root.find("Valor").text)
    pipe = '''echo "{comando_valor}" > /home/pi/HousePi/mplayer_control'''
    
    executar = ""

    if comando == "Play":
        #executar = '''find /home/pi/HousePi/Musicas/ -name "*mp3" -o -name "*flac" -type f > ~/playlist
        #              mplayer -slave -input file=/home/pi/HousePi/mplayer_control -playlist ~/playlist </dev/null >/dev/null 2>&1 &'''         
        song = '-playlist <(find /home/pi/HousePi/Musicas/ -name "*mp3" -o -name "*flac" -type f)'
        cmd = ['mplayer', '-slave', '-quiet', song]
        controleMPlayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    elif comando == "Pause":
        print perform_command(controleMPlayer, 'get_file_name', 'ANS_FILENAME')
        #executar = pipe.format(comando_valor = "pause")
    elif comando == "Stop":
        executar = pipe.format(comando_valor = "stop")
    elif comando == "Anterior":
        executar = pipe.format(comando_valor = "pt_step " + valor)
    elif comando == "Proxima":
        executar = pipe.format(comando_valor = "pt_step " + valor)
    elif comando == "Volume":
        executar = pipe.format(comando_valor = "set_property volume " + valor)
    
    #print executar
    #os.system(executar)
    
def perform_command(p, cmd, expect):
    
    
    p.stdin.write(cmd + '\n') # there's no need for a \n at the beginning
    while select.select([p.stdout], [], [], 0.05)[0]: # give mplayer time to answer...
        output = p.stdout.readline()
        print("output: {}".format(output.rstrip()))
        split_output = output.split(expect + '=', 1)
        if len(split_output) == 2 and split_output[0] == '': # we have found it
            value = split_output[1]
            return value.rstrip()

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
                    enviarConfiguracaoStatusRele()
                elif root.tag == "StatusAlarme":
                    enviarConfiguracaoStatusAlarme()   
                elif root.tag == "GravarAgendamento":
                    gravarAgendamento(root)
                elif root.tag == "EnviarAgendamento":
                    enviarAgendamento()
                elif root.tag == "RemoverAgendamento":
                    removerAgendamento(root)
                elif root.tag == "AlterarUsuarioSenha":
                    alterarUsuarioSenha(root)
                elif root.tag == "AlterarConfiguracaoRele":
                    alterarConfiguracaoRele(root)
                elif root.tag == "AlterarConfiguracaoEmail":
                    alterarConfiguracaoEmail(root)
                elif root.tag == "EnviarConfiguracaoEmail":
                    enviarConfiguracaoEmail()
                elif root.tag == "EnviarConfiguracaoAlarme":
                    enviarConfiguracaoAlarme()
                elif root.tag == "AlterarConfiguracaoAlarme":
                    alterarConfiguracaoAlarme(root)
                elif root.tag == "EnviarListaMusica":
                    enviarListaMusica()
                elif root.tag == "ControlarSomAmbiente":
                    controlarSomAmbiente(root)
            except Exception as e: 
                print "Erro: ", e
                con.send("Erro\n")
                
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

configurarReles()
configurarAlarme()
carregarListaAgendamento()
iniciarAgendamento()
iniciarSomAmbiente()

#inicia a transmisao do video/webcam
os.system('mjpg-streamer/mjpg-streamer.sh start')

print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"

#para fechar o programa
def signal_handler(signal, frame):
    print "\nEncerrando aplicativo..."
    
    global threadAgendamento
    threadAgendamento.stop()
    
    listaReles[12].desligar()
    os.system('mjpg-streamer/mjpg-streamer.sh stop')
    tcp.close;
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:
   con, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([con, cliente]))
    
tcp.close()
