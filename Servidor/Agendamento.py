#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import Base

class Agendamento(Base.Base):
    
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
        try
            if self.alarme <> None:
                alarme = 1
            else:
                alarme = 0
                
            sql = "insert into Agendamento (Nome, DataHoraInicial, DataHoraFinal, Alarme) values ('{nome}', '{dataInicial}', '{dataFinal}', {alarme}')"
            sql = sql.format(nome = self.nome, dataInicial = self.dataHoraInicial, dataFinal = self.dataHoraFinal, alarme = alarme)
            
            self.executarComando(sql)
        
            self.consultarRegistro("select max(Id) from Agendamento")
            idAgendamento = int(row["Id"])
        
            for str in self.listaDias:
                sql = "insert into DiaAgendamento (IdAgendamento, Dia) values (idAgendamento, Dia)"
                sel = sql.format(idAgendamento = idAgendamento, Dia = int(str))
            
            for str in self.reles:
                sql = "insert into ReleAgendamento (IdAgendamento, IdRele) values (idAgendamento, Dia)"
                sel = sql.format(idAgendamento = idAgendamento, Dia = int(str))
            
        
            return True
        except Exception, e:
            print "Erro ao gravar agendamento: ", e
            return False
        
    #funcao para remover o agendamento no banco de dados
    def removerRegistroBanco(self): 
        sql = "delete from Agendamento where Id = {idRegistro}".format(idRegistro = self.id)
        
        return self.executarComando(sql)
        
    #funcao para desativar o agendamento no banco de dados
    def desativarRegistroBanco(self): 
        sql = "update Agendamento set Ativo = 0 where Id = {idRegistro}".format(idRegistro = self.id)
        
        if self.executarComando(sql):
            self.ativo = 0
            return True
        else:
            return False
            
    #destrutor
    #def __done__(self):