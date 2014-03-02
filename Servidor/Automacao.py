#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base
import Usuario
import TemperaturaHumidade
import SomAmbiente
import Email
import Rele
import Alarme
import Funcoes
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        self.GPIOSirene = int(Funcoes.lerConfiguracaoIni("GPIOSirene")) 
        self.usuario = Usuario.Usuario()
        self.temperaturaHumidade = TemperaturaHumidade.TemperaturaHumidade()
        self.somAmbiente = SomAmbiente.SomAmbiente()
        self.email = Email.Email()
        self.reles = self.getReles()
        self.alarme = Alarme.Alarme(self.reles[self.GPIOSirene], self.email)
    
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
        try:
            for child in root:
                self.reles[int(child.get("Id"))].nome = str(child.get("Nome").encode('utf-8')) 
                self.reles[int(child.get("Id"))].gravarNomeBanco();
            
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
    
    #liga ou desliga o alarme
    def controlarAlarme(self, root, con):
        acao = root.find("Acao").text
        
        if acao == "Ligar":
            self.alarme.ligarAlarme() 
        else:
            self.alarme.desligarAlarme()
        
        con.send("Ok\n")
                
    #liga ou desliga a funcao panico do alarme
    def controlarFuncaoPanico(self, root, con):
        acao = root.find("Acao").text
        
        if acao == "Ligar":
            self.alarme.ligarPanicoAlarme()
        else:
            self.alarme.desligarPanicoAlarme()
        
        con.send("Ok\n")
    
    #funcao que envia o status do alarme
    def enviarConfiguracaoStatusAlarme(self, con):
        root = Element("Alarme")
        status = ""
        
        if self.alarme.status == 1:
            status = "Disparado"
        elif alarme.status == 0:
            status = "Normal"
        else:
            status = "Desligado"
        
        root.append(Element("SensorAlarme", Status=status, Ligado=str(int(self.alarme.alarmeLigado))))
        root.append(Element("PanicoAlarme", Ligado=str(int(self.alarme.panicoAlarmeLigado))))
        
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
        
    #funcao para enviar as configuracoes atuais do alarme
    def enviarConfiguracaoAlarme(self, con):
        root = Element("EnviarConfiguracaoAlarme")
        root.append(Element("Geral", TempoDisparo=str(self.alarme.tempoDisparo), UsarSirene=str(self.alarme.usarSirene), UsarEmail=str(self.alarme.usarEmail)))
    
        for sensor in self.alarme.sensores:
            sensores.append(Element("Sensor" + str(row["Id"]), Nome=str(sensor.nome).decode('utf-8'), Ativo=str(sensor.ativo)))
        
        root.append(sensores)
        xmlstr = ET.tostring(root) + "\n"       
        con.send(xmlstr)
            
    #funcao para gravar as novas configuracoes do alarme
    def alterarConfiguracaoAlarme(root, con):
        try:
            tempoDisparo = int(root.find("TempoDisparo").text)
            usarSirene   = int(root.find("UsarSirene").text
            usarEmail    = int(root.find("UsarEmail").text)
            
            
            self.alarme.alterarConfiguracao(tempoDisparo, usarSirene, usarEmail)
            
            cursor.execute(sql)
            sensores  = root.find("Sensores")
        
            for child in sensores:
                sql = "update SensorAlarme set Nome = '{novoNome}', Ativo = {ativo} where Id = {idSensor}"
                sql = sql.format(novoNome = child.get("Nome").encode('utf-8'), ativo = int(child.get("Ativo")), idSensor = int(child.get("Id")))
                cursor.execute(sql)
            
            conBanco.commit()
            conBanco.close()
            con.send("Ok\n")
        except:
            print "Erro ao executar o comando: " + sql
            con.send("Erro\n")
            conBanco.rollback()
            conBanco.close()