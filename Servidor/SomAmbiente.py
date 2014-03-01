#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class SomAmbiente(object):
    
    #construtor
    def __init__(self):
    
        self.__playlist = Funcoes.lerConfiguracaoIni("CaminhoPlaylist") # Diretorio onde encontra-se a playlist de musicas
        self.__musicas  = Funcoes.lerConfiguracaoIni("CaminhoMusicas")  # Diretorio das musicas
            
    #funcoes
    