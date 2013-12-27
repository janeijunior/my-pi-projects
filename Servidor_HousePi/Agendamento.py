#!/usr/bin/python

import Funcoes
import MySQLdb

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
    

        #try:
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        if self.rele == None:
            sql = "insert into Agendamento (Nome, DataHoraInicial, DataHoraFinal, EhAlarme) values ('{nome}', '{dataInicial}', '{dataFinal}', 1)".format(nome = self.nome, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
        else:
            sql = "insert into Agendamento (Nome, IdRele, DataHoraInicial, DataHoraFinal, EhAlarme) values ('{nome}', {idRele}, '{dataInicial}', '{dataFinal}', 0)".format(nome = self.nome, idRele = self.rele.id, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
    
        print sql
    
        cursor.execute(sql)
        conBanco.commit()
        return True
        #except:
        #    conBanco.rollback()
        #    return False
            
    #funcao para desativar o agendamento no banco de dados
    #def desativarRegistroBanco(self): 
    
    #destrutor
    #def __done__(self):
        