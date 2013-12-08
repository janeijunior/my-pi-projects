class Conexao:
    #classe de conexão com as funções de envio e recibimento de dados por socket
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def conectar(self, host, porta):
        self.sock.connect((host, porta))

    def enviar(self, msg):
        totalenviado = 0
        while totalenviado < MSGLEN:
            sent = self.sock.send(msg[totalenviado:])
            if sent == 0:
                raise RuntimeError("Erro na conexao")
            totalenviado = totalenviado + sent

    def receber(self):
        msg = ''
        while len(msg) < MSGLEN:
            chunk = self.sock.recv(MSGLEN-len(msg))
            if chunk == '':
                raise RuntimeError("Erro na conexao")
            msg = msg + chunk
        return msg