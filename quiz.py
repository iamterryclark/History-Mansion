#History Mansion - A history slider game
#quiz.py Created By Terry Clark
#Released under a "Simplified BSD" License

import pygame, os, sys, random, quizSubmitScore, winLoseDisplay
from context import *
from pygame.locals import *
from decimal import ROUND_UP

class quiz:
    
    def __init__(self):
        #Screen Size
        self.WINDOWWIDTH = (1100)
        self.WINDOWHEIGHT = (700)
        
        #Set In Game colors and assets
        self.WHITE =   ( 255, 255, 255 )
        self.BLACK =   (   0,   0,   0 )
        self.BROWN =   ( 180, 120,  40 )
        self.BGCOLOR = self.BLACK
        self.BGIMAGE = pygame.image.load("Assets/images/Pictures/mansion/fireplace.jpg")
        self.BORDERCOLOR = self.BROWN
        self.BUTTONTEXTCOLOR = self.WHITE
                                          
        #Quiz Variables       
        self.CHAR = ('flo','geng','ghandi','henry','queen','cleo')
        self.randQuestSel = random.choice(range(23))
        self.titleInstruct = "Complete all questions to submit your score!"
        self.instruct = "Select a person below....."
        self.questNum = 1
        self.quizScore = 0
        self.percent = 0
        
        #Option buttons
        self.EXIT_SURF, self.EXIT_RECT = self.makeText('EXIT', self.BUTTONTEXTCOLOR, 30, 10, self.WINDOWHEIGHT - 40)
        self.quizTitle, self.quizTitleRect = self.makeTextCenter("QUIZ!", self.WHITE, 40, (self.WINDOWWIDTH/2), 100)
        self.titleInstruct, self.titleInstructRect = self.makeTextCenter(self.titleInstruct, self.WHITE, 30, self.WINDOWWIDTH/2, 150)
        self.quizInstruct, self.quizInstructRect = self.makeTextCenter(self.instruct, self.WHITE, 30, self.WINDOWWIDTH/2, 330)

        self.screen = pygame.display.get_surface()
        
    #/---Event loop function---\#
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.EXIT_RECT.collidepoint(event.pos):
                    if top() is self:
                        pop()
                        
                #User presses character images to answer question
                if self.ansImgRect1.collidepoint(event.pos):
                    self.checkAns(self.CHAR[0])
                elif self.ansImgRect2.collidepoint(event.pos):
                    self.checkAns(self.CHAR[1])
                elif self.ansImgRect3.collidepoint(event.pos):
                    self.checkAns(self.CHAR[2])
                elif self.ansImgRect4.collidepoint(event.pos):
                    self.checkAns(self.CHAR[3])
                elif self.ansImgRect5.collidepoint(event.pos):
                    self.checkAns(self.CHAR[4])
                elif self.ansImgRect6.collidepoint(event.pos):
                    self.checkAns(self.CHAR[5])  
            
            #Escaping the game
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if top() is self:
                        pop()
            
            elif event.type == QUIT:
                sys.exit()
                
    #/-----Draw to screen-----\#
    def draw(self, dt):
         
        #Display background
        self.screen.blit(self.BGIMAGE, (0, 0))
        pygame.draw.rect(self.screen, self.BLACK, (0, 180, self.WINDOWWIDTH, 300))

        self.scoreText, self.scoreTextRect = self.makeTextCenter("Score: " + str(self.quizScore), self.WHITE, 40, (self.WINDOWWIDTH/2), 500)        

        #End quiz conditional
        if self.questNum == 23:
            push(quizSubmitScore.submitScore(self.quizScore))
            self.questNum = 1
            self.quizScore = 0
            self.percent = 0
            
        #Display quest and answer
        self.QandAList()
        self.displayAnswers()
        
        #Game text and buttons
        self.screen.blit(self.quizTitle, self.quizTitleRect)
        self.screen.blit(self.titleInstruct, self.titleInstructRect)
        self.screen.blit(self.quizInstruct, self.quizInstructRect)
        self.screen.blit(self.scoreText, self.scoreTextRect)
        self.screen.blit(self.EXIT_SURF, self.EXIT_RECT)
        
        pygame.display.flip()      
    
    #/-----In Game Functions-----\#
    def think(self, dt):
        self.update(dt)
        self.draw(dt) 
            
    def QandAList(self):
        self.questList = {  #cleo
                        0 : ("Who ruled Egypt between 51 BC and 30 BC?", "cleo"),
                        1 : ("Who had a daughter called Pharaoh Ptolemy XII Auletes?", "cleo"),
                        2 : ("Whose father was called King Ptolemy XII?", "cleo"),
                        3 : ("Who died after their son had committed suicide?", "cleo"),
                        
                        #geng
                        4 : ("Who was born around 1162 AD and died at the age of 65?", "geng"),
                        5 : ("Who conquered nearly 12 millions square miles of territory?", "geng"),
                        6 : ("Who was originally named Temujin?", "geng"),
                        7 : ("Who killed over 40 million people?", "geng"),
                       
                        #ghandi  
                        8 : ("Which person was born on October 2 1869 in Porbandar, India?", "ghandi"),
                        9 : ("Who fought for the independence of India?", "ghandi"),
                        10 : ("Who went to Law School in London?", "ghandi"),
                        11 : ("Which person was killed on January 30, 1948?", "ghandi"),
                                    
                        #henry
                        12 : ("Which person was born in 1491, the Tudor Age?", "henry"),
                        13 : ("Who had six wives and was the King of England?", "henry"),
                        14 : ("Who chopped off peoples heads when they were cross with them?", "henry"),
                        15 : ("Which person died in 1547?", "henry"),       
                        
                        #queen
                        16 : ("Who was born in 1819?", "queen"),
                        17 : ("Which person became Queen in 1837 when they was 18?", "queen"),
                        18 : ("Who had a the Victorian Age named after them?", "queen"),
                        19 : ("Who died in January 1901 living to see the start of the 20th century?", "queen"),
                                    
                        #flo
                        20 : ("Who was born in 1820, prior to the steam railway?", "flo"),
                        21 : ("Who was the founder of modern nursing?", "flo"),
                        22 : ("Who showed that cleaner hospitals helped sick people get better?", "flo"),
                        23 : ("Which person died in 1910?", "flo"),     
                    }
        
        questNumText, questNumTextRect = self.makeTextCenter("Question " + str(self.questNum) + " of 22:", self.WHITE, 30, self.WINDOWWIDTH/2, 220)
        quest, questRect = self.makeTextCenter(self.questList[self.randQuestSel][0], self.WHITE, 25, self.WINDOWWIDTH/2, 260)

        self.screen.blit(questNumText, questNumTextRect)
        self.screen.blit(quest, questRect)
            
    def displayAnswers(self):
        imgLocation = "Assets/images/Pictures/quiz_images/"
      
        x = 0 
        xadj = 140 
        y = 350
        
        #for z in range(6):
        #    self.ansImgz, self.ansImgRectz = self.imgClickSurf(imgLocation + self.CHAR[z-1] + ".jpg", (x + xadj), y)
        #    x += 140
        
        self.ansImg1, self.ansImgRect1 = self.imgClickSurf(imgLocation + self.CHAR[0] + ".jpg", (x + xadj), y)
        self.ansImg2, self.ansImgRect2 = self.imgClickSurf(imgLocation + self.CHAR[1] + ".jpg", (x + xadj * 2), y)
        self.ansImg3, self.ansImgRect3 = self.imgClickSurf(imgLocation + self.CHAR[2] + ".jpg", (x + xadj * 3), y)
        self.ansImg4, self.ansImgRect4 = self.imgClickSurf(imgLocation + self.CHAR[3] + ".jpg", (x + xadj * 4), y)
        self.ansImg6, self.ansImgRect6 = self.imgClickSurf(imgLocation + self.CHAR[5] + ".jpg", (x + xadj * 6), y)
        self.ansImg5, self.ansImgRect5 = self.imgClickSurf(imgLocation + self.CHAR[4] + ".jpg", (x + xadj * 5), y)
           
        self.screen.blit(self.ansImg1, self.ansImgRect1)
        self.screen.blit(self.ansImg2, self.ansImgRect2)
        self.screen.blit(self.ansImg3, self.ansImgRect3)
        self.screen.blit(self.ansImg4, self.ansImgRect4)
        self.screen.blit(self.ansImg5, self.ansImgRect5)
        self.screen.blit(self.ansImg6, self.ansImgRect6)
    
    def imgClickSurf (self, img, top, left):
        image = pygame.image.load(os.path.join(img))
        imageRect = image.get_rect()
        imageRect.topleft = (top, left)
        return (image, imageRect)
    
    def checkAns(self, char):
        if char == self.questList[self.randQuestSel][1]:
            self.quizScore += 10
            self.questNum += 1
            self.randQuestSel = random.choice(range(23))
            isCorrect = True
            push(winLoseDisplay.winLoseDisplay(isCorrect))
            
        else:
            self.questNum += 1
            self.randQuestSel = random.choice(range(23))
            isCorrect = False
            push(winLoseDisplay.winLoseDisplay(isCorrect))
           
    def makeText(self, text, color, size, top, left):
        font = pygame.font.SysFont("monospace", size, bold=True, italic = False)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)
    
    def makeTextCenter(self,  text, color, size, centerx, height):
        font = pygame.font.SysFont("monospace", size, bold=True, italic = False)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = (centerx, height)
        return (textSurf, textRect)