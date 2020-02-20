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

EASY = 6
NORMAL = 9
HARD = 14

import random

class Logica:
    
    def __init__(self, tamanho = EASY, tabuleiro = [], interface = []):
        self._tamanho = tamanho
        self._bombas = self._numeroDeBombas()     
        self.montaTabuleiros(tabuleiro, interface)
   
        
    def montaTabuleiros(self, tabuleiro, interface):    
        if (tabuleiro == [] and interface == []):
            self._tabuleiro = [[0 for i in range(self._tamanho)] for i in range(self._tamanho)]      
            self._interface = [[0 for i in range(self._tamanho)] for i in range(self._tamanho)]            
            self._preencheInterface()
            self._colocaBombas()    
            
        elif (interface == []):
            self._tabuleiro = tabuleiro
            self._interface = [[0 for i in range(self._tamanho)] for i in range(self._tamanho)]            
            self._preencheInterface()
            
        else:
            self._tabuleiro = tabuleiro
            self._interface = interface
        
    def tabuleiro(self):
        return self._tabuleiro
    
    def interface(self):
        return self._interface

    def tamanho(self):
        return self._tamanho
    
    def _numeroDeBombas(self):
        if (self._tamanho == EASY):
            return 7
        elif (self._tamanho == NORMAL):            
            return 17
        elif (self._tamanho == HARD):  
            return 39 
    
    def _colocaBombas(self):            
        for i in range(self._bombas):
            x = random.randint(0, self._tamanho - 1)
            y = random.randint(0, self._tamanho - 1)
            while (self._tabuleiro[x][y] == 'B'):
                x = random.randint(0, self._tamanho - 1)
                y = random.randint(0, self._tamanho - 1)           
            self._tabuleiro[x][y] = 'B'
        self._montaTabuleiro()
        
    def achouBomba(self):
        self._bombas = self._bombas - 1
                        
    def ehCasaDesconhecida(self, x, y):
        return self._interface[x][y] == "#"
    
    def ehBomba(self, x,y):
        return self._tabuleiro[x][y] == 'B'
    
    def getBombas(self):
        return self._bombas
   
    def atualizaBombasI(self, x, y):
        self._interface[x][y] = 'iB'
    
    def atualizaCasaAtual(self, x, y):                
        self._interface[x][y] = self._tabuleiro[x][y]   
    
    def ehCasaVazia(self, x, y):
        return self._tabuleiro[x][y] == 0
    
    def _preencheInterface(self):
        for x in range(self._tamanho):
            for y in range(self._tamanho):
                self._interface[x][y] = "#"
      
    def _montaTabuleiro(self):
        for x in range(self._tamanho):           
            for y in range(self._tamanho):
                if (self._tabuleiro[x][y] != 'B'):                   
