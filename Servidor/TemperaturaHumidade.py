#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes
import Adafruit_DHT

class TemperaturaHumidade(object):
    def getDados(self):
        sensor = Adafruit_DHT.DHT22
        pin = Funcoes.lerConfiguracaoIni("GPIODHT")
        
        humidade, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity is not None and temperature is not None:            
            print 'Temperatura={0:0.1f}*C  Humidade={1:0.1f}%'.format(temperature, humidity)
            
            lista = []
            lista.insert(0, "%.1f" % temp)
            lista.insert(1, "%.1f" % hum)
        else:
            print 'Falha ao obter os dados!'

        return lista
