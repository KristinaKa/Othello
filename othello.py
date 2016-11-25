import pygame, sys
from pygame.locals import *

########## CONSTANT VARIABLES #############

FPS = 30 #frames per second
BOARD_X=5 #the top left x position of the board
BOARD_Y=60 #the top left y position
BOARD_W=BOARD_H=400 #the sizes of the board
WIN_L=BOARD_H+65 #window length
WIN_W=BOARD_W+15 #window width
X_MARGIN=BOARD_X #same variable, used for the rectangle drawing
Y_MARGIN=BOARD_Y
SQUARE_SIZE=50 #the size of a square of the board
PIECE_R=24 #the dradius of the pieces
LINE_SIZE=2 #the size of the line defining the grid of the board
SCORE_BOX_W=100 #width of the two score rectangles
SCORE_BOX_H=50 #height
SCORE_BOX_1_X=120 #top left x of the first score rectangle
SCORE_BOX_2_X=SCORE_BOX_1_X+SCORE_BOX_W+5 # top left x of the second score rectangle

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 102,   51)
BLUE  = (  0,   0, 255)
GREY  = ( 160,  160,  160)
DARK_GREY  = ( 64,  64,  64)

############### GAME ###################

def main():
	global FPSCLOCK, DISPLAYSURF, board
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WIN_W, WIN_L))
	pygame.display.set_caption("Othello")
	DISPLAYSURF.fill(WHITE)	
	
	mousex = 0
	mousey = 0 

	board = initializeBoard()

	player = 0 #0=BLACK, 1=WHITE
	possibleMoves = getPossibleMoves(board, player)
	displayScores()
	drawBoard(board, possibleMoves, player)


	while True:

		mouseClicked = False

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True
		
		# if no possible moves, change player
		if possibleMoves == []:
			player = changePlayer(player)
			possibleMoves = getPossibleMoves(board, player)

		# If still no more possible moves, game over
		if possibleMoves == []:
			drawBoard(board, [], 0)
			displayScores()
			displayWinner()

		else:
			drawBoard(board, possibleMoves, player)
			displayScores()
			squareLine, squareColumn = getSquareAtPixel(mousex, mousey)
			if squareLine != None and squareColumn != None:
				if (mouseClicked) and ((squareLine, squareColumn) in possibleMoves):
					placePiece(board, squareLine, squareColumn, player)
					#player changes and possileMoves change if a move is made
					player = changePlayer(player)
					possibleMoves=getPossibleMoves(board, player)

		# Redraw the screen and wait a clock tick.
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def changePlayer(player):
	player= 1 - player
	return player


def initializeBoard():
	"""
	Initializes the data structure board
	Board is a grid of 16 squares
	Black square=0, White square=1, Empty square=2 
	"""

	board=[]
	for i in range(8):
		board.append([])
		for j in range(8):
			board[i].append(2)

	board[3][3]=1
	board[3][4]=0
	board[4][3]=0
	board[4][4]=1

	return board


def drawBoard(board, possibleMoves, player):
	#rect(Surface, color, Rect, width=0)
	#Rect(left, top, width, height)= Rect(x,y, width, height)
	DISPLAYSURF.fill(WHITE)	
	pygame.draw.rect(DISPLAYSURF, GREEN, (X_MARGIN, Y_MARGIN, BOARD_W, BOARD_H))
	for i in range(9): 
		# vertical lines
		pygame.draw.line(DISPLAYSURF, BLACK, (BOARD_X+i*SQUARE_SIZE, BOARD_Y), (BOARD_X+i*SQUARE_SIZE, BOARD_Y+BOARD_H), LINE_SIZE)
	 	# orizontal lines
		pygame.draw.line(DISPLAYSURF, BLACK, (BOARD_X, BOARD_Y+i*SQUARE_SIZE), (BOARD_X+BOARD_W, BOARD_Y+i*SQUARE_SIZE), LINE_SIZE)


	color=None
	for line in range(len(board)):
		for column in range(len(board[line])):
			if board[line][column] != 2:
				if board[line][column]==0:
					color= BLACK
				if board[line][column]==1:
					color=WHITE
				pygame.draw.circle(DISPLAYSURF, color, (X_MARGIN+column*SQUARE_SIZE+SQUARE_SIZE/2, Y_MARGIN+line*SQUARE_SIZE+SQUARE_SIZE/2), PIECE_R, 0)
			elif (line, column) in possibleMoves:
				if player == 0:
					color= DARK_GREY
				else:
					color=GREY
				pygame.draw.circle(DISPLAYSURF, color, (X_MARGIN+column*SQUARE_SIZE+SQUARE_SIZE/2, Y_MARGIN+line*SQUARE_SIZE+SQUARE_SIZE/2), PIECE_R/2, 0)


