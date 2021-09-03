import matplotlib

import matplotlib.animation as animation

import numpy as np
import matplotlib.pyplot as plt
import random as rnd

from numpy.ma import count

N = 500
T = 500
W = 30
TH = 0.85
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
        if self.p == 0:
            self.color = "blue"
        else:
            self.color = "red"

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
        if (self.isOverlapped()):
            self.findNewSpace()

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


rnd.seed(Seed)
for i in range(N):
    a = Agent(i%2)
    a.findNewSpace()
    agents.append(a)

#agents = [Agent() for i in range(N)]

fig = plt.figure()
average = []
Time = []

def main_loop(t):
    step()
    update(t)

def step():
    rnd.shuffle(agents)
    for a in agents:
        a.seek()

def update(t):
    fig.clear()
    ax1 = fig.add_subplot(2, 2, 1)
    x1 = [a.x for a in agents if a.p == 0]
    y1 = [a.y for a in agents if a.p == 0]
    x2 = [a.x for a in agents if a.p == 1]
    y2 = [a.y for a in agents if a.p == 1]

    x = [a.x for a in agents]
    y = [a.y for a in agents]
    s = [a.s for a in agents]
    average.append(np.mean(s))
    Time.append(t)


    ax1.scatter(x1, y1, color = "red", s = 0.3)
    ax1.scatter(x2, y2, color = "blue", s = 0.3)
    ax1.axis([-1, W, -1, W])
    ax1.set_title('t = ' + str(t))

    # ax2 = fig.add_subplot(2, 3, 3)
    # ax2.hist(x, W)
    # ax2.axis([-1, W, -1, W])
    #
    # ax3 = fig.add_subplot(2, 3, 4)
    # ax3.hist(y, W)
    # ax3.axis([-1, W, -1, W])

    ax4 = fig.add_subplot(2, 2, 3)
    ax4.plot(Time,average)
#    ax4.axis([-1, T, -1, 1])

    ax5 = fig.add_subplot(2, 2, 4)
    ax5.hist(s, color = "red", rwidth=1)
    ax5.axis([0, 1, -1, N])



ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=25, repeat=False)
plt.show()
