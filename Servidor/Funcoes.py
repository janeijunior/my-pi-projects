#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb
from unicodedata import normalize

#funcao para conectar no banco de dados
def conectarBanco():
    HOST   = "localhost"
    USER   = "root"
    PASSWD = "batistello"
    BANCO  = "HousePi"

    try:
        conBanco = MySQLdb.connect(HOST, USER, PASSWD)
        conBanco.select_db(BANCO)
    except MySQLdb.Error, e:
        print "Nao foi possivel conectar ao banco de dados.", e

    return conBanco

#persiste um SQL no banco de dados
def executarSql(sql):
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
        return False
        
#retorna o resultado da consulta SQL
def consultarSql(sql):

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