from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def state_value_of(state):
    return V[state]

fig = plt.figure()
ax = fig.gca(projection='3d')

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
            Z[has_ace][i,j] = state_value_of(state)

print(Z)

# # Make data.
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z['1'], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Customize the x axis.
# TODO: change the x and y ticks
# ax.set_xticks(d)

# ax.set_yticks(s)

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()