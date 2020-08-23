
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import animation

# ------------------------------
vc0 = 50 # mm/min
vc1 = 100000 # mm/min
pmin = 1 # mm minimum distance between channels

dmax = 120 # mm # suggested: 154 - 254, 120 is the size of a CD
dmin = 15 # mm

d0 = 15
d1 = 120

framerate = 50 # Hz # suggested:divisor of 1000, like 100
# ------------------------------

# initial point coordinates
x0 = d0/2
y0 = 0

# convert mm/minto mm/s
vc0 = vc0/60
vc1 = vc1/60

om1 = np.sqrt((vc1**2)/((pmin/2/np.pi)**2 + (d1/2)**2)) # rad / s
vf = pmin*om1/2/np.pi # mm/s

# check that vc0 is at least equal to vf
vc0 = max([vc0,vf])

# check that vc0 is smaller than the maximum allowed initial speed
vc0 = min([vc0,np.sqrt(vf**2+(d0/2*om1)**2)])

om0 = np.sqrt((vc0**2-vf**2)/(d0/2)**2) # rad / s

L = (d1-d0)/2 # mm
T = L/vf #s

nframes = round(framerate*T)
dT = 1000/framerate # ms

dl = vf*dT/1000 # mm


# First set up the figure, the axis, and the plot element we want to animate
# note that "line, " means to take the first element of the return value for ax.plot



fig = plt.figure(figsize=(8, 8), dpi=80)
ax = plt.axes(xlim=(-d1*0.5, d1*0.5), ylim=(-d1*0.5, d1*0.5))

# ranges = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#
# vrange10 = plt.Circle((0, 0), 0.05*d1, color=(0.8, 0.8, 0.8))
# vrange20 = plt.Circle((0, 0), 0.1*d1, color=(1.0, 1.0, 1.0))
# vrange30 = plt.Circle((0, 0), 0.15*d1, color=(0.8, 0.8, 0.8))
# vrange40 = plt.Circle((0, 0), 0.2*d1, color=(1.0, 1.0, 1.0))
# vrange50 = plt.Circle((0, 0), 0.25*d1, color=(0.8, 0.8, 0.8))
# vrange60 = plt.Circle((0, 0), 0.3*d1, color=(1.0, 1.0, 1.0))
# vrange70 = plt.Circle((0, 0), 0.35*d1, color=(0.8, 0.8, 0.8))
# vrange80 = plt.Circle((0, 0), 0.4*d1, color=(1.0, 1.0, 1.0))
# vrange90 = plt.Circle((0, 0), 0.45*d1, color=(0.8, 0.8, 0.8))
# vrange100 = plt.Circle((0, 0), 0.5*d1, color=(1.0, 1.0, 1.0))
#
# ax.add_artist(vrange100)
# plt.text(0.5*d1, 0, np.round(np.sqrt((vf)**2+(0.5*d1*om0*60)**2)))
# ax.add_artist(vrange90)
# plt.text(-0.45*d1, 0, np.round(vf+0.45*d1*om0*60))
# ax.add_artist(vrange80)
# plt.text(0.4*d1, 0, np.round(vf+0.4*d1*om0*60))
# ax.add_artist(vrange70)
# plt.text(-0.35*d1, 0, np.round(vf+0.35*d1*om0*60))
# ax.add_artist(vrange60)
# plt.text(0.3*d1, 0, np.round(vf+0.3*d1*om0*60))
# ax.add_artist(vrange50)
# plt.text(-0.25*d1, 0, np.round(vf+0.25*d1*om0*60))
# ax.add_artist(vrange40)
# plt.text(0.2*d1, 0, np.round(vf+0.2*d1*om0*60))
# ax.add_artist(vrange30)
# plt.text(-0.15*d1, 0, np.round(vf+0.15*d1*om0*60))
# ax.add_artist(vrange20)
# plt.text(0.1*d1, 0, np.round(vf+0.1*d1*om0*60))
# ax.add_artist(vrange10)
# plt.text(-0.05*d1, 0, np.round(vf+0.05*d1*om0*60))

label_vf = ax.text(-d1/2, d1/2+d1/40, "traverse speed: "+str(round(vf*60))+" mm/min")
label_rpm = ax.text(-d1/2, d1/2+2*d1/40, "")
label_vc = ax.text(-d1/2, d1/2+3*d1/40, "")
label_T = ax.text(-d1/2, d1/2+4*d1/40, "")



line, = ax.plot([], [], 'k')
point, = ax.plot(0,0,'ro')
inlet, = ax.plot(x0,y0,'bo')

#create the disk =========================
theta = np.linspace(0,2*np.pi,200)
xc0 = d0/2*np.cos(theta)
yc0 = d0/2*np.sin(theta)
xc1 = d1/2*np.cos(theta)
yc1 = d1/2*np.sin(theta)

ax.plot(xc0,yc0,'k')
ax.plot(xc1,yc1,'k')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    point.set_data(x0,y0)
    label_rpm.set_text("")
    label_vc.set_text("")
    label_T.set_text("")

    return point, line, label_rpm, label_vc, label_T

# animation function.  This is called sequentially
def animate(i):

    om = i*(om1-om0)/nframes + om0
    dt = om/framerate

    rot = np.array([[np.cos(dt),np.sin(dt)],[-np.sin(dt),np.cos(dt)]])

    #x = x0 - vf/60/framerate*i
    x = x0 + i*dl
    y = y0

    #if(x<0):
    #    dt = -dt

    #ddata = disk.get_data()
    ldata = line.get_data()

    #rotation = np.matmul(rot,np.array(ddata))
    #ddata2 = rotation.tolist()

    rotation = np.matmul(rot,np.array(ldata))
    ldata2 = rotation.tolist()

    point.set_marker("")

    ldata2[0].append(x)
    ldata2[1].append(y)
    point.set_marker("o")
    point.set_data(x, y)

    #disk.set_data(ddata2)
    line.set_data(ldata2)
    #inlet.set_data([[d1/2*np.cos(theta0-i*dt)],[d1/2*np.sin(theta0-i*dt)]])

    label_rpm.set_text("rotation speed: "+str(np.round(om*60/2/np.pi))+" rpm")
    label_vc.set_text("cutting speed: "+str(round(np.sqrt((vf**2+(x*om)**2))*60))+" mm/min")
    label_T.set_text("experiment time: "+str(i*dT/1000)+"/"+str(round(T))+" s")

    return point, line, label_rpm, label_vc, label_T

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nframes, interval=dT, blit=False, repeat=False)


plt.show()
