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
        try:
            conBanco = Funcoes.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            if self.rele == None:
                sql = "insert into Agendamento (Nome, DataHoraInicial, DataHoraFinal, EhAlarme) values ('{nome}', '{dataInicial}', '{dataFinal}', 1)".format(nome = self.nome, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
            else:
                sql = "insert into Agendamento (Nome, IdRele, DataHoraInicial, DataHoraFinal, EhAlarme) values ('{nome}', {idRele}, '{dataInicial}', '{dataFinal}', 0)".format(nome = self.nome, idRele = self.rele.id, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal)
        
            print sql
        
            cursor.execute(sql)
            conBanco.commit()
            conBanco.close()
            
            return True
        except:
            conBanco.rollback()
            conBanco.close()
            return False
            
    #funcao para remover o agendamento no banco de dados
    def removerRegistroBanco(self): 
        try:
            conBanco = Funcoes.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            sql = "delete from Agendamento where Id = {idRegistro}".format(idRegistro = self.codigo)
        
            print sql
        
            cursor.execute(sql)
            conBanco.commit()
            conBanco.close()
            
            return True
        except:
            conBanco.rollback()
            conBanco.close()
            return False
    
    #funcao para desativar o agendamento no banco de dados
    def desativarRegistroBanco(self): 
        try:
            conBanco = Funcoes.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            sql = "update Agendamento set Ativo = 0 where Id = {idRegistro}".format(idRegistro = self.codigo)
        
            print sql
        
            cursor.execute(sql)
            conBanco.commit()
            conBanco.close()
            
            self.ativo = 0
            
            return True
        except:
            conBanco.rollback()
            conBanco.close()
            return False
    
    #destrutor
    #def __done__(self):
        