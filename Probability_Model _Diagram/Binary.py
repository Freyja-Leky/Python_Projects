import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.special import comb, perm

rnd.seed(100)

N = 100
T = 20
miu = 0.00
data = []
M = [i for i in range(N+1)]

fig= plt.figure()

def Binomial(N,m):
    return (miu**m)*((1-miu)**(N-m))*comb(N,m)

def update(t):
    fig.clear()
    data.clear()
    global miu
    miu = t*0.05
    for m in range (N+1):
        data.append(Binomial(N,m))
    print(str(data))
    plt.plot(M, data)
    plt.xlabel('m')
    plt.ylabel('Bin(m)')
    plt.ylim(ymin = 0.0, ymax = 0.2)
    plt.title('Miu = '+ str(round(miu,2)))


ani = animation.FuncAnimation(fig, update, np.arange(0, T+1), interval=300, repeat=False)
ani.save('test.gif', writer='pillow')
plt.show()







