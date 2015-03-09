#History Mansion - A history slider game
#quiz.py Created By Terry Clark
#Released under a "Simplified BSD" License

import pygame, os, sys, random
from context import *
from pygame.locals import *

class quiz:
    
    def __init__(self):
        self.WINDOWWIDTH = (1100)
        self.WINDOWHEIGHT = (700)
        
        #Colors     R    G    B
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        
        #Set In Game colors and assets
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = self.BROWN
        
        #Font
        self.BASICFONTSIZE = 40 
        self.BASICFONT = pygame.font.SysFont("monospace", self.BASICFONTSIZE, bold=True, italic = True)
        
        self.TITLEFONTSIZE = 45 
        self.TITLEFONT = pygame.font.SysFont("monospace", self.TITLEFONTSIZE, bold=True, italic = False)

        #Button Attributes
        self.BUTTONTEXTCOLOR = self.WHITE
        
        #Option buttons
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('EXIT', self.BUTTONTEXTCOLOR, 10, self.WINDOWHEIGHT - 40)
        self.NEXT_SURF, self.NEXT_RECT = self.makeText('NEXT', self.BUTTONTEXTCOLOR, self.WINDOWWIDTH - 100, 440)
        
        self.screen = pygame.display.get_surface()
                                                 
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        
        self.randQuestSel = random.choice(range(3))
        self.questAnsd = 0
        self.questRight = 0
        self.questWrong = 0
        self.score = 0

    #/---Event loop function---\#
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.NEXT_RECT.collidepoint(event.pos):
                    self.randQuestSel = random.choice(range(3))
                    self.QandA()
                elif self.EXIT_RECT.collidepoint(event.pos):
                    if top() is self:
                        pop()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
        
    #/-----Draw to screen-----\#
    def draw(self, dt): 
        #Display background
        self.screen.blit(self.BGIMAGE, (0, 0))
        pygame.draw.rect(self.screen, self.BLACK, (0, 180, self.WINDOWWIDTH, 300))
        
        #Display header and instructions
        quizTitle, quizTitleRect = self.makeTextCent("QUIZ!", self.WHITE, (self.WINDOWWIDTH/2), 100)
        quizInstruct, quizInstructRect = self.makeTextCent("Complete the quiz to gain points for the hall of fame!", self.WHITE, self.WINDOWWIDTH/2, self.TITLEFONTSIZE + 100)
        self.screen.blit(quizTitle, quizTitleRect)
        self.screen.blit(quizInstruct, quizInstructRect)
        
        #Display quest and answer
        self.QandA()
        self.displayAnswers()
        
        #Game buttons
        self.screen.blit(self.EXIT_SURF, self.EXIT_RECT)
        self.screen.blit(self.NEXT_SURF, self.NEXT_RECT)
        
        pygame.display.flip()      
    
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt) 
            
    def QandA(self):
        questList = { 0 : ("Who ruled Egypt between 51 BC and 30 BC?", 
                              "cleo", ),
                      1 : ("Who had a daughter called Pharaoh Ptolemy XII Auletes?", 
                               "cleo"),
                      2 : ("Whose father was called King Ptolemy XII?", 
                               "cleo")    
                    }

        quest, questRect = self.makeTextCent(questList[self.randQuestSel][0], self.WHITE, self.WINDOWWIDTH/2, 200)
        self.screen.blit(quest, questRect)
            
    def displayAnswers(self):
        imgLocation = "Assets/images/Pictures/main_images/quiz_images/"
      
        x = 170  
        y = 350
        margin = 20
        
        for z in range(6):    
            ansImgz = pygame.image.load(os.path.join(imgLocation + self.CHAR[z-1] + ".jpg"))    
            self.screen.blit(ansImgz, (x, y))
            x += 100 + margin
        
    def makeText(self, text, color, top, left):
        textSurf = self.BASICFONT.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)
    
    def makeTextCent(self, text, color, centerx, height):
        textSurf2 = self.BASICFONT.render(text, True, color)
        textRect2 = textSurf2.get_rect()
        textRect2.center = (centerx, height)
        return (textSurf2, textRect2)
