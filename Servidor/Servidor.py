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
import Rele
import signal
import sys
import SensorDHT
import Funcoes
import Agendamento
import ThreadAgendamento
import subprocess
import select
import MySQLdb
import Automacao

HOST     = ""                                            # IP do Servidor (em branco = IP do sistema)
PORT     = int(Funcoes.lerConfiguracaoIni("Porta"))      # Porta do Servidor
SIRENE   = int(Funcoes.lerConfiguracaoIni("GPIOSirene")) # Numero GPIO da sirene
MJPG     = Funcoes.lerConfiguracaoIni("CaminhoMJPG")     # Caminho stream de video

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

#lista de conexoes ativas na camera
listaConexoesCamera = []

#classe automacao
automacao = Automacao.Automacao()

#Configura todos os pinos necessarios para o envio de comandos 
def configurarReles():
    print "Configurando reles..."
    rows = Funcoes.consultarRegistros("select * from Rele")

    for row in rows:
        rele = Rele.Rele(id = row["Id"], numeroGPIO = row["NumeroGPIO"], status = row["Status"], nome = row["Nome"])        
        
        if rele.status == 1:
            rele.ligar()
        else:
            rele.desligar()
        
        listaReles.insert(row["Id"], rele)

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
    global alarme
    global listaAgendamento
    
    print "Carregando agendamentos..."
    listaAgendamento = []

    rows = Funcoes.consultarRegistros("select * from Agendamento where Ativo = 1")

    for row in rows:
        agendamento = Agendamento.Agendamento(id = row["Id"], nome = row["Nome"], dias = str(row["DiasDaSemana"]), equipamentos = str(row["Equipamentos"]),
                          dataHoraInicial = row["DataHoraInicial"], dataHoraFinal = row["DataHoraFinal"], ativo = int(row["Ativo"]), listaReles = listaReles, alarme = alarme)        
                
        listaAgendamento.insert(row["Id"], agendamento)    

#liga ou desliga os reles/atuadores
def controlarRele(root, con):
    acao = root.find("Acao").text
    numero = root.find("Numero").text
    
    if acao == "Ligar":
        listaReles[int(numero)].ligar()
    else:
        listaReles[int(numero)].desligar()
    
    con.send("Ok\n")
        
#liga ou desliga o alarme
def controlarAlarme(root, con):
    global alarme
    acao = root.find("Acao").text
    
    if acao == "Ligar":
        if alarme.alarmeLigado == False:
            alarme.ligarAlarme() 
            print "Alarme ativado."
    else:
        alarme.desligarAlarme()
        print "Alarme desativado."
    
    con.send("Ok\n")
            
#liga ou desliga a funcao panico do alarme
def controlarFuncaoPanico(root, con):
    global alarme
    acao = root.find("Acao").text
    
    if acao == "Ligar":
        alarme.ligarPanicoAlarme()
    else:
        alarme.desligarPanicoAlarme()
    
    con.send("Ok\n")
    
#funcao que envia as configuracoes dos reles e status
def enviarConfiguracaoStatusRele(con):
    root = Element("StatusRele")
    
    for rele in listaReles:
        root.append(Element("Rele" + str(rele.id), Status=str(rele.status), Nome=rele.nome.decode('utf-8')))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que envia o status do alarme
def enviarConfiguracaoStatusAlarme(con):
    global alarme
    root = Element("Alarme")
    
    status = ""
    
    if alarme.getStatusAlarme() == 1:
        status = "Disparado"
    elif alarme.getStatusAlarme() == 0:
        status = "Normal"
    else:
        status = "Desligado"
    
    root.append(Element("SensorAlarme", Status=status, Ligado=str(int(alarme.alarmeLigado))))
    root.append(Element("PanicoAlarme", Ligado=str(int(alarme.panicoAlarmeLigado))))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que insere um novo agendamento no banco de dados e alualiza a lista de agendamentos 
def gravarAgendamento(root, con):
    global listaReles
    global alarme
    global threadAgendamento
    global listaAgendamento
    
    agendamento = Agendamento.Agendamento(id = 0, nome = root.find("Nome").text.encode('utf-8'), dias = root.find("Dias").text, 
                                          equipamentos = root.find("Equipamentos").text, dataHoraInicial = root.find("DataHoraInicial").text, 
                                          dataHoraFinal = root.find("DataHoraFinal").text, ativo = 1, listaReles = listaReles, alarme = alarme)
    
    if agendamento.gravarRegistroBanco():
        con.send("Ok\n")
        #carrega os novos agendamentos
        carregarListaAgendamento()
        #passa a nova lista para a thread
        threadAgendamento.listaAgendamento = listaAgendamento
    else:
        con.send("Erro\n")

