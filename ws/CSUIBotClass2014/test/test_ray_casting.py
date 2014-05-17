#!/usr/bin/python

import numpy as np
import math
from CSUIBotClass2014.util.ray_casting import ray_cast

# Construct the occupancy grid map
grid_map = {'size': (5,5), 'res': 1.0}

grid =  [1,1,1,1,1,\
         1,0,0,0,1,\
         1,0,0,0,1,\
         1,0,0,0,1,\
         1,1,1,1,1]
assert len(grid)==grid_map['size'][0]*grid_map['size'][1], 'grid size is mismatched'
grid = np.asarray(grid)
grid = grid.reshape(grid_map['size'][0], grid_map['size'][1])
grid_map['grid'] = grid

#
x = 2.5
y = 2.5
theta = math.pi/4*7
pose = (x, y, theta)

#
hit = ray_cast(pose, grid_map)
print '(final) hit=', hit
