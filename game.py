#History Mansion - A history slider game
#Edited and adapted By Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame, sys, random, os, pygame.mixer
from pygame.locals import *

    #class game:
    #global WINDOWWIDTH, WINDOWHEIGHT
    
#Set constants (These will change dependent on different levels)
BOARDWIDTH = (4) #Number of columns on the board
BOARDHEIGHT = (4)#Number of rows on the board
TILESIZE = (160 / 2)
WINDOWWIDTH = 900
WINDOWHEIGHT = (1092/2)
FPS = 40
BLANK = None
    
#Set In Game colors and assets
BGCOLOR = Color(0,0,0,0)
BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
BORDERCOLOR = Color(180,120,40)
BASICFONTSIZE = 27 
BUTTONTEXTCOLOR = Color(255,255,255)
MESSAGEBOX = Color(0,0,0,0)
MESSAGECOLOR = Color(255,255,255)

#Init outside loop stops flickering game screen
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('History Mansion')
    
#Character select
CHAR = ('flo','geng','ghandi','henry','queen','cleo')
RANDCHAR = random.choice(CHAR) 

#Load Font
BASICFONT = pygame.font.SysFont("monospace", BASICFONTSIZE)
    
#Load Sounds
TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
WINSOUND = pygame.mixer.Sound("Assets/Audio/win.wav")

#Move Count
moves = 0

#Setting a margin inside the board
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

#Directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

"""def __init__(self):
    
    self.BOARDWIDTH = 4
    self.BOARDHEIGHT = 4
    self.TILESIZE = 80
    self.WINDOWWIDTH = 900
    self.WINDOWHEIGHT = (1092/2)
    self.FPS = 40
    self.BLANK =  None
    self.BGCOLOR = Color(0,0,0,0)
    self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
    self.BORDERCOLOR = Color(180,120,40)
    self.BASICFONTSIZE = 27
    self.BUTTONTEXTCOLOR = Color(255,255,255)
    self.MESSAGEBOX = Color(0,0,0,0)
    self.MESSAGECOLOR = Color(255,255,255)
    self.FPSCLOCK = pygame.time.Clock()
    self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
    self.RANDCHAR = random.choice(CHAR) 
    self.BASICFONT = pygame.font.SysFont("monospace", BASICFONTSIZE)
    self.TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
    self.WINSOUND = pygame.mixer.Sound("Assets/Audio/win.wav")
    self.moves = 0
    self.XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
    self.YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
    self.UP = 'up'
    self.DOWN = 'down'
    self.LEFT = 'left'
    self.RIGHT = 'right'"""

#-------Initialise board------#

def main ():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, TILESOUND, WINSOUND, NEW_SURF, NEW_RECT, RESET_SURF, RESET_RECT, SOLVE_SURF, SOLVE_RECT,  EXIT_SURF, EXIT_RECT, TIMERSURF, TIMERRECT, RANDCHAR, moves 
    
    pygame.init()
    pygame.display.set_caption('History Mansion')
    
    #Option buttons
    NEW_SURF, NEW_RECT = makeText('New Game', BUTTONTEXTCOLOR, WINDOWWIDTH - 200, 10)
    RESET_SURF, RESET_RECT = makeText('Reset Game', BUTTONTEXTCOLOR, WINDOWWIDTH - 200, 40)
    EXIT_SURF, EXIT_RECT = makeText('Exit', BUTTONTEXTCOLOR, WINDOWWIDTH - 200, 70)
    
    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() #same as starting board
    allMoves = [] #empty list to store all moves
    
    while True: #main game loop
        slideTo = None
        msg = 'Click tile or use arrows to slide.' #message to display in message box
        
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'
            #popup box
              

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    #check if the user clicked on an option button?
                    if NEW_RECT.collidepoint(event.pos): #user clicked New button
                        #Character select
                        CHAR = ('flo','geng','ghandi','henry','queen','cleo')
                        RANDCHAR = random.choice(CHAR)
                        #addScore()
                        moves = 0 
                        main()
                    elif RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Solve button
                        allMoves = []
                        moves = 0
                    elif EXIT_RECT.collidepoint(event.pos):
                        #addScore()
                        terminate()
                else:
                    #Was the tile next to blank spot
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
            
            elif event.type == KEYUP:
                #check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                    TILESOUND.play()
                    moves += 1
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                    TILESOUND.play()
                    moves += 1
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                    TILESOUND.play()
                    moves += 1
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
                    TILESOUND.play()
                    moves += 1
        
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or use arrows to slide.', 8) #show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) #records the slide
        
        drawBoard(mainBoard, msg, moves)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#-------In game functions--------#

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): #get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP): #get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() #if ESC key pressed
        pygame.event.post(event) #put all KEYUP event objects back
        
