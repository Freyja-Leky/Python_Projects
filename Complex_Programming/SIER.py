import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import random as rnd

N = 500
T = 100
W = 30

#PR for possibility of recover, PI for infection, PF for the inital proportion of I, PE for E to I, TE is the last time of E
PR = 0.03
PI = 0.05
PF = 0.01
PE = 0.1
TE = 10
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

    def __init__(self, status):
        self.x = rnd.randint(0, W - 1)
        self.y = rnd.randint(0, W - 1)
        self.s = status
        self.t = 0

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
        while (self.isOverlapped()):
            self.randomwalk()

    def infection(self, time):
        for a in agents:
            if ((a != self) and (abs(a.x - self.x) <= 1 and abs(a.y - self.y) <= 1) and a.s == 'S'):
                if (rnd.random() < PI):
                    a.s = 'E'
                    a.t = time


    def recover(self):
        self.s = 'R' if rnd.random() < PR else self.s

#If an E agent is still during incubation period, it will turn into I by PE; if the period is end, it will turn into R
    def E2IorR(self,time):
        if time - self.t < TE:
            self.s = 'I' if rnd.random() < PE else self.s
        else:
            self.s = 'R'

    def updateStatus(self, time):
        if self.s == 'I':
            self.infection(time)
            self.recover()
        elif self.s == 'E':
            self.randomwalk()
            self.infection(time)
            self.E2IorR(time)
        else:
            self.randomwalk()

rnd.seed(Seed)
for i in range(N):
    a = Agent('I' if rnd.random() < PF else 'S')
    a.findNewSpace()
    agents.append(a)

fig = plt.figure()

def main_loop(t):
    step(t)
    update(t)

def step(time):
    rnd.shuffle(agents)
    for a in agents:
        a.updateStatus(time)

s = []
i = []
r = []
e = []
tl =[]

def update(t):
    fig.clear()
    ax = fig.add_subplot(2,2,1)
    x1 = [a.x for a in agents if a.s == 'S']
    y1 = [a.y for a in agents if a.s == 'S']
    x2 = [a.x for a in agents if a.s == 'I']
    y2 = [a.y for a in agents if a.s == 'I']
    x3 = [a.x for a in agents if a.s == 'R']
    y3 = [a.y for a in agents if a.s == 'R']
    x4 = [a.x for a in agents if a.s == 'E']
    y4 = [a.y for a in agents if a.s == 'E']

    ax.scatter(x1, y1, color='blue', s=0.8)
    ax.scatter(x2, y2, color='red', s=0.8)
    ax.scatter(x3, y3, color='green', s=0.8)
    ax.scatter(x4, y4, color='orange', s=0.8)

    ax.axis([-1, W, -1, W])
    ax.set_title('t = ' + str(t))

    bx = fig.add_subplot(2,2,3)
    HD = [len(x1), len(x2), len(x4), len(x3)]
    scale = np.arange(4)
    str1 = ["S","I","E","R"]
    bx.bar(scale,height = HD, tick_label = str1)
    bx.set_ylim(-1,500)

    cx = fig.add_subplot(2,2,4)
    s.append(len(x1))
    i.append(len(x2))
    r.append(len(x3))
    e.append(len(x4))
    tl.append(t)
    cx.plot(tl,s,color = 'blue')
    cx.plot(tl,i,color = 'red')
    cx.plot(tl,r,color = 'green')
    cx.plot(tl,e, color = 'orange')
    cx.set_ylim(-1, 500)
    cx.set_xlim(-1,T)
    # cx.legend()

    dx = fig.add_subplot(2,2,2)
    dx.text (0.1,0.1,"blue = S", color = 'blue')
    dx.text (0.1,0.2,"red = I", color = 'red')
    dx.text(0.1, 0.3, "orange = E", color='orange')
    dx.text(0.1, 0.4, "green = R", color='green')



ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=25, repeat=False)
plt.show()