import numpy as np
from matplotlib import pyplot as plt

dt = np.pi/3

x = [0,1,2]
y = [0,0,1]

rot = np.array([[np.cos(dt),np.sin(dt)],[-np.sin(dt),np.cos(dt)]])

result = np.matmul(rot,np.array([x,y]))

output = result.tolist()
print(output)

plt.plot(x,y,'k')
plt.plot(output[0],output[1],'r')

plt.show()
