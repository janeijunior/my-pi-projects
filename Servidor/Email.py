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

class EnviarEmail(Base.Base):
    def __init__(self):
        self.carregarDados()
    
    def carregarDados(self):
        
        
        self.remetente = remetente
        self.senha = senha
        self.destinatario = destinatario
        self.servidorSMTP = servidorSMTP
        self.portaSMTP = portaSMTP
        self.nomeSensor = nomeSensor
        self.idSensor = idSensor
    
    def __threadEnviar(self):
        form = cgi.FieldStorage()
        
        assunto  = "Alarme disparado!"
        separador = "-----------------------------------------------------------\n"
        
        conteudo = "O alarme de sua residencia esta disparado. \n" + separador + "Sensor: {idSensor} - {nomeSensor}\nData e hora do disparo: {dataHora}\n" + separador + "E-mail enviado automaticamento pelo sistema House Pi"
        conteudo = conteudo.format(idSensor = int(self.idSensor), nomeSensor = Funcoes.removerAcentos(self.nomeSensor), dataHora =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        print 'Enviando e-mail\n'
            
        try:
            msg = MIMEText('%s'% conteudo)
            msg['Subject'] = assunto
            msg['From'] = self.remetente
            msg['To'] = self.destinatario
            smtp = smtplib.SMTP(self.servidorSMTP, int(self.portaSMTP))
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.remetente, self.senha)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.quit()
        except Exception, e:
            print "Erro no envio do e-mail: ", e
        else:
            print "E-mail enviado!"
    
    def enviar(self):
        thread.start_new_thread(self.__threadEnviar)        