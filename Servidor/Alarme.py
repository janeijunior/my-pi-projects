#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import thread
import threading
import time
import SensorAlarme
import Base
import datetime

DESLIGADO = -1
NORMAL    =  0
DISPARADO =  1

class Alarme(Base.Base):
    
    #construtor
    def __init__(self, sirene, email):
        
        #atributos publicos da classe
        self.alarmeLigado = False
        self.panicoLigado = False    
        self.thread = None
        self.status = DESLIGADO
        self.sirene = sirene
        self.email = email
        self.carregarSensores()
        self.carregarConfiguracao()
        
    #funcoes 
    #funcao para ligar o alarme
    def ligarAlarme(self):
        if self.alarmeLigado == False:
            self.status = NORMAL
            self.alarmeLigado = True
            
            if self.thread <> None:
                print "Aguardando thread terminar..."
                self.thread.join()
                
            self.thread = threading.Thread(None, self.__monitorarSensores, None, ())
            self.thread.start()
            
            self.atualizarStatusBanco()
            
            print "Alarme ligado!"
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        if self.alarmeLigado == True:
            self.alarmeLigado = False
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
            
            print "Alarme desligado!"
        
    #funcao para ligar o panico do alarme
    def ligarPanico(self):
        self.sirene.ligar()
        self.panicoLigado = True
        self.atualizarStatusBanco()
        
    #funcao para desligar o panico do alarme
    def desligarPanico(self):
        if self.status <> 1:
            self.sirene.desligar()
        
        self.panicoLigado = False
        self.atualizarStatusBanco()
    
    #funcao para atualizar os status no banco
    def atualizarStatusBanco(self):
       sql = "update ConfiguracaoAlarme set StatusAlarme = {statusAlarme}, StatusPanico = {statusPanico}"
       sql = sql.format(statusAlarme = int(self.alarmeLigado), statusPanico = int(self.panicoLigado))
       
       return self.executarComando(sql)
     
    #função que atualiza as configuracoes no banco
    def gravarConfiguracaoBanco(self):
        sql = '''update ConfiguracaoAlarme 
                    set TempoDisparo = {tempo}, 
                        UsarSirene = {usarSirene},
                        EnviarEmail = {enviarEmail},
                        DesligarDisparoConsecutivo = {desligarDisparoConsecutivo}'''
            
        sql = sql.format(tempo = int(self.tempoDisparo), usarSirene = int(self.usarSirene), enviarEmail = int(self.enviarEmail), desligarDisparoConsecutivo = int(self.desligarDisparoConsecutivo))
            
        return self.executarComando(sql)
     
    #insere os sensores na lista passando seus atributos recuperados do banco
    def carregarSensores(self):
        self.sensores = [];
        
        rows = self.consultarRegistros("select * from SensorAlarme")

        for row in rows:
            sensor = SensorAlarme.SensorAlarme(row["Id"], row["NumeroGPIO"], row["Ativo"], row["Nome"])        
            self.sensores.insert(int(row["Id"]), sensor)    
    
    #carrega as configurações
    def carregarConfiguracao(self):
        row = self.consultarRegistro("select * from ConfiguracaoAlarme")
        
        self.tempoDisparo               = row["TempoDisparo"]
        self.usarSirene                 = row["UsarSirene"]
        self.enviarEmail                = row["EnviarEmail"]
        self.desligarDisparoConsecutivo = row["DesligarDisparoConsecutivo"]
        
        if row['StatusAlarme'] == 1:
            self.ligarAlarme()
        
        if row['StatusPanico'] == 1:
            self.ligarPanico()     
    
    #grava o disparo no banco de dados
    def gravarRegistroDisparo(self, idSensorDisparo):
        sql = "insert into DisparoAlarme (IdSensorAlarme, DataHora) values ({idSensor}, '{dataHora}')"
        sql = sql.format(idSensor = idSensorDisparo, dataHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
       
        return self.executarComando(sql)        

    #retorna os ultimos 20 disparos do alarme
    def getUltimosDisparos(self):
        return self.consultarRegistros('''select DA.Id, 
                                                 SA.Nome, 
                                                 DA.DataHora 
                                            from DisparoAlarme DA 
                                            join SensorAlarme SA 
                                              on SA.Id = DA.IdSensorAlarme 
                                        order by DA.Id desc
                                           limit 10''')

    #função que é executada como thread que monitora os sensores    
    def __monitorarSensores(self):
        if self.usarSirene == 1:
            self.sirene.ligar()
            time.sleep(0.2)
            self.sirene.desligar()
        
        disparos =  0
        idSensor = -1
        
        #executa enquanto o alarme estiver ativo
        while self.alarmeLigado: 
            #percorre os sensores
            for sensor in self.sensores:
                #le os status dos sensores ativos
                if (self.alarmeLigado) and (sensor.ativo == 1):
                    if (sensor.lerStatus() == 0):
                    
                        time.sleep(0.5)
                        
                        #duas leituras para garantir que esta realmente disparado
                        if (self.alarmeLigado) and (sensor.ativo == 1):
                            if (sensor.lerStatus() == 0):
                                disparos = disparos + 1
                                idSensor = sensor.id
                                
                                print str(disparos) + "º disparo consecutivo..."
                                
                                if (disparos > 3) and (self.desligarDisparoConsecutivo == 1):
                                    disparos = 0
                                    self.desligarAlarme()
                                    break
                                
                                self.status = DISPARADO
                                
                                #se estiver violado mostra msg na tela
                                print("Sensor: " + str(sensor.id) + " - " + sensor.nome + " violado.")
                                
                                #se estiver configurado dispara a sirene
                                if self.usarSirene == 1:
                                    self.sirene.ligar()
                                
                                #se estiver configurado envia o e-mail
                                if self.enviarEmail == 1:
                                    self.email.carregarConfiguracao()
                                    self.email.enviar(sensor.id, sensor.nome) 
                                
                                #grava o disparo no banco
                                self.gravarRegistroDisparo(sensor.id)
                                
                                #aguarda o tempo configurado ate iniciar a proxima leitura
                                tempo = 0
                                
                                while tempo < self.tempoDisparo:
                                    if self.alarmeLigado == False:
                                        print "Break tempo disparo..."
                                        break
                                    
                                    time.sleep(1)
                                    tempo = tempo + 1
                                
                                if self.alarmeLigado:
                                    print "Alarme ligado novamente..."
                                    self.status = NORMAL
                                
                                #desliga a sirene se necessario
                                if self.usarSirene == 1:
                                    self.sirene.desligar() 
                            else:
                                disparos = 0;
                    else:
                        disparos = 0
            time.sleep(0.05)

    #destrutor
    def __done__(self):
        self.desligarPanico()
        self.desligarAlarme()