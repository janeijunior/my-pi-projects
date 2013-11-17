import cgi, cgitb
import smtplib
import sys
import commands

from email.MIMEText import MIMEText

form = cgi.FieldStorage()

efrom = 'rodrigobatistello@hotmail.com'
eto = 'robatistello@gmail.com'
esubject = 'Alarme disparado!'
eservidor = 'smtp.gmail.com'
esenha = form.getvalue('senha')
econteudo = form.getvalue('mensagem')

print 'enviando email\n'
  try:
      msg1 = MIMEText('%s'% econteudo)
      msg1['Subject'] = econteudo
      msg1['From'] = efrom
      msg1['To'] = eto
      serv=smtplib.SMTP(eservidor,587)
      serv.ehlo()
      serv.starttls()
      serv.login(efrom,esenha)
      serv.sendmail(msg1['From'], msg1['To'], msg1.as_string())
      serv.quit()
  except Exception, e:
      print "Erro ",e
  else:
      print "Enviado!"
  print ""