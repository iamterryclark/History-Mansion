#History Mansion - A history slider game
#context.py created by Terry Clark
#Released under a "Simplified BSD" License

import pygame, main, startScreen, game, scoreBoard
from pygame.locals import *

def push(top_context):
    game_stack.append(top_context)
    print('Context: pushed {}'.format(top_context))
    print('Context: stack {}'.format(game_stack))

def pop():
    try:
        popped = game_stack.pop()
        print('Context: popped {}'.format(popped))
        print('Context: stack {}'.format(game_stack))
    except IndexError:
        pass

def top():
    try:
        return game_stack[-1]
    except IndexError:
        return None

game_stack = []