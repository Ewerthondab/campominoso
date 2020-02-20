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
#    Ewerthon Dyego
#    Estefano Gomes
#    Pablo Diego
#

# this file lets your PC read from a TCP/IP socket to which a phone has been connected to.
# this file is the PC server 
# the corresponding client file on the phone is called tcp_phone_client.py


import socket
import appuifw

class Servidor:
    
    def __init__(self, HOST = "127.0.0.1", PORT = 8080):
        self.host = HOST
        self.port = PORT        
        self.string  = 0         
                 
    def desconectar(self):
        self.conn.close()

    def _tabuleiroString(self, tabuleiro):
        data = "" 
        tamanho = len(tabuleiro)
        for x in range(tamanho):                    
            for y in range(tamanho):
                data = data + " " + str ( tabuleiro[x][y] )
            data = data + '\n'    
        return data
            
            
    def conectar(self, data):     
        print 'SERVER'
        print "define the socket"        
        print "bind the socket"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print "waiting of the client to connect"
        self.conn, addr = self.sock.accept()
        print 'Connected by', addr
        self.conn.send(self._tabuleiroString(data))

class BTSender:

    def __init__(self):
	self.sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)	
        self.host = ""
        self.port = socket.bt_rfcomm_get_available_server_channel(self.sock)        

    def conectar(self, data): 
	print "bind done"
	self.sock.bind((self.host, self.port))
	self.sock.listen(1)
	socket.bt_advertise_service( u"jurgen", self.sock, True, socket.RFCOMM)
	socket.set_security(self.sock, socket.AUTH)
	print "I am listening"

	(self.conn, peer_addr) = self.sock.accept()
	print "Connection from %s"%peer_addr
	self.conn.send(self._tabuleiroString(data))

    def desconectar(self):
        self.conn.close()

    def _tabuleiroString(self, tabuleiro):
        data = "" 
        tamanho = len(tabuleiro)
        for x in range(tamanho):                    
            for y in range(tamanho):
                data = data + " " + str ( tabuleiro[x][y] )
            data = data + '\n'    
        return data