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
    def controlarSomAmbiente(self, root, con):
        comando = str(root.find("Comando").text)
        valor   = str(root.find("Valor").text.encode('utf-8'))
        
        if comando == "Play":
            self.somAmbiente.play()
        elif comando == "Pause":
            self.somAmbiente.pause()
        elif comando == "Stop":
            self.somAmbiente.stop()
        elif comando == "AnteriorProxima":
            self.somAmbiente.step(valor)
        elif comando == "Volume":
           self.somAmbiente.volume(valor)
        elif comando == "ReproduzirPorNome":
            self.somAmbiente.playNome(valor)    
    
    #envia a lista de musicas para o aparelho
    def enviarListaMusica(self, con):
        lista = self.somAmbiente.getListaMusica()
        
        root = Element("EnviarListaMusica")

        for linha in lista:
            str = linha[len(PLAYLIST):len(linha) -1]
            root.append(Element("Musicas", Nome=str.decode('utf-8')))
                
        xmlstr = ET.tostring(root) + "\n"  
        con.send(xmlstr)
        