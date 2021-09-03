import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import random as rnd

L = 10
SEED = 101
rnd.seed(SEED)

t1 = [6, 9, 7, 1, 5, 8, 3, 2, 4, 0]
t2 = [9, 6, 7, 1, 5, 8, 2, 4, 0, 3]


def checkRepeat(i, split):
    for j in split:
        if j == i:
            return True
    return False


def crossover(a1, a2):
    o1 = a1
    o2 = a2
    # point1 = rnd.randint(0, L - 1)
    # point2 = rnd.randint(point1, L)

    point1 = 7
    point2 = 9

    print("p1:" + str(point1) + ",p2:" + str(point2))

    for i in range(point1, point2):
        o1[i], o2[i] = o2[i], o1[i]
    print(str(o1))
    print(str(o2))
    m1 = o1[point1:point2]
    m2 = o2[point1:point2]
    print(str(m1))
    counter1 = 0
    counter2 = 0
    for i in range(0, L):
        sp1 = []
        sp2 = []
        if i < point1:
            sp1 = m1
            sp1 += (o1[:i])
            sp2 = m2
            sp2 += (o2[:i])
        elif i >= point2:
            sp1 += o1[:i]
            sp2 += o2[:i]
            print("1")
        else:
            continue
        while checkRepeat(o1[i], sp1):
            o1[i] = counter1
            counter1 += 1
        while checkRepeat(o2[i], sp2):
            o2[i] = counter2
            counter2 += 1

    return o1, o2


p1, p2 = crossover(t1, t2)
print("S1:" + str(p1))
print("S2:" + str(p2))
