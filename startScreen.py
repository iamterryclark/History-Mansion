#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Date Created: 10/02/2015
#Released under a "Simplified BSD" License

import pygame, sys, game, scoreBoard, main 
from context import *
from pygame.locals import *

class startScreen():
    
    def __init__(self):
        self.WINDOWWIDTH = (1800/2)
        self.WINDOWHEIGHT = (1092/2)
        self.FPS = 40
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        self.BORDERCOLOR = self.BROWN
        self.BASICFONTSIZE = 45 
        self.BUTTONTEXTCOLOR = self.WHITE
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
        self.WINDOWWIDTH = (1800/2)
        self.WINDOWHEIGHT = (1092/2)
        self.FPS = 40
    
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
    
        #Set In Game colors and assets
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        self.BORDERCOLOR = self.BROWN
    
        #Font
        self.BASICFONTSIZE = 45 
    
        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
        
        #Option buttons
        self.START_SURF, self.START_RECT = self.makeText('Start Game', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 300)
        self.SCOREBOARD_SURF, self.SCOREBOARD_RECT = self.makeText('Score Board', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 350)
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('Exit', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH/2, 400)
        self.startSOUND.play()
        
    #/---Event loop function---\#
    def update(self, dt):
        self.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.START_RECT.collidepoint(event.pos): #user clicked start button
                     push(game.game())
                elif self.SCOREBOARD_RECT.collidepoint(event.pos):#user clicked start button
                    push(scoreBoard)
                elif self.EXIT_RECT.collidepoint(event.pos):
                    self.terminate()
    
            #pygame.display.flip()
            
    #/-----In Game Functions-----\#
    
    def draw(self, dt): 
        DISPLAYSURF = pygame.display.get_surface()
        
        # Blit everything to the screen
        DISPLAYSURF.blit(self.BGIMAGE, (0, 0))
        DISPLAYSURF.blit(self.START_SURF, self.START_RECT)
        DISPLAYSURF.blit(self.SCOREBOARD_SURF, self.SCOREBOARD_RECT)
        DISPLAYSURF.blit(self.EXIT_SURF, self.EXIT_RECT)
        pygame.display.flip() 
   
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
            
    def makeText(self, text, color, centerx, height):
        self.textSurf = self.BASICFONT.render(text, True, color)
        self.textRect = self.textSurf.get_rect()
        self.textRect.midbottom = (centerx, height)
        return (self.textSurf, self.textRect)
     