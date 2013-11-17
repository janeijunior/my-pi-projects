import cgi, cgitb
import smtplib
import sys
import commands

from email.MIMEText import MIMEText

def EnviarEmail():
    form = cgi.FieldStorage()
    
    remetente = 'robatistello@gmail.com'
    destinatario = 'rodrigobatistello@hotmail.com'
    assunto = 'Alarme disparado!'
    servidor = 'smtp.gmail.com'
    porta = 587
    senha = 'britsp3021281ney'
    conteudo = 'E-mail enviado automaticamento pelo aplicativo House Pi'
    
    print 'Enviando e-mail\n'
    try:
        msg = MIMEText('%s'% conteudo)
        msg['Subject'] = assunto
        msg['From'] = remetente
        msg['To'] = destinatario
        
        smtp = smtplib.SMTP(servidor, porta)
        
        smtp.ehlo()
        smtp.starttls()
        smtp.login(remetente, senha)
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp.quit()
    except Exception, e:
        print "Erro: ",e
    else:
        print "Enviado!"