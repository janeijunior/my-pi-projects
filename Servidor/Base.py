#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb 
import Funcoes

class Base(object):  
    
    #funcao para conectar no banco de dados
    def conectarBanco(self):
        try:
            self.__hostBanco    = Funcoes.lerConfiguracaoIni('HostBanco')
            self.__usuarioBanco = Funcoes.lerConfiguracaoIni('UsuarioBanco')
            self.__senhaBanco   = Funcoes.lerConfiguracaoIni('SenhaBanco')
            self.__nomeBanco    = Funcoes.lerConfiguracaoIni('NomeBanco') 
            
            conBanco = MySQLdb.connect(self.__hostBanco, self.__usuarioBanco, self.__senhaBanco)
            conBanco.select_db(self.__nomeBanco)
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