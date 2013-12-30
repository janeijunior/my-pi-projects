#!/usr/bin/python

import cgi, cgitb
import smtplib
import sys
import commands
import datetime
import thread
import threading

from email.MIMEText import MIMEText

class EnviarEmail(threading.Thread):
    def __init__(self, remetente, senha, destinatario, servidorSMTP, portaSMTP, nomeSensor, idSensor):
        threading.Thread.__init__(self)
        self.name = 'ThreadEnviaEmail' 
        
        self.remetente = remetente
        self.senha = senha
        self.destinatario = destinatario
        self.servidorSMTP = servidorSMTP
        self.portaSMTP = portaSMTP
        self.nomeSensor = nomeSensor
        self.idSensor = idSensor
    
    def run(self):
        form = cgi.FieldStorage()
        
        assunto  = 'Alarme disparado!'
        
        conteudo = '''       O alarme de sua residencia esta disparado.
        -----------------------------------------------------------
        Sensor: {idSensor} - {nomeSensor}  
        Data e hora do dispado: {dataHora}
        -----------------------------------------------------------
        E-mail enviado automaticamento pelo sistema House Pi'''.format(idSensor = int(self.idSensor), nomeSensor = self.nomeSensor, dataHora =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
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
            print "Erro no envio do e-mail: ",e
        else:
            print "E-mail enviado!"