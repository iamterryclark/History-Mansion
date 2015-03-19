#History Mansion - A history slider game
#submitScore.py Created by Terry Clark
#Released under a "Simplified BSD" License

import pygame, sys, game, main, puzHighScore
import random
from context import *
from pygame.locals import *

class submitScore():
    
    def __init__(self, score):
        self.WINDOWWIDTH = 1100
        self.WINDOWHEIGHT = 700

        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK = 0, 0, 0
    
        #Font
        self.BASICFONTSIZE = 35
         
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        
        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #get screen resolution-
        self.screen = pygame.display.get_surface()
        
        self.__playerName = ""
        self.score = score
        
    #/---Event loop function---\#
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                pass
            
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:
                    puzHighScore.Highscore().add(self.__playerName, self.score)

                    if top() is self:
                        pop()
                        
                        
                        
                elif event.key >= 65 and event.key <= 122:
                    self.__playerName += chr(event.key)
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
            
            elif event.type == QUIT:
                sys.exit()
        
    #/-----Draw to screen-----\#
    def draw(self, dt):
        pygame.draw.rect(self.screen, self.BLACK, (0, 180, self.WINDOWWIDTH, 300))
        
        self.TITLE = self.BASICFONT.render('Type your name and press enter to save your score!', 1, self.WHITE)
        self.askNameText = self.BASICFONT.render('Name:', 1, self.WHITE)
        self.askName = self.BASICFONT.render(self.__playerName, 1, self.WHITE)
        
        self.screen.blit(self.TITLE, (20, 205))
        self.screen.blit(self.askNameText, (100, 305))        
        self.screen.blit(self.askName, (200, 305)) 
        
        pygame.display.flip()

    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)