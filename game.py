#History Mansion - A history slider game
#game.py edited and adapted by Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame, sys, random, os, pygame.mixer, startScreen, submitScore, main
from context import *
from pygame.locals import *
 
class game():
    
    def __init__(self):  
        #Set constants (These will change dependent on different levels)
        self.BOARDWIDTH = 4 #Number of columns on the board
        self.BOARDHEIGHT = 4#Number of rows on the board
        self.TILESIZE = 80
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700
        self.BLANK = None
    
        #Set In Game colors and assets and fonts
        self.BGCOLOR = Color(0,0,0,0)
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = Color(180,120,40)
        
        self.BUTTONTEXTCOLOR = Color(255,255,255)
        self.MESSAGEBOX = Color(0,0,0,0)
        self.MESSAGECOLOR = Color(255,255,255)
            
        #Score Calculations and Move Count
        self.moves = 0
        self.topScore = self.BOARDWIDTH * self.BOARDHEIGHT * 100 
        self.score = 0  
        
        #Setting a margin inside the board
        self.XMARGIN = int((self.WINDOWWIDTH - (self.TILESIZE * self.BOARDWIDTH + (self.BOARDWIDTH - 1))) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (self.TILESIZE * self.BOARDHEIGHT + (self.BOARDHEIGHT - 1))) / 2)
        
        #Directions
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        
        self.BASICFONT = pygame.font.SysFont("monospace", 30, bold=True, italic = True)
        self.factFONT = pygame.font.SysFont("monospace", 25, bold=True, italic = True)
            
        #Option buttons
        self.NEW_SURF, self.NEW_RECT = self.makeText('New Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 10)
        self.RESET_SURF, self.RESET_RECT = self.makeText('Reset Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 40)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Main Menu', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 200, 70)
  
        #Character select
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        self.RANDCHAR = "cleo" #random.choice(self.CHAR) 
        
        self.randomNumber = random.randrange(100,150)
        
        #Load Sounds
        self.TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
        self.win = pygame.mixer.Sound("Assets/Audio/win.wav")
        self.lose = pygame.mixer.Sound("Assets/Audio/lose.wav")
        self.screen = pygame.display.get_surface() 
        
        self.mainBoard = None

        #For scoreboard
        self.__playerName = ""
        
        
    #-------Initialise board------#
    def make_new_puzzle(self):
        self.mainBoard, self.solutionSeq = self.generateNewPuzzle(80)
        self.SOLVEDBOARD = self.getStartingBoard() #same as starting board
        self.allMoves = [] #empty list to store all moves

    #/-----Event loop function-----\#
    def update(self, dt): 
        if self.mainBoard is None:
            self.make_new_puzzle()
            
        self.slideTo = None
        self.msg = 'Click tile or use arrows to slide.'
        self.msg2 = 'Solve the puzzle to release the facts!' #message to display in message box
        if self.mainBoard == self.SOLVEDBOARD:
            self.msg = 'Solved!'
            self.msg2 = "Click 'New Game' to submit your score and start a new game" 
                       
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.spotx, self.spoty = self.getSpotClicked(self.mainBoard, event.pos[0], event.pos[1])
                
                if (self.spotx, self.spoty) == (None, None):
                    #check if the user clicked on an option button?
                    if self.NEW_RECT.collidepoint(event.pos): #user clicked New button
                        if self.msg == 'Solved!':
                            push(submitScore.submitScore(self.score))
                            
                            #Random character selection
                        else:
                            self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
                            self.RANDCHAR = random.choice(self.CHAR)
                            self.moves = 0 
                            self.randomNumber = random.randrange(100,150)
                            self.make_new_puzzle()
                    elif self.RESET_RECT.collidepoint(event.pos):#user clicked Reset button
                        self.resetAnimation(self.mainBoard, self.allMoves) # clicked on Solve button
                        self.allMoves = []
                        self.moves = 0
                    elif self.EXIT_RECT.collidepoint(event.pos):
                        if top() is self:
                            pop()
                    if self.moves >= self.randomNumber:
                        if self.SOLVE_RECT.collidepoint(event.pos):#user clicked Reset button
                            self.resetAnimation(self.mainBoard, self.solutionSeq + self.allMoves) # clicked on Solve button
                            self.allMoves = []
                            self.moves = 0                    

                else:
                    #Check if the tile next to blank spot
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
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
                elif event.key in (K_LEFT, K_a) and self.isValidMove(self.mainBoard, self.LEFT):
                    self.slideTo = self.LEFT
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_RIGHT, K_d) and self.isValidMove(self.mainBoard, self.RIGHT):
                    self.slideTo = self.RIGHT
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_UP, K_w) and self.isValidMove(self.mainBoard, self.UP):
                    self.slideTo = self.UP
                    self.TILESOUND.play()
                    self.moves += 1
                elif event.key in (K_DOWN, K_s) and self.isValidMove(self.mainBoard, self.DOWN):
                    self.slideTo = self.DOWN
                    self.TILESOUND.play()
                    self.moves += 1
            elif event.type == QUIT:
                sys.exit()
    
        if self.slideTo:
            self.slideAnimation(self.mainBoard, self.slideTo, 'Click tile or use arrows to slide.', 'Solve the puzzle to release the facts!',  8) #show slide on screen
            self.makeMove(self.mainBoard, self.slideTo)
            self.allMoves.append(self.slideTo) #records the slide
    
    #/-----Draw to screen-----\#                
    def draw(self, dt):
        screen = pygame.display.get_surface() 
        self.drawBoard(self.mainBoard, self.msg, self.msg2)
        pygame.display.flip()
        
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)
            
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
        self.blankx, self.blanky = self.getBlankPosition(board)
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
        pygame.draw.rect(self.screen, self.BUTTONTEXTCOLOR, (self.left + adjx, self.top + adjy, self.TILESIZE, self.TILESIZE))
        self.TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + self.RANDCHAR + "/l1/" + self.RANDCHAR + "_" + str(number - 1) + ".jpg"))
        self.TILERECT = self.TILEIMAGE.get_rect()
        self.TILERECT.center = self.left + int(self.TILESIZE / 2) + adjx, self.top + int(self.TILESIZE / 2) + adjy
        self.screen.blit(self.TILEIMAGE, self.TILERECT)
        
    def makeText(self, text, color, top, left):
        #create the button objects
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft = (top, left)
        return (self.textSurf, self.textRect)
 
    def funFact(self, RANDCHAR):  
        pygame.draw.rect(self.screen, self.BORDERCOLOR, (20, 440, 1060, 250), 4)
        
        factList =  { "cleo" : ("Cleopatra" ,
                        "1: Ruled Egypt from 51 BC - 30 BC", 
                        "2: Was daughter of Pharaoh Ptolemy XII Auletes", 
                        "3: Her father was King Ptolemy XII", 
                        "4: Died in after her son commit suicide in 30 BC" ),
                    
                    "geng" : ("Ghengis Khan",
                        "1: Was thought to be born in 1162 AD and died on 18th August 1227",
                        "2: Conquered nearly 12 million square miles of territory",
                        "3: Was originally named Temujin, which means 'of iron' or 'blacksmith'",
                        "4: Killed as many as 40 million people" ), 
                   
                    "ghandi" : ("Ghandi",           
                        "1: Was born on October 2 1869 in Porbandar, India",
                        "2: Fought for the independence of India",
                        "3: Went to Law School in London",
                        "4: Was killed on January 30, 1948" ),
                    
                    "henry" : ("Henry VIII",
                        "1: Was born in 1491 (Tudor Age)",
                        "2: Had six wives and was the King of England",
                        "3: People who made him cross risked having their heads chopped off!",
                        "4: Died in 1547" ),
                    
                    "queen" : ("Queen Victoria", 
                        "1: Was born in 1819",
                        "2: Became Queen in 1837 when she was 18",
                        "3: Had a long period of history is named after her - the Victorian Age",
                        "4: Lived to see the start of the 20th century, dying in January 1901." ),
                    
                    "flo" : ("Florence Knightingale",
                        "1: Was born in 1820, prior to the steam railway",
                        "2: She was the founder of modern nursing",
                        "3: Showed that trained nurses and clean hospitals helped sick people get better",
                        "4: Died in 1910, after the age of electricity, cars and planes began"),
        }
        
        marginleft = 30
        yAxis = 530 
        
        self.factTitle = self.BASICFONT.render('Did you know?...', 1, self.MESSAGECOLOR)
        self.screen.blit(self.factTitle, (marginleft, 460))
        
        self.charName = self.BASICFONT.render(factList[RANDCHAR][0], 1, self.MESSAGECOLOR)
        self.screen.blit(self.charName, (marginleft, 495))
          
        for x in range(4):
            x += 1
            self.factx = self.factFONT.render(factList[RANDCHAR][x],  1, self.MESSAGECOLOR)
            self.screen.blit(self.factx, (marginleft, yAxis))
            yAxis += 35
            
    def drawBoard(self, board, message, message2): 
        self.screen.blit(self.BGIMAGE, (0,0))

        if message:
            self.background = self.screen
            self.text = self.BASICFONT.render(message, 1, self.MESSAGECOLOR)
            self.textpos = self.text.get_rect()
            self.textpos.center = (self.WINDOWWIDTH/2, self.WINDOWHEIGHT/2 + 30)
            self.screen.blit(self.text, self.textpos)
            
        if message2:
            self.background = self.screen
            self.text2 = self.BASICFONT.render(message2, 1, self.MESSAGECOLOR)
            self.textpos = self.text2.get_rect()
            self.textpos.center = (self.WINDOWWIDTH/2, self.WINDOWHEIGHT/2 + 55)
            self.screen.blit(self.text2, self.textpos)
            
        self.score = self.topScore - (self.moves * 10)
        
        self.movesCount = self.BASICFONT.render("Score: " + str(self.score), 1, self.MESSAGECOLOR)
        self.screen.blit(self.movesCount, (10,10))
        
        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:     
                    self.drawTile(tilex, tiley-2, board[tilex][tiley])
                   
        self.left, self.top = self.getLeftTopOfTile(0, -2)
        self.width = self.BOARDWIDTH * self.TILESIZE
        self.height = self.BOARDHEIGHT * self.TILESIZE
        pygame.draw.rect(self.screen, self.BORDERCOLOR, (self.left - 8, self.top - 8, self.width + 20, self.height + 20), 11)
        
        self.screen.blit(self.RESET_SURF, self.RESET_RECT)
        self.screen.blit(self.NEW_SURF, self.NEW_RECT)
        self.screen.blit(self.EXIT_SURF, self.EXIT_RECT)
        self.soundCheck(message)
                  
        if self.moves >= self.randomNumber:
            self.SOLVE_SURF, self.SOLVE_RECT = self.makeText('Solve Game', self.BUTTONTEXTCOLOR, 20, 100)
            self.screen.blit(self.SOLVE_SURF, self.SOLVE_RECT)
        
        if message == 'Solved!':
            self.funFact(self.RANDCHAR)
        
    def slideAnimation(self, board, direction, message, message2, animationSpeed):
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

        self.drawBoard(board, message, message2)
        self.baseSurf = self.screen.copy()
        #Blank space over moving tile
        self.moveLeft, self.moveTop = self.getLeftTopOfTile(self.movex, self.movey-2)
        pygame.draw.rect(self.baseSurf, self.BGCOLOR, (self.moveLeft, self.moveTop, self.TILESIZE, self.TILESIZE)) 

        for i in range(0, self.TILESIZE, animationSpeed):
            #Animate the tile sliding over
            self.screen.blit(self.baseSurf, (0, 0))
            if direction == self.UP:
                self.drawTile(self.movex, self.movey - 2, board[self.movex][self.movey], 0, -i)
            if direction == self.DOWN:
                self.drawTile(self.movex, self.movey - 2, board[self.movex][self.movey], 0, i)
            if direction == self.LEFT:
                self.drawTile(self.movex, self.movey - 2, board[self.movex][self.movey], -i, 0)
            if direction == self.RIGHT:
                self.drawTile(self.movex, self.movey - 2, board[self.movex][self.movey], i, 0)
        
            pygame.display.update()
            self.FPSCLOCK = pygame.time.Clock()
            self.FPSCLOCK.tick(60)
    
    def generateNewPuzzle(self, numSlides):        
        #numSlides is the number of moves and this function will animate these moves
        self.sequence = []
        self.board = self.getStartingBoard()
        self.drawBoard(self.board, '', '')
        pygame.time.wait(500) #Pause for 500 milliseconds for effect
        self.lastMove = None
        for i in range(numSlides):
            self.move = self.getRandomMove(self.board, self.lastMove)
            self.slideAnimation(self.board, self.move, 'Generating new puzzle...', '',  animationSpeed=int(self.TILESIZE / 2))
            self.makeMove(self.board, self.move)
            self.sequence.append(self.move)
            self.lastMove = self.move
        return (self.board, self.sequence)
    
    def resetAnimation(self, board, allMoves):
        #reverse allMoves
        self.revAllMoves = allMoves[:]
        self.revAllMoves.reverse()
        for move in self.revAllMoves:
            if move == self.UP:
                self.oppositeMove = self.DOWN
            elif move == self.DOWN:
                self.oppositeMove = self.UP
            elif move == self.LEFT:
                self.oppositeMove = self.RIGHT
            elif move == self.RIGHT:
                self.oppositeMove = self.LEFT
                
            self.slideAnimation(board, self.oppositeMove, '', '',animationSpeed=int(self.TILESIZE / 2 ))
            self.makeMove(board, self.oppositeMove)
            
    def soundCheck(self, message):
        if message == "Solved!":
            self.win.play(0)
        if self.score == 0:
            self.lose.play(0)