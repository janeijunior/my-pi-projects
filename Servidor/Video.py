#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
from pyomxplayer import OMXPlayer
from pprint import pprint
    
class Video(object):
    
    #construtor
    def __init__(self): 
        self.__caminhoVideo = Funcoes.lerConfiguracaoIni("CaminhoVideos")  # Diretorio das musicas
        
    #funcoes
    #retorna a lista de videos de uma pasta pre determinada
    def getListaVideo(self):
        
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
    