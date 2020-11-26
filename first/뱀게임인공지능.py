import numpy as np

class 뉴런그룹_레이어(object):

    def __init__(self,입력개수,뉴런개수,출력개수):
        self.적합도 = 0
        self.입력개수 = 입력개수
        self.뉴런개수 = 뉴런개수
        self.출력개수 = 출력개수
        #   만약 뉴런개수 = 6
        #   6-12-12
        self.w1 = np.random.randn(self.입력개수, self.뉴런개수)
        self.w2 = np.random.randn(self.뉴런개수, self.뉴런개수)      
        self.w3 = np.random.randn(self.뉴런개수, self.출력개수)       

        self.b1 = np.random.randn(self.뉴런개수)
        self.b2 = np.random.randn(self.뉴런개수)
        self.b3 = np.random.randn(self.출력개수)

        self.레이어 = []

    def 계산(self, inputs):
        self.레이어.insert(0,np.matmul(      inputs, self.w1)+self.b1)
        self.레이어.insert(1,self.상하한값(  self.레이어[0]))
        self.레이어.insert(2,np.matmul(      self.레이어[1], self.w2)+self.b2)
        self.레이어.insert(3,self.상하한값(  self.레이어[2]))
        self.레이어.insert(4,np.matmul(      self.레이어[3], self.w3)+self.b3)
        self.레이어.insert(5,self.상하한값(  self.레이어[4]))
        return self.레이어[5]

    def 상하한값(self, x):
        return 1/(1+np.exp(x))

    def 계산리턴(self,레이어번호):
        return self.레이어[레이어번호]
