#!/usr/bin/python
#-*- coding: utf-8 -*-

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import socket
import thread
import threading
import time
import os
import commands
import Alarme
import MySQLdb
import Rele
import signal
import sys
import SensorDHT
import Funcoes
import Agendamento
import ThreadAgendamento
import subprocess
import select

HOST = ""    # IP do Servidor (em branco = IP do sistema)
PORT = 5002  # Porta do Servidor
SIRENE = 10  # Numero GPIO da sirene
PLAYLIST = "/home/pi/HousePi/playlist" # Diretorio onde encontra-se a playlist de musicas
MJPG = "/usr/share/adafruit/webide/repositories/my-pi-projects/Servidor/mjpg-streamer/mjpg-streamer.sh" #caminho stream de video

orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(orig)
tcp.listen(1)

#variavel para controle do alarme
alarme = None

#variavel para controle do agendamento
threadAgendamento = None
listaAgendamento = []

#lista dos reles
listaReles = [];

#variavel para controle do subprocesso do mplayer do linux
mplayer = None

#lista de conexoes ativas
listaConexoes = []

#Configura todos os pinos necessarios para o envio de comandos 
def configurarReles():
    print "Configurando reles..."

    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Rele")

    rows = cursor.fetchall()

    for row in rows:
        rele = Rele.Rele(id = row["Id"], numeroGPIO = row["NumeroGPIO"], status = row["Status"], nome = row["Nome"])        
        
        if rele.status == 1:
            rele.ligar()
        else:
            rele.desligar()
        
        listaReles.insert(row["Id"], rele)
    
    conBanco.close()

    listaReles[12].ligar()

#inicializa o alarme
def configurarAlarme():
    global alarme
    
    alarme = Alarme.Alarme(sirene=listaReles[SIRENE])

#inicializar thread do agendamento
def iniciarAgendamento():
    global threadAgendamento
    global listaAgendamento
    
    threadAgendamento = ThreadAgendamento.ThreadAgendamento(listaAgendamento)
    threadAgendamento.start() 
        
#carregar lista de agendamentos
def carregarListaAgendamento():
    global alarme
    global listaAgendamento
    
    print "Carregando agendamentos..."
    
    listaAgendamento = []

    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Agendamento where Ativo = 1")

    rows = cursor.fetchall()

    for row in rows:
        equipamentos = Funcoes.stringToList(row["Equipamentos"])
        dias = Funcoes.stringToList(row["DiasDaSemana"])
        
        agendamento = Agendamento.Agendamento(id = row["Id"], nome = row["Nome"], dias = dias,
                          dataHoraInicial = row["DataHoraInicial"], dataHoraFinal = row["DataHoraFinal"], ativo = int(row["Ativo"]))        
        
        for e in equipamentos:
            if e <> "":
                if e == "-1":
                    agendamento.alarme = alarme
                else:
                    agendamento.reles.insert(len(agendamento.reles) + 1, listaReles[int(e)])
        
        listaAgendamento.insert(row["Id"], agendamento)
    
    conBanco.close()
    
        
#função para validar o usuario e a senha, se nao estiverem certos desconecta!
def efetuarLogin(root, con):
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select Usuario, Senha from Configuracao")
    
    row = cursor.fetchone()
    
    usuario = root.find("Usuario").text.encode('utf-8')
    senha = root.find("Senha").text.encode('utf-8')
    
    conBanco.close()
    
    global listaConexoes
    
    if row["Usuario"] == usuario and row["Senha"]  == senha:
        print "Conectado: ", cliente
        listaConexoes.insert(len(listaConexoes) + 1, cliente)
        con.send("Logado\n")
        controlarCamera()
    else:
        print "Usuario ou senha invalidos.", cliente
        con.send("NaoLogado\n")
        con.close
        thread.exit()

#liga ou desliga os reles/atuadores
def controlarRele(root, con):
    acao = root.find("Acao").text
    numero = root.find("Numero").text
    
    if acao == "Ligar":
        listaReles[int(numero)].ligar()
    else:
        listaReles[int(numero)].desligar()
    
    con.send("Ok\n")
        
