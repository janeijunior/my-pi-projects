#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base
import Usuario
import TemperaturaHumidade
import SomAmbiente
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        self.usuario = Usuario.Usuario()
        self.temperaturaHumidade = TemperaturaHumidade.TemperaturaHumidade()
        self.somAmbiente = SomAmbiente.SomAmbiente()
    
    #funcoes da classe
    
    #função para validar o usuario e a senha, se nao estiverem certos desconecta!
    def efetuarLogin(self, root, con):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        if self.usuario.validarLogin(usuario, senha):
            con.send("Logado\n")
        else:
            con.send("NaoLogado\n")
            con.close
    
    #le o sensor de temperatura e humidade e envia os resultados
    def enviarTemperaturaHumidade(self, con):    
        #global listaConexoesCamera
        
        try:
            #desligarCamera()
            #time.sleep(1)
            
            resultado = self.temperaturaHumidade.getDados()    
            root  = Element("TemperaturaHumidade")
            dados = Element("Dados", Temperatura=resultado[0], Humidade=resultado[1])
            root.append(dados)
            xmlstr = ET.tostring(root) + "\n"   
            con.send(xmlstr)    
            
            #if len(listaConexoesCamera) > 0:
            #    ligarCamera()        
        except Exception as e: 
            print "Erro: ", e
            con.send("Erro\n")
            
            #if len(listaConexoesCamera) > 0:
            #    ligarCamera() 
    
    #controla o som ambiente
    def controlarSomAmbiente(self, root, con)
        comando = str(root.find("Comando").text)
        valor   = str(root.find("Valor").text.encode('utf-8'))
        
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
    
            