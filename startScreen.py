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
        self.BGCOLOR = BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/mansion.jpg")
        self.BORDERCOLOR = BROWN
    
        #Font
        self.BASICFONTSIZE = 45 
    
        #Button Attributes
        self.BUTTONTEXTCOLOR = WHITE
        
        self.BASICFONT = pygame.font.SysFont("monospace", BASICFONTSIZE, bold=True, italic = True)
        self.startSOUND = pygame.mixer.Sound("Assets/Audio/Mansion.wav")
    
    def startScreen():
        global FPSCLOCK, DISPLAYSURF, BASICFONT, TILESOUND, WINSOUND, NEW_SURF, NEW_RECT, RESET_SURF, RESET_RECT, SOLVE_SURF, SOLVE_RECT,  EXIT_SURF, EXIT_RECT, moves 
    
        # Initialise screen
        pygame.display.set_caption('History Mansion')
        
        # Fill background
        background = pygame.Surface(DISPLAYSURF.get_size())
        background = background.convert()
        background.blit(BGIMAGE, (0,0))
        startSOUND.play()
        
    def draw(self, dt): 
        DISPLAYSURF = pygame.display.get_surface()
        DISPLAYSURF.fill((0, 0, 0))
        
        #Option buttons
        START_SURF, START_RECT = makeText('Start Game', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 300)
        SCOREBOARD_SURF, SCOREBOARD_RECT = makeText('Score Board', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 350)
        EXIT_SURF, EXIT_RECT = makeText('Exit', BUTTONTEXTCOLOR, WINDOWWIDTH/2, 400)
    
        # Blit everything to the screen
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(START_SURF, START_RECT)
        DISPLAYSURF.blit(SCOREBOARD_SURF, SCOREBOARD_RECT)
        DISPLAYSURF.blit(EXIT_SURF, EXIT_RECT)
        pygame.display.flip()
        
    #/---Event loop---\#
    def think(self, dt):
        self.upate(dt)
        self.draw(dt)
 
    def update(self, dt):
        while True:
            checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    if START_RECT.collidepoint(event.pos): #user clicked New button
                        mygame.main()
                        return True
                    elif SCOREBOARD_RECT.collidepoint(event.pos):
                        return True
                    elif EXIT_RECT.collidepoint(event.pos):
                        terminate()
    
            pygame.display.flip()
            
    #/-----In Game Functions-----\#       
    def terminate():
        pygame.quit()
        sys.exit()
        
    def checkForQuit():
        for event in pygame.event.get(QUIT): #get all the QUIT events
            terminate()
        for event in pygame.event.get(KEYUP): #get all the KEYUP events
            if event.key == K_ESCAPE:
                terminate() #if ESC key pressed
            pygame.event.post(event) #put all KEYUP event objects back
            
    def makeText(text, color, centerx, height):
        textSurf = BASICFONT.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.midbottom = (centerx, height)
        return (textSurf, textRect)
    
    if __name__ == '__main__':
        startScreen()
     