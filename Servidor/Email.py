#!/usr/bin/python
#-*- coding: utf-8 -*-

import cgi, cgitb
import smtplib
import sys
import commands
import datetime
import thread
import threading
import Funcoes
import Base
import os
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email import Encoders

class Email(Base.Base):
    
    #construtor
    def __init__(self, camera):
        self.carregarConfiguracao()
        self.camera = camera
    
    #função para carregar os dados de envio
    def carregarConfiguracao(self):
        
        row = self.consultarRegistro("select * from ConfiguracaoEmail")
        
        self.remetente    = row["Remetente"]
        self.destinatario = row["Destinatario"]
        self.servidorSMTP = row["ServidorSMTP"]
        self.portaSMTP    = row["PortaSMTP"]
        self.senha        = row["Senha"]
        
    #função para alterar os dados de envio
    def alterarConfiguracao(self, remetente, destinatario, servidorSMTP, portaSMTP, senha):
        sql = '''update ConfiguracaoEmail 
                    set Remetente = '{novoRemetente}', 
                        Senha = '{novaSenha}',
                        Destinatario = '{novoDestinatario}',
                        ServidorSMTP = '{novoServidor}',
                        PortaSMTP = {novaPorta}'''
        
        sql = sql.format(novoRemetente = remetente, novaSenha = senha, novoDestinatario = destinatario, novoServidor = servidorSMTP, novaPorta = portaSMTP)

        if self.executarComando(sql):
            self.remetente    = remetente
            self.destinatario = destinatario
            self.servidorSMTP = servidorSMTP
            self.portaSMTP    = portaSMTP
            self.senha        = senha
                        
            return True
        else:
            return False     
    
    #função chamada como uma thread para enviar o e-mail
    def __threadEnviar(self):
        form = cgi.FieldStorage()
        
        assunto   = "Alarme disparado!"
        separador = "-----------------------------------------------------------\n"
        
        mensagem = "O alarme de sua residencia esta disparado. \n" + separador + "Sensor: {idSensor} - {nomeSensor}\nData e hora do disparo: {dataHora}\n" + separador + "E-mail enviado automaticamento pelo sistema House Pi"
        mensagem = mensagem.format(idSensor = int(self.idSensor), nomeSensor = Funcoes.removerAcentos(self.nomeSensor), dataHora =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        print 'Enviando e-mail\n'
            
        try:
            msg = MIMEMultipart()
            msg['To'] = self.destinatario
            msg['Subject'] = assunto
            msg['From'] = self.remetente
            msg['Pass'] = self.senha
            msg['SMTP'] = self.servidorSMTP
            
            if mensagem != '':
                msg.attach(MIMEText(mensagem))
            
            part = MIMEBase('application', 'octet-stream')
            
            anexo = datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S.jpg")
            device = '/dev/video0'
            self.camera.CapturarImagem(device, anexo)
            
            if anexo != '':
                part.set_payload(open(anexo, 'rb').read())
                part.add_header('Content-Disposition', 'attachment; filename="%s"' %  os.path.basename(anexo))
            
            msg.attach(part)
            Encoders.encode_base64(part)
            mailServer = smtplib.SMTP(msg['SMTP'], int(self.portaSMTP))
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(msg['From'], msg['Pass'])
            mailServer.sendmail(msg['From'], self.destinatario, msg.as_string())
            mailServer.close()
            
        except Exception, e:
            print "Erro no envio do e-mail: ", e
        else:
            print "E-mail enviado!"
    
    #função que inicia a thread que envia o e-mail
    def enviar(self, idSensor, nomeSensor):    
        self.nomeSensor = nomeSensor
        self.idSensor = idSensor
    
        thread.start_new_thread(self.__threadEnviar, ()) 