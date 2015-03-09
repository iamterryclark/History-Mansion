#History Mansion - A history slider game
#scoreBoard Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, startScreen, main, highScore
from context import *
from pygame.locals import *

class scoreBoard():

    def __init__(self):
        self.WINDOWWIDTH = (1100)
        self.WINDOWHEIGHT = (700)
        self.FPS = 40
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.WHITEOP = ( 255, 255, 255, 100)
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        
        #Set In Game colors and assets
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = self.BROWN
        
        #Font
        self.BASICFONTSIZE = 40 
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        
        self.TITLEFONTSIZE = 45 
        self.TITLEFONT = pygame.font.SysFont("monospace", self.TITLEFONTSIZE, bold=True, italic = False)

        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #Option buttons
        self.BACK_SURF, self.BACK_RECT = self.makeButton('Back', self.BUTTONTEXTCOLOR, 10, self.WINDOWHEIGHT - 40)
    
    
        self.screen = pygame.display.get_surface() 

    #/-----Event loop function-----\#
    def update(self, dt):
        for event in pygame.event.get():
            
            if event.type == MOUSEBUTTONUP:
                if self.BACK_RECT.collidepoint(event.pos):
                    if top() is self:
                        pop()
            
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
    
            elif event.type == QUIT:
                sys.exit()

    #/-----Draw to screen-----\#                
    def draw(self, dt): 
        # Blit everything to the screen
        self.screen.blit(self.BGIMAGE, (0, 0))
        pygame.draw.rect(self.screen, self.BROWN, (100,100, (self.WINDOWWIDTH - 200), (self.WINDOWHEIGHT) - 200), 9)
        pygame.draw.rect(self.screen, self.WHITEOP, (108,108, (self.WINDOWWIDTH - 217), (self.WINDOWHEIGHT - 217)))
        
        self.TITLE = self.TITLEFONT.render('HIGHSCORES', 1, self.BLACK)
        self.screen.blit(self.TITLE, (410, 110))
        
        highscoreObj = highScore.Highscore()
        
        x = 250
        y = 200
        
        for score in highscoreObj.getScores():
            self.player = self.BASICFONT.render(score[0], 1, self.BLACK)
            self.screen.blit(self.player, (x, y))        

            self.playerScore = self.BASICFONT.render(str(score[1]), 1, self.BLACK)
            self.screen.blit(self.playerScore, (x + 400, y)) 
            
            y += 30

        self.screen.blit(self.BACK_SURF,self.BACK_RECT)
        pygame.display.flip()
            
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)

    def makeButton(self, text, color, top, left):
        #create the button objects
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft = (top, left)
        return (self.textSurf, self.textRect)