#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb 
import Funcoes

class Base(object):  
    
    #funcao para conectar no banco de dados
    def conectarBanco(self):
        try:
            hostBanco    = Funcoes.lerConfiguracaoIni('HostBanco')
            usuarioBanco = Funcoes.lerConfiguracaoIni('UsuarioBanco')
            senhaBanco   = Funcoes.lerConfiguracaoIni('SenhaBanco')
            nomeBanco    = Funcoes.lerConfiguracaoIni('NomeBanco') 
            
            conBanco = MySQLdb.connect(hostBanco, usuarioBanco, senhaBanco)
            conBanco.select_db(nomeBanco)
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