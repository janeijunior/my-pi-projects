#!/usr/bin/python

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
        print "Não foi possivel conectar ao banco de dados.", e

    return conBanco
