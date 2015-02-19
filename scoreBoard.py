#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Date Created: 10/02/2015
#Released under a "Simplified BSD" License

import pygame, sys, startScreen
from context import *
from pygame.locals import *

class scoreBoard():

    def __init__(self):
        self.WINDOWWIDTH = (1800/2)
        self.WINDOWHEIGHT = (1092/2)
        self.FPS = 40
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        
        #Set In Game colors and assets
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = self.BROWN
        
        #Font
        self.BASICFONTSIZE = 30 
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        
        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #Option buttons
        self.BACK_SURF, self.BACK_RECT = self.makeText('Back', self.BUTTONTEXTCOLOR, 10, self.WINDOWHEIGHT - 45)
    
    def update(self, dt):    
        self.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.BACK_RECT.collidepoint(event.pos): #user clicked New button
                    pop()
                
        #pygame.display.flip()
        
    def draw(self, dt): 
        
        DISPLAYSURF = pygame.display.get_surface()       
        # Blit everything to the screen
        DISPLAYSURF.blit(self.BGIMAGE, (0, 0))
        DISPLAYSURF.blit(self.BACK_SURF,self.BACK_RECT)
        pygame.display.flip()
            
    #/-----In Game Functions-----\#
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
            
    def makeText(self, text, color, top, left):
        #create the button objects
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft = (top, left)
        return (self.textSurf, self.textRect)
