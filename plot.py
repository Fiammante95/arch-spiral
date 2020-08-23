
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import animation

# ------------------------------
#vf = input("specifificare valore di Vf (mm/min): ") # mm.min-1 # suggested:20-30
vf = 500
rpm = 100 # rounds.min-1 # suggested: 60-100
d0 = 154 # mm # suggested: 154 - 254

framerate = 100 # Hz # suggested:120
#theta0 = 0*np.pi # rad # suggested:0
x0 = 10 # mm
y0 = 0
x1 = d0/2
y1 = 0

ramp = 0.01
step = 0
# ------------------------------

vf = float(vf)
#x0 = d0/2*np.cos(theta0)
#y0 = d0/2*np.sin(theta0)

L = np.sqrt((x1-x0)**2+(y1-y0)**2)

theta0 = np.arctan((y1-y0)/(x1-x0))

vx0 = vf*np.cos(theta0)
vy0 = vf*np.sin(theta0)

om0 = rpm*2*np.pi/60 # rad / s
#T = (2*x0)/vf*60 #s
T = L/vf*60 #s
nframes = round(framerate*T)
dT = 1000/framerate #ms

dx = vx0*dT/1000/60
dy = vy0*dT/1000/60

j = 0

# First set up the figure, the axis, and the plot element we want to animate
# note that "line, " means to take the first element of the return value for ax.plot



fig = plt.figure(figsize=(8, 8), dpi=80)
ax = plt.axes(xlim=(-d0*0.7, d0*0.7), ylim=(-d0*0.7, d0*0.7))

vrange10 = plt.Circle((0, 0), 0.05*d0, color=(0.8, 0.8, 0.8))
vrange20 = plt.Circle((0, 0), 0.1*d0, color=(1.0, 1.0, 1.0))
vrange30 = plt.Circle((0, 0), 0.15*d0, color=(0.8, 0.8, 0.8))
vrange40 = plt.Circle((0, 0), 0.2*d0, color=(1.0, 1.0, 1.0))
vrange50 = plt.Circle((0, 0), 0.25*d0, color=(0.8, 0.8, 0.8))
vrange60 = plt.Circle((0, 0), 0.3*d0, color=(1.0, 1.0, 1.0))
vrange70 = plt.Circle((0, 0), 0.35*d0, color=(0.8, 0.8, 0.8))
vrange80 = plt.Circle((0, 0), 0.4*d0, color=(1.0, 1.0, 1.0))
vrange90 = plt.Circle((0, 0), 0.45*d0, color=(0.8, 0.8, 0.8))
vrange100 = plt.Circle((0, 0), 0.5*d0, color=(1.0, 1.0, 1.0))

ax.add_artist(vrange100)
ax.add_artist(vrange90)
ax.add_artist(vrange80)
ax.add_artist(vrange70)
ax.add_artist(vrange60)
ax.add_artist(vrange50)
ax.add_artist(vrange40)
ax.add_artist(vrange30)
ax.add_artist(vrange20)
ax.add_artist(vrange10)

line, = ax.plot([], [], 'k')
point, = ax.plot(0,0,'ro')
inlet, = ax.plot(x0,y0,'bo')

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
    global j
    if(i/nframes < step):
        dt = 0
        j = j + 1

    else:
        dt = om0*((i-j)/(ramp*nframes))/framerate

    if((i-j)/nframes > ramp):
        dt = om0/framerate

    rot = np.array([[np.cos(dt),np.sin(dt)],[-np.sin(dt),np.cos(dt)]])

    #x = x0 - vf/60/framerate*i
    x = x0 + i*dx
    y = y0 + i*dy

    #if(x<0):
    #    dt = -dt

    ddata = disk.get_data()
    ldata = line.get_data()

    rotation = np.matmul(rot,np.array(ddata))
    ddata2 = rotation.tolist()

    rotation = np.matmul(rot,np.array(ldata))
    ldata2 = rotation.tolist()

    point.set_marker("")

    ldata2[0].append(x)
    ldata2[1].append(y)
    point.set_marker("o")
    point.set_data(x, y)

    disk.set_data(ddata2)
    line.set_data(ldata2)
    #inlet.set_data([[d0/2*np.cos(theta0-i*dt)],[d0/2*np.sin(theta0-i*dt)]])

    return line, point, disk, inlet,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nframes, interval=dT, blit=True, repeat=False)


plt.show()
