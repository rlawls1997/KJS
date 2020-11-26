import pygame as 게임
import sys
import time
import random
from pygame.locals import *



class 뱀게임_클래스():

    def __init__(self,가로블럭개수,세로블럭개수,블럭크기,가로보조크기,세로보조크기):
        self.가로블럭개수 = 가로블럭개수
        self.세로블럭개수 = 가로블럭개수
        self.블럭크기 = 블럭크기

        self.가로보조 = 가로보조크기
        self.세로보조 = 세로보조크기

        self.가로픽셀 = self.가로블럭개수*self.블럭크기
        self.세로픽셀 = self.가로블럭개수*self.블럭크기

        self.가로보조픽셀 = self.가로보조*self.블럭크기
        self.세로보조픽셀 = self.세로보조*self.블럭크기


        #   0,0         n,0
        #   
        #   
        #   0,n         n,n
        self.뱀머리방향= {'위':(0,-1), '아래':(0,1),'좌':(-1,0),'우':(1,0)}
        
        self.점수 = 0
        self.게임속도 = 30
        self.게임시계 = 게임.time.Clock()

        self.새뱀만들기()
        self.뱀색상 =(255,0,0)
    
        self.먹이위치 =(0,0)
        self.먹이색상 =(0,100,0)

        self.먹이만들기()


    def 새뱀만들기(self):
        self.뱀길이 = 2
        self.뱀몸통 = [[(self.가로픽셀/2),self.세로픽셀/2],[(self.가로픽셀/2),self.세로픽셀/2]]
        self.뱀방향 = self.뱀머리방향['위']


    def 뱀그리기(self,화면):
        for 한개씩 in self.뱀몸통:
            사각형 = self.게임.Rect((한개씩[0]+10,한개씩[1]),(self.블럭크기,self.블럭크기))
            self.게임.draw.rect(화면,self.뱀색상,사각형)

    def 자동이동(self) :
        머리위치 = self.뱀몸통[0]
        좌표x,좌표y = self.뱀방향
        새머리위치 = (머리위치[0]+(좌표x*self.블럭크기))%self.가로픽셀, \
                    (머리위치[1]+(좌표y*self.블럭크기))%self.세로픽셀

        if 새머리위치 in self.뱀몸통[1:]:
            self.새뱀만들기()
        else:
            self.뱀몸통.insert(0,새머리위치)
            if len(self.뱀몸통) > self.뱀길이:
                self.뱀몸통.pop()

    def 앙(self):
        self.뱀길이 +=1


    def 먹이만들기(self):
        self.먹이위치 = ((random.randint(0,self.가로블럭개수-1))*self.블럭크기, \
                        (random.randint(0,self.세로블럭개수-1))*self.블럭크기)
    
    def 먹이그리기(self,화면):
        
        먹이위치 = (self.먹이위치[0]+20,self.먹이위치[1])
        사각형 = self.게임.Rect(먹이위치,(self.블럭크기,self.블럭크기))
        self.게임.draw.rect(화면,self.먹이색상,사각형)

    def 먹었음체크(self):
        if self.뱀몸통[0] == self.먹이위치 :
            self.앙()
            self.먹이만들기()
 
    def 게임_방향(self,방향):
        if (방향[0]*-1,방향[1]*-1) == self.뱀방향:
            return
        else:
            self.뱀방향 = 방향


    def 게임_생성(self):
        self.게임 = 게임
        self.게임.init()

        self.window = self.게임.display.set_mode((  self.가로픽셀+self.세로보조픽셀, \
                                                    self.세로픽셀+self.세로보조픽셀),0,32)
        self.게임.display.set_caption('뱀게임')
        self.화면 = self.게임.Surface(self.window.get_size())
        self.화면 = self.화면.convert()
        self.화면.fill((0,0,0))
        self.window.blit(self.화면,(0,0))
    
    def 자동구동_그리기(self):
        pass

    #. 목록 [v,[x,y]]    #. 값, 위치 
    def 제어_그리기(self,리스트):
        for 값,위치 in 리스트:
            # Draw a circle outline
            self.게임.draw.circle(self.화면, (51,255,51),위치,10,2)
            # Draw a solid circle
            self.게임.draw.circle(self.화면, (값,0,0),위치,8)

            # 5 pixels wide.
            # self.게임.draw.line(self.화면, GREEN, [0,0], [100,150],5)

                 

    def 게임_구동(self):
        while True :

            self.화면.fill((0,0,0))

            for event in self.게임.event.get() :
                if event.type == QUIT:                   
                    self.게임.quit()
                    sys.exit()
                elif event.type == KEYDOWN :
                    #pass
                    if event.key == K_UP:
                        self.게임_방향(self.뱀머리방향['위'])
                    elif event.key == K_DOWN:
                        self.게임_방향(self.뱀머리방향['아래'])
                    elif event.key == K_LEFT:
                        self.게임_방향(self.뱀머리방향['좌'])
                    elif event.key == K_RIGHT:
                        self.게임_방향(self.뱀머리방향['우'])

            self.자동이동()     
            self.먹었음체크()

            속도 = (self.게임속도 + self.뱀길이)/2

            self.게임.display.set_caption(   "뱀 게임 " + 
                                        "       길이 : " + str(self.뱀길이) +
                                        "       속도 : " + str(round(속도,2)))
            #경계선 그리기.
            self.게임.draw.line(self.화면, (0,255,0),[0,0], [600,0],5)
            self.게임.draw.line(self.화면, (0,255,0),[0,600], [600,600],5)
            self.게임.draw.line(self.화면, (0,255,0),[600,0], [600,600],5)                      

            self.뱀그리기(self.화면)                
            self.먹이그리기(self.화면)

            #self.제어_그리기()
            self.window.blit(self.화면,(0,0))
            

            self.게임.display.flip()
            self.게임.display.update()

            self.게임시계.tick(속도)



뱀게임 = 뱀게임_클래스(30,30,20,10,10)
뱀게임.게임_생성()
뱀게임.게임_구동()


