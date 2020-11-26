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

class 뱀클래스(object):


    def __init__(self):
        self.만들기()
        self.색상 =(255,0,0)

    def 만들기(self):
        self.길이 = 2
        self.위치 = [[(가로/2),세로/2],[(가로/2),세로/2]]
        self.방향 = (0,0)

    def 그리기(self,화면):
        for 한개씩 in self.위치:
            사각형 = 게임.Rect((한개씩[0],한개씩[1]),(블럭크기,블럭크기))
            게임.draw.rect(화면,self.색상,사각형)

    def 제어(self,방향):
        self.방향 = 방향

        머리위치 = self.위치[0]
        좌표x,좌표y = self.방향
        새머리위치 = (머리위치[0]+(좌표x*블럭크기))%세로,(머리위치[1]+(좌표y*블럭크기))%세로

        self.위치.insert(0,새머리위치)  
        self.위치.pop()
        

if __name__ == "__main__":

    뱀 = 뱀클래스()
    게임.init()

    window = 게임.display.set_mode((800,600),0,32)
    게임.display.set_caption('뱀게임')
    화면 = 게임.Surface(window.get_size())
    화면 = 화면.convert()
    화면.fill((0,0,0))
    window.blit(화면,(0,0))


    
    while True :

        화면.fill((0,0,0))
        for event in 게임.event.get() :
            if event.type == QUIT:
                게임.quit()
                sys.exit()
            elif event.type == KEYDOWN :
                if event.key == K_UP:
                    뱀.제어(위)
                elif event.key == K_DOWN:
                    뱀.제어(아래)
                elif event.key == K_LEFT:
                    뱀.제어(좌)
                elif event.key == K_RIGHT:
                    뱀.제어(우)
               
        뱀.그리기(화면)
        window.blit(화면,(0,0))
        게임.display.flip()
        게임.display.update()