1 import socket
   2 import thread
   3 
   4 HOST = ''              # Endereco IP do Servidor
   5 PORT = 5000            # Porta que o Servidor esta
   6 
   7 def conectado(con, cliente):
   8     print 'Conectado por', cliente
   9 
  10     while True:
  11         msg = con.recv(1024)
  12         if not msg: break
  13         print cliente, msg
  14 
  15     print 'Finalizando conexao do cliente', cliente
  16     con.close()
  17     thread.exit()
  18 
  19 tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  20 
  21 orig = (HOST, PORT)
  22 
  23 tcp.bind(orig)
  24 tcp.listen(1)
  25 
  26 while True:
  27     con, cliente = tcp.accept()
  28     thread.start_new_thread(conectado, tuple([con, cliente]))
  29 
  30 tcp.close()