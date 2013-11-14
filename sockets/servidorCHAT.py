import socket
from threading import Thread
HOST, PORT = "192.168.5.125", 7000
class verificaMensagensClientes(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn
        print "criada a thread"
    def run(self):
        print "RODANDO A THREAD"
        global listaConectados
        for i in listaConectados:
            print listaConectados
        while (1):
            data = self.conn.recv(1024)
            print data
            for conexao in listaConectados:
                if(conexao != self.conn):
                    conexao.send(data)
        
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((HOST, PORT))
tcp_server_socket.listen(2)
conectados =0
listaConectados =[]
listaThread =[]
"""Set the quantifier of initial clients you wait to start the chat"""
while (conectados<2):
    print "Conectados: "+str(conectados)
    conn, addr = tcp_server_socket.accept()
    temp = verificaMensagensClientes(conn)
    listaThread.append(temp)
    listaConectados.append(conn)
    conectados+=1

for i in listaConectados:
    print "conetado por",i


print "comecou"
print len(listaThread)
for i in listaThread:
    i.start()
    print "ativando as threads"   

#continue accepting news clients
while 1:
    print "Conectados: "+str(conectados)
    conn, addr = tcp_server_socket.accept()
    temp = verificaMensagensClientes(conn)
    listaThread.append(temp)
    listaConectados.append(conn)
    temp.start()
    conectados+=1

for i in listaConectados:
    i.close()

