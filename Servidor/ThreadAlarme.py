#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import time
import Email
import SensorAlarme
import Funcoes

DESLIGADO = -1
NORMAL = 0
DISPARADO = 1

class ThreadAlarme(threading.Thread):
    def __init__(self, sirene):
        threading.Thread.__init__(self)
        self.name = 'ThreadAlarme'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.sirene = sirene
        self.status = NORMAL
        
        row = Funcoes.consultarRegistro("select * from ConfiguracaoAlarme")
        
        self.tempoDisparo = row["TempoDisparo"]
        self.usarSirene   = row["UsarSirene"]
        self.enviarEmail  = row["EnviarEmail"]
    
    def stop(self):
        self.sirene.desligar()
        self.__stop_thread_event.set()
        
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
        
    def run(self):
        #insere os sensores na lista passando seus atributos recuperados do banco
        listaSensores = [];
        
        rows = Funcoes.consultarRegistros("select * from SensorAlarme")

        for row in rows:
            sensor = SensorAlarme.SensorAlarme(id = row["Id"], numeroGPIO = row["NumeroGPIO"], ativo = row["Ativo"], nome = row["Nome"])        
            listaSensores.insert(int(row["Id"]) - 1 , sensor)
        
        if self.usarSirene == 1:
            self.sirene.ligar()
            time.sleep(0.2)
            self.sirene.desligar()
        
        #executa enquanto o alarme estiver ativo
        while not self.__stop_thread_event.isSet(): 
            #percorre os sensores
            for i in range(0, 8):
                #le os status dos sensores ativos
                if (listaSensores[i].ativo == 1) and (listaSensores[i].lerStatus() == 0):
                    self.status = DISPARADO
                    
                    #se estiver violado mostra msg na tela
                    print("Sensor: " + str(i) + " - " + listaSensores[i].nome + " violado.")
                    
                    
                    #se estiver configurado dispara a sirene
                    if self.usarSirene == 1:
                        self.sirene.ligar()
                    
                    #se estiver configurado envia o e-mail
                    if self.enviarEmail == 1:
                        email = Email.Email()
                        email.enviar() 
                    
                    #aguarda o tempo configurado ate iniciar a proxima leitura
                    time.sleep(self.tempoDisparo)
                    
                    self.status = NORMAL
                    
                    #desliga a sirene se necessario
                    if self.usarSirene == 1:
                        self.sirene.desligar() 
                        
            time.sleep(0.05)
