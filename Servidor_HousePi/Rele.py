class Rele(object):
    
    #construtor
    def __init__(self, numero, status, nome):
        self.numero = numero
        self.status = status
        self.nome = nome
        
    #propriedades
    @property
    def getNumero(self):
        return self.numero
        
    @property
    def getStatus(self):
        return self.status
    
    @property
    def getNome(self):
        return self.nome
    
    @property
    def setNumero(self, numero):
        self.numero = numero
    
    @property
    def setStatus(self, status):
        self.status = status
    
    @property
    def setNome(self, nome):
        self.nome = nome
    
    #destrutor
    def __done__(self):
    
    
    