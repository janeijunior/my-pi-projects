#!/usr/bin/python
#-*- coding: utf-8 -*-

import ConfigParser
import os
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

#retorna a string lida no ini
def lerConfiguracaoIni(nome):
    cfg = ConfigParser.ConfigParser()
    cfg.read(os.path.dirname(os.path.abspath(__file__)) + 'Config.ini')
    return cfg.get('Dados', nome)
    