#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import thread
import threading
import time
import SensorAlarme
import Base

DESLIGADO = -1
NORMAL = 0
DISPARADO = 1

class Alarme(Base.Base):
    
    #construtor
    def __init__(self, sirene, email):
        
        #atributos publicos da classe
        self.alarmeLigado = False
        self.panicoAlarmeLigado = False    
        self.sirene = sirene
        self.email = email
        self.carregarSensores()
        self.carregarConfiguracao()
        
        #pega os status do banco e se necessario liga o alarme/panico
        row = self.consultarRegistro("select StatusAlarme, StatusPanico from ConfiguracaoAlarme")
        
        if row['StatusAlarme'] == 1:
            self.ligarAlarme()
        
        if row['StatusPanico'] == 1:
            self.ligarPanicoAlarme()     
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.status = NORMAL
        self.alarmeLigado = True
        
        self.thread = threading.Thread(None, self.__monitorarSensores, None, ())
        self.thread.start()
        
        self.atualizarStatusBanco()
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.alarmeLigado = False
        self.thread.stop()
        self.sirene.desligar()
        
        if self.usarSirene == 1:
            if self.status == DISPARADO:
                time.sleep(0.5)    
        
        self.sirene.ligar()
        time.sleep(0.2)
        self.sirene.desligar()
        time.sleep(0.5)
        self.sirene.ligar()
        time.sleep(0.2)
        self.sirene.desligar()
    
        self.status = DESLIGADO
        self.atualizarStatusBanco()
    
    #funcao para ler o status do alarme
    def getStatusAlarme(self):
        self.status
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.sirene.ligar()
        self.panicoAlarmeLigado = True
        self.atualizarStatusBanco()
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        if self.getStatusAlarme() <> 1:
            self.sirene.desligar()
        
        self.panicoAlarmeLigado = False
        self.atualizarStatusBanco()
    
    #funcao para atualizar os status no banco
    def atualizarStatusBanco(self):
       sql = "update ConfiguracaoAlarme set StatusAlarme = {statusAlarme}, StatusPanico = {statusPanico}"
       sql = sql.format(statusAlarme = int(self.alarmeLigado), statusPanico = int(self.panicoAlarmeLigado))
       
       return self.executarComando(sql)
     
    #insere os sensores na lista passando seus atributos recuperados do banco
    def carregarSensores(self):
        self.sensores = [];
        
        rows = self.consultarRegistros("select * from SensorAlarme")

        for row in rows:
            sensor = SensorAlarme.SensorAlarme(row["Id"], row["NumeroGPIO"], row["Ativo"], row["Nome"])        
            self.sensores.insert(int(row["Id"]) - 1 , sensor)    
    
    #carrega as configurações
    def carregarConfiguracao(self):
        row = self.consultarRegistro("select * from ConfiguracaoAlarme")
        
        self.tempoDisparo = row["TempoDisparo"]
        self.usarSirene   = row["UsarSirene"]
        self.enviarEmail  = row["EnviarEmail"]
    
    #função que é executada como thread que monitora os sensores    
    def __monitorarSensores(self):
        if self.usarSirene == 1:
            self.sirene.ligar()
            time.sleep(0.2)
            self.sirene.desligar()
        
        #executa enquanto o alarme estiver ativo
        while self.alarmeLigado: 
            #percorre os sensores
            for i in range(0, 8):
                #le os status dos sensores ativos
                if (self.sensores[i].ativo == 1) and (self.sensores[i].lerStatus() == 0):
                    self.status = DISPARADO
                    
                    #se estiver violado mostra msg na tela
                    print("Sensor: " + str(i) + " - " + self.sensores[i].nome + " violado.")
                    
                    #se estiver configurado dispara a sirene
                    if self.usarSirene == 1:
                        self.sirene.ligar()
                    
                    #se estiver configurado envia o e-mail
                    if self.enviarEmail == 1:
                        self.email.enviar(self.sensores[i].id, self.sensores[i].nome) 
                    
                    #aguarda o tempo configurado ate iniciar a proxima leitura
                    time.sleep(self.tempoDisparo)
                    
                    self.status = NORMAL
                    
                    #desliga a sirene se necessario
                    if self.usarSirene == 1:
                        self.sirene.desligar() 
                        
            time.sleep(0.05)

    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()