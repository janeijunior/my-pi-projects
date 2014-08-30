#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import Adafruit_DHT

class TemperaturaHumidade(object):
    def getDados(self):
        sensor = Adafruit_DHT.DHT22
        
        humidade, temperatura = Adafruit_DHT.read_retry(sensor, int(Funcoes.lerConfiguracaoIni("GPIODHT")))
        
        if humidade is not None and temperatura is not None:            
            print 'Temperatura={0:0.1f}*C  Humidade={1:0.1f}%'.format(temperatura, humidade)
            
            lista = []
            lista.insert(0, "%.1f" % temperatura)
            lista.insert(1, "%.1f" % humidade)
        else:
            print 'Falha ao obter os dados!'

        return lista
