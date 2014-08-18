#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import subprocess
import select
import os
import time
from pyomxplayer import OMXPlayer
from pprint import pprint
    
class SomAmbiente(object):
    
    #construtor
    def __init__(self): 
        self.__caminhoPlaylist = Funcoes.lerConfiguracaoIni("CaminhoPlaylist") # Diretorio onde encontra-se a playlist de musicas
        self.__caminhoMusicas  = Funcoes.lerConfiguracaoIni("CaminhoMusicas")  # Diretorio das musicas
        self.__mplayer = None
        
    #funcoes
    #retorna a lista de musicas de uma pasta pre determinada
    def getListaMusica(self):
        playlist = 'find ' + self.__caminhoMusicas + ' -name "*mp3" -o -name "*m4a" -o -name "*wma" -type f | sort > ' + self.__caminhoPlaylist
        os.system(playlist)
        arquivo = open(self.__caminhoPlaylist)
    
        lista = []
        
        for linha in arquivo:
            str = linha[len(self.__caminhoPlaylist):len(linha) -1]
            lista.insert(len(lista) + 1, str)
            
        arquivo.close()
        return lista
    
    #retorna a posicao da musica com o nome passado por parametro
    def getPosicaoMusica(self, nome):
        arquivo = open(self.__caminhoPlaylist)
        
        i = 0
        for linha in arquivo:
            musica = linha[len(self.__caminhoPlaylist):len(linha) -5]
            
            if musica == nome:
                return i
                break
                arquivo.close()
            i = i + 1
        
        arquivo.close()
        return 0
    
    #executa um comando no subprocesso do mplayer e devolve o resultado
    def executarComandoMPlayer(self, cmd, retorno):
        self.__mplayer.stdin.write(cmd + '\n') 
        while select.select([self.__mplayer.stdout], [], [], 0.05)[0]: 
            output = self.__mplayer.stdout.readline()
            print("output: {}".format(output.rstrip()))
            split_output = output.split(retorno + '=', 1)
            if len(split_output) == 2 and split_output[0] == '':
                value = split_output[1]
                return value.rstrip()
        
    #executa a musica
    def play(self):
        self.omx = OMXPlayer('/home/pi/HousePi/Videos/Ariana.mp4')
        pprint(self.omx.__dict__)
                
        try:
            print self.executarComandoMPlayer("get_file_name", "ANS_FILENAME")   
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.__caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)            
            
    #pausa a musica
    def pause(self):
        self.executarComandoMPlayer("pause", "")
    
    #para a execucao
    def stop(self):
        self.omx.stop()
        self.executarComandoMPlayer("stop", "")
        
    #avanca ou retrocede a faixa
    def step(self, valor):
        try:         
            self.executarComandoMPlayer("pt_step " + valor, "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.__caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)    
            self.executarComandoMPlayer("pt_step " + str(int(valor) - 1), "")

    #volume
    def volume(self, valor):
        self.executarComandoMPlayer("set_property volume " + valor, "")
        
    #reproduz a faixa a partir do nome
    def playNome(self, valor):
        try:
            time.sleep(0.5)
            
            nome = self.executarComandoMPlayer("get_file_name", "ANS_FILENAME")
            
            time.sleep(0.5)
            
            if valor <> nome[1:len(nome) -5]: 
                atual = self.getPosicaoMusica(nome[1:len(nome) -5])
                proxima = self.getPosicaoMusica(str(valor))
                step = proxima - atual
                self.executarComandoMPlayer("pt_step " + str(step), "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.__caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            proxima = self.getPosicaoMusica(valor)
            
            if proxima <> 0: 
                self.executarComandoMPlayer("pt_step " + str(proxima), "")           