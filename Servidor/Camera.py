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
    def ligarCamera(self):
        os.system("sudo " + self.MJPG) #iniciar, porta, resolucao, fps
        
    #para o servico da camera
    def desligarCamera(self):
        os.system("sudo " + self.MJPG + " stop")
    
    #inicia ou para o servico de stream da camera
    def acionamentoCamera(self):
        if len(self.conexoes) < 1:
            self.desligarCamera()
        elif len(self.conexoes) > 0:
            self.ligarCamera()
    
    #remove o cliente da lista de conexões 
    def removerConexaoCamera(self, cliente):
        if len(self.conexoes) > 0:
            for i in range(-1, len(self.conexoes)):
                if self.conexoes[i] == cliente:
                    del self.conexoes[i]
                    self.acionamentoCamera()
    
    #adiciona o cliente na lista de conexões
    def adicionarConexaoCamera(self, cliente):
        self.conexoes.insert(len(self.conexoes) + 1, cliente)
                