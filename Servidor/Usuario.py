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
        sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'"
        sql = sql.format(novoUsuario =  root.find("Usuario").text.encode('utf-8'), novaSenha = root.find("Senha").text.encode('utf-8'))
        
        if Funcoes.executarComando(sql):
            con.send("Ok\n")
        else:
            con.send("Erro\n")
        
    
    #funcao para validar o login do sistema
    def efetuarLogin(usuario, senha):
        