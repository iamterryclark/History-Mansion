#History Mansion - A history slider game
#main.py created by Terry Clark
#Released under a "Simplified BSD" License

import pygame, startScreen
from context import *
from pygame.locals import *

def run():
    pygame.init()
    pygame.display.set_caption('History Mansion')

    resolution = 1100, 700
    screen = pygame.display.set_mode(resolution)

    clock = pygame.time.Clock()

    push(startScreen.startScreen(screen))
    while top():
        dt = clock.tick(1000)

        top_context = top()
        if top_context:
            top_context.think(dt)

if __name__ == '__main__':    
    run()