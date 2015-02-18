#History Mansion - A history slider game
#Edited and adapted By Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame, sys, random, os, pygame.mixer
from pygame.locals import *


class game(): 
   
    def __init__(self):
        #Set constants (These will change dependent on different levels)
        self.BOARDWIDTH = (4) #Number of columns on the board
        self.BOARDHEIGHT = (4)#Number of rows on the board
        self.TILESIZE = (160 / 2)
        self.WINDOWWIDTH = 900
        self.WINDOWHEIGHT = (1092/2)
        self.FPS = 40
        self.BLANK = None
            
        #Set In Game colors and assets and fonts
        self.BGCOLOR = Color(0,0,0,0)
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = Color(180,120,40)
        self.BASICFONTSIZE = 27 
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        
        self.BUTTONTEXTCOLOR = Color(255,255,255)
        self.MESSAGEBOX = Color(0,0,0,0)
        self.MESSAGECOLOR = Color(255,255,255)
    
       #Option buttons
        self.RESET_SURF, self.RESET_RECT = self.makeText('Reset Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 40)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Exit', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 70)
            
        #Character select
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        self.RANDCHAR = random.choice(self.CHAR) 
             
        #Load Sounds
        self.TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
        self.WINSOUND = pygame.mixer.Sound("Assets/Audio/win.wav")
        
        #Move Count
        self.moves = 0
        
        #Setting a margin inside the board
        self.XMARGIN = int((self.WINDOWWIDTH - (self.TILESIZE * self.BOARDWIDTH + (self.BOARDWIDTH - 1))) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (self.TILESIZE * self.BOARDHEIGHT + (self.BOARDHEIGHT - 1))) / 2)
        
        #Directions
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
    
    #-------Initialise board------#
    
    def update (self, dt):                
        self.mainBoard, self.solutionSeq = self.generateNewPuzzle(80)
        self.SOLVEDBOARD = self.getStartingBoard() #same as starting board
        self.allMoves = [] #empty list to store all moves
        
        self.slideTo = None
        self.msg = 'Click tile or use arrows to slide.' #message to display in message box
        
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'
            #popup box
              
        self.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    #check if the user clicked on an option button?
                    if NEW_RECT.collidepoint(event.pos): #user clicked New button
                        #Character select
                        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
                        self.RANDCHAR = random.choice(CHAR)
                        #addScore()
                        self.moves = 0 
                        update()
                    elif RESET_RECT.collidepoint(event.pos):
                        self.resetAnimation(self.mainBoard, self.allMoves) # clicked on Solve button
                        self.allMoves = []
                        self.moves = 0
                    elif EXIT_RECT.collidepoint(event.pos):
                        #addScore()
                        self.terminate()
                else:
                    #Was the tile next to blank spot
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        self.slideTo = self.LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        self.slideTo = self.RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        self.slideTo = self.UP
                    elif spotx == blankx and spoty == blanky - 1:
                        self.slideTo = self.DOWN
            
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
            
            self.drawBoard(mainBoard, msg, moves)
            #self.pygame.display.update()
            #self.FPSCLOCK.tick(FPS)
    
    #-------In game functions--------#
    def think(self, dt):
        self.update(dt)
        self.drawBoard(board, message, moves, dt)
    
    def terminate(self):
        pygame.quit()
        sys.exit()
    
    def checkForQuit(self):
        for event in pygame.event.get(QUIT): #get all the QUIT events
            terminate()
        for event in pygame.event.get(KEYUP): #get all the KEYUP events
            if event.key == K_ESCAPE:
                terminate() #if ESC key pressed
            pygame.event.post(event) #put all KEYUP event objects back
            
    def getStartingBoard(self):
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
    
    def getBlankPosition(self, board):
        #Return the x and y of board coordinates of the blank space.
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[x][y] == BLANK:
                    return(x, y)
                
    def makeMove(self, board, move):
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
            
    def isValidMove(self, board, move):
        blankx, blanky = getBlankPosition(board)
        return (move == UP and blanky != len(board[0]) -1) or \
               (move == DOWN and blanky != 0) or \
               (move == LEFT and blankx != len(board[0]) -1) or \
               (move == RIGHT and blankx != 0)
               
    def getRandomMove(self, board, lastMove=None):
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
    
    def getLeftTopOfTile(self, tileX, tileY):
        left = XMARGIN + (tileX * TILESIZE) + (tileX -1)
        top = YMARGIN + (tileY * TILESIZE) + (tileY -1)
        return (left, top)
    
    def getSpotClicked(self, board, x ,y):
        #From the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                left, top = getLeftTopOfTile(tileX, tileY)
                tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)
    
    def drawTile(self, tilex, tiley, number, adjx=0, adjy=0):
        #draw a tile at board coordinates tileX and tileY, optionally a few
        #pixels over determined by adjx and adjY
        left, top = getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(DISPLAYSURF, BUTTONTEXTCOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + RANDCHAR + "/l1/" + RANDCHAR + "_" + str(number-1) + ".jpg"))
        TILERECT = TILEIMAGE.get_rect()
        TILERECT.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(TILEIMAGE, TILERECT)
        
    def makeText(self, text, color, top, left):
        #create the button objects
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft = (top, left)
        return (self.textSurf, self.textRect)
    
    def drawBoard(self, board, message, moves, dt):    
        self.DISPLAYSURF.blit(self.BGIMAGE, [0,0])    
    
        if message:
            self.background = pygame.Surface(DISPLAYSURF.get_size())
            self.text = self.BASICFONT.render(message, 1, MESSAGECOLOR)
            self.textpos = self.text.get_rect()
            self.textpos.midbottom = self.background.get_rect().midbottom
            self.DISPLAYSURF.blit(self.text, self.textpos)
        
        if moves >= 0:
            self.movesCount = self.BASICFONT.render("Moves taken: " + str(moves), 1, MESSAGECOLOR)
            self.DISPLAYSURF.blit(movesCount, (10,10))
        
        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:     
                    self.drawTile(self.tilex, self.tiley-1, self.board[self.tilex][self.tiley])
                   
        self.left, self.top = self.getLeftTopOfTile(0, -1)
        self.width = BOARDWIDTH * TILESIZE
        self.height = BOARDHEIGHT * TILESIZE
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 3, top - 3, width + 9, height + 9), 2)
            
        DISPLAYSURF.blit(self.RESET_SURF, self.RESET_RECT)
        DISPLAYSURF.blit(self.NEW_SURF, self.NEW_RECT)
        DISPLAYSURF.blit(self.EXIT_SURF, self.EXIT_RECT)
            
    def slideAnimation(self, board, direction, message, animationSpeed):
        #This does not check if valid move....
        
        self.blankx, self.blanky = self.getBlankPosition(board)
        if self.direction == UP:
            self.movex = self.blankx
            self.movey = self.blanky + 1
        elif self.direction == DOWN:
            self.movex = self.blankx
            self.movey = self.blanky - 1
        elif self.direction == LEFT:
            self.movex = self.blankx + 1
            self.movey = self.blanky
        elif self.direction == RIGHT:
           self.movex = blankx - 1
           self.movey = blanky
        
        #Prepare surface
        self.drawBoard(self.board, self.message, self.moves)
        self.baseSurf = self.DISPLAYSURF.copy()
        
        #Blank space over moving tile
        self.moveLeft, self.moveTop = self.getLeftTopOfTile(self.movex, self.movey-1)
        pygame.draw.rect(self.baseSurf, self.BGCOLOR, (self.moveLeft, self.moveTop, self.TILESIZE, self.TILESIZE))
    
        for i in range(0, TILESIZE, animationSpeed):
            #Animate the tile sliding over
            self.checkForQuit()
            self.DISPLAYSURF.blit(self.baseSurf, (0,0))
            if self.direction == UP:
                self.drawTile(self.movex, self.movey - 1, self.board[self.movex][self.movey], 0, -i)
            if self.direction == DOWN:
                self.drawTile(self.movex, self.movey - 1, self.board[self.movex][self.movey], 0, i)
            if self.direction == LEFT:
                self.drawTile(self.movex, self.movey - 1, self.board[self.movex][self.movey], -i, 0)
            if self.direction == RIGHT:
                self.drawTile(self.movex, self.movey - 1, self.board[self.movex][self.movey], i, 0)
            
            #pygame.display.update()
            #FPSCLOCK.tick(FPS)
    
    def generateNewPuzzle(self, numSlides):        
        #numSlides is the number of moves and this function will animate these moves
        self.sequence = []
        self.board = getStartingBoard()
        self.drawBoard(board, '', None)
        pygame.display.update()
        pygame.time.wait(500) #Pause for 500 milliseconds for effect
        self.lastMove = None
        for i in range(numSlides):
            self.move = getRandomMove(board, lastMove)
            self.slideAnimation(self.board, self.move, 'Generating new puzzle...', animationSpeed=int(self.TILESIZE / 2))
            self.makeMove(self.board, self.move)
            self.sequence.append(self.move)
            self.lastMove = self.move
        return (self.board, self.sequence)
    
    def resetAnimation(self, board, allMoves):
        #reverse allMoves
        self.revAllMoves = self.allMoves[:]
        self.revAllMoves.reverse()
        for move in revAllMoves:
            if self.move == self.UP:
                self.oppositeMove = self.DOWN
            elif self.move == self.DOWN:
                self.oppositeMove = self.UP
            elif self.move == self.LEFT:
                self.oppositeMove = self.RIGHT
            elif self.move == self.RIGHT:
                self.oppositeMove = self.LEFT
                
            self.slideAnimation(self.board, self.oppositeMove, '', animationSpeed=int(self.TILESIZE / 2 ))
            self.makeMove(self.board, self.oppositeMove)