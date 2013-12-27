#!/usr/bin/python

import Funcao

class Agendamento(object):
    
    #construtor
    def __init__(self, codigo, nome, dataHoraInicial, dataHoraFinal, cAlarme, rele, ativo):
        
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
        
        try:
            conBanco = Funcoes.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            if self.rele == None:
                sql = "insert into Agendamento (DataHoraInicial, DataHoraFinal, EhAlarme) values ({dataInicial}, {dataFinal}, 1)".format(dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
            else:
                sql = "insert into Agendamento (IdRele, DataHoraInicial, DataHoraFinal, EhAlarme) values ({idRele}, {dataInicial}, {dataFinal}, 0)".format(idRele = self.rele.id, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
        
            print sql
        
            cursor.execute(sql)
            conBanco.commit()
            return True
        except:
            conBanco.rollback()
            return False
            
    #funcao para desativar o agendamento no banco de dados
    def desativarRegistroBanco(self): 
    
    #destrutor
    #def __done__(self):
        