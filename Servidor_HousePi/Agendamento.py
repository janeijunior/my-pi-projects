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
    #funcao para gravar um novo agendamento no banco de dados
    def gravarAgendamento(self):
        
    #funcao para desativar o agendamento no banco de dados
    def desativarAgendamento(self): 
     
    #destrutor
    #def __done__(self):
        