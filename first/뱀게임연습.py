import pygame as 게임 #'pygame'을 '게임'이라고 부르겠습니다.
import sys
import time
import random
from pygame.locals import *

가로 = 800
세로 = 600
블럭크기 = 20

가로칸수 = 가로/블럭크기
세로칸수 = 세로/블럭크기

#   0,0         n,0
#   
#   
#   0,n         n,n
위   = (0,-1)
아래 = (0,1)
좌   = (-1,0)
우   = (1,0)

class 뱀(object):

    def 만들기(self):
        self.크기 = 2
        self.위치 = [[(가로/2),세로/2],[(가로/2),세로/2]]
        self.방향 = random.choice([up,dn,lt,rt])
    
    def control(self,xy):
        if (xy[0]*-1,xy[1]*-1) == self.direction:
            return
        else:
            self.direction = xy
    
    def move(self):
        cur = self.positons[0]
        x,y = self.direction
        new = (cur[0]+(x*bk_size))%width,(cur[1]+(y*bk_size))%hight   

        if new in self.positons[2:]:
            self.create()
        else:
            self.positons.insert(0,new)
            if len(self.positons) > self.length:
                self.positons.pop()

    def eat(self):
        self.length +=1
    
    def draw(self,surface):
        for p in self.positons:
            draw_object(surface,self.color,p)


if __name__ == "__main__":
    게임.init()
    window = 게임.display.set_mode((800,600),0,32)
    게임.display.set_caption('뱀게임')
    화면 = 게임.Surface(window.get_size())
    화면 = 화면.convert()
    화면.fill((0,0,0))
    window.blit(화면,(0,0))
    print('키보드 키가 눌리면, 색상이 바뀝니다.')
    while True :
        for event in 게임.event.get() :
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN :
                화면.fill((0,100,0))
                print('화면 색상이 녹색으로 바뀌었습니다.')
        window.blit(화면,(0,0))
        게임.display.flip()
        게임.display.update()