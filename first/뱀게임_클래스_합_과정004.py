import pygame as 게임
import sys
import time
import random
from pygame.locals import *

import numpy as np
import copy


움직임상한 = 150
적합도먹이 = 5
적합도움직임 = 1
뉴런들총개수 = 30 


class 뉴런그룹_레이어(object):

    def __init__(self,입력개수,뉴런개수,출력개수):
        self.적합도  = 0        
        self.움직임제한 = 0

        self.입력개수 = 입력개수
        self.뉴런개수 = 뉴런개수
        self.출력개수 = 출력개수
        #   만약 뉴런개수 = 6
        #   6-12-12-4
        self.w1 = np.random.randn(self.입력개수, self.뉴런개수)
        self.w2 = np.random.randn(self.뉴런개수, self.뉴런개수)     
        self.w3 = np.random.randn(self.뉴런개수, self.뉴런개수)     
        self.w4 = np.random.randn(self.뉴런개수, self.출력개수)       

        self.b1 = np.random.randn(self.뉴런개수)
        self.b2 = np.random.randn(self.뉴런개수)
        self.b3 = np.random.randn(self.뉴런개수)
        self.b4 = np.random.randn(self.출력개수)

        self.레이어 = []

    def 계산(self, 입력):
        self.레이어.insert(0,np.matmul(      입력,          self.w1)+self.b1)
        self.레이어.insert(1,self.상하한값(  self.레이어[0]))
        self.레이어.insert(2,np.matmul(      self.레이어[1], self.w2)+self.b2)
        self.레이어.insert(3,self.상하한값(  self.레이어[2]))
        self.레이어.insert(4,np.matmul(      self.레이어[3], self.w3)+self.b3)
        self.레이어.insert(5,self.상하한값(  self.레이어[4]))
        self.레이어.insert(6,np.matmul(      self.레이어[5], self.w4)+self.b4)
        self.레이어.insert(7,self.상하한값(  self.레이어[6]))
        return self.레이어[7]

    def 상하한값(self, x):
        return 1/(1+np.exp(x))
        # if x > 0 : 
        #     return 1
        # else :
        #     return 0
        #return x * (x >= 0)

    def 히든리턴(self,레이어번호):
        return self.레이어[레이어번호]

    def 히든최종리턴(self):
        return self.레이어[7]



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
        self.뱀머리방향= {'위':[0,-1], '아래':[0,1],'좌':[-1,0],'우':[1,0]}
        
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
        #self.뱀몸통 = [[300,300],[300,300]]
        self.뱀방향 = self.뱀머리방향['위']

    def 뱀그리기(self,화면):
        for 한개씩 in self.뱀몸통:
            사각형 = self.게임.Rect((한개씩[0],한개씩[1]+self.세로보조픽셀),(self.블럭크기,self.블럭크기))
            self.게임.draw.rect(화면,self.뱀색상,사각형)

    def 자동이동(self) :
        머리위치 = self.뱀몸통[0]
        좌표x,좌표y = self.뱀방향
        새머리위치 = [(머리위치[0]+(좌표x*self.블럭크기))%self.가로픽셀, \
                    (머리위치[1]+(좌표y*self.블럭크기))%self.세로픽셀]

        if 새머리위치 in self.뱀몸통[1:]:
            self.새뱀만들기()
        else:
            self.뱀몸통.insert(0,새머리위치)
            if len(self.뱀몸통) > self.뱀길이:
                self.뱀몸통.pop()

    def 먹었음체크(self):
        if self.뱀몸통[0] == self.먹이위치 :
            self.앙()
            self.먹이만들기()

    def 앙(self):
        self.뱀길이 +=1

    def 먹이만들기(self):
        self.먹이위치 = [(random.randint(0,self.가로블럭개수-1))*self.블럭크기, \
                        (random.randint(0,self.세로블럭개수-1))*self.블럭크기]

    def 먹이그리기(self,화면):
        먹이위치 = (self.먹이위치[0],self.먹이위치[1]+ self.세로보조픽셀)
        사각형 = self.게임.Rect(먹이위치,(self.블럭크기,self.블럭크기))
        self.게임.draw.rect(화면,self.먹이색상,사각형)


    def 게임_방향(self,방향):
        if (방향[0]*-1,방향[1]*-1) == self.뱀방향:
            return 0
        else:
            self.뱀방향 = 방향
            return 적합도움직임

    def 게임_방향2(self,방향,적합도,시간리셋):
        if 방향 == self.뱀방향:
            return 적합도,시간리셋
        else:
            self.뱀방향 = 방향
            시간리셋 = 0
            적합도 += 적합도움직임
            return 적합도,시간리셋

    def 게임_생성(self):
        self.게임 = 게임
        self.게임.init()
        
        self.font = self.게임.font.Font('C:/Windows/Fonts/gulim.ttc',20)
        self.font.set_bold(True)

        self.window = self.게임.display.set_mode((  self.가로픽셀+self.가로보조픽셀, \
                                                    self.세로픽셀+self.세로보조픽셀),0,32)
        self.게임.display.set_caption('뱀게임')
        self.화면 = self.게임.Surface(self.window.get_size())
        self.화면 = self.화면.convert()
        self.화면.fill((0,0,0))
        self.window.blit(self.화면,(0,0))


    
    def 자동구동_그리기(self):
        pass

    #. 목록 [v,[x,y]]
    #. 값, 위치
    def 제어_그리기(self,리스트):
        for 값,위치 in 리스트:
            # 도너트형 원 그리기.
            self.게임.draw.circle(self.화면, (51,255,51),위치,10,2)
            # 내부채운 원 그리기.
            self.게임.draw.circle(self.화면, (값,0,0),위치,8)


    def 글씨넣기(self,글씨,좌표,색상):
        self.화면.blit(self.font.render(글씨, False, 색상),좌표)

    def 표시(self):
        속도 = (self.게임속도 + self.뱀길이)/2
        self.window.blit(self.화면,(0,0))
        self.게임.display.flip()
        self.게임.display.update()
        self.게임시계.tick(속도*10)



    def 게임_구동(self):
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


        # self.자동이동()     
        # self.먹었음체크()

        속도 = (self.게임속도 + self.뱀길이)/2

        self.게임.display.set_caption(   "뱀 게임 " + 
                                    "       길이 : " + str(self.뱀길이) +
                                    "       속도 : " + str(round(속도,2)))

        self.뱀그리기(self.화면)                
        self.먹이그리기(self.화면)

        #경계선 그리기.
        self.게임.draw.line(self.화면, (0,255,0),[0,self.세로보조픽셀-5], \
                                                    [self.가로보조픽셀,self.세로보조픽셀-5],5)
        self.게임.draw.line(self.화면, (0,255,0),[self.가로픽셀,self.세로보조픽셀-7], \
                                                    [self.가로픽셀,self.세로픽셀+self.세로보조픽셀],5)

        #self.제어_그리기()
        


