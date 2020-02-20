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

import sys
import appuifw
import socket
import e32
import os

COMPUTER = 1
REMOTE = 2
PLAYER = 3
IMPOSSIBLE = 4

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

class Jogo:
    def __init__(self, tamanho, MODE = 1, conexao = 0):        
        self.lista = []
        self.jogador = 0
        self.outro = 0
	self.conexao = conexao
        self.daVez = PLAYER
        self.modalidade = MODE
        self._acionaModalidade(tamanho)

    def exit(self):
        print ''

    def _acionaModalidade(self, tamanho):
        #importando as bibliotecas
        sys.path.append(PATHLIB)
	import logica
	self._logica = logica.Logica(tamanho)

        if (self.modalidade == COMPUTER):
	    import jogador
            self.computador = jogador.Inteligencia()  

        elif (self.modalidade == IMPOSSIBLE):
	    import jogador
            self.computador = jogador.Inteligencia(IMPOSSIBLE, self._logica.tabuleiro())
            self.modalidade = COMPUTER

        elif (self.modalidade == REMOTE):  
	    INTERNET = 0
	    BLUETOOTH = 1
	    import aserver
	    if (self.conexao == INTERNET):      
		
		ap_id = socket.select_access_point()
		apo = socket.access_point(ap_id)
		apo.start()
		ip = apo.ip()

        	self.servidor = aserver.Servidor(ip)	
		appuifw.query(u"Mostre o IP ao seu amigo: " + str (ip), 'info')	    

	    elif (self.conexao == BLUETOOTH):
		self.servidor = aserver.BTSender()

	    self.servidor.conectar(self._logica.tabuleiro())

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

    def getBombas(self):
        return self._logica.getBombas()
 
    def _bomba(self):
        self._logica.bombas()
                      
    def _mostraTabuleiro(self, tabuleiro):           
        for x in range(self._logica.tamanho()):
            resposta = ""
            for y in range(self._logica.tamanho()):
                resposta = resposta + " " + str(tabuleiro[x][y])
            print resposta
    
    def abre(self, x, y):  
	self.lista = []
        if (self._logica.ehCasaDesconhecida(x,y)):  
             self.atualizaTabuleiro(x, y)
        return self.lista
                 
    def atualizaTabuleiro(self, x, y):
        self.adiciona(x, y)               
        if ( self._logica.ehBomba(x, y) ):            
            self._logica.achouBomba()    
            if (self.daVez == COMPUTER or self.daVez == REMOTE):
                 self.atualizaBombasI(x, y)     
                 self.outro = self.outro + 1
            else:
                self._logica.atualizaCasaAtual(x, y)                           
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
                
    def adiciona(self,x,y):
        self.lista.append([x, y])  
        
    def _continuaJogo(self):
        if (self._logica.getBombas() == 0):
             return False
        
        for x in range(self._logica.tamanho() - 1):        
            for y in range(self._logica.tamanho() - 1):
                if (self._logica.casaValida(x,y)):
                    return True            
        return False 
 
    def _escolheCasa(self):
        x = int ( raw_input('Escolhe x: ') )
        y = int ( raw_input('Escolhe y: ') )     
        return x,y
           
    def printer(self, lista):
        print 'comeco'
        print lista
            
    def jogaJogador(self):
        vez = self.daVez
        lista = []
        while (vez == self.daVez):        
            x, y = self._escolheCasa()           
            lista = self.adicionaNaLista(self.abre(x, y), lista)
        self.lista = lista
        return  lista
    
    def adicionaNaLista(self, lista, outra):
        for i in range(len(lista)):
            outra.append(lista[i])
        return outra
            
    def jogaOponente(self, lista):
        if (self.modalidade == COMPUTER):
            return self._jogaInteligencia()
        elif (self.modalidade == REMOTE):
            return self._jogaRemote(lista)
       
    def _jogaInteligencia(self):
        vez = self.daVez
        lista = []
        while (vez == self.daVez):
            x, y = self.computador.jogada(self._logica.tamanho(), self._logica.interface())
            lista = self.adicionaNaLista(self.abre(x, y), lista)
        return lista        
    
    def _jogaRemote(self, lista):
        return self.transformaData(self._enviaInformacoes(lista))
    
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

    def _enviaInformacoes(self, lista):
        return self.enviaDataERecebe(lista)
    
    def enviaDataERecebe(self, lista):
        data = ""
        for z in range(len(lista)):
            data = data + " " + str( lista[z][0] ) + "," + str ( lista[z][1] ) 
	self.servidor.conn.send(data)
	return self.servidor.conn.recv(1024)
        

    def comecaJogo(self):
        while(self._continuaJogo()):
            print 'do jogo'
            self._mostraTabuleiro(self._logica.tabuleiro())
            print 'interface'
            self._mostraTabuleiro(self._logica.interface()) 
            
            print 'Jogador'
            self.printer(self.jogaJogador())
            
            print 'Inteligencia'
            self.printer(self.jogaOponente())
            
        self._mostraTabuleiro(self._logica.interface())           
        print 'Fim de jogo'
        
#game = Jogo(6)
#game.comecaJogo()