#!/usr/bin/python
#-*- coding: utf-8 -*-

import Base

class Usuario(Base.Base):
    
    #construtor
    def __init__(self):
        self.carregarUsuario()
            
    #funcoes
    #funcao para carregar as propriedades da classe
    def carregarUsuario(self):
        row = self.consultarRegistro("select Usuario, Senha from Usuario")
        
        self.usuario = row["Usuario"]
        self.senha = row["Senha"]        
    
    #funcao para alterar o usuario e a senha 
    def alterarUsuarioSenha(root, con):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        sql = "update Configuracao set Usuario = '{novoUsuario}', Senha = '{novaSenha}'"
        sql = sql.format(novoUsuario =  usuario, novaSenha = senha)
        
        if self.executarComando(sql):
            con.usuario = usuario
            con.senha   = senha
            con.send("Ok\n")
        else:
            con.send("Erro\n")        
    
    #funcao para validar o login do sistema
    def efetuarLogin(self, root, con):
        if (self.usuario == usuario) and (self.senha == senha):
            return True
        else:
            return False