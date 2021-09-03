import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy as sps
from scipy.special import comb, perm
from scipy.stats import beta

rnd.seed(100)

T = 15
a = 0.5
b = 0.5
miu = np.arange(0.01, 1, 0.01)
density = []

fig= plt.figure()

def update(t):
    fig.clear()
    global a, b
    if t != 0:
        if a == 0.5:
            a = 1
            b = 1
        elif a == 1:
            a = 2
            b = 3
        else:
            a += 1
            b += 1
    density = beta.pdf(miu,a,b)
    plt.plot(miu, density)
    plt.xlabel('m')
    plt.ylabel('Density')
    # plt.ylim(ymin = 0.0, ymax = 3.0)
    plt.title('a = '+ str(a)+', b = '+ str(b))


ani = animation.FuncAnimation(fig, update, np.arange(0, T+1), interval=500, repeat=False)
ani.save('test.gif', writer='pillow')
plt.show()







