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

IMPOSSIBLE = 4

import random

class Inteligencia:
    
    def __init__(self, modo = EASY, tabuleiro = []):
        self._interface = []
        self._tabuleiro = tabuleiro
        self.__tamanho = 0
        self._modalidade = modo
        
    def jogada(self, tamanho, tabuleiro):
        self._interface = tabuleiro
        self.__tamanho = tamanho  
        if (self._modalidade != IMPOSSIBLE):
            return self.verMelhorJogada()
        else: 
            return self.superJogada()
    
    def superJogada(self):
        chance = random.randint(0, 1)
        if (chance != 0):
            return self.verMelhorJogada()
        else:
            return self.super()                       

    def super(self):
        maiorX, maiorY = self.escolheRandomicamente()
        for x in range(self.__tamanho - 1):        
            for y in range(self.__tamanho - 1):
                if (self._tabuleiro[x][y] == 'B' and self._interface[x][y] == '#'):
                    return x, y    
        return maiorX, maiorY

    def verMelhorJogada(self):
        maiorX, maiorY = self.escolheRandomicamente()
        melhorChance = self.__verifica(maiorX, maiorY)    
                    
        for x in range(self.__tamanho - 1):        
            for y in range(self.__tamanho - 1):
                if (self.casaValida(x,y)):
                    chance = self.__verifica(x, y)
                    if (chance > melhorChance):                         
                        melhorChance = chance
                        maiorX, maiorY = self.escolheCasa(x, y)

        return maiorX, maiorY
 
    def temJogadaPossivel(self):
        for x in range(self.__tamanho - 1):        
                for y in range(self.__tamanho - 1):
                    if (self.casaValida(x,y)):
                        return True
            
        return False
    
    
    def escolheRandomicamente(self):
        temJogada = self.temJogadaPossivel()
        maiorX = random.randint(0, self.__tamanho - 1)
        maiorY = random.randint(0, self.__tamanho - 1)

        while self._interface[maiorX][maiorY] != '#' and temJogada:
            maiorX = random.randint(0, self.__tamanho - 1)
            maiorY = random.randint(0, self.__tamanho - 1)       
        return maiorX, maiorY
    
    def casaValida(self, x, y):
        return self._interface[x][y] == '#' 
    
    def escolheCasa(self, x, y):
        return x, y

    def __verifica(self, x, y):
        chance = 0
        if (self._interface[x][y] != '#' and self._interface[x][y] != 'B' and self._interface[x][y] != 'iB'):
            chance = self._interface[x][y]
## pontas      
        #ponta esquerda de cima
        if (x == 0 and y == 0):
            chance =  chance + self.__casaEmBaixo(x,y)
            chance =  chance + self.__casaDoLadoDireito(x,y) 
            chance =  chance + self.__casaDiagonalDireitaDeBaixo(x, y)

        #ponta direita de cima                                     
        elif (x == self.__tamanho - 1 and y == 0):               
            chance =  chance + self.__casaEmBaixo(x, y)
            chance =  chance + self.__casaDoLadoEsquerdo(x, y)
            chance =  chance + self.__casaDiagonalEsquerdaDeBaixo(x, y)
                       
        #ponta esquerda de baixo                                         
        elif (x == 0 and y == self.__tamanho - 1 ):
            chance =  chance + self.__casaEmCima(x,y)
            chance =  chance + self.__casaDoLadoDireito(x,y)
            chance =  chance + self.__casaDiagonalDireitaDeCima(x, y)    
   
            #ponta direita de baixo                                   
        elif (x == self.__tamanho - 1 and y == self.__tamanho - 1 ):
            chance =  chance + self.__casaEmCima(x,y) 
            chance =  chance + self.__casaDoLadoEsquerdo(x,y) 
            chance =  chance +  self.__casaDiagonalEsquerdaDeCima(x, y) 
##paredes do tabuleiro                           
   
            #parede da esquerda
        elif (x == 0 and y > 0 and y < self.__tamanho - 1):
            chance =  chance + self.__casaEmBaixo(x,y) 
            chance =  chance + self.__casaEmCima(x,y) 
            chance =  chance + self.__casaDoLadoDireito(x,y) 
            chance =  chance + self.__casaDiagonalDireitaDeCima(x, y) 
            chance =  chance + self.__casaDiagonalDireitaDeBaixo(x, y)
                                       
        #parede de cima
        elif (x > 0 and y == 0 and x < self.__tamanho - 1):
            chance =  chance + self.__casaEmBaixo(x,y)
            chance =  chance + self.__casaDoLadoDireito(x,y) 
            chance =  chance + self.__casaDoLadoEsquerdo(x,y)       
            chance =  chance + self.__casaDiagonalDireitaDeBaixo(x, y)
            chance =  chance +  self.__casaDiagonalEsquerdaDeBaixo(x, y)            
           
        #parede da direita
        elif (x == self.__tamanho - 1 and y > 0 and y < self.__tamanho - 1):
            chance =  chance + self.__casaEmBaixo(x,y)
            chance =  chance + self.__casaEmCima(x,y)
            chance =  chance + self.__casaDoLadoEsquerdo(x,y)
            chance =  chance + self.__casaDiagonalEsquerdaDeCima(x, y)    
            chance =  chance + self.__casaDiagonalEsquerdaDeBaixo(x, y)
           
        #parede de baixo       
        elif (x > 0 and y == self.__tamanho - 1 and x < self.__tamanho - 1):
            chance =  chance + self.__casaEmCima(x,y)
            chance =  chance + self.__casaDoLadoDireito(x, y)
            chance =  chance + self.__casaDoLadoEsquerdo(x,y)
            chance =  chance + self.__casaDiagonalDireitaDeCima(x, y)             
            chance =  chance + self.__casaDiagonalEsquerdaDeCima(x, y)    
## o resto              
        #casas de dentro do tabuleiro
        else:                       
            chance =  chance + self.__casaEmBaixo(x,y)
            chance =  chance + self.__casaEmCima(x,y)
            chance =  chance + self.__casaDoLadoDireito(x,y)   
            chance =  chance + self.__casaDoLadoEsquerdo(x,y)
            chance =  chance + self.__casaDiagonalDireitaDeCima(x, y)             
            chance =  chance + self.__casaDiagonalEsquerdaDeCima(x, y)   
            chance =  chance + self.__casaDiagonalDireitaDeBaixo(x, y)
            chance =  chance + self.__casaDiagonalEsquerdaDeBaixo(x, y)
        
        return chance
   
    def verificaCasa(self, x, y):
        if (self._interface[x][y] == '#'):
            return 0
        elif (self._interface[x][y] == 'B' or self._interface[x][y] == 'iB'):
            return -1
        return self._interface[x][y]
   
    def __casaEmBaixo(self, x, y):
        return self.verificaCasa(x, y + 1)

    def __casaEmCima(self, x, y):
        return self.verificaCasa(x, y - 1)
               
    def __casaDoLadoEsquerdo(self, x, y):
        return self.verificaCasa(x - 1, y)
               
    def __casaDoLadoDireito(self, x, y):
        return self.verificaCasa(x + 1, y)

    def __casaDiagonalEsquerdaDeCima(self, x,y):
        return self.verificaCasa(x - 1, y - 1)
       
    def __casaDiagonalDireitaDeCima(self, x,y):
        return self.verificaCasa(x + 1, y - 1)
       
    def __casaDiagonalEsquerdaDeBaixo(self, x,y):
        return self.verificaCasa(x - 1, y + 1)
   
    def __casaDiagonalDireitaDeBaixo(self, x,y):   
        return self.verificaCasa(x + 1, y + 1)
  