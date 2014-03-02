#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import thread
import threading
import time
import SensorAlarme
import Base
import MySQLdb

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
        self.status = DESLIGADO
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        if self.alarmeLigado == False:
            self.status = NORMAL
            self.alarmeLigado = True
            
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
     
    #função que atualiza as congiguracoes no banco
    def gravarConfiguracaoBanco(self):
        try:
            conBanco = self.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            sql = '''update Configuracao 
                        set TempoDisparo = {tempo}, 
                            UsarSirene   = {usarSirene},
                            EnviarEmail  = {usarEmail}'''
            
            sql = sql.format(tempo = int(root.find("TempoDisparo").text), usarSirene = int(root.find("UsarSirene").text), 
                             usarEmail = int(root.find("UsarEmail").text))
            
            cursor.execute(sql)
            sensores  = root.find("Sensores")
        
            for child in sensores:
                sql = "update SensorAlarme set Nome = '{novoNome}', Ativo = {ativo} where Id = {idSensor}"
                sql = sql.format(novoNome = child.get("Nome").encode('utf-8'), ativo = int(child.get("Ativo")), idSensor = int(child.get("Id")))
                cursor.execute(sql)
            
            conBanco.commit()
            conBanco.close()
            con.send("Ok\n")
        except:
            print "Erro ao executar o comando: " + sql
            con.send("Erro\n")
            conBanco.rollback()
            conBanco.close()
     
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
        
        if row['StatusAlarme'] == 1:
            self.ligarAlarme()
        
        if row['StatusPanico'] == 1:
            self.ligarPanicoAlarme()     
    
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
                        self.email.carregarConfiguracao()
                        self.email.enviar(self.sensores[i].id, self.sensores[i].nome) 
                    
                    #aguarda o tempo configurado ate iniciar a proxima leitura
                    time.sleep(self.tempoDisparo)
                    
                    if self.alarmeLigado:
                        self.status = NORMAL
                    
                    #desliga a sirene se necessario
                    if self.usarSirene == 1:
                        self.sirene.desligar() 
                        
            time.sleep(0.05)

    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()