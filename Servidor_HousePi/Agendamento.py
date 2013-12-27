#!/usr/bin/python

class Agendamento(object):
    
    #construtor
    def __init__(self, codigo, nome, dataHoraInicio, dataHoraFim, alarme, rele, ativo):
        
        #atributos publicos da classe
        self.codigo = codigo
        self.nome = nome    
        self.dataHoraInicio = dataHoraInicio
        self.dataHoraFim = dataHoraFim
        self.alarme = alarme
        self.rele = rele
        self.ativo = ativo
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.threadAlarme = ThreadAlarme.ThreadAlarme(sirene=self.sirene)
        self.threadAlarme.start() 
        self.alarmeLigado = True
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.threadAlarme.stop()
        self.alarmeLigado = False
    
    #funcao para ler o status do alarme
    def getStatusAlarme(self):
        try:
            return self.threadAlarme.status
        except:
            return 0
            print "Erro ao ler status"
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.sirene.ligar()
        self.panicoAlarmeLigado = True
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        if self.getStatusAlarme() == 0:
            self.sirene.desligar()
        
        self.panicoAlarmeLigado = False
        
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()