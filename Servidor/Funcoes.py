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
    