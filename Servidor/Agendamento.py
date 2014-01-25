#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import MySQLdb

class Agendamento(object):
    
    #construtor
    def __init__(self, id, nome, dias, equipamentos, dataHoraInicial, dataHoraFinal, ativo):
        
        #atributos publicos da classe
        self.id = id
        self.nome = nome    
        self.dataHoraInicial = dataHoraInicial
        self.dataHoraFinal = dataHoraFinal
        self.alarme = None
        self.reles = []
        self.ativo = ativo
        self.dias = dias
        self.equipamentos = equipamentos
        self.listaDias = []
        
    #funcoes
    #funcao que retorna a string delimitada dos equipamentos
    def getEquipamentos(self):
        equip = ""
        
        if self.alarme <> None:
            equip = "-1;"
        
        for rele in self.reles:
            equip = equip + str(rele.id) + ";"
            
        return equip
    
    #funcao que retorna os dias da semana delimitados
    def getDias(self):
        strDias = ""
        
        for dia in self.dias:
            strDias = strDias + str(dia) + ";"
            
        return strDias
    
    #funcao para gravar um novo agendamento no banco de dados
    def gravarRegistroBanco(self):
        try:
            conBanco = Funcoes.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            
            sql = "insert into Agendamento (Nome, DataHoraInicial, DataHoraFinal, DiasDaSemana, Equipamentos) values ('{nome}', '{dataInicial}', '{dataFinal}', '{dias}', '{equipamentos}')"
            sql = sql.format(nome = self.nome, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal, dias = self.getDias(), equipamentos = self.getEquipamentos())
            
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
            
            sql = "delete from Agendamento where Id = {idRegistro}".format(idRegistro = self.id)
        
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
            
            sql = "update Agendamento set Ativo = 0 where Id = {idRegistro}".format(idRegistro = self.id)
        
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
        