def getStartingBoard():
    #Return the board structure with tiles in order
    #eg if BOARDWIDTH and BOARDHEIGHT are both 3
    #returns [1, 4, 7] [2, 5, 8] [3, 6, BLANK]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1 #what does this mean?
        
    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board

def getBlankPosition(board):
    #Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return(x, y)
            
def makeMove(board, move):
    #This function does not check if the move is valid
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky] 
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
        
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) -1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board[0]) -1) or \
           (move == RIGHT and blankx != 0)
           
def getRandomMove(board, lastMove=None):
    #start with a list of all valid moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    #remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP) 
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
        
    #return a random move from remaining list
    return random.choice(validMoves)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX -1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY -1)
    return (left, top)

def getSpotClicked(board, x ,y):
    #From the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    #draw a tile at board coordinates tileX and tileY, optionally a few
    #pixels over determined by adjx and adjY
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, BUTTONTEXTCOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + RANDCHAR + "/l1/" + RANDCHAR + "_" + str(number-1) + ".jpg"))
    TILERECT = TILEIMAGE.get_rect()
    TILERECT.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(TILEIMAGE, TILERECT)
    
def makeText(text, color, top, left):
    #create the button objects
    textSurf = BASICFONT.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(board, message, moves):    
    DISPLAYSURF.blit(BGIMAGE, [0,0])    

    if message:
        background = pygame.Surface(DISPLAYSURF.get_size())
        text = BASICFONT.render(message, 1, MESSAGECOLOR)
        textpos = text.get_rect()
        textpos.midbottom = background.get_rect().midbottom
        DISPLAYSURF.blit(text, textpos)
    
    if moves >= 0:
        movesCount = BASICFONT.render("Moves taken: " + str(moves), 1, MESSAGECOLOR)
        DISPLAYSURF.blit(movesCount, (10,10))
    
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:     
                drawTile(tilex, tiley-1, board[tilex][tiley])
               
    left, top = getLeftTopOfTile(0, -1)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 3, top - 3, width + 9, height + 9), 2)
        
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(EXIT_SURF, EXIT_RECT)
        
def slideAnimation(board, direction, message, animationSpeed):
    #This does not check if valid move....
    
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky
    
    #Prepare surface
    drawBoard(board, message, moves)
    baseSurf = DISPLAYSURF.copy()
    
    #Blank space over moving tile
    moveLeft, moveTop = getLeftTopOfTile(movex, movey-1)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        #Animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0,0))
        if direction == UP:
            drawTile(movex, movey - 1, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey - 1, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey - 1, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey - 1, board[movex][movey], i, 0)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):
    global sequence
    
    #numSlides is the number of moves and this function will animate these moves
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '', None)
    pygame.display.update()
    pygame.time.wait(500) #Pause for 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

def resetAnimation(board, allMoves):
    #reverse allMoves
    revAllMoves = allMoves[:]
    revAllMoves.reverse()
    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == LEFT:
            oppositeMove = RIGHT
        elif move == RIGHT:
            oppositeMove = LEFT
            
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2 ))
        makeMove(board, oppositeMove)
        
def addScore():
    return None
    
def funFactRelease():
    if getStartingBoard(board[:4]) == range(4):
        msg = ""
   
        
if __name__ == '__main__':
    main()
        
        
        
        
        
        