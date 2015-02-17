#History Mansion - A history slider game
#startScreen.py Created by Terry Clark 
#Date Created: 10/02/2015
#Released under a "Simplified BSD" License

import pygame, sys
from pygame.locals import *

WINDOWWIDTH = (1800/2)
WINDOWHEIGHT = (1092/2)
FPS = 40

#Colors     R    G    B
WHITE =   ( 255, 255, 255 )
BLACK =   (   0,   0,   0 )
BROWN =   ( 180, 120,  40 )

#Set In Game colors and assets
BGCOLOR = BLACK
BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
BORDERCOLOR = BROWN

#Font
BASICFONTSIZE = 30 

#Button Attributes
BUTTONTEXTCOLOR = WHITE

def scoreBoard():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, TILESOUND, WINSOUND, NEW_SURF, NEW_RECT, RESET_SURF, RESET_RECT, SOLVE_SURF, SOLVE_RECT,  EXIT_SURF, EXIT_RECT, TIMERSURF, TIMERRECT, RANDCHAR, moves 

    # Initialise screen
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('History Mansion')
    BASICFONT = pygame.font.SysFont("monospace", BASICFONTSIZE, bold=True, italic = True)

    # Fill background
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.blit(BGIMAGE, (0,0))
    
    #Option buttons
    BACK_SURF, BACK_RECT = makeText('Back', BUTTONTEXTCOLOR, 10, WINDOWHEIGHT - 45)

    # Blit everything to the screen
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(BACK_SURF,BACK_RECT)
    pygame.display.flip()
    
#/---Event loop---\#

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if BACK_RECT.collidepoint(event.pos): #user clicked New button
                    return True
            
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
        
def makeText(text, color, top, left):
    textSurf = BASICFONT.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

if __name__ == '__main__': 
    