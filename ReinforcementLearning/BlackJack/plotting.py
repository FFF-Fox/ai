import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

# Argument handling.
parser = argparse.ArgumentParser(description="Plot the state value function V(s)")
parser.add_argument('-f', '--filename', help='specify the file to load the values for plotting', type=str)

args = parser.parse_args()

# Enumerate the different parameters of each state.
d = ['A'] + [str(x) for x in range(2,11)]
D = len(d)
s = [str(x) for x in range(12,22)]
S = len(s)
a = [str(x) for x in range(2)]

# Import data.
if args.filename:
    filename = args.filename
else:
    filename = 'results.dat'

with open(filename,'r') as f:
    lines = f.readlines()

# Populate the V(s) dictionary.
V = {}
for line in lines:
    [state, value] = line.split(',')
    V[state] = value

# Make the meshgrid.
x = range(D)
y = range(S)
X, Y = np.meshgrid(x, y)

# Populate the Z values of the plot. Z is a dictionary with keys
# the values of whether the agent has a usable ace or not.
# Z in essence holds two matrices that contain the value of V(s).
# The rows of each matrix show the state values on specific dealer's
# face-up card, while the columns on the agent's sum.
Z = {}
for has_ace in a:
    Z[has_ace] = np.zeros((D,S))
    for i in range(D):
        for j in range(S):
            state = d[i] + ' ' + s[j] + ' ' + has_ace
            Z[has_ace][i,j] = V[state]

# Creating the plots.
titles = ['No usable ace', 'Usable ace']
fig = plt.figure(figsize=plt.figaspect(0.5))
for i in range(2):
    ax = fig.add_subplot(1, 2, i+1, projection='3d')
    
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z[str(i)], rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.0, 1.0)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Customize the labels.
    ax.set_title(titles[i])
    ax.set_xticklabels(s[::2])
    ax.set_xlabel('Player sum')
    ax.set_yticklabels(d[::2])
    ax.set_ylabel('Dealer showing')

plt.show()