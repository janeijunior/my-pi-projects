import RPi.GPIO as GPIO 

class SensorAlarme(object):
    
    #construtor
    def __init__(self, numero, nome):
        self.numero = numero
        self.ativo = ativo
        
        configurar()
        
    #propriedades
    @property
    def getNumero(self):
        return self.numero
    
    @property
    def getAtivo(self):
        return self.ativo
    
    @property
    def setNumero(self, numero):
        self.numero = numero

    @property
    def setAtivo(self, ativo):
        self.ativo = ativo 
    
    #funcoes
    def configurar(self):
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.numero, GPIO.IN)
        
    def lerStatus(self):
        GPIO.input(numero)
    
    def verificaDisparo(self):
        if self.Ativo and lerStatus <> 1:
            
    #destrutor
    #def __done__(self):