#le o sensor de temperatura e humidade e envia os resultados
def enviarTemperaturaHumidade(con):    
    try:
        desligarCamera()
        time.sleep(1)
        
        resultado = SensorDHT.lerTemperaturaHumidade()    
        root = Element("TemperaturaHumidade")
        dados = Element("Dados", Temperatura=resultado[0], Humidade=resultado[1])
        root.append(dados)
        
        print "Temperatura: ", resultado[0], " Humidade: ", resultado[1]
        
        xmlstr = ET.tostring(root) + "\n"   
        con.send(xmlstr)    
        ligarCamera()
    except:
        print "Erro ao obter a temperatura e humidade."
        con.send("Erro\n")
        ligarCamera()
        
#liga ou desliga o alarme
def controlarAlarme(root, con):
    acao = root.find("Acao").text
    
    global alarme
    
    if acao == "Ligar":
        if alarme.alarmeLigado == False:
            alarme.ligarAlarme() 
            print "Alarme ativado."
    else:
        alarme.desligarAlarme()
        print "Alarme desativado."
    
    con.send("Ok\n")
        
    
#liga ou desliga a funcao panico do alarme
def controlarFuncaoPanico(root, con):
    acao = root.find("Acao").text
    
    global alarme
    
    if acao == "Ligar":
        alarme.ligarPanicoAlarme()
    else:
        alarme.desligarPanicoAlarme()
    
    con.send("Ok\n")
    
#funcao que envia as configuracoes dos reles e status
def enviarConfiguracaoStatusRele(con):
    root = Element("StatusRele")
    
    for rele in listaReles:
        root.append(Element("Rele" + str(rele.id), Status=str(rele.status), Nome=rele.nome.decode('utf-8')))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que envia o status do alarme
def enviarConfiguracaoStatusAlarme(con):
    root = Element("Alarme")
    
    global alarme
    
    status = ""
    
    if alarme.getStatusAlarme() == 1:
        status = "Disparado"
    elif alarme.getStatusAlarme() == 0:
        status = "Normal"
    else:
        status = "Desligado"
    
    root.append(Element("SensorAlarme", Status=status, Ligado=str(int(alarme.alarmeLigado))))
    root.append(Element("PanicoAlarme", Ligado=str(int(alarme.panicoAlarmeLigado))))
    
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que insere um novo agendamento no banco de dados e alualiza a lista de agendamentos
def gravarAgendamento(root, con):
    
    global listaReles
    global alarme
    
    if str(root.find("Dias").text) <> "":
        dias = Funcoes.stringToList(str(root.find("Dias").text))
    else:
        dias = []
    
    agendamento = Agendamento.Agendamento(id = 0, nome = root.find("Nome").text.encode('utf-8'), dias = dias, dataHoraInicial = 
                                          root.find("DataHoraInicial").text, dataHoraFinal = root.find("DataHoraFinal").text, ativo = 1)
    
    equipamentos = root.find("Equipamentos")
    
    for child in equipamentos:
        if str(child.get("Id")) == "-1":
            agendamento.alarme = alarme    
        else:
            agendamento.reles.insert(len(agendamento.reles) + 1, listaReles[int(child.get("Id"))])
    
    print "Passou"
    
    if agendamento.gravarRegistroBanco():
        con.send("Ok\n")
        
        #carrega os novos agendamentos
        carregarListaAgendamento()
        
        global threadAgendamento
        global listaAgendamento
        
        #passa a nova lista para a thread
        threadAgendamento.listaAgendamento = listaAgendamento
    else:
        con.send("Erro\n")

#funcao que retorna os agendamentos do servidor para o aplicativo movel
def enviarAgendamento(con):
    root = Element("EnviarAgendamento")
    
    #atualiza a lista de agendamentos
    carregarListaAgendamento()
    
    global listaAgendamento
    
    for agendamento in listaAgendamento:
        root.append(Element("Agendamento" + str(agendamento.id), Id=str(agendamento.id), Nome=agendamento.nome.decode('utf-8'), 
                                DataHoraInicial=str(agendamento.dataHoraInicial), DataHoraFinal=str(agendamento.dataHoraFinal), Dias=agendamento.getDias()))
        
        equipamentos = Element("Equipamentos")
        
        if agendamento.alarme <> None:
            equipamentos.append(Element("Alarme", Id = "-1"))
        
        for rele in agendamento.reles:
            equipamentos.append(Element("Rele", Id = str(rele.Id)))        
        
        root.append(equipamentos)
        
    xmlstr = ET.tostring(root) + "\n"   
    con.send(xmlstr)

