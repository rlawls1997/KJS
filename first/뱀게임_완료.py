import pygame as 게임
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
        self.방향 = (1,0)

    def 그리기(self,화면):
        for 한개씩 in self.위치:
            사각형 = 게임.Rect((한개씩[0],한개씩[1]),(블럭크기,블럭크기))
            게임.draw.rect(화면,self.색상,사각형)

    def 제어(self,방향):
        
        if (방향[0]*-1,방향[1]*-1) == self.방향:
            return
        else:
            self.방향 = 방향

    def 자동이동(self) :
        머리위치 = self.위치[0]
        좌표x,좌표y = self.방향
        새머리위치 = (머리위치[0]+(좌표x*블럭크기)),(머리위치[1]+(좌표y*블럭크기))
        #새머리위치 = (머리위치[0]+(좌표x*블럭크기))'''%가로''',(머리위치[1]+(좌표y*블럭크기))'''%세로'''

        if 새머리위치 in self.위치[1:]:
            self.만들기()
        elif 새머리위치[0] < 0 or 새머리위치[1] < 0 or 새머리위치[0] >= 가로 or 새머리위치[1] >= 세로:
            self.만들기()
        else:
            self.위치.insert(0,새머리위치)
            if len(self.위치) > self.길이:
                self.위치.pop()


    def 앙(self):
        self.길이 +=1


class 먹이클래스(object):
    def __init__(self):
        self.위치 =(0,0)
        self.색상 =(0,100,0)
        self.만들기()

    def 만들기(self):
        self.위치 = (random.randint(0,가로칸수-1)*블럭크기, random.randint(0,세로칸수-1)*블럭크기)
    
    def 그리기(self,화면):    
        사각형 = 게임.Rect(self.위치,(블럭크기,블럭크기))
        게임.draw.rect(화면,self.색상,사각형)



def 먹었음체크(뱀,먹이):
    if 뱀.위치[0] == 먹이.위치 :
        뱀.앙()
        먹이.만들기()



if __name__ == "__main__":

    뱀 = 뱀클래스()
    먹이 = 먹이클래스()

    게임.init()
    
    font = 게임.font.Font('C:/Windows/Fonts/gulim.ttc',20)
    font.set_bold(True)
    
    속도시계 = 게임.time.Clock()

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

        뱀.자동이동()     
        먹었음체크(뱀,먹이)

        속도 = (10 + 뱀.길이)/2

        게임.display.set_caption(   "뱀 게임 " + 
                                    "       길이 : " + str(뱀.길이) +
                                    "       속도 : " + str(round(속도,2)))
        

        뱀.그리기(화면)                
        먹이.그리기(화면)
        window.blit(화면,(0,0))
        게임.display.flip()

        score_ts = font.render(str(뱀.길이), False, (255, 255, 255))
        window.blit(score_ts, (5, 5))

        score_ts = font.render('시작', False, (255, 255, 255))
        window.blit(score_ts, (5, 25))

        게임.display.update()

        속도시계.tick(속도)