def displayScores():
	pygame.draw.rect(DISPLAYSURF, BLACK, (SCORE_BOX_1_X, 5, SCORE_BOX_W, SCORE_BOX_H), 2)
	pygame.draw.rect(DISPLAYSURF, BLACK, (SCORE_BOX_2_X, 5, SCORE_BOX_W, SCORE_BOX_H), 2)
	pygame.draw.circle(DISPLAYSURF, BLACK, (SCORE_BOX_1_X+PIECE_R, 5+PIECE_R), PIECE_R, 0)
	pygame.draw.circle(DISPLAYSURF, BLACK, (SCORE_BOX_2_X+PIECE_R, 5+PIECE_R), PIECE_R, 2)
	font = pygame.font.SysFont('Arial', 25)
	score1, score2 = countScores()
	DISPLAYSURF.blit(font.render(str(score1), True, (0,0,0)), (SCORE_BOX_1_X+2*PIECE_R+5, 5+2))
	DISPLAYSURF.blit(font.render(str(score2), True, (0,0,0)), (SCORE_BOX_2_X+2*PIECE_R+5, 5+2))


def leftTopCoordsOfSquare(x, y):
	# x and y are the coordinates of a square in the board
	# Convert board coordinates to pixel coordinates
	left = x * SQUARE_SIZE + X_MARGIN
	top = y * SQUARE_SIZE + Y_MARGIN
	return (left, top)

def getSquareAtPixel(x, y):
	# x and y are the coordinates of a square in the board
	# they correspond to the line and the column of the square
	for boardx in range(BOARD_W):
		for boardy in range(BOARD_H):
			left, top = leftTopCoordsOfSquare(boardx, boardy)
			squareRect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
			if squareRect.collidepoint(x, y):
				return (boardy, boardx)
	return (None, None)

def getPossibleMoves(board, player):
	""" 
	Finds the squares owned by the player and any moves and
	calls the function ckeckMovesForSquare
	"""
	moves = []
	player2= 1 - player
	for line in range(len(board)):
		for column in range(len(board[line])):
			if (line < 8 and column < 8) and board[line][column] == player:
				movesForThisSquare = checkMovesForSquare(board, line, column, player2)
				for m in movesForThisSquare:
					moves.append(m)

	return moves

def checkMovesForSquare(board, line, column, player2):
	"""
	Checks if any opponent pieces are next to this piece owned 
	by the splayer. If yes, maybe there is a possible move the player
	can do and getMoveRecursively is called
	"""
	moves = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (line+i < 8 and column+j < 8) and board[line+i][column+j] == player2:
				move = getMoveRecursively(board, line+i+i, column+j+j, i, j, 1-player2)
				if move != None:
					moves.append(move)

	return moves

def getMoveRecursively(board, line, column, i, j, player):
	"""
	Returns the square where the player can put their piece if there is any
	i, j indicate the x and y directions towards which the research continues
	"""
	if (line >= 8 or column >= 8):
		return None

	elif board[line][column] == 2:
		return (line, column)

	elif board[line][column] == player:
		return None
	
	else:
		return getMoveRecursively(board, line+i, column+j, i, j, player)


def placePiece(board, line, column, player):
	"""
	Places the piece and calls flipRecursiverly to reverse the opponent piece
	trails that are to be reversed
	"""
	board[line][column]= player
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (line+i < 8 and column+j < 8):
				if board[line+i][column+j] == 1- player:
					flipRecursively(board, line+i, column+j, i, j, player)


def flipRecursively(board, line, column, i, j, player):
	"""
	Flips the colors in the trail if a player piece is found at the end of it
	i, j indicate the x and y directions towards which we go
	"""
	if (line >= 8 or column >= 8):
		return False

	elif board[line][column] == 2:
		return False

	elif board[line][column] == player:
		return True
	
	else:
		toFlip = flipRecursively(board, line+i, column+j, i, j, player)
		if toFlip == True:
			board[line][column] = player
		return toFlip


def countScores():
	player1 = 0
	player2 = 0
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				player1 += 1
			elif board[i][j] == 1:
				player2 += 1

	return player1, player2

def findWinner():
	p1, p2 = countScores()
	if p1 > p2:
		return 0
	if p1 == p2:
		return 2
	else:
		return 1

def displayWinner():
	pygame.draw.rect(DISPLAYSURF, WHITE, (SCORE_BOX_1_X, 200, 150, 50))
	font = pygame.font.SysFont('Arial', 25)
	text = ""
	winner = findWinner()
	if (winner == 0):
		text = "Black wins!"
	if (winner == 1):
		text = "White wins!"

	DISPLAYSURF.blit(font.render(text, True, (0,0,0)), (SCORE_BOX_1_X+2, 203))

if __name__ == '__main__':
    main()
