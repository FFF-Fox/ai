from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


d = ['A'] + [str(x) for x in range(2,11)]
D = len(d)
s = [str(x) for x in range(12,22)]
S = len(s)
a = [str(x) for x in range(2)]
V = {}

# Import data.
filename = 'fvmc.dat'

with open(filename,'r') as f:
    lines = f.readlines()

for line in lines:
    [state, value] = line.split(',')
    V[state] = value

x = range(D)
y = range(S)
X, Y = np.meshgrid(x, y)

Z = {}
for has_ace in a:
    Z[has_ace] = np.zeros((D,S))
    for i in range(D):
        for j in range(S):
            state = d[i] + ' ' + s[j] + ' ' + has_ace
            Z[has_ace][i,j] = V[state]

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z['0'], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Customize the x,y axis.
ax.set_xticklabels(s[::2])
ax.set_yticklabels(d[::2])

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()