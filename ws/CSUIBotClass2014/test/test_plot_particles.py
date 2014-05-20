#!/usr/bin/python

# @author: vektor dewanto
# @obj: demonstrate how to plot particles in an occupancy grid map, _although_, for now, all positions are valid

import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.cm as cmx
from matplotlib import colors

# Construct the occupancy grid map
grid_map = {'size': (10,10), 'res': 1.0}

grid =  [1,1,1,1,1,1,1,1,1,1,\
         1,0,0,1,0,1,0,0,0,1,\
         1,0,0,1,0,1,0,0,0,1,\
         1,0,0,0,0,1,0,1,1,1,\
         1,1,1,1,0,0,0,0,0,1,\
         1,0,0,1,0,0,0,0,0,1,\
         1,0,0,0,0,0,0,0,0,1,\
         1,0,0,1,0,0,0,0,0,1,\
         1,0,0,1,0,0,0,0,1,1,\
         1,1,1,1,1,1,1,1,1,1]
assert len(grid)==grid_map['size'][0]*grid_map['size'][1], 'grid size is mismatched'
grid = np.asarray(grid)
grid = grid.reshape(grid_map['size'][0], grid_map['size'][1])
grid_map['grid'] = grid

# Plot the map
plt.subplot(1,1,1)
plt.pcolormesh(grid_map['grid'], edgecolors='k', linewidths=0.1, cmap=colors.ListedColormap(['w','b']))
plt.title('The occupancy grid map with particles')

# At t=0, initiate X with n_particle particles drawn from a uniform distribution (since this is a global loc. problem)
# For now, we donot check whether the particle is on an occupied grid
n_particle = 100;
X_tmp = np.random.uniform(0.0, 10.0, n_particle)
Y_tmp = np.random.uniform(0.0, 10.0, n_particle)
THETA_tmp = np.random.uniform(0.0, math.pi*2.0, n_particle)
XYTHETA_tmp = zip(X_tmp, Y_tmp, THETA_tmp)
W = [1.0/n_particle] * n_particle# uniform
X = zip(XYTHETA_tmp, W)

# Plot positions, the color corresponds to the weight
ax = plt.axes()
ax.scatter([e[0][0] for e in X], [e[0][1] for e in X], c=[e[1] for e in X], marker='o', s=20, cmap=cmx.jet)

# Plot bearings
for e in X:
    x = e[0][0]
    y = e[0][1]
    theta = e[0][2]
    
    # convert polar to cartesian coord
    r = 0.1
    dx = r * math.cos(theta)
    dy = r * math.sin(theta) 
    
    ax.arrow(x, y, dx, dy, head_width=0.05, head_length=0.1, fc='k', ec='k')

plt.show()
