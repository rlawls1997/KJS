import numpy as np

class 인공지능클래스():
    def __init__(self,입력개수,뉴런개수,출력개수):
        self.fitness = 0
        
        self.w1 = np.random.randn(입력개수, 뉴런개수)
        self.w2 = np.random.randn(뉴런개수, 뉴런개수*2)
        self.w3 = np.random.randn(뉴런개수*2, 뉴런개수)
        self.w4 = np.random.randn(뉴런개수, 출력개수)

        self.b1 = np.random.randn(입력개수)
        self.b2 = np.random.randn(뉴런개수)
        self.b3 = np.random.randn(뉴런개수*2)
        self.b4 = np.random.randn(뉴런개수)

        print(self.w1)
        print(self.w2)
        print(self.w3)
        print(self.w4)
    def 계산(self, inputs):
        net = np.matmul(inputs, self.w1)
        net = self.relu(net)
        net = np.matmul(net, self.w2)
        net = self.relu(net)
        net = np.matmul(net, self.w3)
        net = self.relu(net)
        net = np.matmul(net, self.w4)
        net = self.softmax(net)
        return net

    def relu(self, x):
        return x * (x >= 0)

    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def leaky_relu(self, x):
        return np.where(x > 0, x, x * 0.01)