## pontas                   
                    #ponta esquerda de cima
                    if (x == 0 and y == 0):
                        self._verificaEmBaixo(x,y)
                        self._verificaDoLadoDireito(x,y)
                        self._verificaDiagonalDireitaDeBaixo(x, y)
                   
                    #ponta direita de cima                                           
                    elif (x == self._tamanho - 1 and y == 0):
                        self._verificaEmBaixo(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDiagonalEsquerdaDeBaixo(x, y)                     
                       
                    #ponta esquerda de baixo   
                    elif (x == 0 and y == self._tamanho - 1 ):
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoDireito(x,y)
                        self._verificaDiagonalDireitaDeCima(x, y)

                    #ponta direita de baixo                                   
                    elif (x == self._tamanho - 1 and y == self._tamanho - 1 ):
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDiagonalEsquerdaDeCima(x, y)
##paredes do tabuleiro                           
                    #parede da esquerda
                    elif (x == 0 and y > 0 and y < self._tamanho - 1):
                        self._verificaEmBaixo(x,y)
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoDireito(x,y)
                        self._verificaDiagonalDireitaDeCima(x, y)
                        self._verificaDiagonalDireitaDeBaixo(x, y)
                       
                    #parede de cima
                    elif (x > 0 and y == 0 and x < self._tamanho - 1):
                        self._verificaEmBaixo(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDoLadoDireito(x,y)                       
                        self._verificaDiagonalEsquerdaDeBaixo(x, y)
                        self._verificaDiagonalDireitaDeBaixo(x, y)
                       
                    #parede da direita
                    elif (x == self._tamanho - 1 and y > 0 and y < self._tamanho - 1):
                        self._verificaEmBaixo(x,y)
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDiagonalEsquerdaDeBaixo(x, y)
                        self._verificaDiagonalEsquerdaDeCima(x, y)
                   
                    #parede de baixo       
                    elif (x > 0 and y == self._tamanho - 1 and x < self._tamanho - 1):
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDoLadoDireito(x, y)
                        self._verificaDiagonalEsquerdaDeCima(x, y)
                        self._verificaDiagonalDireitaDeCima(x, y)

## o resto              
                    #casas de dentro do tabuleiro
                    else:                       
                        self._verificaEmBaixo(x,y)
                        self._verificaEmCima(x,y)
                        self._verificaDoLadoEsquerdo(x,y)
                        self._verificaDoLadoDireito(x,y)
                        self._verificaDiagonalEsquerdaDeBaixo(x, y)
                        self._verificaDiagonalEsquerdaDeCima(x, y)
                        self._verificaDiagonalDireitaDeBaixo(x, y)
                        self._verificaDiagonalDireitaDeCima(x, y)
   
    def _adicionaUm(self, x, y):
        self._tabuleiro[x][y] = self._tabuleiro[x][y] + 1
       
    def _verificaEmBaixo(self, x, y):
        if (self._tabuleiro[x][y + 1] == 'B'):
             self._adicionaUm(x, y)
           
    def _verificaEmCima(self, x, y):
        if (self._tabuleiro[x][y - 1] == 'B'):
             self._adicionaUm(x, y)

    def _verificaDoLadoEsquerdo(self, x, y):
        if (self._tabuleiro[x - 1][y] == 'B'):
             self._adicionaUm(x, y)
   
    def _verificaDoLadoDireito(self, x, y):
        if (self._tabuleiro[x + 1][y] == 'B'):
             self._adicionaUm(x, y)           
           
    def _verificaDiagonalEsquerdaDeCima(self, x,y):   
        if (self._tabuleiro[x - 1][y - 1] == 'B'):
             self._adicionaUm(x, y)  
   
    def _verificaDiagonalDireitaDeCima(self, x,y):   
        if (self._tabuleiro[x + 1][y - 1] == 'B'):
             self._adicionaUm(x, y)

    def _verificaDiagonalEsquerdaDeBaixo(self, x,y):   
        if (self._tabuleiro[x - 1][y + 1] == 'B'):
             self._adicionaUm(x, y)               
   
    def _verificaDiagonalDireitaDeBaixo(self, x,y):   
        if (self._tabuleiro[x + 1][y + 1] == 'B'):
             self._adicionaUm(x, y)   

    def casasVazias(self, x, y):
        self.lista = []
        self._casasVazias(x, y)
        return self.lista
             
    def _casasVazias(self,x, y):
        if (self._interface[x][y] == '#'):
            self._interface[x][y] = self._tabuleiro[x][y]        
## pontas      
            #ponta esquerda de cima
            if (x == 0 and y == 0):
                self._casaVaziaEmBaixo(x,y)
                self._casaVaziaDoLadoDireito(x,y)
                self._casaVaziaDiagonalDireitaDeBaixo(x, y)

            #ponta direita de cima                                     
            elif (x == self._tamanho - 1 and y == 0):               
                self._casaVaziaEmBaixo(x, y)
                self._casaVaziaDoLadoEsquerdo(x, y)
                self._casaVaziaDiagonalEsquerdaDeBaixo(x, y)
                           
            #ponta esquerda de baixo                                         
            elif (x == 0 and y == self._tamanho - 1 ):
                 self._casaVaziaEmCima(x,y)
                 self._casaVaziaDoLadoDireito(x,y)       
                 self._casaVaziaDiagonalDireitaDeCima(x, y)    
   
            #ponta direita de baixo                                   
            elif (x == self._tamanho - 1 and y == self._tamanho - 1 ):
                self._casaVaziaEmCima(x,y)
                self._casaVaziaDoLadoEsquerdo(x,y)         
                self._casaVaziaDiagonalEsquerdaDeCima(x, y) 
##paredes do tabuleiro                           
   
            #parede da esquerda
            elif (x == 0 and y > 0 and y < self._tamanho - 1):
                self._casaVaziaEmBaixo(x,y)
                self._casaVaziaEmCima(x,y)
                self._casaVaziaDoLadoDireito(x,y)
                self._casaVaziaDiagonalDireitaDeCima(x, y)    
                self._casaVaziaDiagonalDireitaDeBaixo(x, y)
                                           
            #parede de cima
            elif (x > 0 and y == 0 and x < self._tamanho - 1):
                self._casaVaziaEmBaixo(x,y)
                self._casaVaziaDoLadoDireito(x,y) 
                self._casaVaziaDoLadoEsquerdo(x,y)       
                self._casaVaziaDiagonalDireitaDeBaixo(x, y)
                self._casaVaziaDiagonalEsquerdaDeBaixo(x, y)            
               
            #parede da direita
            elif (x == self._tamanho - 1 and y > 0 and y < self._tamanho - 1):
                self._casaVaziaEmBaixo(x,y)
                self._casaVaziaEmCima(x,y)
                self._casaVaziaDoLadoEsquerdo(x,y)
                self._casaVaziaDiagonalEsquerdaDeCima(x, y)    
                self._casaVaziaDiagonalEsquerdaDeBaixo(x, y)
               
            #parede de baixo       
            elif (x > 0 and y == self._tamanho - 1 and x < self._tamanho - 1):
                self._casaVaziaEmCima(x,y)
                self._casaVaziaDoLadoDireito(x, y)
                self._casaVaziaDoLadoEsquerdo(x,y)
                self._casaVaziaDiagonalDireitaDeCima(x, y)             
                self._casaVaziaDiagonalEsquerdaDeCima(x, y)    
## o resto              
            #casas de dentro do tabuleiro
            else:                       
                self._casaVaziaEmBaixo(x,y)
                self._casaVaziaEmCima(x,y)
                self._casaVaziaDoLadoDireito(x,y)   
                self._casaVaziaDoLadoEsquerdo(x,y)
                self._casaVaziaDiagonalDireitaDeCima(x, y)             
                self._casaVaziaDiagonalEsquerdaDeCima(x, y)   
                self._casaVaziaDiagonalDireitaDeBaixo(x, y)
                self._casaVaziaDiagonalEsquerdaDeBaixo(x, y)
       
    def verificaCasa(self, x, y):
        if (self._interface[x][y] == '#'):
            if (self._tabuleiro[x][y] == 0):
                 self._casasVazias(x, y)       
            self._interface[x][y] = self._tabuleiro[x][y] 
            self.adiciona(x, y)       
            
    def adiciona(self,x,y):
        self.lista.append([x, y])  
   
    def _casaVaziaEmBaixo(self, x, y):
        self.verificaCasa(x, y + 1)

    def _casaVaziaEmCima(self, x, y):
        self.verificaCasa(x, y - 1)
               
    def _casaVaziaDoLadoEsquerdo(self, x, y):
        self.verificaCasa(x - 1, y)
               
    def _casaVaziaDoLadoDireito(self, x, y):
        self.verificaCasa(x + 1, y)

    def _casaVaziaDiagonalEsquerdaDeCima(self, x,y):
        self.verificaCasa(x - 1, y - 1)
       
    def _casaVaziaDiagonalDireitaDeCima(self, x,y):
        self.verificaCasa(x + 1, y - 1)
       
    def _casaVaziaDiagonalEsquerdaDeBaixo(self, x,y):
        self.verificaCasa(x - 1, y + 1)
   
    def _casaVaziaDiagonalDireitaDeBaixo(self, x,y):   
        self.verificaCasa(x + 1, y + 1)
     
    def casaValida(self, x, y):
        return self._interface[x][y] == '#' 