#funcao que retorna os agendamentos do servidor para o aplicativo movel
def enviarAgendamento(con):
    global listaAgendamento
    root = Element("EnviarAgendamento")
    
    #atualiza a lista de agendamentos
    carregarListaAgendamento()
    
    for agendamento in listaAgendamento:
        root.append(Element("Agendamento" + str(agendamento.id), Id=str(agendamento.id), Nome=agendamento.nome.decode('utf-8'), 
                            DataHoraInicial=str(agendamento.dataHoraInicial), DataHoraFinal=str(agendamento.dataHoraFinal), 
                            Dias=agendamento.dias, Equipamentos=agendamento.equipamentos, NomeEquipamentos=agendamento.getNomeEquipamento().decode('utf-8')))
                
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que remove o agendamento da lita e do banco de dados
def removerAgendamento(root, con):
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
def alterarUsuarioSenha(root, con):
    usuario = root.find("Usuario").text.encode('utf-8')
    senha = root.find("Senha").text.encode('utf-8')
    
    sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'".format(novoUsuario = usuario, novaSenha = senha)
    
    if Funcoes.executarComando(sql):
        con.send("Ok\n")
    else:
        con.send("Erro\n")
            
#funcao para renomear os reles atraves da aba de configuracoes
def alterarConfiguracaoRele(root, con):
    global listaReles
    
    try:
        for child in root:
            listaReles[int(child.get("Id"))].nome = str(child.get("Nome").encode('utf-8')) 
            listaReles[int(child.get("Id"))].gravarNomeBanco();
        
        con.send("Ok\n")
    except:
        con.send("Erro\n")
        
#funcao que grava a nova configuracao de email
def alterarConfiguracaoEmail(root, con):
    usuario = root.find("Usuario").text.encode('utf-8')
    senha = root.find("Senha").text.encode('utf-8')
    destinatario = root.find("Destinatario").text.encode('utf-8')
    servidor = root.find("Servidor").text.encode('utf-8')
    porta = root.find("Porta").text.encode('utf-8')
            
    sql = '''update Configuracao 
                set RemetenteEmail = '{novoUsuario}', 
                    SenhaEmail = '{novaSenha}',
                    DestinatarioEmail = '{novoDestinatario}',
                    ServidorSMTP = '{novoServidor}',
                    PortaSMTP = {novaPorta}'''.format(novoUsuario = usuario, novaSenha = senha, 
                                                      novoDestinatario = destinatario, novoServidor = servidor, novaPorta = porta)
    if Funcoes.executarComando(sql):
        con.send("Ok\n")
    else:
        con.send("Erro\n")

#envia a configuracao atual de email para o solicitante
def enviarConfiguracaoEmail(con):
    row = Funcoes.consultarRegistro("select * from Configuracao")
    
    root = Element("EnviarConfiguracaoEmail")
    dados = Element("Dados", Usuario = str(row["RemetenteEmail"]).decode('utf-8'), Senha = str(row["SenhaEmail"]).decode('utf-8'), Destinatario = str(row["DestinatarioEmail"]).decode('utf-8'),
                             Servidor = str(row["ServidorSMTP"]).decode('utf-8'), Porta = str(row["PortaSMTP"]))
    root.append(dados)
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
    
#funcao para enviar as configuracoes atuais do alarme
def enviarConfiguracaoAlarme(con):
    row = Funcoes.consultarRegistro("select EnviarEmailAlarme, UsarSireneAlarme, TempoDisparoAlarme from Configuracao")
    
    root = Element("EnviarConfiguracaoAlarme")
    root.append(Element("Geral", TempoDisparo=str(row["TempoDisparoAlarme"]), UsarSirene=str(row["UsarSireneAlarme"]), UsarEmail=str(row["EnviarEmailAlarme"])))

    rows = Funcoes.consultarRegistros("select Id, Nome, Ativo from SensorAlarme")
    sensores = Element("Sensores")
    
    for row in rows:
        sensores.append(Element("Sensor" + str(row["Id"]), Nome=str(row["Nome"]).decode('utf-8'), Ativo=str(row["Ativo"])))
    
    root.append(sensores)
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
        
#funcao para gravar as novas configuracoes do alarme
def alterarConfiguracaoAlarme(root, con):
    try:
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = '''update Configuracao 
                    set TempoDisparoAlarme = {tempo}, 
                        UsarSireneAlarme = {usarSirene},
                        EnviarEmailAlarme = {usarEmail}'''
        
        sql = sql.format(tempo = int(root.find("TempoDisparo").text), usarSirene = int(root.find("UsarSirene").text), 
                         usarEmail = int(root.find("UsarEmail").text))
        
        cursor.execute(sql)
        sensores  = root.find("Sensores")
    
        for child in sensores:
            sql = "update SensorAlarme set Nome = '{novoNome}', Ativo = {ativo} where Id = {idSensor}"
            sql = sql.format(novoNome = child.get("Nome").encode('utf-8'), ativo = int(child.get("Ativo")), idSensor = int(child.get("Id")))
            cursor.execute(sql)
        
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        print "Erro ao executar o comando: " + sql
        con.send("Erro\n")
        conBanco.rollback()
        conBanco.close()
        
