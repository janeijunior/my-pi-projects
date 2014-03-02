#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb 
import Funcoes

class Base(object):  
    
    #construtor
    def __init__(self):
        self.hostBanco    = Funcoes.lerConfiguracaoIni('HostBanco')
        self.usuarioBanco = Funcoes.lerConfiguracaoIni('UsuarioBanco')
        self.senhaBanco   = Funcoes.lerConfiguracaoIni('SenhaBanco')
        self.nomeBanco    = Funcoes.lerConfiguracaoIni('NomeBanco') 
    
    
    #funcao para conectar no banco de dados
    def conectarBanco(self):
        HOST   = Funcoes.lerConfiguracaoIni('HostBanco')
        USER   = Funcoes.lerConfiguracaoIni('UsuarioBanco')
        PASSWD = Funcoes.lerConfiguracaoIni('SenhaBanco')
        BANCO  = Funcoes.lerConfiguracaoIni('NomeBanco')
    
        try:
            conBanco = MySQLdb.connect(self.hostBanco, self.usuarioBanco, self.senhaBanco)
            conBanco.select_db(self.nomeBanco)
        except MySQLdb.Error, e:
            print "Nao foi possivel conectar ao banco de dados.", e
    
        return conBanco
    
    #persiste um SQL no banco de dados
    def executarComando(self, sql):
        try:
            conBanco = self.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            conBanco.commit()
            conBanco.close()
            return True
        except:
            conBanco.rollback()
            conBanco.close()
            print "Erro ao executar o comando: " + sql
            return False
    
    #retorna o resultado da consulta SQL em uma linha
    def consultarRegistro(self, sql):
        try:
            conBanco = self.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            row = cursor.fetchone()
            conBanco.close()
        
            return row
        except:
            print "Erro ao executar o comando: " + sql
            return None
    
    #retorna o resultado da consulta SQL em varias linhas
    def consultarRegistros(self, sql):
        try:
            conBanco = self.conectarBanco()
            cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            rows = cursor.fetchall()
            conBanco.close()
            
            return rows
        except:
            print "Erro ao executar o comando: " + sql
            return None