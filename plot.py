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

# ------------------------------
vf = 1000 # mm.min-1 # suggested:20-30
rpm = 60 # rounds.min-1 # suggested: 60-100
d0 = 154 # mm # suggested: 154 - 254

framerate = 120 # Hz # suggested:120
theta0 = 0*np.pi # rad # suggested:0
oncycle = 0.5 # 0.5 stops the cutting when reach the center
# ------------------------------

x0 = d0/2*np.cos(theta0)
y0 = d0/2*np.sin(theta0)

om = rpm*2*np.pi/60 # rad / s
T = (2*x0)/vf*60 #s
nframes = round(framerate*T)
dT = np.round(1000/framerate)

# First set up the figure, the axis, and the plot element we want to animate
# note that "line, " means to take the first element of the return value for ax.plot
fig = plt.figure(figsize=(8, 8), dpi=80)
ax = plt.axes(xlim=(-d0*0.7, d0*0.7), ylim=(-d0*0.7, d0*0.7))
line, = ax.plot([], [], 'k')
point, = ax.plot(0,0,'ro')
inlet, = ax.plot(x0,y0,'bo')

cutpoints = [[],[]]

#create the disk
theta = np.linspace(0,2*np.pi,200)
xc = d0/2*np.cos(theta)
yc = d0/2*np.sin(theta)
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

    dt = om/framerate

    x = x0 - vf/60/framerate*i
    y = y0

    data = disk.get_data()
    rot = np.array([[np.cos(dt),np.sin(dt)],[-np.sin(dt),np.cos(dt)]])
    rotation = np.matmul(rot,np.array(data))
    data2 = rotation.tolist()

    point.set_marker("")

    if(i/nframes < oncycle):
        data2[0].append(x)
        data2[1].append(y)
        point.set_marker("o")
        point.set_data(x, y)

    disk.set_data(data2)
    #inlet.set_data([[d0/2*np.cos(theta0-i*dt)],[d0/2*np.sin(theta0-i*dt)]])

    return line, point, disk, inlet,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nframes, interval=dT, blit=True, repeat=False)


plt.show()