#funcao que remove o agendamento da lita e do banco de dados conforme solicitado
def removerAgendamento(root, con):
    global threadAgendamento
    global listaAgendamento
    
    for agendamento in listaAgendamento:
        if agendamento.id == int(root.find("Id").text):
            if agendamento.removerRegistroBanco():
                con.send("Ok\n")
                
                #atualiza a lista de agendamentos
                carregarListaAgendamento()
                
                #passa a nova lista de agendamentos para a thread
                threadAgendamento.listaAgendamento = listaAgendamento
            
                break
            else:
                con.send("Erro\n")

#funcao para alterar o usuario e a senha
def alterarUsuarioSenha(root, con):
    try:
        usuario = root.find("Usuario").text.encode('utf-8')
        senha = root.find("Senha").text.encode('utf-8')
        
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'".format(novoUsuario = usuario, novaSenha = senha)
        print sql
        
        cursor.execute(sql)
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")
            
#funcao para renomear os reles atraves da aba de configuracoes
def alterarConfiguracaoRele(root, con):
    try:
        global listaReles
        
        for child in root:
            listaReles[int(child.get("Id"))].nome = str(child.get("Nome").encode('utf-8')) 
            listaReles[int(child.get("Id"))].gravarNomeBanco();
        
        con.send("Ok\n")
    except:
        con.send("Erro\n")
        
#funcao que grava a nova configuracao de email
def alterarConfiguracaoEmail(root, con):
    try:
        usuario = root.find("Usuario").text.encode('utf-8')
        senha = root.find("Senha").text.encode('utf-8')
        destinatario = root.find("Destinatario").text.encode('utf-8')
        servidor = root.find("Servidor").text.encode('utf-8')
        porta = root.find("Porta").text.encode('utf-8')
                
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = '''update Configuracao 
                    set RemetenteEmail = '{novoUsuario}', 
                        SenhaEmail = '{novaSenha}',
                        DestinatarioEmail = '{novoDestinatario}',
                        ServidorSMTP = '{novoServidor}',
                        PortaSMTP = {novaPorta}'''.format(novoUsuario = usuario, novaSenha = senha, 
                                                          novoDestinatario = destinatario, novoServidor = servidor, novaPorta = porta)
        print sql
        
        cursor.execute(sql)
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")

#envia a configuracao atual de email para o solicitante
def enviarConfiguracaoEmail(con):
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Configuracao")

    row = cursor.fetchone()
    
    root = Element("EnviarConfiguracaoEmail")
    dados = Element("Dados", Usuario = str(row["RemetenteEmail"]).decode('utf-8'), Senha = str(row["SenhaEmail"]).decode('utf-8'), Destinatario = str(row["DestinatarioEmail"]).decode('utf-8'),
                             Servidor = str(row["ServidorSMTP"]).decode('utf-8'), Porta = str(row["PortaSMTP"]))
    root.append(dados)
    
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
    conBanco.close()

#funcao para enviar as configuracoes atuais do alarme
def enviarConfiguracaoAlarme(con):
    conBanco = Funcoes.conectarBanco()
    cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
    cursor.execute("select EnviarEmailAlarme, UsarSireneAlarme, TempoDisparoAlarme from Configuracao")
    row = cursor.fetchone()

    root = Element("EnviarConfiguracaoAlarme")
    root.append(Element("Geral", TempoDisparo=str(row["TempoDisparoAlarme"]), UsarSirene=str(row["UsarSireneAlarme"]), UsarEmail=str(row["EnviarEmailAlarme"])))

    cursor.execute("select Id, Nome, Ativo from SensorAlarme")
    rows = cursor.fetchall()
    
    sensores = Element("Sensores")
    
    for row in rows:
         sensores.append(Element("Sensor" + str(row["Id"]), Nome=str(row["Nome"]).decode('utf-8'), Ativo=str(row["Ativo"])))
    
    root.append(sensores)
    xmlstr = ET.tostring(root) + "\n"       
    con.send(xmlstr)
    conBanco.close()
        
