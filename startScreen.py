#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Date Created: 10/02/2015
#Released under a "Simplified BSD" License

import pygame, sys
from pygame.locals import *

class startScreen():
    
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
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        self.BORDERCOLOR = self.BROWN
    
        #Font
        self.BASICFONTSIZE = 45 
    
        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
    
    def startScreen(): 
        # Initialise screen
        pygame.display.set_caption('History Mansion')
        
    def draw(self, dt): 
        DISPLAYSURF = pygame.display.get_surface()
        
        # Fill background
        background = pygame.Surface(DISPLAYSURF.get_size())
        background = background.convert()
        background.blit(BGIMAGE, (0,0))
        startSOUND.play()
        
        #Option buttons
        self.START_SURF, self.START_RECT = makeText('Start Game', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 300)
        self.SCOREBOARD_SURF, self.SCOREBOARD_RECT = makeText('Score Board', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 350)
        self.EXIT_SURF, self.EXIT_RECT = makeText('Exit', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 400)
    
        # Blit everything to the screen
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(self.START_SURF, START_RECT)
        DISPLAYSURF.blit(SCOREBOARD_SURF, SCOREBOARD_RECT)
        DISPLAYSURF.blit(EXIT_SURF, EXIT_RECT)
        pygame.display.flip()
        
    #/---Event loop---\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt)
 
    def update(self, dt):
        while True:
            self.checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    if START_RECT.collidepoint(event.pos): #user clicked New button
                        push(game.game())
                        return True
                    elif SCOREBOARD_RECT.collidepoint(event.pos):
                        return True
                    elif EXIT_RECT.collidepoint(event.pos):
                        self.terminate()
    
            pygame.display.flip()
            
    #/-----In Game Functions-----\#       
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
        textSurf = BASICFONT.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.midbottom = (centerx, height)
        return (textSurf, textRect)
     