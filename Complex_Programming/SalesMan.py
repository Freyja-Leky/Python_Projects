
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import random as rnd

def clip(x):
    if x < 0:
        return (x + W)
    elif x >= W:
        return (x - W)
    else:
        return (x)

def gtypeToPtype(gtype):
    return gtype

def fitnessFunction(ptype):
    Route = 0
    for i in range(L-1):
        Route +=((Map[ptype[i]].x - Map[ptype[i+1]].x)**2+(Map[ptype[i]].y - Map[ptype[i+1]].y)**2)**0.5
    return Route

class Agent(object):
    def __init__(self, gtype):
        self.genotype = gtype[:]
        self.phenotype = self.genotype
        self.fitness = 0.0
        self.mute = False
        self.Cross = False

    # def ini(self):
    #     self.mute = False
    #     self.Cross = False

    def getOffspring(self):
        o = Agent(self.genotype)
        for i in range(L):
            if (rnd.random() < MUT):
                j = rnd.randint(1,L-1)
                o.genotype[i], o.genotype[j] = o.genotype[j], o.genotype[i]
                self.mute = True
                # o.genotype[i] = 1 - o.genotype[i]
        return (o)

    def develop(self, dfunc):
        self.phenotype= dfunc(self.genotype)

    def evaluate(self, efunc):
        self.fitness= efunc(self.genotype)


class City(object):
    def __init__(self):
        self.x = rnd.randint(0, W - 1)
        self.y = rnd.randint(0, W - 1)

    def randomwalk(self):
        self.x += rnd.randint(-1, 1)
        self.y += rnd.randint(-1, 1)
        self.x = clip(self.x)
        self.y = clip(self.y)

    def isOverlapped(self):
        for a in Map:
            if (a != self):
                if (a.x == self.x and a.y == self.y):
                    return True
        return False

    def findNewSpace(self):
        self.randomwalk()
        while (self.isOverlapped()):
            self.randomwalk()

def selectAnAgentByTournament(pop,order):
    pop.sort(key = lambda  x:x.fitness, reverse=False)
    return (pop[order])

def checkRepeat(i,split):
    for j in split:
        if j == i:
            return True
    return False


def crossover(a1, a2):
    # if (operator.eq(a1,a2)):
    #     return a1,a2
    o1 = a1
    o2 = a2
    point1 = rnd.randint(1, L - 1)
    point2 = rnd.randint(point1, L)
    # print("p1:"+str(point1)+"p2:"+str(point2))
    # print("F1")
    # print("a1:"+str(a1.genotype))
    # print("a2:"+str(a2.genotype))
    # print("o1:"+str(o1.genotype))
    # print("o2:"+str(o2.genotype))

    for i in range(point1, point2):
        # print(str(o1.genotype[i]))
        # print(str(o2.genotype[i]))
        temp = o1.genotype[i]
        o1.genotype[i]=o2.genotype[i]
        o2.genotype[i]=temp
        # o1.genotype[i], o2.genotype[i] = o2.genotype[i], o1.genotype[i]
    # print("F2")
    # print("o1:"+str(o1.genotype))
    # print("o2:"+str(o2.genotype))
    m1 = o1.genotype[point1:point2]
    m2 = o2.genotype[point1:point2]
    counter1 = 0
    counter2 = 0
    for i in range(0, L):
        sp1 = []
        sp2 = []
        if i < point1:
            sp1 = m1
            sp1 += (o1.genotype[:i])
            sp2 = m2
            sp2 += (o2.genotype[:i])
        elif i >= point2:
            sp1 += o1.genotype[:i]
            sp2 += o2.genotype[:i]
        else:
            continue
        while checkRepeat(o1.genotype[i], sp1):
            o1.genotype[i] = counter1
            counter1 += 1
        while checkRepeat(o2.genotype[i], sp2):
            o2.genotype[i] = counter2
            counter2 += 1
    # print("F3")
    # print("o1:"+str(o1.genotype))
    # print("o1:"+str(o2.genotype))
    o1.Cross = True
    o2.Cross = True
    return o1, o2

#N for Gene, L for city and the length
SEED=101
T = 100
W = 30
N = 30
L = 30
MUT= 0.05
CROSS= 0.2
rnd.seed(SEED)
fig= plt.figure()

Map = []
for i in range(L):
    c = City()
    c.findNewSpace()
    Map.append(c)

No = [i for i in range(L)]
population= [Agent(rnd.sample(No,L)) for i in range(N)]

averageFitness= []
bestFitness= []
best = population[0]

# def check(gene):
#     for i in range(L):
#         for j in range(L):
#             if (gene[i]==gene[j] and i!=j):
#                 return False
#     return True
#
# for g in population:
#     print(str(g.genotype))
#     print(str(check(g.genotype)))

def main_loop(t):
    step()
    update(t)

def step():
    global population,best
    best = population[0]
    for p in population:
        p.evaluate(fitnessFunction)
        if p.fitness < best.fitness:
            best = p
    averageFitness.append(np.average([a.fitness for a in population]))
    bestFitness.append(best.fitness)

    print(str(best.genotype) + ":" + str(best.fitness))
    # print("Mute"+str(best.mute))
    # print("Cross"+str(best.Cross))

    newpop = []
    for i in range(int(N / 2)):
        n1 = selectAnAgentByTournament(population,i).getOffspring()
        n2 = selectAnAgentByTournament(population,i+1).getOffspring()

        s1 = n1
        s2 = n2

        if rnd.random() < CROSS:
            s1,s2 = crossover(n1, n2)
        newpop.append(s1)
        newpop.append(s2)

    population = newpop


def update(t):
    fig.clear()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title('T = ' + str(t))
    ax1.axis([-1, W, -1, W])
    xd = [m.x for m in Map]
    yd = [m.y for m in Map]
    ax1.scatter(xd,yd)
    for i in range(L-1):
        start = Map[best.phenotype[i]]
        end = Map[best.phenotype[i+1]]
        plt.arrow(start.x,start.y,end.x-start.x,end.y-start.y,length_includes_head = True)

    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(averageFitness)
    ax2.plot(bestFitness)
    ax2.set_xlabel("generaiton")
    ax2.set_ylabel("average / best fitness")

ani = animation.FuncAnimation(fig, main_loop, np.arange(0, T), interval=25, repeat=False)
plt.show()

