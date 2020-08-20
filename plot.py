"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.special import expit, logit

# First set up the figure, the axis, and the plot element we want to animate
# note that "line, " means to take the first element of the return value for ax.plot
fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], 'k')
point, = ax.plot(0,0,'ro')

cutpoints = [[],[]]

#create the disk
theta = np.linspace(0,2*np.pi,200)
xc = np.cos(theta)
yc = np.sin(theta)
#xl = np.linspace(0,1,100)
#yl = np.linspace(0,0,100)
#x = np.concatenate((xc,xl))
#y = np.concatenate((yc,yl))
disk, = ax.plot(xc,yc,'k')


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    point.set_data(0,0)
    return line, point, disk,

# animation function.  This is called sequentially
def animate(i):

    dt = np.pi/300
    if(i>2500):
        dt = -np.pi/300

    x = (1-i/2500)
    y = 0

    data = disk.get_data()
    rot = np.array([[np.cos(dt),np.sin(dt)],[-np.sin(dt),np.cos(dt)]])
    rotation = np.matmul(rot,np.array(data))
    data2 = rotation.tolist()
    data2[0].append(x)
    data2[1].append(y)
    disk.set_data(data2)
    point.set_data(x, y)

    return line, point, disk,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=5000, interval=1, blit=True, repeat=False)


plt.show()