#finaliza os processos em execucao para encerrar o aplicativo servidor
def finalizarProcessos():
    global alarme
    global threadAgendamento
    
    if alarme.alarmeLigado:
        alarme.desligarAlarme()
    
    alarme.desligarPanicoAlarme()
    threadAgendamento.stop()
    
    for rele in listaReles:	
		rele.desligar()
	
    desligarCamera()

#funcao para reiniciar ou desligar o servidor conforme solicitado pelo app android
def reiniciarDesligarServidor(root, con):
    acao = root.find("Acao").text
    finalizarProcessos()
    con.send("Ok\n")    
    
    if acao == "Reiniciar":
        os.system("/usr/bin/sudo /sbin/shutdown -r now")
    else:
        os.system("/usr/bin/sudo /sbin/shutdown -h now")

#inicia o servico da camera
def ligarCamera():
    os.system("sudo " + MJPG + " start 5005 320x240 2") #iniciar, porta, resolucao, fps
    
#para o servico da camera
def desligarCamera():
    os.system("sudo " + MJPG + " stop")

#inicia ou para o servico de stream da camera
def acionamentoCamera():
    global listaConexoesCamera
    
    if len(listaConexoesCamera) < 1:
        desligarCamera()
    elif len(listaConexoesCamera) > 0:
        ligarCamera()

#remove o cliente da lista de conexões 
def removerConexaoCamera(cliente):
    global listaConexoesCamera
    
    if len(listaConexoesCamera) > 0:
        for i in range(-1, len(listaConexoesCamera)):
            if listaConexoesCamera[i] == cliente:
                del listaConexoesCamera[i]
                acionamentoCamera()
                break

#liga ou desliga o servico da camera
def controlarCamera(root, con, cliente):
    global listaConexoesCamera
    
    acao = root.find("Acao").text  
    
    if acao == "Ligar":
        listaConexoesCamera.insert(len(listaConexoesCamera) + 1, cliente) 
        acionamentoCamera()
        con.send("Ok\n")
    else:
        con.send("Ok\n")
        removerConexaoCamera(cliente)

#cliente conectado, verifica os comandos recebidos
def conectado(con, cliente):    
    while True:
        msg = con.recv(1024)
        comando = msg[2:len(msg)]
     
        if not msg: 
            break
        
        if len(comando) > 0:
            try:
                #root = XML recebido/elemento principal
                root = ET.fromstring(comando)
                print cliente, "Comando recebido: " + root.tag 
        
                if root.tag == "Logar":
                    automacao.efetuarLogin(root, con)
                elif root.tag == "Rele":
                    controlarRele(root, con)
                elif root.tag == "Temperatura":
                    automacao.enviarTemperaturaHumidade(con)
                elif root.tag == "Alarme":
                    controlarAlarme(root, con)
                elif root.tag == "Panico":
                    controlarFuncaoPanico(root, con)           
                elif root.tag == "StatusRele":
                    enviarConfiguracaoStatusRele(con)
                elif root.tag == "StatusAlarme":
                    enviarConfiguracaoStatusAlarme(con)   
                elif root.tag == "GravarAgendamento":
                    gravarAgendamento(root, con)
                elif root.tag == "EnviarAgendamento":
                    enviarAgendamento(con)
                elif root.tag == "RemoverAgendamento":
                    removerAgendamento(root, con)
                elif root.tag == "AlterarUsuarioSenha":
                    alterarUsuarioSenha(root, con)
                elif root.tag == "AlterarConfiguracaoRele":
                    alterarConfiguracaoRele(root, con)
                elif root.tag == "AlterarConfiguracaoEmail":
                    alterarConfiguracaoEmail(root, con)
                elif root.tag == "EnviarConfiguracaoEmail":
                    enviarConfiguracaoEmail(con)
                elif root.tag == "EnviarConfiguracaoAlarme":
                    enviarConfiguracaoAlarme(con)
                elif root.tag == "AlterarConfiguracaoAlarme":
                    alterarConfiguracaoAlarme(root, con)
                elif root.tag == "EnviarListaMusica":
                    automacao.enviarListaMusica(con)
                elif root.tag == "ControlarSomAmbiente":
                    automacao.controlarSomAmbiente(root, con)
                elif root.tag == "ReiniciarDesligar":
                    reiniciarDesligarServidor(root, con)
                elif root.tag == "ControlarCamera":
                    controlarCamera(root, con, cliente)
            except Exception as e: 
                print "Erro: ", e
                con.send("Erro\n")
                
    print "Finalizando conexao do cliente", cliente
    
    removerConexaoCamera(cliente)
    
    con.close()
    thread.exit()

configurarReles()
configurarAlarme()
carregarListaAgendamento()
iniciarAgendamento()

print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"

#para fechar o programa
def signal_handler(signal, frame):
    print "\nEncerrando aplicativo..."
    finalizarProcessos()
    tcp.close;
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:
   conexao, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([conexao, cliente]))
    
tcp.close()