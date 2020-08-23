
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import animation

# ------------------------------
#vf = input("specifificare valore di Vf (mm/min): ") # mm.min-1 # suggested:20-30
vf = 30
# rpm = 10 # rounds.min-1 # suggested: 60-100
vmin = 10 # mm/min
vmax = 10000 # mm/min
d = 120 # mm # suggested: 154 - 254, 120 is the size of a CD
d0 = 15 # mm

framerate = 200 # Hz # suggested:divisor of 1000, like 100
#theta0 = 0*np.pi # rad # suggested:0
x0 = 10 # mm
y0 = 0 # mm
x1 = d/2 # mm
y1 = 0 # mm


ramp = 1
step = 0
# ------------------------------

vf = float(vf)
#x0 = d/2*np.cos(theta0)
#y0 = d/2*np.sin(theta0)

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
ax = plt.axes(xlim=(-d*0.5, d*0.5), ylim=(-d*0.5, d*0.5))

ranges = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

vrange10 = plt.Circle((0, 0), 0.05*d, color=(0.8, 0.8, 0.8))
vrange20 = plt.Circle((0, 0), 0.1*d, color=(1.0, 1.0, 1.0))
vrange30 = plt.Circle((0, 0), 0.15*d, color=(0.8, 0.8, 0.8))
vrange40 = plt.Circle((0, 0), 0.2*d, color=(1.0, 1.0, 1.0))
vrange50 = plt.Circle((0, 0), 0.25*d, color=(0.8, 0.8, 0.8))
vrange60 = plt.Circle((0, 0), 0.3*d, color=(1.0, 1.0, 1.0))
vrange70 = plt.Circle((0, 0), 0.35*d, color=(0.8, 0.8, 0.8))
vrange80 = plt.Circle((0, 0), 0.4*d, color=(1.0, 1.0, 1.0))
vrange90 = plt.Circle((0, 0), 0.45*d, color=(0.8, 0.8, 0.8))
vrange100 = plt.Circle((0, 0), 0.5*d, color=(1.0, 1.0, 1.0))

ax.add_artist(vrange100)
plt.text(0.5*d, 0, np.round(np.sqrt((vf)**2+(0.5*d*om0*60)**2)))
ax.add_artist(vrange90)
plt.text(-0.45*d, 0, np.round(vf+0.45*d*om0*60))
ax.add_artist(vrange80)
plt.text(0.4*d, 0, np.round(vf+0.4*d*om0*60))
ax.add_artist(vrange70)
plt.text(-0.35*d, 0, np.round(vf+0.35*d*om0*60))
ax.add_artist(vrange60)
plt.text(0.3*d, 0, np.round(vf+0.3*d*om0*60))
ax.add_artist(vrange50)
plt.text(-0.25*d, 0, np.round(vf+0.25*d*om0*60))
ax.add_artist(vrange40)
plt.text(0.2*d, 0, np.round(vf+0.2*d*om0*60))
ax.add_artist(vrange30)
plt.text(-0.15*d, 0, np.round(vf+0.15*d*om0*60))
ax.add_artist(vrange20)
plt.text(0.1*d, 0, np.round(vf+0.1*d*om0*60))
ax.add_artist(vrange10)
plt.text(-0.05*d, 0, np.round(vf+0.05*d*om0*60))

plt.text(-d/2, d/2+d/40, "traverse speed: "+str(vf)+" mm/min")
plt.text(-d/2, d/2+2*d/40, "rotation speed: "+str(rpm)+" rpm")
plt.text(-d/2, d/2+3*d/40, "min spiral step: "+str(2*np.pi/om0*vx0/60)+" mm")
plt.text(-d/2, d/2+4*d/40, "experiment duration: "+str(T)+" s")



line, = ax.plot([], [], 'k')
point, = ax.plot(0,0,'ro')
inlet, = ax.plot(x0,y0,'bo')

#create the disk
theta = np.linspace(0,2*np.pi,200)
xc = d/2*np.cos(theta)
yc = d/2*np.sin(theta)
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
    #inlet.set_data([[d/2*np.cos(theta0-i*dt)],[d/2*np.sin(theta0-i*dt)]])

    return line, point, disk, inlet,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nframes, interval=dT, blit=True, repeat=False)


plt.show()
