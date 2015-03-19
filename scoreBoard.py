#History Mansion - A history slider game
#scoreBoard Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, startScreen, puzHighScore, quizHighScore
from context import *
from pygame.locals import *

class scoreBoard():

    def __init__(self):
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        
        #Set In Game colors and assets
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = self.BROWN
        
        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #Option buttons
        self.BACK_SURF, self.BACK_RECT = self.makeText('Back', self.BUTTONTEXTCOLOR, 30, 10, self.WINDOWHEIGHT - 40)
    
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
        pygame.draw.rect(self.screen, self.WHITE, (108,108, (self.WINDOWWIDTH - 217), (self.WINDOWHEIGHT - 217)))
        
        TITLE, TITLERECT = self.makeText('Hall of fame!', self.BLACK, 40, 410, 110)
        self.screen.blit(TITLE, TITLERECT)
        
        puzHighScoreObj = puzHighScore.Highscore()
        quizHighScoreObj = quizHighScore.Highscore()
        
        puzTitle, puzTitleRect = self.makeText("Puzzle Score", self.BLACK, 30, 190, 170)
        self.screen.blit(puzTitle, puzTitleRect)
        
        quizTitle, quizTitleRect = self.makeText("Quiz Score", self.BLACK, 30, 700, 170)
        self.screen.blit(quizTitle, quizTitleRect)
        
        x = 150
        y = 210
        
        x2 = 650
        y2 = 210
        
        for score in puzHighScoreObj.getScores():         
            
            puzPlayerName, puzPlayerRect = self.makeText(score[0], self.BLACK, 30, x, y)
            self.screen.blit(puzPlayerName, puzPlayerRect)        

            puzPlayerScore, puzPlayerScoreRect = self.makeText(str(score[1]), self.BLACK, 30, x + 250, y)
            self.screen.blit(puzPlayerScore, puzPlayerScoreRect) 
            
            y += 30
            
        for score2 in quizHighScoreObj.getScores():
            
            quizPlayerName, quizPlayerNameRect = self.makeText(score2[0], self.BLACK, 30, x2, y2)
            self.screen.blit(quizPlayerName, quizPlayerNameRect)        

            quizPlayerScore, quizPlayerScoreRect = self.makeText(str(score2[1]), self.BLACK, 30, x2 + 250, y2)
            self.screen.blit(quizPlayerScore, quizPlayerScoreRect) 
            
            y2 += 30

        self.screen.blit(self.BACK_SURF,self.BACK_RECT)
        pygame.display.flip()
            
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)

    def makeText(self, text, color, size, top, left, ):
        font = pygame.font.SysFont("monospace", size, bold=True, italic = True)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)