import random as rnd
import numpy as np
import matplotlib.pyplot as plt

# N = Nerual, T = Time, P = Pattern, S = Nerual Network[T][N]
# Miu = Pattern Network[P][N], W = Weight[N][N]
N = 1000
T = 15
P = 100  # 200
Time = [i for i in range(T)]
S = np.ones((T+1, N), dtype=int)
Miu = np.random.randint(0, 2, size=[P, N])
W = np.zeros((N, N))

Seed = 1000
rnd.seed(Seed)

#Initalize Miu and Weight, to make the initalization of Nerual Network by overlap[0.1,1.0] easier
#I set pattern[0] as all 1 and the conclusion will be compared with pattern[0]
def init():
    global Miu, W

    for m in np.nditer(Miu, op_flags=['readwrite']):
        if m == 0:
            m -= 1

    Miu[0] = np.ones(N, dtype=int)

    for i in range(N):
        w = 0
        for j in range(i + 1, N):
            for p in range(P):
                w += Miu[p, i] * Miu[p, j]
            w /= N
            W[i][j] = w
            W[j][i] = w

#To inital Nerual Network by orignal overlap, I change the o percent to -1 and compare it with
#pattern[0] which is all 1
def Inital_S(o):
    global S
    S.fill(1)
    S[0] = [-1 if rnd.random() < ((1.0-o)/2) else 1 for i in range(N)]

def sgn(u):
    if u >= 0:
        return 1
    else:
        return -1

#Update Nerual Network
def RenewS(t):
    global S
    for i in range(N):
        s = 0
        for j in range(N):
            if i != j:
                s += W[i, j] * S[t, j]
        s = sgn(s)
        S[t + 1, i] = s

#Calculate overlap
def memo(t):
    m = 0
    for i in range(N):
        m += Miu[0, i] * S[t, i]
    m /= N
    return m

#Run one time for a nerual network to memorize itself
def Run(o):
    m = []
    Inital_S(o)
    for t in range(T):
        m.append(memo(t))
        RenewS(t)
    return m

init()

fig = plt.figure()
for i in range(10):
    o = i/10
    Overlap = Run(o)
    plt.plot(Time, Overlap)
    print(Overlap)
plt.xlabel('Time')
plt.ylabel('Overlap')
plt.show()
