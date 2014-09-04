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
        arquivos = [f for f in listdir(mypath) if isfile(join(mypath,f))]
        print arquivos
        return arquivos
        
    #executa os videos
    def play(self):
        self.omx = OMXPlayer('/home/pi/HousePi/Videos/Ariana.mp4')
        pprint(self.omx.__dict__)
                
    #pausa a musica
    def pause(self):
        self.omx.toggle_pause()
    
    #para a execucao
    def stop(self):
        self.omx.stop()
        
    #avanca ou retrocede a faixa
    def step(self, valor):
    
    #reproduz a faixa a partir do nome
    def playNome(self, valor):
    