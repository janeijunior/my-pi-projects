#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import os

class Camera(object):
    
    #construtor
    def __init__(self):
        self.MJPG     = Funcoes.lerConfiguracaoIni("MJPG")  # Caminho stream de video e configurações
        self.conexoes = []
    
    #inicia o servico da camera
    def ligarCamera():
        os.system("sudo " + self.MJPG + " start 5005 320x240 2") #iniciar, porta, resolucao, fps
        
    #para o servico da camera
    def desligarCamera():
        os.system("sudo " + self.MJPG + " stop")
    
    #inicia ou para o servico de stream da camera
    def acionamentoCamera():
        if len(self.conexoes) < 1:
            desligarCamera()
        elif len(self.conexoes) > 0:
            ligarCamera()
    
    #remove o cliente da lista de conexões 
    def removerConexaoCamera(cliente):
        if len(self.conexoes) > 0:
            for i in range(-1, len(self.conexoes)):
                if self.conexoes[i] == cliente:
                    del self.conexoes[i]
                    acionamentoCamera()
    
    #adiciona o cliente na lista de conexões
    def adicionarConexaoCamera(cliente):
        self.conexoes.insert(len(self.conexoes) + 1, cliente)
                