#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
from pyomxplayer import OMXPlayer
from pprint import pprint
from os import listdir
from os.path import isfile, join
    
class Video(object):
    
    #construtor
    def __init__(self): 
        self.__caminhoVideos = Funcoes.lerConfiguracaoIni("CaminhoVideos")
        
    #funcoes
    #retorna a lista de videos de uma pasta pre determinada
    def getListaVideo(self):
        arquivos = [f for f in listdir(self.__caminhoVideos) if isfile(join(self.__caminhoVideos,f))]
        print arquivos
        return arquivos
        
    def pause(self):
        self.omx.toggle_pause()
    
    #para a execucao
    def stop(self):
        self.omx.stop()
        
    #reproduz a partir do nome
    def playNome(self, valor):
        self.stop()
        self.omx = OMXPlayer(self.__caminhoVideos + valor)