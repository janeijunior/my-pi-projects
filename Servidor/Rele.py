#!/usr/bin/python
#-*- coding: utf-8 -*-

import Adafruit_MCP230xx
import Base
import time
import thread
import threading

#variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

#constantes
LIGAR    = 1
DESLIGAR = 0
STATUS_LIGADO = 1
STATUS_DESLIGADO = 0

class Rele(Base.Base):
    
    #construtor
    def __init__(self, id, numeroGPIO, status, nome, ativo):
        
        #atributos publicos da classe
        self.id           = id
        self.numeroGPIO   = numeroGPIO
        self.status       = status
        self.nome         = nome
        self.ativo        = ativo
        self.automatico   = False
        self.temporizador = 0
        self.thread       = None
        
        self.configurar()
            
    #funcoes
    #funcao para configurar o rele para uso
    def configurar(self):
        mcp.config(self.numeroGPIO, mcp.OUTPUT)
    
    #funcao para ligar o rele
    def ligar(self, temporizador = 0):
        try:
            #self.configurar()
            mcp.output(self.numeroGPIO, LIGAR)
            self.status = STATUS_LIGADO
            
            if temporizador > 0:
                print "Temporizando rele para " + str(temporizador) + " minuto(s)."
                
                if self.temporizador == 0:
                    self.temporizador = temporizador
                    self.thread = threading.Thread(None, self.__temporizarRele, None, ())
                    self.thread.start()
                else:
                    self.temporizador = temporizador
            
            return True
        except:
            return False
            
    #funcao para desligar o rele
    def desligar(self):
        try:
            #self.configurar()
            mcp.output(self.numeroGPIO, DESLIGAR)
            self.status = STATUS_DESLIGADO
            self.temporizador = 0
            return True
        except:
            return False
    
    #funcao para gravar o novo nome do rele
    def gravarNomeBanco(self):
        sql = "update Rele set Nome = '{nomeRele}', Ativo = {ativo} where Id = {idRele}".format(nomeRele = self.nome, ativo = self.ativo, idRele = self.id)
        
        return self.executarComando(sql)
    
    #funcao para atualizar o status no banco
    def atualizarStatusBanco(self):
        if self.numeroGPIO < 10:
            sql = "update Rele set Status = '{statusRele}' where Id = {idRele}".format(statusRele = self.status, idRele = self.id)
        
            return self.executarComando(sql)
        else:
            return True
    
    def __temporizarRele(self):
        tempoDecorido = 0
        
        while self.status == STATUS_LIGADO:
            time.sleep(1)
            
            tempoDecorido = tempoDecorido + 1
            
            print "Tempo decorido: " + str(tempoDecorido)
            
            if (tempoDecorido / 60) >= self.temporizador:
                print "Desligando rele via temporizador."
                
                self.desligar()
    
    #destrutor
    #def __done__(self):
    #    self.desligar()
