#!/usr/bin/python

import thread
import threading
import time
import RPi.GPIO as GPIO 
import EnviarEmail
import Rele
import SensorAlarme
import MySQLdb

class ThreadAlarme(threading.Thread):
    def __init__(self, conBanco):
        threading.Thread.__init__(self)
        self.name = 'ThreadAlarme'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.conBanco = conBanco
        
        cursor = self.conBanco.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from ConfiguracaoAlarme")
    
        row = cursor.fetchone()
        
        self.tempoDisparo = row["TempoDisparo"]
        self.usarSirene   = row["UsarSirene"]
        self.enviarEmail  = row["EnviarEmail"]
        self.remetente    = row["Remetente"]
        self.destinatario = row["Destinatario"]
        self.servidorSMTP = row["ServidorSMTP"]
        self.portaSMTP    = row["PortaSMTP"]
        self.senha        = row["Senha"]
        
    def stop(self):
        self.sirene.desligar()
        self.__stop_thread_event.set()
        
    def run(self):
        
        listaSensores = [];
        
        #insere os sensores na lista passando seus atributos recuperados do banco
        cursor = self.conBanco.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from SensorAlarme")

        rows = cursor.fetchall()

        for row in rows:
          sensor = SensorAlarme.SensorAlarme(id = row["Id"], numeroGPIO = row["NumeroGPIO"], ativo = row["Ativo"], nome = row["Nome"])        
          listaSensores.insert(row["Id"] - 1 , sensor)
        
        #rele da sirene
        self.sirene = Rele.Rele(id = 10, numeroGPIO = 10, status = 0, nome = 'Sirene')
        
        #executa enquanto o alarme estiver ativo
        while not self.__stop_thread_event.isSet(): 
            #percorre os sensores
            for i in range(0, 8):
                #le os status dos sensores ativos
                if (listaSensores[i].ativo == 1) and (listaSensores[i].lerStatus() == 0):
                    #se estiver violado mostra msg na tela
                    print("Sensor: " + str(i) + " - " + listaSensores[i].nome + " violado.")
                    
                    #se estiver configurado dispara a sirene
                    if self.usarSirene == 1:
                        self.sirene.ligar()
                    
                    #se estiver configurado envia o e-mail
                    if self.enviarEmail == 1:
                        email = EnviarEmail.EnviarEmail(remetente = self.remetente, senha = self.senha, 
                                                       destinatario = self.destinatario, servidorSMTP = self.servidorSMTP,
                                                       portaSMTP = self.portaSMTP, nomeSensor = listaSensores[i].nome)
                        email.start() 
                    
                    #aguarda o tempo configurado ate iniciar a proxima leitura
                    time.sleep(self.tempoDisparo)
                    
                    #desliga a sirene se necessario
                    if self.usarSirene == 1:
                        self.sirene.desligar() 
                        
            time.sleep(0.05)
