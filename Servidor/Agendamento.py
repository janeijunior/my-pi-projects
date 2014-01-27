#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import MySQLdb

class Agendamento(object):
    
    #construtor
    def __init__(self, id, nome, dias, equipamentos, dataHoraInicial, dataHoraFinal, ativo, listaReles, alarme):
        
        #atributos publicos da classe
        self.id = id
        self.nome = nome    
        self.dataHoraInicial = dataHoraInicial
        self.dataHoraFinal = dataHoraFinal
        self.alarme = None
        self.ativo = ativo
        self.dias = dias
        self.equipamentos = equipamentos
        self.listaDias = []
        self.reles = []
        
        if self.dias.strip() <> "":
            listaDiasTemp = Funcoes.stringToList(self.dias)
            for dia in listaDiasTemp:
                if dia.strip() <> "":
                    self.listaDias.insert(len(self.listaDias) + 1, dia)
        
        listaEquipamentos = Funcoes.stringToList(self.equipamentos)
        for equip in listaEquipamentos:
            if equip.strip() <> "":
                if equip == "-1":
                    self.alarme = alarme
                else:
                    self.reles.insert(len(self.reles) + 1, listaReles[int(equip)])

    #funcoes    
    #funcao que retorna os nomes dos equipamentos
    def getNomeEquipamento(self):
        equip = ""
        
        if self.alarme <> None:
            equip = "Alarme"
        
        for rele in self.reles:
            if equip == "":
                equip = rele.nome
            else:
                equip = equip + ', ' + rele.nome
        return equip
        
    #funcao para gravar um novo agendamento no banco de dados
    def gravarRegistroBanco(self):
        sql = "insert into Agendamento (Nome, DataHoraInicial, DataHoraFinal, DiasDaSemana, Equipamentos) values ('{nome}', '{dataInicial}', '{dataFinal}', '{dias}', '{equipamentos}')"
        sql = sql.format(nome = self.nome, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal, dias = self.dias, equipamentos = self.equipamentos)
        
        return Funcoes.executarComando(sql)
        
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
        