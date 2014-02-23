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
    def alterarUsuarioSenha(usuario, senha):
        
    
    #funcao para validar o login do sistema
    def efetuarLogin(usuario, senha):
        