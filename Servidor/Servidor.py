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
import Email

HOST     = ""                                            # IP do Servidor (em branco = IP do sistema)
PORT     = int(Funcoes.lerConfiguracaoIni("Porta"))      # Porta do Servidor

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
email = Email.Email()

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
                    automacao.controlarRele(root, con)
                elif root.tag == "Temperatura":
                    automacao.enviarTemperaturaHumidade(con)
                elif root.tag == "Alarme":
                    automacao.controlarAlarme(root, con)
                elif root.tag == "Panico":
                    automacao.controlarFuncaoPanico(root, con)           
                elif root.tag == "StatusRele":
                    automacao.enviarConfiguracaoStatusRele(con)
                elif root.tag == "StatusAlarme":
                    automacao.enviarConfiguracaoStatusAlarme(con)   
                elif root.tag == "GravarAgendamento":
                    gravarAgendamento(root, con)
                elif root.tag == "EnviarAgendamento":
                    enviarAgendamento(con)
                elif root.tag == "RemoverAgendamento":
                    removerAgendamento(root, con)
                elif root.tag == "AlterarUsuarioSenha":
                    automacao.alterarUsuarioSenha(root, con)
                elif root.tag == "AlterarConfiguracaoRele":
                    automacao.alterarConfiguracaoRele(root, con)
                elif root.tag == "AlterarConfiguracaoEmail":
                    automacao.alterarConfiguracaoEmail(root, con)
                elif root.tag == "EnviarConfiguracaoEmail":
                    automacao.enviarConfiguracaoEmail(con)
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

#configurarReles()
#configurarAlarme()
#carregarListaAgendamento()
#iniciarAgendamento()

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