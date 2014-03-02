#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import os

class Camera(object):
    
    #construtor
    def __init__(self):
        self.MJPG     = Funcoes.lerConfiguracaoIni("CaminhoMJPG")
        self.conexoes = []
    
    #inicia o servico da camera
    def ligar(self):
        os.system("sudo " + self.MJPG + " start " +  Funcoes.lerConfiguracaoIni("ConfiguracaoMJPG") ) #iniciar, porta, resolucao, fps
        
    #para o servico da camera
    def desligar(self):
        os.system("sudo " + self.MJPG + " stop")
    
    #inicia ou para o servico de stream da camera
    def acionamento(self):
        if len(self.conexoes) < 1:
            self.desligar()
        elif len(self.conexoes) > 0:
            self.ligar()
    
    #remove o cliente da lista de conexões 
    def removerConexao(self, cliente):
        if len(self.conexoes) > 0:
            for i in range(-1, len(self.conexoes)):
                if self.conexoes[i] == cliente:
                    del self.conexoes[i]
                    self.acionamento()
                    break
    
    #adiciona o cliente na lista de conexões
    def adicionarConexao(self, cliente):
        self.conexoes.insert(len(self.conexoes) + 1, cliente)
                