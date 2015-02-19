import pygame, main, startScreen, game, scoreBoard
from pygame.locals import *

def push(top_context):
    game_stack.append(top_context)

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