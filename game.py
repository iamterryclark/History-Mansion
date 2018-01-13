#History Mansion - A history slider game
#game.py edited and adapted by Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import sys, random, os, pygame.mixer, submitScore
from context import *
from pygame.locals import *
 
class game():
    
    def __init__(self, TILESIZE, BOARDWIDTH, BOARDHEIGHT):  
        #Set constants (These will change dependent on different levels)
        self.BOARDWIDTH = BOARDWIDTH #Number of columns on the board
        self.BOARDHEIGHT = BOARDHEIGHT #Number of rows on the board
        self.TILESIZE = TILESIZE
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700
        self.BLANK = None
    
        #Set In Game colors and assets and fonts
        self.BGCOLOR = Color(0,0,0,0)
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = Color(180,120,40)
        
        self.BUTTONTEXTCOLOR = Color(255,255,255)
        self.MESSAGECOLOR = Color(255,255,255)
        self.MESSAGECOLOR2 = Color(240,240,20)
            
        #Score Calculations and Move Count
        self.moves = 0
        
        if self.TILESIZE == 80:
            self.topScore = self.BOARDWIDTH * self.BOARDHEIGHT * 100
            self.randomNumber = random.randrange(100,150) 
        
        elif self.TILESIZE == 64:
            self.topScore = self.BOARDWIDTH * self.BOARDHEIGHT * 100
            self.randomNumber = random.randrange(200,250)
        
        #Setting a margin inside the board
        self.XMARGIN = int((self.WINDOWWIDTH - (self.TILESIZE * self.BOARDWIDTH + (self.BOARDWIDTH - 1))) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (self.TILESIZE * self.BOARDHEIGHT + (self.BOARDHEIGHT - 1))) / 2)
                    
        #Option buttons
        self.NEW_SURF, self.NEW_RECT = self.makeText('New Game', self.BUTTONTEXTCOLOR, 30, self.WINDOWWIDTH - 200, 10)
        self.RESET_SURF, self.RESET_RECT = self.makeText('Reset Game', self.BUTTONTEXTCOLOR, 30, self.WINDOWWIDTH - 200, 40)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Main Menu', self.BUTTONTEXTCOLOR, 30, self.WINDOWWIDTH - 200, 70)
  
        #Character select
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        self.RANDCHAR = random.choice(self.CHAR) 
        
        #Load Sound
        self.TILESOUND = pygame.mixer.Sound("Assets/Audio/slide.wav")
        
        #Directions
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        
        self.mainBoard = None
        self.screen = pygame.display.get_surface()
        
        #This is to display the player name to the screen whilst they type
        self.__playerName = ""
        
        #This is for the highscore submit
        self.puzOrQuiz = "puz"
    
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
        self.msg = 'Use keyboard arrows to slide the tiles'
        self.msg2 = '^^^^^^^^Solve the puzzle to release the facts!^^^^^^^^' #message to display in message box
        if self.mainBoard == self.SOLVEDBOARD:
            self.msg = 'YOU DID IT!'
            self.msg2 = "Click New Game to save score"
                       
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.spotx, self.spoty = self.getSpotClicked(self.mainBoard, event.pos[0], event.pos[1])
                
                if (self.spotx, self.spoty) == (None, None):
                    #check if the user clicked on an option button?
                    if self.NEW_RECT.collidepoint(event.pos): #user clicked New button
                        if self.mainBoard == self.SOLVEDBOARD:
                            push(submitScore.submitScore(self.score, self.puzOrQuiz))
                            #Random character selection  
                        self.RANDCHAR = random.choice(self.CHAR)
                        self.moves = 0
                        self.make_new_puzzle()
                        
                    elif self.RESET_RECT.collidepoint(event.pos):#user clicked Reset button
                        self.resetAnimation(self.mainBoard, self.allMoves) # clicked on Solve button
                        self.allMoves = []
                        self.moves = 0
                    elif self.EXIT_RECT.collidepoint(event.pos):
                        if top() is self:
                            pop()
                            pop()
                    if self.moves >= self.randomNumber:
                        if self.SOLVE_RECT.collidepoint(event.pos):#user clicked Reset button
                            self.resetAnimation(self.mainBoard, self.solutionSeq + self.allMoves) # clicked on Solve button
                            self.allMoves = []                 

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
            self.slideAnimation(self.mainBoard, self.slideTo, 'Use keyboard arrows to slide the tiles', '^^^^^^^^Solve the puzzle to release the facts!^^^^^^^^',  8) #show slide on screen
            self.makeMove(self.mainBoard, self.slideTo)
            self.allMoves.append(self.slideTo) #records the slide
    
    #/-----Draw to screen-----\#                
    def draw(self, dt):
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
            self.counter -= self.BOARDWIDTH * (self.BOARDHEIGHT - 1) + self.BOARDWIDTH - 1
            
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
        
        if self.TILESIZE == 80:
            self.TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + self.RANDCHAR + "/l1/" + self.RANDCHAR + "_" + str(number - 1) + ".jpg"))
            self.TILERECT = self.TILEIMAGE.get_rect()
            self.TILERECT.center = self.left + int(self.TILESIZE / 2) + adjx, self.top + int(self.TILESIZE / 2) + adjy
            self.screen.blit(self.TILEIMAGE, self.TILERECT)
        
        elif self.TILESIZE == 64:
            self.TILEIMAGE = pygame.image.load(os.path.join("Assets/images/Pictures/grid/" + self.RANDCHAR + "/l2/" + self.RANDCHAR + "_" + str(number - 1) + ".jpg"))
            self.TILERECT = self.TILEIMAGE.get_rect()
            self.TILERECT.center = self.left + int(self.TILESIZE / 2) + adjx, self.top + int(self.TILESIZE / 2) + adjy
            self.screen.blit(self.TILEIMAGE, self.TILERECT)  
        
            
    def makeText(self, text, color, size, top, left):
        #create the button objects
        font = pygame.font.SysFont("monospace", size, bold=True, italic = False)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)
    
    def makeTextCenter(self, text, color, size, centerx, height):
        #create the button objects
        font = pygame.font.SysFont("monospace", size, bold=True, italic = False)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = (centerx, height)
        return (textSurf, textRect)
 
    def funFact(self, RANDCHAR):  
        pygame.draw.rect(self.screen, self.BORDERCOLOR, (20, 410, 1060, 220), 4)
        
        factList =  { "cleo" : ("Cleopatra" ,
                        "1: Ruled Egypt from 51 BC - 30 BC", 
                        "2: Was the daughter of Pharaoh Ptolemy XII Auletes", 
                        "3: Her father was King Ptolemy XII", 
                        "4: Killed herself after her son commit suicide in 30 BC" ),
                    
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
                        "1: Was born in 1491 aka the 'Tudor Age'",
                        "2: Had six wives and was the King of England",
                        "3: People who made him cross risked having their heads chopped off!",
                        "4: Died in 1547" ),
                    
                    "queen" : ("Queen Victoria", 
                        "1: Was born in 1819",
                        "2: Became Queen in 1837 when she was 18",
                        "3: Had a long period of history is named after her - the Victorian Age",
                        "4: Lived to see the start of the 20th century and died in January 1901." ),
                    
                    "flo" : ("Florence Knightingale",
                        "1: Was born in 1820, prior to the steam railway",
                        "2: She was the founder of modern nursing",
                        "3: Showed that trained nurses and clean hospitals helped sick people get better",
                        "4: Died in 1910, after the age of electricity, cars and planes began"),
        }
        
        marginleft = 30
        yAxis = 500 
        
        factTitle, factTitleRect = self.makeText('Did you know?...', self.MESSAGECOLOR, 40, marginleft, 415)
        self.screen.blit(factTitle, factTitleRect)
        
        charName, charNameRect = self.makeText(factList[RANDCHAR][0], self.MESSAGECOLOR, 40, marginleft, 450)
        self.screen.blit(charName, charNameRect)
          
        for x in range(4):
            x += 1
            factx, factxRect = self.makeText(factList[RANDCHAR][x], self.MESSAGECOLOR, 20, marginleft, yAxis)
            self.screen.blit(factx, factxRect)
            yAxis += 35
            
    def drawBoard(self, board, message, message2): 
        self.screen.blit(self.BGIMAGE, (0,0))

        if message:
            messageText, messageTextRect  = self.makeTextCenter(message, self.MESSAGECOLOR, 30, self.WINDOWWIDTH/2, self.WINDOWHEIGHT/2 + 30)
            self.screen.blit(messageText, messageTextRect)
            
        if message2:
            message2Text, message2TextRect  = self.makeTextCenter(message2, self.MESSAGECOLOR2, 30, self.WINDOWWIDTH/2, self.WINDOWHEIGHT - 30)
            self.screen.blit(message2Text, message2TextRect)
            
        self.score = self.topScore - (self.moves * 10)
        
        scoreText, scoreRect = self.makeText("Score: ", self.MESSAGECOLOR, 40, 10, 10)
        self.screen.blit(scoreText, scoreRect)
        
        movesCount, moveCountRect = self.makeText(str(self.score), self.MESSAGECOLOR2, 40, 150,10)
        self.screen.blit(movesCount, moveCountRect)
        
        if self.TILESIZE == 80: 
            for tilex in range(len(board)):
                for tiley in range(len(board[0])):
                    if board[tilex][tiley]:
                        self.drawTile(tilex, tiley-2, board[tilex][tiley])
        
            self.left, self.top = self.getLeftTopOfTile(0, -2)
            
        elif self.TILESIZE == 64: 
            for tilex in range(len(board)):
                for tiley in range(len(board[0])):
                    if board[tilex][tiley]:             
                        self.drawTile(tilex, tiley-2.5, board[tilex][tiley])
            
            self.left, self.top = self.getLeftTopOfTile(0, -2.5)
        
        self.width = self.BOARDWIDTH * self.TILESIZE
        self.height = self.BOARDHEIGHT * self.TILESIZE
        pygame.draw.rect(self.screen, self.BORDERCOLOR, (self.left - 8, self.top -8, self.width + 20, self.height + 20), 11)
                      
        self.screen.blit(self.RESET_SURF, self.RESET_RECT)
        self.screen.blit(self.NEW_SURF, self.NEW_RECT)
        self.screen.blit(self.EXIT_SURF, self.EXIT_RECT)
                          
        if self.moves >= self.randomNumber:
            self.SOLVE_SURF, self.SOLVE_RECT = self.makeText('Solve Game', self.BUTTONTEXTCOLOR, 30, 20, 100)
            self.screen.blit(self.SOLVE_SURF, self.SOLVE_RECT)
        
        if message == "YOU DID IT!":
            self.funFact(self.RANDCHAR)
        
    def slideAnimation(self, board, direction, message, message2, animationSpeed):
        #This does not check if valid move....
        self.blankx, self.blanky = self.getBlankPosition(board)
        if direction == self.UP:
            movex = self.blankx
            movey = self.blanky + 1
        elif direction == self.DOWN:
            movex = self.blankx
            movey = self.blanky - 1
        elif direction == self.LEFT:
            movex = self.blankx + 1
            movey = self.blanky
        elif direction == self.RIGHT:
            movex = self.blankx - 1
            movey = self.blanky

        self.drawBoard(board, message, message2)
        baseSurf = self.screen.copy()
        
        #Blank space over moving tile
        if self.TILESIZE == 80:
            moveLeft, moveTop = self.getLeftTopOfTile(movex, movey-2)
        elif self.TILESIZE == 64:
            moveLeft, moveTop = self.getLeftTopOfTile(movex, movey-2.5)
            
        pygame.draw.rect(baseSurf, self.BGCOLOR, (moveLeft, moveTop, self.TILESIZE, self.TILESIZE)) 
        
        for i in range(0, self.TILESIZE, animationSpeed):
            #Animate the tile sliding over
            self.screen.blit(baseSurf, (0, 0))
            if direction == self.UP:
                if self.TILESIZE == 80:
                    self.drawTile(movex, movey - 2, board[movex][movey], 0, -i)
                elif self.TILESIZE == 64:
                    self.drawTile(movex, movey - 2.5, board[movex][movey], 0, -i)
            if direction == self.DOWN:
                if self.TILESIZE == 80:
                    self.drawTile(movex, movey - 2, board[movex][movey], 0, i)
                elif self.TILESIZE == 64:
                    self.drawTile(movex, movey - 2.5, board[movex][movey], 0, i)
            if direction == self.LEFT:
                if self.TILESIZE == 80:
                    self.drawTile(movex, movey - 2, board[movex][movey], -i, 0)
                elif self.TILESIZE == 64:
                    self.drawTile(movex, movey - 2.5, board[movex][movey], -i, 0)
            if direction == self.RIGHT:
                if self.TILESIZE == 80:
                    self.drawTile(movex, movey - 2, board[movex][movey], i, 0)
                elif self.TILESIZE == 64:
                    self.drawTile(movex, movey - 2.5, board[movex][movey], i, 0)
            
            pygame.display.flip()
            self.FPSCLOCK = pygame.time.Clock()
            self.FPSCLOCK.tick(60)
    
    def generateNewPuzzle(self, numSlides):        
        #numSlides is the number of moves and this function will animate these moves
        sequence = []
        board = self.getStartingBoard()
        self.drawBoard(board, '', '')
        #pygame.time.wait(5) #Pause for 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.slideAnimation(board, move, 'Generating new puzzle...', '',  animationSpeed=int(self.TILESIZE / 2))
            self.makeMove(board, move)
            sequence.append(move)
            lastMove = move
        return (board, sequence)
    
    def resetAnimation(self, board, allMoves):
        #reverse allMoves
        revAllMoves = allMoves[:]
        revAllMoves.reverse()
        for move in revAllMoves:
            if move == self.UP:
                oppositeMove = self.DOWN
            elif move == self.DOWN:
                oppositeMove = self.UP
            elif move == self.LEFT:
                oppositeMove = self.RIGHT
            elif move == self.RIGHT:
                oppositeMove = self.LEFT
                
            self.slideAnimation(board, oppositeMove, '', '',animationSpeed=int(self.TILESIZE / 2 ))
            self.makeMove(board, oppositeMove)