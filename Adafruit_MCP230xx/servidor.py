import socket
import time
import Adafruit_MCP230xx

 
host = ''
port = 1234
 
addr = (host, port)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_socket.bind(addr)
serv_socket.listen(10)
 
print 'aguardando conexao'
con, cliente = serv_socket.accept()
print 'conectado'
print "aguardando mensagem"
#recebe = con.recv(1024)

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

try:
    msg = True
    
    while msg != None:
        msg = con.recv(1024)
        print "Mensagem recebida de -> %s" % (msg.strip())
        
        if (msg.strip() == "l1"):
          mcp.output(1, 1)    
   
except KeyboardInterrupt:   #   Trata o CTRL+C
    print "Saindo..."
    exit(0)


#mcp.output(0, 1) # Pin High 
#mcp.output(1, 1) 
#mcp.output(2, 1)  
#mcp.output(3, 1)  
#mcp.output(4, 1)
#mcp.output(5, 1) 
#mcp.output(6, 1)  
#mcp.output(7, 1)  
#mcp.output(8, 1)
#mcp.output(9, 1) 
#time.sleep(3)
#mcp.output(0, 0) # Pin Low 
#mcp.output(1, 0) 
#mcp.output(2, 0)
#mcp.output(3, 0)
#mcp.output(4, 0) 
#mcp.output(5, 0) 
#mcp.output(6, 0)
#mcp.output(7, 0)
#mcp.output(8, 0) 
#mcp.output(9, 0)

#print "mensagem recebida: "+ recebe
#serv_socket.close()
