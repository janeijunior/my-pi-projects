#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base
import Usuario
import TemperaturaHumidade
import SomAmbiente
import Email
import Rele
import Alarme
import Camera
import Funcoes
import time
import os
import Agendamento
import ControleAgendamento
import xml.etree.ElementTree as ET
import Adafruit_DHT
import RFID

from xml.etree.ElementTree import Element

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        
        #atributos
        self.GPIOSirene = int(Funcoes.lerConfiguracaoIni("GPIOSirene")) 
        self.GPIODHT = int(Funcoes.lerConfiguracaoIni("GPIODHT"))
        self.usuario = Usuario.Usuario()
        self.somAmbiente = SomAmbiente.SomAmbiente()
        self.email = Email.Email()
        self.camera = Camera.Camera(self.usuario)
        self.reles = []
        self.carregarReles()
        self.alarme = Alarme.Alarme(self.reles[self.GPIOSirene], self.email)
        self.controleAgendamento = None
        self.agendamentos = []
        self.carregarAgendamentos()
        self.controleAgendamento = ControleAgendamento.ControleAgendamento(self.agendamentos)
        self.controleAgendamento.start() 
        self.RFID = RFID.RFID(self.alarme)
        self.RFID.start()
        self.card = []
        self.carregarTag()
        
    #funcoes da classe
    
    #carrega a lista com os reles já configurados
    def carregarReles(self):
        rows  = self.consultarRegistros("select * from Rele")
        self.reles = []

        for row in rows:
            rele = Rele.Rele(row["Id"], row["NumeroGPIO"], row["Status"], row["Nome"])        
            
            if rele.status == 1:
                rele.ligar()
                rele.atualizarStatusBanco()
            else:
                rele.desligar()
                rele.atualizarStatusBanco()
                
            self.reles.insert(row["Id"], rele)    
    
    #liga ou desliga os reles/atuadores
    def controlarRele(self, root, con):
        acao   = root.find("Acao").text
        numero = root.find("Numero").text
        
        if acao == "Ligar":
            if self.reles[int(numero)].ligar():
                con.send("Ok\n")
                self.reles[int(numero)].atualizarStatusBanco()
            else:
                con.send("Erro\n")
            
        else:
            if self.reles[int(numero)].desligar():
                con.send("Ok\n")
                self.reles[int(numero)].atualizarStatusBanco()
            else:
                con.send("Erro\n")
    
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
        sensor = Adafruit_DHT.DHT22
        humidade, temperatura = Adafruit_DHT.read_retry(sensor, self.GPIODHT)
        
        if humidade is not None and temperatura is not None:            
            print 'Temperatura = {0:0.1f}*C  Humidade = {1:0.1f}%'.format(temperatura, humidade)
            
            root  = Element("TemperaturaHumidade")
            dados = Element("Dados", Temperatura="%.1f" % temperatura, Humidade="%.1f" % humidade)
            root.append(dados)
            xmlstr = ET.tostring(root) + "\n"   
            con.send(xmlstr)    
        else:
            print 'Falha ao obter os dados!'
            con.send("Erro\n")
    
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

    #liga ou desliga o alarme se validar o RFID
    def controlarRFID(self, root):
        cartao = ''
        
        for child in root:
            cartao = str(child.get("Cartao")) 
        
        if cartao in card:
            if self.alarme.alarmeLigado:
                self.alarme.desligarAlarme()
            else:
                self.alarme.ligarAlarme()

    #liga ou desliga a funcao panico do alarme
    def controlarFuncaoPanico(self, root, con):
        acao = root.find("Acao").text
        
        if acao == "Ligar":
            self.alarme.ligarPanico()
        else:
            self.alarme.desligarPanico()
        
        con.send("Ok\n")
    
    #funcao que envia o status do alarme
    def enviarConfiguracaoStatusAlarme(self, con):
        root = Element("Alarme")
        status = ""
        
        if self.alarme.status == 1:
            status = "Disparado"
        elif self.alarme.status == 0:
            status = "Normal"
        else:
            status = "Desligado"
        
        root.append(Element("SensorAlarme", Status=status, Ligado=str(int(self.alarme.alarmeLigado))))
        root.append(Element("PanicoAlarme", Ligado=str(int(self.alarme.panicoLigado))))
        
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
        
    #funcao para enviar as configuracoes atuais do alarme
    def enviarConfiguracaoAlarme(self, con):
        root = Element("EnviarConfiguracaoAlarme")
        root.append(Element("Geral", TempoDisparo=str(self.alarme.tempoDisparo), UsarSirene=str(self.alarme.usarSirene), UsarEmail=str(self.alarme.enviarEmail)))
    
        sensores = Element("Sensores")
        
        for sensor in self.alarme.sensores:
            sensores.append(Element("Sensor" + str(sensor.id), Nome=str(sensor.nome).decode('utf-8'), Ativo=str(sensor.ativo)))
        
        root.append(sensores)
        xmlstr = ET.tostring(root) + "\n" 
        con.send(xmlstr)
            
    #funcao para gravar as novas configuracoes do alarme
    def alterarConfiguracaoAlarme(self, root, con):
        try:
            self.alarme.tempoDisparo = int(root.find("TempoDisparo").text)
            self.alarme.usarSirene   = int(root.find("UsarSirene").text)
            self.alarme.enviarEmail  = int(root.find("UsarEmail").text)
            
            self.alarme.gravarConfiguracaoBanco()
            sensores  = root.find("Sensores")
        
            for child in sensores:
                id = int(child.get("Id")) 
                
                self.alarme.sensores[id].nome  = child.get("Nome").encode('utf-8')
                self.alarme.sensores[id].ativo = int(child.get("Ativo"))
                self.alarme.sensores[id].gravarRegistroBanco()
                
            con.send("Ok\n")
        except Exception, e:
            print "Erro ao alterar configuração do alarme: ", e
            con.send("Erro\n")
    
    #liga ou desliga o servico da camera
    def controlarCamera(self, root, con, cliente):
        acao = root.find("Acao").text  
        device = root.find("Camera").text  
        
        if acao == "Ligar":
            if self.camera.device <> device:
                self.camera.desligar()
            
            self.camera.device = device
            self.camera.adicionarConexao(cliente) 
            self.camera.acionamento()
            con.send("Ok\n")
        else:
            con.send("Ok\n")
            self.camera.removerConexao(cliente)
    
    #carregar lista de agendamentos
    def carregarAgendamentos(self):
        self.agendamentos = []
    
        rows = self.consultarRegistros("select * from Agendamento where Ativo = 1")
    
        for row in rows:
            dias = ''
            
            if int(row["Alarme"]) == 1:
                equipamentos = "-1;"
            else:
                equipamentos = ''
                
            rowsdia = self.consultarRegistros("select Dia from DiaAgendamento where IdAgendamento = {id}".format(id = row["Id"]))
            for rowdia in rowsdia:
                dias = dias + str(rowdia["Dia"]) + ";"
            
            rowsequip = self.consultarRegistros("select IdRele from ReleAgendamento where IdAgendamento = {id}".format(id = row["Id"]))
            for rowequip in rowsequip:
                equipamentos = equipamentos + str(rowequip["IdRele"]) + ";"
            
            agendamento = Agendamento.Agendamento(row["Id"], row["Nome"], dias, equipamentos, row["DataHoraInicial"], row["DataHoraFinal"], int(row["Ativo"]), self.reles, self.alarme)        
            self.agendamentos.insert(row["Id"], agendamento)    
            
    #funcao que insere um novo agendamento no banco de dados e alualiza a lista de agendamentos 
    def gravarAgendamento(self, root, con):
        agendamento = Agendamento.Agendamento(0, root.find("Nome").text.encode('utf-8'), root.find("Dias").text, root.find("Equipamentos").text,
                                              root.find("DataHoraInicial").text, root.find("DataHoraFinal").text, 1, self.reles, self.alarme)
        
        if agendamento.gravarRegistroBanco():
            con.send("Ok\n")
            self.carregarAgendamentos()
            self.controleAgendamento.listaAgendamento = self.agendamentos
        else:
            con.send("Erro\n")
    
    #funcao que retorna os agendamentos do servidor para o aplicativo movel
    def enviarAgendamento(self, con):
        root = Element("EnviarAgendamento")
        
        self.carregarAgendamentos()
        
        for agendamento in self.agendamentos:
            root.append(Element("Agendamento" + str(agendamento.id), Id=str(agendamento.id), Nome=agendamento.nome.decode('utf-8'), 
                                DataHoraInicial=str(agendamento.dataHoraInicial), DataHoraFinal=str(agendamento.dataHoraFinal), 
                                Dias=agendamento.dias, Equipamentos=agendamento.equipamentos, NomeEquipamentos=agendamento.getNomeEquipamento().decode('utf-8')))
                    
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
    
    #funcao que remove o agendamento da lita e do banco de dados
    def removerAgendamento(self, root, con):
        for agendamento in self.agendamentos:
            if agendamento.id == int(root.find("Id").text):
                if agendamento.removerRegistroBanco():
                    con.send("Ok\n")
                    self.carregarAgendamentos()
                    self.controleAgendamento.listaAgendamento = self.agendamentos
                    break
                else:
                    con.send("Erro\n")
	
    #funcao para enviar os ultimos disparos do alarme
    def enviarUltimosDisparos(self, con):
        root = Element("EnviarUltimosDisparos")
        rows = self.alarme.getUltimosDisparos() 
        
        for row in rows:	
            root.append(Element("Disparo", Id=str(row["Id"]),  NomeSensor=row["Nome"].decode('utf-8'), DataHora=str(row["DataHora"])))
                    
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
    
    #controla a inserção, remoção das tags RFID
    def configuracaoRFID(self, root, con):
        comando = str(root.find("Comando").text)
        valor   = str(root.find("Valor").text.encode('utf-8'))
        
        if comando == "Adicionar":
            sql = "insert into RFID (Tag) values ('{tag}')".format(tag = valor)
            self.executarComando(sql)
        elif comando == "Remover":
            sql = "delete from RFID where Tag = '{tag}'".format(tag = valor)
            self.executarComando(sql)
        
        con.send("Ok\n")
        self.carregarTag()
        
    #envia as tags RFID cadastradas
    def enviarRFID(self, con):
        root = Element("EnviarRFID")
        rows = self.consultarRegistros("select Tag from RFID") 
        
        for row in rows:    
            root.append(Element("RFID", Tag=str(row["Tag"])))
                    
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)
    
    #carrega as tags na lista
    def carregarTag(self):
        rows  = self.consultarRegistros("select * from RFID")
        self.card = []

        for row in rows:
            self.card.insert(row["Id"], row["Tag"])    

    #remove o cliente
    def removerConexao(self, cliente):
        self.camera.removerConexao(cliente)

    #Finaliza os processos em execucao para encerrar o aplicativo servidor
    def finalizarProcessos(self):
        if self.alarme.alarmeLigado:
            alarme.desligarAlarme()
        
        self.alarme.desligarPanico()
        self.controleAgendamento.stop()
        self.RFID.stop()
        
        for rele in self.reles:    
    		rele.desligar()
    	
        self.camera.desligar()
    
    #funcao para reiniciar ou desligar o servidor conforme solicitado pelo app android
    def reiniciarDesligarServidor(self, root, con):
        acao = root.find("Acao").text
        self.finalizarProcessos()
        con.send("Ok\n")    
        
        if acao == "Reiniciar":
            os.system("/usr/bin/sudo /sbin/shutdown -r now")
        else:
            s.system("/usr/bin/sudo /sbin/shutdown -h now")