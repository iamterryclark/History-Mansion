#History Mansion - A history slider game
#scoreBoard Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, quiz
from context import *
from pygame.locals import *
import time

class levelSelect():

    def __init__(self):
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
                
        #Set In Game colors and assets
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        
        self.screen = pygame.display.get_surface() 

    #/-----Event loop function-----\#
    def update(self, dt):
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONUP:
                if self.easyRect.collidepoint(event.pos):
                   push(game.game(80, 4, 4))
                if self.hardRect.collidepoint(event.pos):
                   push(game.game(64, 5, 5))
                    
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
                    
                if event.key == K_RETURN:
                    if top() is self:
                        pop()  
            
            elif event.type == QUIT:
                sys.exit()

    #/-----Draw to screen-----\#
    def draw(self, dt): 
        #Display background
        self.screen.blit(self.BGIMAGE, (0, 0))
        pygame.draw.rect(self.screen, self.BLACK, (0, 180, self.WINDOWWIDTH, 300))
        
        titleText, titleRect = self.makeTextCenter("Select Level Difficulty....", self.WHITE, 40, self.WINDOWWIDTH/2, 260)
        self.easyText, self.easyRect = self.makeTextCenter("Easy", self.WHITE, 80, self.WINDOWWIDTH/4, 360)
        self.hardText, self.hardRect = self.makeTextCenter("Hard", self.WHITE, 80, self.WINDOWWIDTH/4 * 3, 360)
            
        self.screen.blit(titleText, titleRect)
        self.screen.blit(self.easyText, self.easyRect)
        self.screen.blit(self.hardText, self.hardRect)
            
        pygame.display.flip()      
            
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)

    def makeTextCenter(self,  text, color, size, centerx, height):
        font = pygame.font.SysFont("monospace", size, bold=True, italic = False)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = (centerx, height)
        return (textSurf, textRect)