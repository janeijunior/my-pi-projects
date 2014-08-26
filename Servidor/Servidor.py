#!/usr/bin/python
#-*- coding: utf-8 -*-

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import socket
import thread
import threading
import Funcoes
import Automacao
import signal

if __name__ == '__main__': 
    
    #para fechar o programa
    def signal_handler(signal, frame):
        print "\nEncerrando aplicativo..."
        automacao.finalizarProcessos()
        tcp.close;
        sys.exit(0)

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
                        automacao.gravarAgendamento(root, con)
                    elif root.tag == "EnviarAgendamento":
                        automacao.enviarAgendamento(con)
                    elif root.tag == "RemoverAgendamento":
                        automacao.removerAgendamento(root, con)
                    elif root.tag == "AlterarUsuarioSenha":
                        automacao.alterarUsuarioSenha(root, con)
                    elif root.tag == "AlterarConfiguracaoRele":
                        automacao.alterarConfiguracaoRele(root, con)
                    elif root.tag == "AlterarConfiguracaoEmail":
                        automacao.alterarConfiguracaoEmail(root, con)
                    elif root.tag == "EnviarConfiguracaoEmail":
                        automacao.enviarConfiguracaoEmail(con)
                    elif root.tag == "EnviarConfiguracaoAlarme":
                        automacao.enviarConfiguracaoAlarme(con)
                    elif root.tag == "AlterarConfiguracaoAlarme":
                        automacao.alterarConfiguracaoAlarme(root, con)
                    elif root.tag == "EnviarListaMusica":
                        automacao.enviarListaMusica(con)
                    elif root.tag == "ControlarSomAmbiente":
                        automacao.controlarSomAmbiente(root, con)
                    elif root.tag == "ReiniciarDesligar":
                        automacao.reiniciarDesligarServidor(root, con)
                    elif root.tag == "ControlarCamera":
                        automacao.controlarCamera(root, con, cliente)
                    elif root.tag == "EnviarUltimosDisparos":
                        automacao.enviarUltimosDisparos(con)
                    elif root.tag == "RFID":
                        automacao.controlarRFID(root)
                    else:
                        print "Comando não reconhecido!"
                except Exception as e: 
                    print "Erro: ", e
                    con.send("Erro\n")
                    
        print "Finalizando conexao do cliente", cliente
        
        automacao.removerConexao(cliente)
        
        con.close()
        thread.exit()
    
    #inicia o servidor    
    HOST = ""                                       
    PORT = int(Funcoes.lerConfiguracaoIni("Porta")) 
    
    orig = (HOST, PORT)
    
    tcp  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(orig)
    tcp.listen(1)
    
    #classe automacao
    automacao = Automacao.Automacao()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"
    
    while True:
       conexao, cliente = tcp.accept()
       thread.start_new_thread(conectado, tuple([conexao, cliente]))
       
    tcp.close()