#funcao para gravar as novas configuracoes do alarme
def alterarConfiguracaoAlarme(root, con):
    try:
        conBanco = Funcoes.conectarBanco()
        cursor = conBanco.cursor(MySQLdb.cursors.DictCursor)
        
        sql = '''update Configuracao 
                    set TempoDisparoAlarme = {tempo}, 
                        UsarSireneAlarme = {usarSirene},
                        EnviarEmailAlarme = {usarEmail}'''.format(tempo = int(root.find("TempoDisparo").text), usarSirene = int(root.find("UsarSirene").text), usarEmail = int(root.find("UsarEmail").text))
        print sql
        cursor.execute(sql)
        
        sensores = root.find("Sensores")
        
        for child in sensores:
            sql = '''update SensorAlarme set Nome = '{novoNome}', Ativo = {ativo} where Id = {idSensor}'''.format(novoNome = child.get("Nome").encode('utf-8'), ativo = int(child.get("Ativo")), idSensor = int(child.get("Id")))
            print sql
            cursor.execute(sql)
        
        conBanco.commit()
        conBanco.close()
        con.send("Ok\n")
    except:
        conBanco.rollback()
        conBanco.close()
        con.send("Erro\n")

#envia a lista de musicas de uma pasta pre determinada
def enviarListaMusica(con):
    playlist = 'find /home/pi/HousePi/Musicas/ -name "*mp3" -o -name "*flac" -o -name "*m4a" -o -name "*wma" -type f | sort > /home/pi/HousePi/playlist'
    os.system(playlist)
    
    arquivo = open(PLAYLIST)

    root = Element("EnviarListaMusica")

    for linha in arquivo:
        str = linha[len(PLAYLIST):len(linha) -1]
        root.append(Element("Musicas", Nome=str.decode('utf-8')))
    
    arquivo.close()
    
    xmlstr = ET.tostring(root) + "\n"  
    con.send(xmlstr)

#retorna a posicao da musica com o nome passado por parametro
def getPosicaoMusica(nome):
    arquivo = open(PLAYLIST)
    
    i = 0
    
    for linha in arquivo:
        musica = linha[len(PLAYLIST):len(linha) -5]
        
        if musica == nome:
            return i
            break
            arquivo.close()
        
        i = i + 1
    
    return -1
    arquivo.close()
    
#controla o mplayer do linux
def controlarSomAmbiente(root, con):
    global mplayer
    
    comando = str(root.find("Comando").text)
    valor = str(root.find("Valor").text.encode('utf-8'))
    
    
    if comando == "Play":
        try:
            print executarComandoMPlayer("get_file_name", "ANS_FILENAME")   
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
            mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    elif comando == "Pause":
        executarComandoMPlayer("pause", "")
    elif comando == "Stop":
        executarComandoMPlayer("stop", "")
    elif comando == "AnteriorProxima":
        try:         
            executarComandoMPlayer("pt_step " + valor, "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
            mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)    
            executarComandoMPlayer("pt_step " + str(int(valor) - 1), "")
    elif comando == "Volume":
       executarComandoMPlayer("set_property volume " + valor, "")
    elif comando == "ReproduzirPorNome":
        try:
            nome = executarComandoMPlayer("get_file_name", "ANS_FILENAME")
            atual = getPosicaoMusica(nome[1:len(nome) -5])
            proxima = getPosicaoMusica(str(valor))
            
            step = proxima - atual
            
            executarComandoMPlayer("pt_step " + str(step), "")
        except:
            cmd = ['mplayer', '-slave', '-quiet', '-playlist', PLAYLIST]
            mplayer = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            
            proxima = getPosicaoMusica(valor)
            executarComandoMPlayer("pt_step " + str(proxima), "")
        
#executa um comando no subprocesso do mplayer e devolve o resultado
def executarComandoMPlayer(cmd, retorno):
    global mplayer
    
    mplayer.stdin.write(cmd + '\n') 
    while select.select([mplayer.stdout], [], [], 0.05)[0]: 
        output = mplayer.stdout.readline()
        print("output: {}".format(output.rstrip()))
        split_output = output.split(retorno + '=', 1)
        if len(split_output) == 2 and split_output[0] == '':
            value = split_output[1]
            return value.rstrip()

