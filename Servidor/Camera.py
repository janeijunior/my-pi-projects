#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class Camera(object):
    
    #construtor
    def __init__(self):
        self.MJPG = Funcoes.lerConfiguracaoIni("CaminhoMJPG") # Caminho stream de video
    
    