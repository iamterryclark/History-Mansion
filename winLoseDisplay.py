#History Mansion - A history slider game
#scoreBoard Created by Terry Clark 
#Released under a "Simplified BSD" License

import pygame, sys, main, quiz
from context import *
from pygame.locals import *
import time

class winLoseDisplay():

    def __init__(self, isCorrect):
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        
        self.isCorrect = isCorrect
        
        #Set In Game colors and assets
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        
        self.screen = pygame.display.get_surface() 

    #/-----Event loop function-----\#
    def update(self, dt):
        for event in pygame.event.get(): 
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    if top() is self:
                        pop()  
            if event.type == QUIT:
                sys.exit()

    #/-----Draw to screen-----\#
    def draw(self, dt): 
        #Display background
        self.screen.blit(self.BGIMAGE, (0, 0))
        pygame.draw.rect(self.screen, self.BLACK, (0, 180, self.WINDOWWIDTH, 300))
        
        if self.isCorrect == True:
            isCorrectText, isCorrectTextRect = self.makeTextCenter("Right Answer!", self.WHITE, 60, self.WINDOWWIDTH/2, 320)
            instruct, instructRect = self.makeTextCenter("Press ENTER to continue", self.WHITE, 30, self.WINDOWWIDTH/2, 400)
            
            self.screen.blit(isCorrectText, isCorrectTextRect)
            self.screen.blit(instruct, instructRect)
            
        elif self.isCorrect == False:
            isCorrectText, isCorrectTextRect = self.makeTextCenter("Wrong Answer!", self.WHITE, 60, self.WINDOWWIDTH/2, 320)
            instruct, instructRect = self.makeTextCenter("Press ENTER to continue", self.WHITE, 30, self.WINDOWWIDTH/2, 400)
            
            self.screen.blit(isCorrectText, isCorrectTextRect)
            self.screen.blit(instruct, instructRect)
            
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