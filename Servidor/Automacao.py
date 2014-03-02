#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base
import Usuario
import TemperaturaHumidade
import SomAmbiente
import Email
import Rele
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        self.usuario = Usuario.Usuario()
        self.temperaturaHumidade = TemperaturaHumidade.TemperaturaHumidade()
        self.somAmbiente = SomAmbiente.SomAmbiente()
        self.email = Email.Email()
        self.reles = self.getReles();
    
    #funcoes da classe
    
    #retorna uma lista com os reles já configurados
    def getReles(self):
        rows  = self.consultarRegistros("select * from Rele")
        lista = []

        for row in rows:
            rele = Rele.Rele(row["Id"], row["NumeroGPIO"], row["Status"], row["Nome"])        
            
            if rele.status == 1:
                rele.ligar()
            else:
                rele.desligar()
            
            lista.insert(row["Id"], rele)    
    
    return lista
    
    #liga ou desliga os reles/atuadores
    def controlarRele(self, root, con):
        acao   = root.find("Acao").text
        numero = root.find("Numero").text
        
        if acao == "Ligar":
            self.reles[int(numero)].ligar()
        else:
            self.reles[int(numero)].desligar()
        
        con.send("Ok\n")
    
    #funcao que envia as configuracoes dos reles e status
    def enviarConfiguracaoStatusRele(self, con):
        root = Element("StatusRele")
        
        for rele in self.reles:
            root.append(Element("Rele" + str(rele.id), Status=str(rele.status), Nome=rele.nome.decode('utf-8')))
        
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
    
    #funcao para renomear os reles atraves da aba de configuracoes
    def alterarConfiguracaoRele(self, root, con):
        global listaReles
        
        try:
            for child in root:
                listaReles[int(child.get("Id"))].nome = str(child.get("Nome").encode('utf-8')) 
                listaReles[int(child.get("Id"))].gravarNomeBanco();
            
            con.send("Ok\n")
        except:
            con.send("Erro\n")
    
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
    def alterarConfiguracaoEmail(self, root, con):
        usuario      = root.find("Usuario").text.encode('utf-8')
        senha        = root.find("Senha").text.encode('utf-8')
        destinatario = root.find("Destinatario").text.encode('utf-8')
        servidor     = root.find("Servidor").text.encode('utf-8')
        porta        = root.find("Porta").text.encode('utf-8')
                
        if self.email.alterarConfiguracao(usuario, destinatario, servidor, porta, senha):
            con.send("Ok\n")
        else:
            con.send("Erro\n")
    
    #envia a configuracao atual de email para o dispositivo
    def enviarConfiguracaoEmail(self, con):
        root = Element("EnviarConfiguracaoEmail")
        dados = Element("Dados", Usuario = self.email.remetente.decode('utf-8'), Senha = str(self.email.senha).decode('utf-8'), 
                                 Destinatario = self.email.destinatario.decode('utf-8'), Servidor = str(self.email.servidorSMTP).decode('utf-8'),
                                 Porta = str(self.email.portaSMTP))
        root.append(dados)
        xmlstr = ET.tostring(root) + "\n"       
        con.send(xmlstr)
            