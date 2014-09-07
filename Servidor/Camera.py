#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import os
import Base

class Camera(Base.Base):
    
    #construtor
    def __init__(self, usuario):
        self.MJPG     = Funcoes.lerConfiguracaoIni("CaminhoMJPG")
        self.conexoes = []
        self.usuario = usuario
        
    #inicia o servico da camera
    def ligar(self):
        rows = self.consultarRegistros("select * from Camera") 
        
        for row in rows:    
            autenticacao = self.usuario.usuario + ":" + self.usuario.senha
            os.system("sudo " + self.MJPG + " start " +  str(row["Porta"]) + " " + Funcoes.lerConfiguracaoIni("ConfiguracaoMJPG") + " " + str(row["Device"]) + " " + autenticacao) 
        
    #para o servico da camera
    def desligar(self):
        rows = self.consultarRegistros("select * from Camera") 
        
        for row in rows:    
            os.system("sudo " + self.MJPG + " stop " + str(row["Device"]))
    
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
    
    #captura uma imagem com o nome passado por parametro
    def CapturarImagem(self, nome):
        