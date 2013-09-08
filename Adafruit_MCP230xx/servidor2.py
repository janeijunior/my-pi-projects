import socket
import time
import Adafruit_MCP230xx
from threading import Thread
HOST, PORT = "192.168.1.104", 7000

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
        
        
        mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)
        
        mcp.config(0, mcp.OUTPUT)
        mcp.config(1, mcp.OUTPUT)
        mcp.config(2, mcp.OUTPUT)
        mcp.config(3, mcp.OUTPUT)
        mcp.config(4, mcp.OUTPUT)
        mcp.config(5, mcp.OUTPUT)
        mcp.config(6, mcp.OUTPUT)
        mcp.config(7, mcp.OUTPUT)
        mcp.config(8, mcp.OUTPUT)
        mcp.config(9, mcp.OUTPUT)

        
        while (1):
            for conexao in listaConectados:
                if(conexao != self.conn):
                    msg = conexao.recv(1024)
          
                    comando = msg.strip() 
             
                if len(comando) > 0:
                    print "Mensagem recebida de -> " + msg.strip()
                    
                    if comando[2] == "l" and comando[3] == "0":
                        mcp.output(0, 1)
                    elif comando[2] == "l" and comando[3] == "1":
                        mcp.output(1, 1)
                    elif comando[2] == "l" and comando[3] == "2":
                        mcp.output(2, 1)
                    elif comando[2] == "l" and comando[3] == "3":
                        mcp.output(3, 1)
                    elif comando[2] == "l" and comando[3] == "4":
                        mcp.output(4, 1)
                    elif comando[2] == "l" and comando[3] == "5":
                        mcp.output(5, 1)
                    elif comando[2] == "l" and comando[3] == "6":
                        mcp.output(6, 1)
                    elif comando[2] == "l" and comando[3] == "7":
                        mcp.output(7, 1)
                    elif comando[2] == "l" and comando[3] == "8":
                        mcp.output(8, 1)
                    elif comando[2] == "l" and comando[3] == "9":
                        mcp.output(9, 1)
                    elif comando[2] == "d" and comando[3] == "0":
                        mcp.output(0, 0)
                    elif comando[2] == "d" and comando[3] == "1":
                        mcp.output(1, 0)
                    elif comando[2] == "d" and comando[3] == "2":
                        mcp.output(2, 0)
                    elif comando[2] == "d" and comando[3] == "3":
                        mcp.output(3, 0)
                    elif comando[2] == "d" and comando[3] == "4":
                        mcp.output(4, 0)
                    elif comando[2] == "d" and comando[3] == "5":
                        mcp.output(5, 0)
                    elif comando[2] == "d" and comando[3] == "6":
                        mcp.output(6, 0)
                    elif comando[2] == "d" and comando[3] == "7":
                        mcp.output(7, 0)
                    elif comando[2] == "d" and comando[3] == "8":
                        mcp.output(8, 0)
                    elif comando[2] == "d" and comando[3] == "9":
                        mcp.output(9, 0)
                    else:
                        print "Comando invalido!"
        
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((HOST, PORT))
tcp_server_socket.listen(2)
conectados =0
listaConectados =[]
listaThread =[]
"""Set the quantifier of initial clients you wait to start the chat"""
while (conectados<1):
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

