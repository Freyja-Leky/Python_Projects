
import numpy as np
import matplotlib.pyplot as plt
import random as rnd


N = 500
T = 100
W = 30
Seed = 101
agents = []


def clip(x):
    if x < 0:
        return (x + W)
    elif x >= W:
        return (x - W)
    else:
        return (x)

class Agent(object):

    def __init__(self,sp):
        self.x = rnd.randint(0, W - 1)
        self.y = rnd.randint(0, W - 1)
        self.s = 0
        self.p = sp

    def randomwalk(self):
        self.x += rnd.randint(-1, 1)
        self.y += rnd.randint(-1, 1)
        self.x = clip(self.x)
        self.y = clip(self.y)

    def isOverlapped(self):
        for a in agents:
            if (a != self):
                if (a.x == self.x and a.y == self.y):
                    return True
        return False


    def findNewSpace(self):
        self.randomwalk()
        while self.isOverlapped():
            self.randomwalk()

    def updateSatisfaction(self):
        neighbors = []
        for a in agents:
            if ((a != self) and (abs(a.x-self.x)<=1 and abs(a.y-self.y)<=1)):
                neighbors.append(a)
        neighborsCount = len(neighbors)
        if (neighborsCount == 0):
            self.s = 0
        else:
            sameCount = [a for a in neighbors if (a.p == self.p)]
            s = len(sameCount)/neighborsCount
            self.s = s

    def seek(self):
        self.updateSatisfaction()
        if (self.s<TH):
            self.findNewSpace()


average = []
TH_Series = []

def init():
    rnd.seed(Seed)
    agents.clear()
    for i in range(N):
        a = Agent(i % 2)
        a.findNewSpace()
        agents.append(a)

def loop():
    for t in range(T):
        step()

def step():
    rnd.shuffle(agents)
    for a in agents:
        a.seek()

def update():
    s = [a.s for a in agents]
    average.append(np.mean(s))


for i in range(10):
    TH = i/10
    TH_Series.append(TH)
    init()
    loop()
    update()

fig = plt.figure()
plt.plot(TH_Series,average)
plt.show()
