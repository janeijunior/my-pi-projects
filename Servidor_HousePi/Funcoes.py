#!/usr/bin/python

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

#remove caracteres invalidos
def removerAcentos(txt, codif='utf-8'):
    if  isinstance(txt, unicode):
        return normalize('NFKD', txt).encode('ASCII','ignore')
    else:
        return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

#converte para ISO-8859-1
def converterISO(txt, codif='utf-8'):
    if  isinstance(txt, unicode):
        return txt.encode('ISO-8859-1','ignore')
    else:
        return txt.decode(codif).encode('ISO-8859-1','ignore')
