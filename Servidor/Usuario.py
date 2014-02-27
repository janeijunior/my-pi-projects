#!/usr/bin/python
#-*- coding: utf-8 -*-

import Funcoes

class Usuario(object):
    
    #construtor
    def __init__(self):
        
        self.carregarUsuario()
            
    #funcoes
    #funcao para carregar as propriedades da classe
    def carregarUsuario(self):
        row = Funcoes.consultarRegistro("select Usuario, Senha from Usuario")
        
        self.usuario = row["Usuario"]
        self.senha = row["Senha"]        
    
    #funcao para alterar o usuario e a senha 
    def alterarUsuarioSenha(root, con):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'"
        sql = sql.format(novoUsuario =  usuario, novaSenha = senha)
        
        if Funcoes.executarComando(sql):
            self.usuario = usuario
            self.senha   = senha
            con.send("Ok\n")
        else:
            con.send("Erro\n")        
    
    #funcao para validar o login do sistema
    def efetuarLogin(usuario, senha):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        if row["Usuario"] == usuario and row["Senha"]  == senha:
            print "Conectado: ", cliente
            con.send("Logado\n")
        else:
            print "Usuario ou senha invalidos.", cliente
            con.send("NaoLogado\n")
            con.close
            thread.exit()