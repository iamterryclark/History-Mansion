#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, game, scoreBoard, main, quiz
from context import *
from pygame.locals import *

class startScreen():
    
    def __init__(self):
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700

        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
    
        #Set In Game colors and assets
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        self.userNameIMAGE = pygame.image.load("Assets/images/Pictures/mansion/nameSign.png")
        self.BORDERCOLOR = self.BROWN
    
        #Font
        self.BASICFONTSIZE = 45 
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)

        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
        
        #Option buttons
        self.START_SURF, self.START_RECT = self.makeText('Start Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 400)
        self.SCOREBOARD_SURF, self.SCOREBOARD_RECT = self.makeText('Score Board', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 450)
        self.QUIZ_SURF, self.QUIZ_RECT = self.makeText('Take a Quiz', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 500)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Exit', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 550)
        self.startSOUND.play()
        
        self.DISPLAYSURF = pygame.display.get_surface()
        self.popup = 0
        
    #/---Event loop function---\#
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.START_RECT.collidepoint(event.pos): #user clicked start button
                    #choose level here
                    push(game.game())
                elif self.SCOREBOARD_RECT.collidepoint(event.pos):#user clicked start button
                    push(scoreBoard.scoreBoard())
                elif self.QUIZ_RECT.collidepoint(event.pos):#user clicked start button
                    push(quiz.quiz())
                elif self.EXIT_RECT.collidepoint(event.pos):
                    if top() is self:
                        pop()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
        
    #/-----Draw to screen-----\#
    def draw(self, dt): 
        # Blit everything to the screen
        self.DISPLAYSURF.blit(self.BGIMAGE, (0, 0))
        self.DISPLAYSURF.blit(self.START_SURF, self.START_RECT)
        self.DISPLAYSURF.blit(self.SCOREBOARD_SURF, self.SCOREBOARD_RECT)
        self.DISPLAYSURF.blit(self.QUIZ_SURF, self.QUIZ_RECT)
        self.DISPLAYSURF.blit(self.EXIT_SURF, self.EXIT_RECT)
        
        pygame.display.flip()      
    
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt) 
        
    def levelChoice(self):
        pass
            
    def makeText(self, text, color, centerx, height):
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.midbottom = (centerx, height)
        return (self.textSurf, self.textRect)