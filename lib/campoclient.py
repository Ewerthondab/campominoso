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


COMPUTER = 1
REMOTE = 2
PLAYER = 3

import random
import sys
import appuifw
import e32
import os

PATHLIB  = "\\python\\lib"

def get_path(app_name):
	drives_list = e32.drive_list()

	#Gives preference to load from drive 'E:'
	drives_list.reverse()
	for drive in [str(x) for x in drives_list]:
        	if os.path.isdir(os.path.join(drive, app_name)):
	        	return os.path.join(drive, app_name)

#atualizando caminho
PATHLIB = get_path(PATHLIB)

class JogadorRemoto:
    
    def __init__(self, tamanho, conexao):
        self._tamanho = tamanho
	self.conexao = conexao
        self.criaCliente()
        self.running  = 1
        self.lista = []        
        self.jogador = 0
        self.outro = 0
        self.daVez = PLAYER
        self.modalidade = REMOTE
        self._bombas = self._bomba()
        self.running = 1

    def getBombas(self):
        return self._logica.getBombas()

    def criaCliente(self):
	INTERNET = 0
	BLUETOOTH = 1
	sys.path.append(PATHLIB)
	import aclient
	
	if (self.conexao == INTERNET):		
		#data = appuifw.query(u"Escreva o ip do seu amigo", "text")
		data = "169.254.250.189"        
		self.cliente = aclient.Cliente( data )  

	elif (self.conexao == BLUETOOTH):
		self.cliente = aclient.BTReader()

	self.conecta()
    
    def getTabuleiro(self):
        return self._logica.interface()

    def conecta(self):
        sys.path.append(PATHLIB)
	import logica
	self._logica = logica.Logica( self._tamanho, tabuleiro = self.cliente.conecta() )
        

    def desconecta(self):
        self.cliente.desconecta()

    def jogaOponente(self):
        data = self.cliente.sock.recv(1024)
        return self.transformaData(data) 
        
    def _mostraTabuleiro(self, tabuleiro):           
        for x in range(self._tamanho):
            resposta = ""
            for y in range(self._tamanho):
                resposta = resposta + " " + str(tabuleiro[x][y])
            print resposta  
      
    def _escolheCasa(self):
        print 'do jogo'
        self._mostraTabuleiro(self._logica.tabuleiro())
        print 'interface'
        self._mostraTabuleiro(self._logica.interface()) 
        
        x = int ( raw_input('Escolhe x: ') )
        y = int ( raw_input('Escolhe y: ') )     
        return x,y
           
    def abre(self, x, y):   
	self.lista = []
        if (self._logica.ehCasaDesconhecida(x,y)):  
             self.atualizaTabuleiro(x, y)
        return self.lista
    
    def adiciona(self,x,y):
        self.lista.append([x, y])   
    
    def atualizaTabuleiro(self, x, y):
        self.adiciona(x, y)               
        if ( self._logica.ehBomba(x, y) ):            
            self._logica.achouBomba()    
            if (self.daVez == COMPUTER or self.daVez == REMOTE):
                 self._logica.atualizaCasaAtual(x, y)                
                 self.outro = self.outro + 1
            else:
		self.atualizaBombasI(x, y)                
                self.jogador = self.jogador + 1
        else:
            if ( self._logica.ehCasaVazia(x, y) ):
                self.lista = self.adicionaNaLista(self._logica.casasVazias(x, y), self.lista)
            else:
                self._logica.atualizaCasaAtual(x, y)               
            
            if (self.daVez == COMPUTER or self.daVez == REMOTE):
                self.daVez = PLAYER
                
            elif (self.daVez == PLAYER):
                self.daVez = self.modalidade      
                
    def adicionaNaLista(self, lista, outra):
        for i in range(len(lista)):
            outra.append(lista[i])
        return outra 
    
    def tabuleiro(self):
        return self._logica.tabuleiro()
    
    def interface(self):
        return self._logica.interface()

    def ehBomba(self, x, y):
        return self._logica.ehBomba(x, y)

    def ehCasaDesconhecida(self, x, y):
        return self._logica.ehCasaDesconhecida(x, y)

    def atualizaBombasI(self, x,y):
        self._logica.atualizaBombasI(x, y)

    def _bomba(self):
        self._logica.getBombas()
      
    def getLista(self):
        lista = self.jogada()        
        return self.enviaData(lista)
    
    def enviaDataERecebe(self, lista):
        data = ""
        for z in range(len(lista)):
            data = data + " " + str( lista[z][0] ) + "," + str ( lista[z][1] )
	self.cliente.sock.send (data)
	return self.cliente.sock.recv(1024)
    
    def jogaJogador(self):
        vez = self.daVez
        lista = []
        while (vez == self.daVez):        
            x, y = self._escolheCasa()           
            lista = self.adicionaNaLista(self.abre(x, y), lista)
        self.lista = lista
        return  lista    
    
    def transformaData(self, data):
        linhas = data.split(" ")
        jogada = []
        for l in range(len(linhas)):
            coordenadas = linhas[l].split(",")
            if (len(coordenadas) > 1):
                x = int ( coordenadas[0] )
                y = int ( coordenadas[1] )
                jogada.append([x,y])
                self.abre(x, y)
        return jogada
    
    def comecaJogo(self):
        while(self.running):
            self.jogaOponente()
            self.jogada()
            self.cliente.sock.send(self.enviaData(self.lista))