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

from graphics import Image
import key_codes
import appuifw
import sysinfo
import e32
import sys
import os
import audio
 

PATHLIB  = "\\python\\lib"
PATHICON = "\\python\\icons\\"
PATHSOM = "\\python\\som\\"

def get_path(app_name):
	drives_list = e32.drive_list()

	#Gives preference to load from drive 'E:'
	drives_list.reverse()
	for drive in [str(x) for x in drives_list]:
        	if os.path.isdir(os.path.join(drive, app_name)):
	        	return os.path.join(drive, app_name)

#atualizando caminho
PATHICON = get_path(PATHICON)
PATHLIB = get_path(PATHLIB)
PATHSOM = get_path(PATHSOM)


CASAS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 'B', '#', 'iB']
DEMARCADORES = [ 'ultima']
MASCARAS = ['iultima']
AUDIO = ['bolha','introducao', 'mina']

EASY = 6
NORMAL = 9
HARD = 14


class interfaceServer:

    def __init__(self, tamanho, modo, conexao = 0):	

        #importando as bibliotecas
	sys.path.append(PATHLIB)
                          
        #importando a logica do campo minado
	import campominado

	self.tamanho = tamanho
	self.jogo = campominado.Jogo(self.tamanho, modo, conexao)  

	#variaveis
	self.correnteX = 0
	self.correnteY = 0
	self.largura = 0
	self.altura = 0
	self.limiteLargura = 0 
	self.limiteAltura = 0

	self.inimigoX = 0
	self.inimigoY = 0
	
	self.vezDoOutro = False

	self.imagemCasa = self.imagensCasas()

	self.sons = self.som()

	self.outro = 0
	self.jogador = 0
	self.bombas = self.jogo.getBombas()
	
	self.podeJogar = True  
	self.img = Image.new(sysinfo.display_pixels())

	self.defineCorpoDaAplicacao(appuifw.Canvas(redraw_callback=self.handle_redraw))

	self.setkeys()
	self.lista = []
	self.somEnable = True
	self.acabou = False

	# define um evento de saída da aplicação       
	# appuifw.app.exit_key_handler = self.exit      
    
    def exit(self):
	#self.canvas = None
	#self.img = None
	self.close()
        self.jogo.exit() 

    def defineCorpoDaAplicacao(self, canvas):
        ## Define o corpo da aplicação
	self.canvas =  canvas
	appuifw.app.body = self.canvas
	appuifw.app.title = u'Campo Minado'
	appuifw.app.screen = 'full' #normal, large, full

    def close(self):
	for x in range(len(AUDIO)):	
		self.sons[AUDIO[x]].close()

	for x in range(len(CASAS)):
		self.imagemCasa[CASAS[x]].clear()

	for x in range(len(DEMARCADORES)):
		self.imagemCasa[DEMARCADORES[x]].clear()

	for x in range(len(MASCARAS)):
		self.imagemCasa[MASCARAS[x]].clear()

    def imagensCasas(self):
	imagens = {}
	for x in range(len(CASAS)):
		imagens[CASAS[x]] = Image.open(self.getPathFigura(CASAS[x]))
		imagens["u"+ str(CASAS[x])] = Image.open(self.getPathFigura(CASAS[x], 'u'))

	for x in range(len(DEMARCADORES)):
		imagens[DEMARCADORES[x]] = Image.open(self.getPathFigura(DEMARCADORES[x]))

	for x in range(len(MASCARAS)):
		imagens[MASCARAS[x]] = Image.open(self.getPathFigura(MASCARAS[x]))
	
	return imagens

	
    def getPathFigura(self, figura, string = ''):
	if (string == ''):
	        if self.tamanho == EASY:
		   return PATHICON + str(figura) + ".PNG"

		elif self.tamanho == NORMAL:
		   return PATHICON + str(figura) + "o" +".PNG"

		elif self.tamanho == HARD:
		   return PATHICON + str(figura) + "f" +".PNG"
	else:
	        if self.tamanho == EASY:
		   return PATHICON + 'u' + str(figura) + ".PNG"

		elif self.tamanho == NORMAL:
		   return PATHICON + 'u' + str(figura) + "o" +".PNG"

		elif self.tamanho == HARD:
		   return PATHICON + 'u' + str(figura) + "f" +".PNG"


    def som(self):
	sons = {}
	for x in range(len(AUDIO)):	
		sons[AUDIO[x]] = audio.Sound.open(PATHSOM + AUDIO[x] + ".wav")	
	return sons
	

    def setkeys(self):
	## Define key_codes
        self.canvas.bind(key_codes.EKey2, self.moveCima)
        self.canvas.bind(key_codes.EKeyUpArrow, self.moveCima)

        self.canvas.bind(key_codes.EKey4, self.moveEsquerda)
        self.canvas.bind(key_codes.EKeyLeftArrow, self.moveEsquerda)

        self.canvas.bind(key_codes.EKey5, self.abreEstaCasa)
        self.canvas.bind(key_codes.EKeySelect, self.abreEstaCasa)

        self.canvas.bind(key_codes.EKey6, self.moveDireita)
        self.canvas.bind(key_codes.EKeyRightArrow, self.moveDireita)

        self.canvas.bind(key_codes.EKey8, self.moveBaixo)
        self.canvas.bind(key_codes.EKeyDownArrow, self.moveBaixo)


    def abreEstaCasa(self):
	if (self.podeJogar):
		self.podeJogar = False
		self.abreCasa(int (self.correnteX / self.largura), int(self.correnteY / self.altura))
		self.escolha()
        
    def abreCasa(self, x, y):
	if (self.jogo.ehCasaDesconhecida(x, y)):
		self.desenhaJogador(x,y)
		if (self.vezDoOutro):
			self.desenhaOutro(self.jogo.jogaOponente(self.lista))
			self.lista = []
			self.vezDoOutro = False
		self.escolha()


    def desenhaJogador(self,x, y):
	jogada = self.jogo.abre(x, y)
	self.adicionaLista(jogada)
	self.desenhaLista(jogada)

	if (self._ehBomba(x, y)):
		self.podeJogar = True
		self.jogador = self.jogador + 1
		self.placarAzul()
		self.desenhaTotal()
		self.verificaPlacar()
	self.escolha()

    def adicionaLista(self, outra):
        for i in range(len(outra)):
            self.lista.append(outra[i])

    def desenhaLista(self, lista):	
        for x in range(len(lista)):
		self.desenhaCasaAtual(lista[x][0], lista[x][1])

    def verificaPlacar(self):
	if (self.bombas == 0):
		atualX, atualY = self.getAtual()
		self.desenhaCasaAtual(atualX, atualY)
		self.acabou = True
		if (self.jogador > self.outro):			
			appuifw.note(u"O Jogador Ganhou!", "info")

			#self.exit()
		else:
			appuifw.note(u"O Computador Ganhou!", "info")
			#self.exit()
			

    def desenhaOutro(self, lista):
	self.escolha()
	self.podeJogar = False
	if (len(lista) > 0):
		self.desenhaCasaAtual(self.inimigoX, self.inimigoY)
		if (self.jogo.ehBomba(lista[0][0], lista[0][1])):
			self.inimigoX, self.inimigoY = lista[len(lista) - 1][0], lista[len(lista) - 1][1]
			self.desenhaListaC(lista)	
			self.desenhaUltimaEscolha(self.inimigoX, self.inimigoY)
		else:
			self.inimigoX, self.inimigoY = lista[0][0], lista[0][1]
			self.desenhaLista(lista)
			self.desenhaUltimaEscolha(self.inimigoX, self.inimigoY)
			self.tocaSom('bolha')
	self.podeJogar = True


    def desenhaListaC(self, lista):	
	ultimo = 0
	verificaSeEhBomba = True
        for x in range(len(lista)):
		self.desenhaCasaAtual(lista[ultimo][0], lista[ultimo][1])
		if (verificaSeEhBomba):
			self.desenhaUltimaEscolha(lista[x][0], lista[x][1])
			if (self._ehBomba(lista[x][0], lista[x][1])):
				self.outro = self.outro + 1
				self.placarVermelho()
				self.desenhaTotal()
				self.verificaPlacar()
				verificaSeEhBomba = True
			else:
				verificaSeEhBomba = False
		ultimo = x

	self.desenhaCasaAtual(lista[ultimo][0], lista[ultimo][1])

    def _ehBomba(self, x,y):	
	if (self.jogo.ehBomba(x, y)):
		self.tocaSom('mina')
		self.bombas = self.bombas - 1
		self.vezDoOutro = False
		return True
	else:
		self.tocaSom('bolha')
		self.vezDoOutro = True
		return False

    def tocaSom(self, nome):
	if (self.somEnable) :
		self.stopAll()
		self.sons[nome].play()
		e32.ao_sleep(1)	

    def desenhaUltimaEscolha(self,x, y):
	self.desenhaCasaAtual(x, y)
	mask_name = Image.new(self.imagemCasa["iultima"].size,'1')
	mask_name.blit(self.imagemCasa["iultima"])
	self.canvas.blit(self.imagemCasa["ultima"], target=(self.largura * x, self.altura * y), mask = mask_name)


    def desenhaCasaAtual(self, x, y, string = ''):
	casa = self.jogo.interface()[x][y]
	if (string == ''):
	        self.canvas.blit(self.imagemCasa[casa], target=(self.largura * x, self.altura * y))	
	else:
	        self.canvas.blit(self.imagemCasa[string + str(casa)],target=(self.largura * x, self.altura * y))


    def getAtual(self):
	x, y = self.correnteX / self.largura, self.correnteY / self.altura
	return int(x), int(y)
		
    def stopAll(self):
	for x in range(len(AUDIO)):	
		self.sons[AUDIO[x]].stop() 
	
    def moveDireita(self):
	if (self.correnteX < self.limiteLargura):
		atualX, atualY = self.getAtual()
		self.desenhaCasaAtual(atualX, atualY)
		self.correnteX = self.correnteX + self.largura
	self.escolha()

    def moveEsquerda(self):
	if (self.correnteX - self.largura >= 0):
		atualX, atualY = self.getAtual()
		self.desenhaCasaAtual(atualX, atualY)
		self.correnteX = self.correnteX - self.largura 
	self.escolha()

    def moveBaixo(self):
	if (self.correnteY < self.limiteAltura):
		atualX, atualY = self.getAtual()
		self.desenhaCasaAtual(atualX, atualY)
		self.correnteY = self.correnteY + self.altura
	self.escolha()

    def moveCima(self):	
	if (self.correnteY - self.altura >= 0):
		atualX, atualY = self.getAtual()
		self.desenhaCasaAtual(atualX, atualY)
		self.correnteY = self.correnteY - self.altura
	self.escolha()
      
    def handle_redraw(self,rect):
        if self.canvas:
		self.canvas.blit(self.img)	
		self.desenhaTabuleiro()
		self.placares()
		self.escolha()

    def desenhaTabuleiro(self):        
	tabuleiro = self.jogo.interface()
	for x in range(self.tamanho):
		for y in range(self.tamanho): 
   	     		# carrega a image      
			logo = self.imagemCasa[tabuleiro[x][y]]

			# obtem a largura e altura da image
			self.largura, self.altura = logo.size

			# desenha a imagem
			self.canvas.blit(logo, target=(self.largura * x, self.altura * y))

	self.limiteLargura = self.largura * (self.tamanho - 1)
	self.limiteAltura = self.altura * (self.tamanho - 1)
	self.escolha()

    def placares(self):
	self.placarVermelho()
	self.placarAzul()
	self.desenhaTotal()

    def desenhaTotal(self):
	figura = Image.open(PATHICON + "total.PNG") 
	palavra = u""+ str (self.bombas)
	figura.text((14, 35), palavra, font='normal')
	self.canvas.blit(figura, target = (93,260)) 

    def placarVermelho(self):
	figura = Image.open(PATHICON + "inimigo.PNG")	
	palavra = u""+ str (self.outro)
	figura.text((36, 47), palavra, font='normal')
	self.canvas.blit(figura, target = (149,256)) 

    def placarAzul(self):
	figura = Image.open(PATHICON + "placar.PNG")	
	palavra = u""+ str (self.jogador)
	figura.text((36, 43), palavra, font='normal')
	self.canvas.blit(figura, target = (7,257)) 

    def escolha(self):
	self.desenhaCasaAtual(self.correnteX / self.largura, self.correnteY / self.altura, 'u')

    def comecoSom(self):
	self.tocaSom('introducao')

    def comeco(self):
	#self.desenhaTabuleiro()
	#self.placares()
	self.comecoSom()
	#self.escolha()