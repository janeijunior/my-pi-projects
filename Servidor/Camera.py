#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class Camera(object):
    
    #construtor
    def __init__(self):
        self.MJPG = Funcoes.lerConfiguracaoIni("CaminhoMJPG") # Caminho stream de video
    
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