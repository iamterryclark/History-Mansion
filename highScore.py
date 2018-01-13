#History Mansion - A history slider game
#highScore.py edited and adapted by Terry Clark
#Original Source: http://codeacademy.cc/  https://www.youtube.com/watch?v=kib9nS9YcFI
#Released under a "Simplified BSD" License

import hashlib
import fileinput
import operator

class Highscore:
    
    def __init__(self, puzOrQuiz):
        self.puzOrQuiz = puzOrQuiz
        self.puzHS = "Assets/data/puzHighScore.dat"
        self.quizHS = "Assets/data/quizHighScore.dat"
        
        self.__highscore = self.load()
    
    def getScores(self):
        return self.__highscore
    
    def load(self):
        highscore = []
        
        if self.puzOrQuiz == "puz":
            self.HS = self.puzHS
        elif self.puzOrQuiz == "quiz":
            self.HS = self.quizHS
        
        for line in fileinput.input(self.HS):
            name, score, md5 = line.split('[::]')
            md5 = md5.replace('\n', '')
            
            if str(hashlib.md5(str.encode(str(name+score+"pygame"))).hexdigest()) == str(md5):
                highscore.append([str(name), int(score), str(md5)])
        
        highscore.sort(key=operator.itemgetter(1), reverse=True)
        highscore = highscore[0:11]
        
        return highscore 
    
    def add(self, name, score):
        hash = hashlib.md5((str(name+str(score)+"pygame")).encode("utf-8"))
        self.__highscore.append([name, str(score), hash.hexdigest()])
        
        f = open(self.HS, "w")
        for name, score, md5 in self.__highscore:
            f.write(str(name)+"[::]" + str(score)+"[::]" + str(md5)+"\n")
            
        f.close()