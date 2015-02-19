#History Mansion - A history slider game
#Edited and adapted By Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame, sys, random, os, pygame.mixer, startScreen, main
from context import *
from pygame.locals import *
 
class game():
    
    def __init__(self):  
        #Set constants (These will change dependent on different levels)
        self.BOARDWIDTH = 4 #Number of columns on the board
        self.BOARDHEIGHT = 4#Number of rows on the board
        self.TILESIZE = 160 / 2
        self.WINDOWWIDTH = 900
        self.WINDOWHEIGHT = 1092/2
        #self.FPS = 40
        self.BLANK = None
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
    
        #Set In Game colors and assets and fonts
        self.BGCOLOR = Color(0,0,0,0)
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = Color(180,120,40)
        self.BASICFONTSIZE = 27 
        
        self.BUTTONTEXTCOLOR = Color(255,255,255)
        self.MESSAGEBOX = Color(0,0,0,0)
        self.MESSAGECOLOR = Color(255,255,255)
            
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
        
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
                    
        #Option buttons
        self.NEW_SURF, self.NEW_RECT = self.makeText('New Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 10)
        self.RESET_SURF, self.RESET_RECT = self.makeText('Reset Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 40)
        self.SOLVE_SURF, self.SOLVE_RECT = self.makeText('Solve Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 60)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Exit', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 70)
                  
        #Character select
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        self.RANDCHAR = random.choice(self.CHAR) 
         
        #Load Sounds
        self.TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
        self.WINSOUND = pygame.mixer.Sound("Assets/Audio/win.wav")  
    
    #-------Initialise board------#
    def update(self, dt): 
        #pygame.init()
        #FPSCLOCK = pygame.time.Clock()
        #pygame.display.set_caption('History Mansion')

        self.mainBoard, self.solutionSeq = self.generateNewPuzzle(80)
        self.SOLVEDBOARD = self.getStartingBoard() #same as starting board
        self.allMoves = [] #empty list to store all moves
        
        #while True: #main game loop
        self.slideTo = None
        self.msg = 'Click tile or use arrows to slide.' #message to display in message box
        if self.mainBoard == self.SOLVEDBOARD:
            self.msg = 'Solved!'
            #popup box
    
        self.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.spotx, self.spoty = self.getSpotClicked(self.mainBoard, event.pos[0], event.pos[1])
                
                if (self.spotx, self.spoty) == (None, None):
                    #check if the user clicked on an option button?
                    if self.NEW_RECT.collidepoint(event.pos): #user clicked New button
                        #Character select
                        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
                        self.RANDCHAR = random.choice(self.CHAR)
                        #addScore()
                        self.moves = 0 
                        self.update()
                    elif self.RESET_RECT.collidepoint(event.pos):
                        self.resetAnimation(self.mainBoard, self.allMoves) # clicked on Solve button
                        self.allMoves = []
                        self.moves = 0
                    elif self.EXIT_RECT.collidepoint(event.pos):
                        #addScore()
                        startScreen.startScreen()
                else:
                    #Was the tile next to blank spot
                    self.blankx, self.blanky = self.getBlankPosition(self.mainBoard)
                    if self.spotx == self.blankx + 1 and self.spoty == self.blanky:
                        self.slideTo = self.LEFT
                    elif self.spotx == self.blankx - 1 and self.spoty == self.blanky:
                        self.slideTo = self.RIGHT
                    elif self.spotx == self.blankx and self.spoty == self.blanky + 1:
                        self.slideTo = self.UP
                    elif self.spotx == self.blankx and self.spoty == self.blanky - 1:
                        self.slideTo = self.DOWN
            
            elif event.type == KEYUP:
                #check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and self.isValidMove(self.mainBoard, self.LEFT):
                    self.slideTo = self.LEFT
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_RIGHT, K_d) and self.isValidMove(self.mainBoard, self.RIGHT):
                    self.slideTo = self.RIGHT
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_UP, K_w) and self.isValidMove(self.mainBoard, self.UP):
                    self.slideTo = UP
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_DOWN, K_s) and self.isValidMove(self.mainBoard, self.DOWN):
                    self.slideTo = self.DOWN
                    self.TILESOUND.play()
                    self.moves += 1
            
        if self.slideTo:
            self.slideAnimation(self.mainBoard, self.slideTo, 'Click tile or use arrows to slide.', 8) #show slide on screen
            self.makeMove(self.mainBoard, self.slideTo)
            self.allMoves.append(self.slideTo) #records the slide
            
        #pygame.display.update()
        #FPSCLOCK.tick(FPS)
            
    #-------In game functions--------#
    
    def draw(self, dt):
        self.drawBoard(self.board, "", self.moves) 
    
    def think(self, dt):
        self.update(dt)
        self.draw(dt)
    
    def terminate(self):
        pygame.quit()
        sys.exit()
    
    def checkForQuit(self):
        for event in pygame.event.get(QUIT): #get all the QUIT events
            self.terminate()
        for event in pygame.event.get(KEYUP): #get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() #if ESC key pressed
            pygame.event.post(event) #put all KEYUP event objects back
            
    def getStartingBoard(self):
        #Return the board structure with tiles in order
        #eg if BOARDWIDTH and BOARDHEIGHT are both 3
        #returns [1, 4, 7] [2, 5, 8] [3, 6, BLANK]
        self.counter = 1
        self.board = []
        for x in range(self.BOARDWIDTH):
            self.column = []
            for y in range(self.BOARDHEIGHT):
                self.column.append(self.counter)
                self.counter += self.BOARDWIDTH
            self.board.append(self.column)
            self.counter -= self.BOARDWIDTH * (self.BOARDHEIGHT - 1) + self.BOARDWIDTH - 1 #what does this mean?
            
        self.board[self.BOARDWIDTH-1][self.BOARDHEIGHT-1] = self.BLANK
        return self.board

    def getBlankPosition(self, board):
        #Return the x and y of board coordinates of the blank space.
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                if board[x][y] == self.BLANK:
                    return(x, y)
                
    def makeMove(self, board, move):
        #This function does not check if the move is valid
        self.blankx, self.blanky = self.getBlankPosition(self.board)
        if move == self.UP:
            board[self.blankx][self.blanky], board[self.blankx][self.blanky + 1] = board[self.blankx][self.blanky + 1], board[self.blankx][self.blanky]
        elif move == self.DOWN:
            board[self.blankx][self.blanky], board[self.blankx][self.blanky - 1] = board[self.blankx][self.blanky - 1], board[self.blankx][self.blanky] 
        elif move == self.LEFT:
            board[self.blankx][self.blanky], board[self.blankx + 1][self.blanky] = board[self.blankx + 1][self.blanky], board[self.blankx][self.blanky]
        elif move == self.RIGHT:
            board[self.blankx][self.blanky], board[self.blankx - 1][self.blanky] = board[self.blankx - 1][self.blanky], board[self.blankx][self.blanky]
            
    def isValidMove(self, board, move):
        self.blankx, self.blanky = self.getBlankPosition(board)
        return (move == self.UP and self.blanky != len(board[0]) -1) or \
               (move == self.DOWN and self.blanky != 0) or \
               (move == self.LEFT and self.blankx != len(board[0]) -1) or \
               (move == self.RIGHT and self.blankx != 0)
               
    def getRandomMove(self, board, lastMove=None):
        #start with a list of all valid moves
        self.validMoves = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
    
        #remove moves from the list as they are disqualified
        if lastMove == self.UP or not self.isValidMove(board, self.DOWN):
            self.validMoves.remove(self.DOWN)
        if lastMove == self.DOWN or not self.isValidMove(board, self.UP):
            self.validMoves.remove(self.UP) 
        if lastMove == self.LEFT or not self.isValidMove(board, self.RIGHT):
            self.validMoves.remove(self.RIGHT)
        if lastMove == self.RIGHT or not self.isValidMove(board, self.LEFT):
            self.validMoves.remove(self.LEFT)
            
        #return a random move from remaining list
        return random.choice(self.validMoves)
    
    def getLeftTopOfTile(self, tileX, tileY):
        self.left = self.XMARGIN + (tileX * self.TILESIZE) + (tileX -1)
        self.top = self.YMARGIN + (tileY * self.TILESIZE) + (tileY -1)
        return (self.left, self.top)
    
    def getSpotClicked(self, board, x ,y):
        #From the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                self.left, self.top = self.getLeftTopOfTile(tileX, tileY)
                self.tileRect = pygame.Rect(self.left, self.top, self.TILESIZE, self.TILESIZE)
                if self.tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)
    
    def drawTile(self, tilex, tiley, number, adjx=0, adjy=0):
        #draw a tile at board coordinates tileX and tileY, optionally a few
        #pixels over determined by adjx and adjY
        self.left, self.top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(self.DISPLAYSURF, self.BUTTONTEXTCOLOR, (self.left + adjx, self.top + adjy, self.TILESIZE, self.TILESIZE))
        self.TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + self.RANDCHAR + "/l1/" + self.RANDCHAR + "_" + str(number - 1) + ".jpg"))
        self.TILERECT = self.TILEIMAGE.get_rect()
        self.TILERECT.center = self.left + int(self.TILESIZE / 2) + adjx, self.top + int(self.TILESIZE / 2) + adjy
        self.DISPLAYSURF.blit(self.TILEIMAGE, self.TILERECT)
        
    def makeText(self, text, color, top, left):
        #create the button objects
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft = (top, left)
        return (self.textSurf, self.textRect)
    
    #def funFact():
    #    self.backgroundFact = pygame.draw.rect(self.DISPLAYSURF, self.BORDERCOLOR,  )
    #    self.text1 = maketext()
    
    def drawBoard(self, board, message, moves):    
        self.DISPLAYSURF.blit(self.BGIMAGE, [0,0])    
    
        if message:
            self.background = pygame.Surface(self.DISPLAYSURF.get_size())
            self.text = self.BASICFONT.render(message, 1, self.MESSAGECOLOR)
            self.textpos = self.text.get_rect()
            self.textpos.midbottom = self.background.get_rect().midbottom
            self.DISPLAYSURF.blit(self.text, self.textpos)
        
        if moves >= 0:
            self.movesCount = self.BASICFONT.render("Moves taken: " + str(moves), 1, self.MESSAGECOLOR)
            self.DISPLAYSURF.blit(self.movesCount, (10,10))
        
        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:     
                    self.drawTile(tilex, tiley-1, self.board[tilex][tiley])
                   
        self.left, self.top = self.getLeftTopOfTile(0, -1)
        self.width = self.BOARDWIDTH * self.TILESIZE
        self.height = self.BOARDHEIGHT * self.TILESIZE
        pygame.draw.rect(self.DISPLAYSURF, self.BORDERCOLOR, (self.left - 3, self.top - 3, self.width + 9, self.height + 9), 2)
        
        #funFact()
        self.DISPLAYSURF.blit(self.RESET_SURF, self.RESET_RECT)
        self.DISPLAYSURF.blit(self.NEW_SURF, self.NEW_RECT)
        self.DISPLAYSURF.blit(self.EXIT_SURF, self.EXIT_RECT)
            
    def slideAnimation(self, board, direction, message, animationSpeed):
        #This does not check if valid move....
        
        self.blankx, self.blanky = self.getBlankPosition(board)
        if direction == self.UP:
            self.movex = self.blankx
            self.movey = self.blanky + 1
        elif direction == self.DOWN:
            self.movex = self.blankx
            self.movey = self.blanky - 1
        elif direction == self.LEFT:
            self.movex = self.blankx + 1
            self.movey = self.blanky
        elif direction == self.RIGHT:
           self.movex = self.blankx - 1
           self.movey = self.blanky
        
        #Prepare surface
        self.drawBoard(board, message, self.moves)
        #self.baseSurf = self.DISPLAYSURF.copy()
        
        #Blank space over moving tile
        self.moveLeft, self.moveTop = self.getLeftTopOfTile(self.movex, self.movey-1)
        pygame.draw.rect(self.DISPLAYSURF, self.BGCOLOR, (self.moveLeft, self.moveTop, self.TILESIZE, self.TILESIZE))
    
        for i in range(0, self.TILESIZE, animationSpeed):
            #Animate the tile sliding over
            self.checkForQuit()
            self.DISPLAYSURF.blit(self.DISPLAYSURF, (0,0))
            if direction == self.UP:
                self.drawTile(self.movex, self.movey - 1, board[self.movex][self.movey], 0, -i)
            if direction == self.DOWN:
                self.drawTile(self.movex, self.movey - 1, board[self.movex][self.movey], 0, i)
            if direction == self.LEFT:
                self.drawTile(self.movex, self.movey - 1, board[self.movex][self.movey], -i, 0)
            if direction == self.RIGHT:
                self.drawTile(self.movex, self.movey - 1, board[self.movex][self.movey], i, 0)
            
        pygame.display.update()
        #self.FPSCLOCK.tick(FPS)
    
    def generateNewPuzzle(self, numSlides):        
        #numSlides is the number of moves and this function will animate these moves
        self.sequence = []
        self.board = self.getStartingBoard()
        #self.drawBoard(self.board, '', None, dt)
        pygame.display.update()
        pygame.time.wait(500) #Pause for 500 milliseconds for effect
        self.lastMove = None
        for i in range(numSlides):
            self.move = self.getRandomMove(self.board, self.lastMove)
            self.slideAnimation(self.board, self.move, 'Generating new puzzle...', animationSpeed=int(self.TILESIZE / 2))
            self.makeMove(self.board, self.move)
            self.sequence.append(self.move)
            self.lastMove = self.move
        return (self.board, self.sequence)
    
    def resetAnimation(self, board, allMoves):
        #reverse allMoves
        self.revAllMoves = allMoves[:]
        self.revAllMoves.reverse()
        for move in revAllMoves:
            if move == UP:
                self.oppositeMove = self.DOWN
            elif move == DOWN:
                self.oppositeMove = self.UP
            elif move == LEFT:
                self.oppositeMove = self.RIGHT
            elif move == RIGHT:
                self.oppositeMove = self.LEFT
                
            self.slideAnimation(board, self.oppositeMove, '', animationSpeed=int(self.TILESIZE / 2 ))
            self.makeMove(board, self.oppositeMove)