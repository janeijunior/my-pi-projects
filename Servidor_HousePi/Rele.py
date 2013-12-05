class Rele(object):
    
    def __init__(self, numero, status, nome):
        self.numero = numero
        self.status = status
        self.nome = nome
        
    def get_velocidade(self):
        return self.alcance / self.tempo
    
    @property
    def numero(self):
        return self.numero
        
    @property
    def status(self):
        return self.status
    
    @property
    def nome(self):
        return self.nome