def 원그리기(뱀게임,뉴런,숫자):
    j = 0
    뉴런입력 = 뉴런.히든리턴(숫자)
    for i in 뉴런입력:
        뱀게임.게임.draw.circle(뱀게임.화면, ((i+1)*125,0,0),(750+숫자*50,200+j*30),8)
        j += 1


#   먹이위치, 머리위치,


뱀게임 = 뱀게임_클래스(30,30,20,30,10)
뱀게임.게임_생성()

뉴런번호 = 0

뉴런들 = [뉴런그룹_레이어(6,15,4) for _ in range(뉴런들총개수)]
뉴런 = 뉴런들[뉴런번호]

while True :

    입력 = []    
    좌표x,좌표y = 뱀게임.뱀몸통[0]
    입력.insert(0,좌표x)
    입력.insert(1,좌표y)

    좌표x,좌표y = 뱀게임.먹이위치
    입력.insert(2,좌표x)
    입력.insert(3,좌표y)

    좌표x,좌표y = 뱀게임.뱀방향
    입력.insert(4,좌표x)
    입력.insert(5,좌표y)
    

    뉴런.계산(입력)
    출력 = 뉴런.히든최종리턴()
    if   (출력[0] > 출력[1]) and (출력[0] > 출력[2])and (출력[0] > 출력[3]):
        뉴런.적합도,뉴런.움직임제한 = 뱀게임.게임_방향2(뱀게임.뱀머리방향['위'],뉴런.적합도,뉴런.움직임제한)
    elif (출력[1] > 출력[0]) and (출력[1] > 출력[2])and (출력[1] > 출력[3]):
        뉴런.적합도,뉴런.움직임제한 = 뱀게임.게임_방향2(뱀게임.뱀머리방향['아래'],뉴런.적합도,뉴런.움직임제한)
    elif (출력[2] > 출력[0]) and (출력[2] > 출력[1])and (출력[2] > 출력[3]):
        뉴런.적합도,뉴런.움직임제한 = 뱀게임.게임_방향2(뱀게임.뱀머리방향['좌'],뉴런.적합도,뉴런.움직임제한)
    elif (출력[3] > 출력[0]) and (출력[3] > 출력[1])and (출력[3] > 출력[2]):
        뉴런.적합도,뉴런.움직임제한 = 뱀게임.게임_방향2(뱀게임.뱀머리방향['우'],뉴런.적합도,뉴런.움직임제한)


    # 뱀 위치 체크.
    머리위치 = 뱀게임.뱀몸통[0]
    좌표x,좌표y = 뱀게임.뱀방향
    새머리위치 = [(머리위치[0]+(좌표x*뱀게임.블럭크기))%뱀게임.가로픽셀, \
                (머리위치[1]+(좌표y*뱀게임.블럭크기))%뱀게임.세로픽셀]

    뉴런.움직임제한 +=1
    if ((새머리위치 in 뱀게임.뱀몸통[1:])and(len(뱀게임.뱀몸통)>3)) or (뉴런.움직임제한 > 움직임상한):
        뉴런.움직임제한 = 0
        뉴런번호 += 1
        if 뉴런번호 >=30 :
            뉴런번호 = 0
            뉴런들.sort(key=lambda 뉴런: 뉴런.적합도 )
            뉴런들[0] = copy.deepcopy(뉴런그룹_레이어(6,15,4))
        else :
            pass
        뉴런 = 뉴런들[뉴런번호]
        뱀게임.새뱀만들기()

    else:
        뱀게임.뱀몸통.insert(0,새머리위치)
        if len(뱀게임.뱀몸통) > 뱀게임.뱀길이:
            뱀게임.뱀몸통.pop()

        # 뱀 먹이 체크. 뱀게임.뱀몸통[0]
        if 새머리위치 == 뱀게임.먹이위치 :
            뉴런.적합도 += 적합도먹이
            뱀게임.앙()
            뱀게임.먹이만들기()
            뉴런.움직임제한 = 0



    뱀게임.게임_구동()
    
    # 화면에 글씨 넣기.
    뱀게임.글씨넣기("시작",(5,25),(255,0,0))

    # 도너트형 원 그리기.
    for i in range(뉴런.입력개수):
        뱀게임.게임.draw.circle(뱀게임.화면, (51,255,51),(700,200+i*30),10,2)
    for i in range(뉴런.뉴런개수):
        뱀게임.게임.draw.circle(뱀게임.화면, (51,255,51),(800,200+i*30),10,2)
    for i in range(뉴런.뉴런개수):
        뱀게임.게임.draw.circle(뱀게임.화면, (51,255,51),(900,200+i*30),10,2)
    for i in range(뉴런.뉴런개수):
        뱀게임.게임.draw.circle(뱀게임.화면, (51,255,51),(1000,200+i*30),10,2)
    for i in range(뉴런.출력개수):
        뱀게임.게임.draw.circle(뱀게임.화면, (51,255,51),(1100,200+i*30),10,2)


    뱀게임.게임.draw.circle(뱀게임.화면, (입력[0]/3,0,0),(700,200),8)
    뱀게임.게임.draw.circle(뱀게임.화면, (입력[1]/3,0,0),(700,200+30),8)

    뱀게임.게임.draw.circle(뱀게임.화면, (입력[2]/3,0,0),(700,200+60),8)
    뱀게임.게임.draw.circle(뱀게임.화면, (입력[3]/3,0,0),(700,200+90),8)

    뱀게임.게임.draw.circle(뱀게임.화면, ((입력[4]+1)*100,0,0),(700,200+120),8)
    뱀게임.게임.draw.circle(뱀게임.화면, ((입력[5]+1)*100,0,0),(700,200+150),8)

    if len(뉴런.레이어) != 0:
        원그리기(뱀게임,뉴런,1)
        원그리기(뱀게임,뉴런,3)
        원그리기(뱀게임,뉴런,5)
        원그리기(뱀게임,뉴런,7)




    뱀게임.표시()




