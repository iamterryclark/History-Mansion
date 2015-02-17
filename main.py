#History Mansion - A history slider game
#Edited and adapted By Terry Clark
#Original Source: http://inventwithpython.com/slidepuzzle.py by Al Sweigart
#Released under a "Simplified BSD" License

import pygame
from pygame.locals import *

def push(context):
    game_stack.append(context)


def pop():
    try:
        game_stack.pop()
    except IndexError:
        pass


def top():
    try:
        return game_stack[-1]
    except IndexError:
        return None

game_stack = []


def run():
    pygame.init()

    resolution = 1024, 768
    screen = pygame.display.set_mode(resolution)
    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()
    max_fps = 0

    push(Menu())
    while top():
        dt = clock.tick(max_fps) / 1000.0

        context = top()
        if context:
            context.think(dt)


if __name__ == '__main__':
    main()
    startScreen()
    scoreBoard()
    run()