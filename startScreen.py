#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, levelSelect, scoreBoard, quiz
from context import *
from pygame.locals import *

class startScreen():
    
    def __init__(self):
        #Screen Size
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700

        #Set In Game colors and assets
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")

        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #Main Theme Tune
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
        
        #Option buttons
        self.START_SURF, self.START_RECT = self.makeText('Start Game', self.BUTTONTEXTCOLOR, 40, self.WINDOWWIDTH/2, 400)
        self.SCOREBOARD_SURF, self.SCOREBOARD_RECT = self.makeText('Score Board', self.BUTTONTEXTCOLOR, 40, self.WINDOWWIDTH/2, 450)
        self.QUIZ_SURF, self.QUIZ_RECT = self.makeText('Take a Quiz', self.BUTTONTEXTCOLOR, 40, self.WINDOWWIDTH/2, 500)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Exit', self.BUTTONTEXTCOLOR, 40, self.WINDOWWIDTH/2, 550)
        self.startSOUND.play()
        
        self.DISPLAYSURF = pygame.display.get_surface()
        
    #/---Event loop function---\#
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.START_RECT.collidepoint(event.pos): #user clicked start button
                    #choose level here
                    push(levelSelect.levelSelect())
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
            
            elif event.type == QUIT:
                sys.exit()
        
    #/-----Draw to screen-----\#
    def draw(self, dt): 
        # Blit (Show) everything to the screen
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
            
    def makeText(self, text, color, size, centerx, height):
        font = pygame.font.SysFont("monospace", size, bold=True, italic = True)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.midbottom = (centerx, height)
        return (textSurf, textRect)