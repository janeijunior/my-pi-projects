#!/usr/bin/python

class Agendamento(object):
    
    #construtor
    def __init__(self, codigo, nome, dataHoraInicial, dataHoraFinal, alarme, rele, ativo):
        
        #atributos publicos da classe
        self.codigo = codigo
        self.nome = nome    
        self.dataHoraInicial = dataHoraInicial
        self.dataHoraFinal = dataHoraFinal
        self.alarme = alarme
        self.rele = rele
        self.ativo = ativo
        
    #funcoes
    #funcao para gravar um novo agendamento no banco de dados
    def gravarRegistroBanco(self):
        
    #funcao para desativar o agendamento no banco de dados
    def desativarRegistroBanco(self): 
    
    #destrutor
    #def __done__(self):
        