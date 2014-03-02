#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base
import Usuario
import TemperaturaHumidade
import SomAmbiente
import Email
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        self.usuario = Usuario.Usuario()
        self.temperaturaHumidade = TemperaturaHumidade.TemperaturaHumidade()
        self.somAmbiente = SomAmbiente.SomAmbiente()
        self.email = Email.Email()
    
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
            root.append(Element("Musicas", Nome=linha.decode('utf-8')))
                
        xmlstr = ET.tostring(root) + "\n"  
        con.send(xmlstr)
    
    #funcao para alterar o usuario e a senha
    def alterarUsuarioSenha(self, root, con):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        if self.usuario.alterarUsuarioSenha(usuario, senha):
            con.send("Ok\n")
        else:
            con.send("Erro\n")
    
    #funcao que grava a nova configuracao de email
    def alterarConfiguracaoEmail(root, con):
        usuario      = root.find("Usuario").text.encode('utf-8')
        senha        = root.find("Senha").text.encode('utf-8')
        destinatario = root.find("Destinatario").text.encode('utf-8')
        servidor     = root.find("Servidor").text.encode('utf-8')
        porta        = root.find("Porta").text.encode('utf-8')
                
        if email.alterarConfiguracao(usuario, destinatario, servidor, porta, senha):
            con.send("Ok\n")
        else:
            con.send("Erro\n")
    
    #envia a configuracao atual de email para o dispositivo
    def enviarConfiguracaoEmail(con):
        root = Element("EnviarConfiguracaoEmail")
        dados = Element("Dados", Usuario = self.email.remetente.decode('utf-8'), Senha = str(self.email.senha).decode('utf-8'), 
                                 Destinatario = self.email.destinatario.decode('utf-8'), Servidor = str(row["ServidorSMTP"]).decode('utf-8'),
                                 Porta = str(self.email.portaSMTP))
        root.append(dados)
        xmlstr = ET.tostring(root) + "\n"       
        con.send(xmlstr)
            