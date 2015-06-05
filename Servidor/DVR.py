#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import date, datetime
import socket
import thread
import threading
import signal
import sys
import urllib
import time

class DVR(threading.Thread):
    def __init__(self, reles):
        threading.Thread.__init__(self)
        self.name = 'ThreadDRV'
        self.__stop_thread_event = threading.Event()

        self.listaRele = reles
        self.tempo = 0
        self.ativo = True
	    self.thread = None

    def stop(self):
        self.__stop_thread_event.set()

    def controlarRele(self):
    	while self.ativo:
    	    if self.tempo > 0:
    		    if self.listaRele[0].status == 0:
    		        if self.listaRele[0].ligar():
    			        self.listaRele[0].automatico = True
    			        #self.listaRele[0].atualizarStatusBanco()
    
    	    elif (self.tempo == 0) and (self.listaRele[0].automatico):
                if self.listaRele[0].status == 1:
    	            if self.listaRele[0].desligar():
    			        self.listaRele[0].automatico = False
                        #self.listaRele[0].atualizarStatusBanco()
    			
    	    if self.tempo > 0:
    	        self.tempo = self.tempo - 1
    	
    	    time.sleep(1)

    def run(self):      
   	    self.thread = threading.Thread(None, self.controlarRele, None, ())
        self.thread.start()

	    orig = ("", 2344)
    
    	tcp  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	tcp.bind(orig)
    	tcp.listen(1)
          	 
    	print "Aguardando notificacoes do DVR..."
    
    	while not self.__stop_thread_event.isSet():
       	    conexao, cliente = tcp.accept()
       
       	    msg = conexao.recv(1024)
		
	        print "Comando DVR: " + msg + " Tamanho: " + str(len(msg))

            horaAtual = datetime.now().strftime("%H%M%S")

            ligar = datetime.strptime("180000", "%H%M%S")
            desligar = datetime.strptime("060000", "%H%M%S")
            anoitecer = datetime.strptime("235959", "%H%M%S")
            amanhecer = datetime.strptime("000001", "%H%M%S")

            horaLigar = ligar.strftime("%H%M%S")
            horaDesligar = desligar.strftime("%H%M%S")
            horaAnoitecer = anoitecer.strftime("%H%M%S")
            horaAmanhecer = amanhecer.strftime("%H%M%S")

            if  len(msg) > 0:
	            if ((horaAtual > horaLigar) and (horaAtual < horaAnoitecer)) or ((horaAtual > horaAmanhecer) and (horaAtual < horaDesligar)):
		            self.tempo = 10
       
   	tcp.close()
	self.ativo = False
