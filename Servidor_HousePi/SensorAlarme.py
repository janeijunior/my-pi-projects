import RPi.GPIO as GPIO 

class Rele(object):
    
    #construtor
    def __init__(self, numero, status, nome):
        self.numero = numero
        self.status = status
        self.ativo = ativo
        
        configurar()
        
    #propriedades
    @property
    def getNumero(self):
        return self.numero
        
    @property
    def getStatus(self):
        return self.status
    
    @property
    def getAtivo(self):
        return self.ativo
    
    @property
    def setNumero(self, numero):
        self.numero = numero
    
    @property
    def setStatus(self, status):
        self.status = status
    
    @property
    def setAtivo(self, ativo):
        self.ativo = ativo
    
    #funcoes
    def configurar(self):
        GPIO.setmode(GPIO.BCM) 
        
    def ligar(self):
        mcp.output(self.numero, 1)
    
    def desligar(self):
        mcp.output(self.numero, 0)
    
    #destrutor
    #def __done__(self):