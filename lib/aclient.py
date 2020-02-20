# Universidade Federal de Campina Grande
# Centro de Engenharia Eletrica e Informatica
# Departamento de Sistemas e Computacao
# Curso de Ciencia da Computacao
#
# Projeto da Disciplina: 
# Introducao ao Desenvolvimento de Software para Dispositivos Moveis
# 
# A nossa ideia para o projeto da disciplina eh um joguinho bastante popular: Campo Minado.
# Neste jogo, ganha quem achar mais bombas. (Voce acha uma bomba clicando em cima dela)
#
#
# Contribuidores:
#    Carolina Nogueira - carolina@embedded.ufcg.edu.br
#


# this file lets your phone connect to a TCP/IP socket
# this file is the phone client 
# the corresponding server side file on the net is called tcp_pc_server.py

import socket
import appuifw
import e32

class Cliente:
    
    def __init__(self, HOST = "127.0.0.1", PORT = 8080):
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    def desconecta(self):
        self.sock.close()

    def conecta(self):
        print 'CLIENT'
        print "define socket"        
        print "trying to connect to socket"
        self.sock.connect((self.host, self.port))
        print "connected"
        return self.transformaData(self.sock.recv(1024))
        
    def transformaData(self, data):
        linhas = data.split("\n")
        tamanho = len(linhas)
        tabuleiro = [[0 for i in range(tamanho - 1)] for i in range(tamanho - 1)]
        for x in range(len(linhas) - 1):
            linha = linhas[x].lstrip()
            colunas = (linha).split(" ") 
            for y in range(len(colunas)): 
                if (colunas[y] == 'B' or colunas[y] == '#' or colunas[y] == 'iB'):
                    tabuleiro[x][y] = colunas[y]                    
                else:
                    tabuleiro[x][y] = int (colunas[y])
        return tabuleiro

class BTReader:
    def __init__(self, HOST = "127.0.0.1", PORT = 8080):
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)

    def conecta(self):
        addr,services=socket.bt_discover()
        print "Discovered: %s, %s"%(addr,services)
        if len(services)>0:
            import appuifw
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                       for x in choices],u'Choose port:')
            port=services[choices[choice]]
        else:
            port=services[services.keys()[0]]
        address=(addr,port)
        print "Connecting to "+str(address)+"...",
        self.sock.connect(address)
        print "OK." 
        return self.transformaData(self.sock.recv(1024))

    def transformaData(self, data):
        linhas = data.split("\n")
        tamanho = len(linhas)
        tabuleiro = [[0 for i in range(tamanho - 1)] for i in range(tamanho - 1)]
        for x in range(len(linhas) - 1):
            linha = linhas[x].lstrip()
            colunas = (linha).split(" ") 
            for y in range(len(colunas)): 
                if (colunas[y] == 'B' or colunas[y] == '#' or colunas[y] == 'iB'):
                    tabuleiro[x][y] = colunas[y]                    
                else:
                    tabuleiro[x][y] = int (colunas[y])
        return tabuleiro

    def desconecta(self):
        self.s.close()