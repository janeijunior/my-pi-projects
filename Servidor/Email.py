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
from email.MIMEText import MIMEText

class Email(Base.Base):
    def __init__(self):
        self.carregarDados()
    
    def carregarDados(self):
        
        row = Funcoes.consultarRegistro("select * from ConfiguracaoEmail")
        
        self.remetente    = row["Remetente"]
        self.destinatario = row["Destinatario"]
        self.servidorSMTP = row["ServidorSMTP"]
        self.portaSMTP    = row["PortaSMTP"]
        self.senha        = row["Senha"]
        
    def __threadEnviar(self):
        form = cgi.FieldStorage()
        
        assunto  = "Alarme disparado!"
        separador = "-----------------------------------------------------------\n"
        
        conteudo = "O alarme de sua residencia esta disparado. \n" + separador + "Sensor: {idSensor} - {nomeSensor}\nData e hora do disparo: {dataHora}\n" + separador + "E-mail enviado automaticamento pelo sistema House Pi"
        conteudo = conteudo.format(idSensor = int(self.idSensor), nomeSensor = Funcoes.removerAcentos(self.nomeSensor), dataHora =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        print 'Enviando e-mail\n'
            
        try:
            msg = MIMEText('%s'% conteudo)
            print 'msg'
            msg['Subject'] = assunto
            print 'assunto'
            msg['From'] = self.remetente
            print 'reme'
            msg['To'] = self.destinatario
            print 'dest'
            smtp = smtplib.SMTP(self.servidorSMTP, int(self.portaSMTP))
            print 'server'
            smtp.ehlo()
            smtp.starttls()
            print "login"
            smtp.login(self.remetente, self.senha)
            print "logou"
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            print "enviou"
            smtp.quit()
        except Exception, e:
            print "Erro no envio do e-mail: ", e
        else:
            print "E-mail enviado!"
    
    def enviar(self, idSensor, nomeSensor):    
        self.nomeSensor = nomeSensor
        self.idSensor = idSensor
    
        thread.start_new_thread(self.__threadEnviar, ())        