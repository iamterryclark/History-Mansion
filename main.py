#History Mansion - A history slider game
#Edited and adapted By Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame, startScreen, game, scoreBoard
from context import *
from pygame.locals import *

def run():
    pygame.init()
    pygame.display.set_caption('History Mansion')

    resolution = 900, 1092/2
    screen = pygame.display.set_mode(resolution)
    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()
    max_fps = 0

    push(startScreen.startScreen())
    while top():
        dt = clock.tick(max_fps) / 1000.0

        top_context = top()
        if top_context:
            top_context.think(dt)

if __name__ == '__main__':
    run()