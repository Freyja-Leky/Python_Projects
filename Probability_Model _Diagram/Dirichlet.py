import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

rng = np.random.default_rng()
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd

T = 10
alpha = [0.1, 0.1, 0.1]
rv = stats.dirichlet.rvs([1,1,1], 3000)
rvs = rv[:,0:2]
list = []
x = rv[:,0]
y = rv[:,1]

# for i in rv:
#     pdf = stats.dirichlet.pdf(i, alpha)
#     list.append(pdf)

fig = plt.figure(dpi=150)

# ax = fig.add_subplot(projection='3d')
# ax.view_init(30, 60)  #仰角30°方位角60°
# # ax.scatter(rvs[:,0],rvs[:,1],list)
# ax.plot_trisurf(x, y, list)

def update(t):

    fig.clear()
    global alpha, list
    list.clear()
    if t > 0:
        if alpha[0] == 0.1:
            alpha = [1.0 ,1.0 ,1.0]
        else:
            alpha = [i+1 for i in alpha]
    for i in rv:
        pdf = stats.dirichlet.pdf(i, alpha)
        list.append(pdf)
    ax = fig.add_subplot(projection='3d')
    ax.plot_trisurf(x, y, list)
    # ax.view_init(30, 60)  #仰角30°方位角60°
    ax.set_title ("ak = "+str(alpha[0]))

ani = animation.FuncAnimation(fig, update, np.arange(0, T+1), interval=500, repeat=False)
ani.save('test.gif', writer='pillow')
plt.show()
