#!/usr/bin/python
#-*- coding: utf-8 -*-

import ConfigParser
from unicodedata import normalize

#remove caracteres invalidos
def removerAcentos(txt, codif='utf-8'):
    if  isinstance(txt, unicode):
        return normalize('NFKD', txt).encode('ASCII','ignore')
    else:
        return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

#transforma uma string delimitada em uma lista
def stringToList(texto):
    lista = []
    lista = texto.split(';')
    return lista

#retorna a configuracao lida do arquivo ini
def lerConfiguracaoIni(nome):
    cfg = ConfigParser.ConfigParser()
    cfg.read('Config.ini')
    return cfg.get('Dados', nome)
    
#funcao para conectar no banco de dados
def conectarBanco():
    HOST   = Funcoes.lerConfiguracaoIni('HostBanco')
    USER   = Funcoes.lerConfiguracaoIni('UsuarioBanco')
    PASSWD = Funcoes.lerConfiguracaoIni('SenhaBanco')
    BANCO  = Funcoes.lerConfiguracaoIni('NomeBanco')

    try:
        conBanco = MySQLdb.connect(HOST, USER, PASSWD)
        conBanco.select_db(BANCO)
    except MySQLdb.Error, e:
        print "Nao foi possivel conectar ao banco de dados.", e

    return conBanco

#persiste um SQL no banco de dados
def executarComando(sql):
    try:
        conBanco = conectarBanco()
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
def consultarRegistro(sql):
    try:
        conBanco = conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        row = cursor.fetchone()
        conBanco.close()
    
        return row
    except:
        print "Erro ao executar o comando: " + sql
        return None

#retorna o resultado da consulta SQL em varias linhas
def consultarRegistros(sql):
    try:
        conBanco = conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conBanco.close()
        
        return rows
    except:
        print "Erro ao executar o comando: " + sql
        return None
    