#finaliza os processos em execucao para encerrar o aplicativo servidor
def finalizarProcessos():
    global alarme
    
    if alarme.alarmeLigado:
        alarme.desligarAlarme()
    
    alarme.desligarPanicoAlarme()
	
    global threadAgendamento
    threadAgendamento.stop()
    
    for rele in listaReles:	
		rele.desligar()
	
    desligarCamera()

#funcao para reiniciar ou desligar o servidor conforme solicitado pelo app android
def reiniciarDesligarServidor(root, con):
    acao = root.find("Acao").text
    
    finalizarProcessos()
    
    con.send("Ok\n")    
    
    if acao == "Reiniciar":
        os.system("/usr/bin/sudo /sbin/shutdown -r now")
    else:
        os.system("/usr/bin/sudo /sbin/shutdown -h now")

#inicia o servico da camera
def ligarCamera():
    os.system("sudo " + MJPG + " start 5005 320x240 2") #iniciar, porta, resolucao, fps
    
#para o servico da camera
def desligarCamera():
    os.system("sudo " + MJPG + " stop")

#inicia ou para o servico de stream da camera
def controlarCamera():
    global listaConexoes
    
    if len(listaConexoes) < 1:
        desligarCamera()
    elif len(listaConexoes) > 0:
        ligarCamera()

#cliente conectado, verifica os comandos recebidos
def conectado(con, cliente):    
    while True:
        msg = con.recv(1024)
        comando = msg[2:len(msg)]
     
        if not msg: 
            break
        
        print cliente, "Comando recebido: " + comando
                  
        
        if len(comando) > 0:
            try:
                #root = XML recebido/elemento principal
                root = ET.fromstring(comando)
            
                if root.tag == "Logar":
                    efetuarLogin(root, con)
                elif root.tag == "Rele":
                    controlarRele(root, con)
                elif root.tag == "Temperatura":
                    enviarTemperaturaHumidade(con)
                elif root.tag == "Alarme":
                    controlarAlarme(root, con)
                elif root.tag == "Panico":
                    controlarFuncaoPanico(root, con)           
                elif root.tag == "StatusRele":
                    enviarConfiguracaoStatusRele(con)
                elif root.tag == "StatusAlarme":
                    enviarConfiguracaoStatusAlarme(con)   
                elif root.tag == "GravarAgendamento":
                    gravarAgendamento(root, con)
                elif root.tag == "EnviarAgendamento":
                    enviarAgendamento(con)
                elif root.tag == "RemoverAgendamento":
                    removerAgendamento(root, con)
                elif root.tag == "AlterarUsuarioSenha":
                    alterarUsuarioSenha(root, con)
                elif root.tag == "AlterarConfiguracaoRele":
                    alterarConfiguracaoRele(root, con)
                elif root.tag == "AlterarConfiguracaoEmail":
                    alterarConfiguracaoEmail(root, con)
                elif root.tag == "EnviarConfiguracaoEmail":
                    enviarConfiguracaoEmail(con)
                elif root.tag == "EnviarConfiguracaoAlarme":
                    enviarConfiguracaoAlarme(con)
                elif root.tag == "AlterarConfiguracaoAlarme":
                    alterarConfiguracaoAlarme(root, con)
                elif root.tag == "EnviarListaMusica":
                    enviarListaMusica(con)
                elif root.tag == "ControlarSomAmbiente":
                    controlarSomAmbiente(root, con)
                elif root.tag == "ReiniciarDesligar":
                    reiniciarDesligarServidor(root, con)
            except Exception as e: 
                print "Erro: ", e
                con.send("Erro\n")
                
    print "Finalizando conexao do cliente", cliente
    
    global listaConexoes
    
    for i in range(-1,  len(listaConexoes)):
        if listaConexoes[i] == cliente:
            del listaConexoes[i]
            controlarCamera()
            break
    
    con.close()
    thread.exit()

configurarReles()
configurarAlarme()
carregarListaAgendamento()
iniciarAgendamento()

print "Aguardando conexoes... (CTRL + C encerra o aplicativo)"

#para fechar o programa
def signal_handler(signal, frame):
    print "\nEncerrando aplicativo..."
    finalizarProcessos()
    tcp.close;
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

while True:
   conexao, cliente = tcp.accept()
   thread.start_new_thread(conectado, tuple([conexao, cliente]))
    
tcp.close()
