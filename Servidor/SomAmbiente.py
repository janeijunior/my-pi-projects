#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class SomAmbiente(object):
    
    #construtor
    def __init__(self):
    
        self.__caminhoPlaylist = Funcoes.lerConfiguracaoIni("CaminhoPlaylist") # Diretorio onde encontra-se a playlist de musicas
        self.__caminhoMusicas  = Funcoes.lerConfiguracaoIni("CaminhoMusicas")  # Diretorio das musicas
            
        __caminhoPlaylist = caminhoPlaylist
        __caminhoMusicas  = caminhoMusicas
        
    #funcoes
    #retorna a lista de musicas de uma pasta pre determinada
    def getListaMusica(self):
        playlist = 'find ' + self.caminhoMusicas + ' -name "*mp3" -o -name "*m4a" -o -name "*wma" -type f | sort > ' + self.caminhoPlaylist
        os.system(playlist)
        arquivo = open(self.caminhoPlaylist)
    
        lista = []
        
        for linha in arquivo:
            str = linha[len(self.caminhoPlaylist):len(linha) -1]
            lista.insert(len(lista) + 1, str)
            
        arquivo.close()
        return lista
    
    #retorna a posicao da musica com o nome passado por parametro
    def getPosicaoMusica(nome):
        arquivo = open(self.caminhoPlaylist)
        
        i = 0
        for linha in arquivo:
            musica = linha[len(self.caminhoPlaylist):len(linha) -5]
            
            if musica == nome:
                return i
                break
                arquivo.close()
            i = i + 1
        
        arquivo.close()
        return 0
    
     #executa um comando no subprocesso do mplayer e devolve o resultado
    def executarComandoMPlayer(cmd, retorno):
        global mplayer
        
        mplayer.stdin.write(cmd + '\n') 
        while select.select([mplayer.stdout], [], [], 0.05)[0]: 
            output = mplayer.stdout.readline()
            print("output: {}".format(output.rstrip()))
            split_output = output.split(retorno + '=', 1)
            if len(split_output) == 2 and split_output[0] == '':
                value = split_output[1]
                return value.rstrip()
        
    #executa a musica
    def play(self):
        try:
            print executarComandoMPlayer("get_file_name", "ANS_FILENAME")   
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            
    #pausa a musica
    def pause(self):
        executarComandoMPlayer("pause", "")
        
    #avanca ou retrocede a faixa
    def step(self, valor):
        try:         
            executarComandoMPlayer("pt_step " + valor, "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)    
            executarComandoMPlayer("pt_step " + str(int(valor) - 1), "")

    #volume
    def volume(self, valor):
        executarComandoMPlayer("set_property volume " + valor, "")
        
    #reproduz a faixa a partir do nome
    def playNome(self, valor):
        try:
            nome = executarComandoMPlayer("get_file_name", "ANS_FILENAME")
            
            if valor <> nome[1:len(nome) -5]: 
                atual = getPosicaoMusica(nome[1:len(nome) -5])
                proxima = getPosicaoMusica(str(valor))
                step = proxima - atual
                executarComandoMPlayer("pt_step " + str(step), "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', self.caminhoPlaylist]
            self.__mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            proxima = getPosicaoMusica(valor)
            
            if proxima <> 0: 
                executarComandoMPlayer("pt_step " + str(proxima), "")           