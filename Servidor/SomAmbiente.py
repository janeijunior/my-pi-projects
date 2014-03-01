#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class SomAmbiente(object):
    
    #construtor
    def __init__(self):
    
        self.__caminhoPlaylist = Funcoes.lerConfiguracaoIni("CaminhoPlaylist") # Diretorio onde encontra-se a playlist de musicas
        self.__caminhoMusicas  = Funcoes.lerConfiguracaoIni("CaminhoMusicas")  # Diretorio das musicas
            
        __caminhoPlaylist = caminhoPlaylist
    #funcoes
    #retorna a lista de musicas de uma pasta pre determinada
    def getListaMusica(self):
        playlist = 'find ' + MUSICAS + ' -name "*mp3" -o -name "*m4a" -o -name "*wma" -type f | sort > ' + self.__caminhoPlaylist
        os.system(playlist)
        arquivo = open(self.__caminhoPlaylist)
    
        lista = []
        
        for linha in arquivo:
            str = linha[len(PLAYLIST):len(linha) -1]
            lista.insert(len(lista) + 1, str)
            
        arquivo.close()
        return lista
    
    #retorna a posicao da musica com o nome passado por parametro
    def __getPosicaoMusica(nome):
        arquivo = open(self.caminhoPlaylist)
        
        i = 0
        for linha in arquivo:
            musica = linha[len(PLAYLIST):len(linha) -5]
            
            if musica == nome:
                return i
                break
                arquivo.close()
            i = i + 1
        
        return 0
        arquivo.close()
        
    #controla o mplayer do linux
    def controlarSomAmbiente(root, con):
        global mplayer
        
        comando = str(root.find("Comando").text)
        valor = str(root.find("Valor").text.encode('utf-8'))
        
        if comando == "Play":
            try:
                print executarComandoMPlayer("get_file_name", "ANS_FILENAME")   
            except:
                cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
                mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        elif comando == "Pause":
            executarComandoMPlayer("pause", "")
        elif comando == "Stop":
            executarComandoMPlayer("stop", "")
        elif comando == "AnteriorProxima":
            try:         
                executarComandoMPlayer("pt_step " + valor, "")
            except:
                cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
                mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)    
                executarComandoMPlayer("pt_step " + str(int(valor) - 1), "")
        elif comando == "Volume":
           executarComandoMPlayer("set_property volume " + valor, "")
        elif comando == "ReproduzirPorNome":
            try:
                nome = executarComandoMPlayer("get_file_name", "ANS_FILENAME")
                
                if valor <> nome[1:len(nome) -5]: 
                    atual = getPosicaoMusica(nome[1:len(nome) -5])
                    proxima = getPosicaoMusica(str(valor))
                    step = proxima - atual
                    executarComandoMPlayer("pt_step " + str(step), "")
            except:
                cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
                mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                proxima = getPosicaoMusica(valor)
                
                if proxima <> 0: 
                    executarComandoMPlayer("pt_step " + str(proxima), "")
            
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
