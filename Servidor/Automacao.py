#!/usr/bin/python
#-*- coding: utf-8 -*-

import Usuario

class Automacao(Base.Base):

    #construtor
    def __init__(self):
        self.usuario = = Usuario.Usuario()
    
    #funcoes da classe
    
    #função para validar o usuario e a senha, se nao estiverem certos desconecta!
    def efetuarLogin(root, con):
        usuario = root.find("Usuario").text.encode('utf-8')
        senha   = root.find("Senha").text.encode('utf-8')
        
        if self.usuario.validarLogin(usuario, senha):
            print "Conectado: ", cliente
            con.send("Logado\n")
        else:
            print "Usuario ou senha invalidos.", cliente
            con.send("NaoLogado\n")
            con.close