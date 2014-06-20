#!/usr/bin/python

# @obj: to reproduce figure 8.11 from the book Prob. Robotics by S. Thrun
# @author: vektor dewanto

import numpy as np

import matplotlib.pyplot as plt
import math
import matplotlib.cm as cmx
import CSUIBotClass2014.util.plotter as plotter
import CSUIBotClass2014.sim.SimulationExtreme.action as action
import CSUIBotClass2014.sim.SimulationExtreme.perception as sensor
#import CSUIBotClass2014.sim.OneDimMobileBot.xaction as action
import CSUIBotClass2014.MCL.standard as MCL

from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages

# Init
print 'hello :)'
plots = []

t_max = 3
T = range(t_max+1)# contains a seq. of discrete time step from 0 to t_max
#n_particle = 20 # fixed, hardcoded

# the world is simply a 1-D straight line in the range of [0.,10.]
#m = {'left-wall': 0.0, 'right-wall': 10.0, 'left-door': 2.0, 'middle-door': 4.0, 'right-door': 9.0, 'start-pos': 2.0, 'door-width': 1.0}

# wall = 'W'
# woodenFlood = ' '
# softCarpet = 'S'
# hardCarpet = 'H'
m = [
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
    [ 'W', ' ', ' ', 'H', 'H', 'S', 'W', ' ', ' ', ' ', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'H', 'H', 'S', 'W', ' ', ' ', ' ', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'H', 'H', 'S', 'W', ' ', ' ', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'H', 'H', 'S', 'W', ' ', ' ', ' ', 'W', 'H', 'H', 'H', ' ', ' ', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'H', 'H', 'S', 'W', ' ', ' ', ' ', 'W', 'H', 'H', 'H', ' ', ' ', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'W', 'S', 'S', 'W', ' ', ' ', ' ', 'W', 'H', 'H', 'H', ' ', ' ', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', 'W', 'S', 'S', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', ' ', 'W', 'W', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'W', 'W', 'S', 'S', 'W'],
    [ 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', 'S', 'W'],
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'H', 'H', 'H', 'W', ' ', ' ', ' ', 'W', 'W', 'W', 'W', 'W', 'W', ' ', ' ', ' ', 'W'],
    [ 'W', 'S', 'S', 'H', 'H', 'H', 'W', ' ', ' ', ' ', 'W', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'H', 'H', 'H', 'W', ' ', ' ', ' ', 'W', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'H', 'H', 'H', 'W', ' ', ' ', ' ', 'W', 'S', 'S', 'S', 'W', 'S', 'S', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'W', 'S', 'S', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'S', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'S', 'S', 'S', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'S', 'S', 'S', 'W'],
    [ 'W', 'S', 'S', 'S', 'S', 'S', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'S', 'S', 'S', 'W'],
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
    ]

# At t=0, initiate X with n_particle particles drawn from a uniform distribution (since this is a global loc. problem)
# For now, we donot check whether the particle is on an occupied grid

# U is movement with velocity motion in 2D
#print map[0][0]
U = [None, {'v': 0, 'w': 0}, {'v': 1, 'w': 0}, {'v': 1, 'w': np.pi / 8 }]

#U = [None, 0.0, 2.0, 2.5]# hardcoded: a list of desired actions in odometry motion model
#assert (len(U)>=len(T)), 'len(U)<len(T)'

# At t=0, initiate X with n_particle particles drawn from a uniform distribution (since this is a global loc. problem)
#X_tmp = np.random.uniform(m['left-wall'], m['right-wall'], n_particle)# _without_ weights, drawn from ['left-wall','right-wall')
#w = 1.0/n_particle# uniform
#X = [(x, w) for x in X_tmp]

#x = np.random.uniform(m['left-wall'], m['right-wall'], n_particle)
#X =[(x, y, theta)]

# Put the robot now!
#x_star = m['start-pos']
x_star = {'x': 1.1, 'y': 1.2, 'theta': -math.pi/4 }

# Localize!
import CSUIBotClass2014.util.ray_casting2 as rc
print 'north'
print rc.ray_casting(x_star, m, 'n')
print 'northwest'
print rc.ray_casting(x_star, m, 'nw')
print 'west'
print rc.ray_casting(x_star, m, 'w')
print rc.ray_casting(x_star, m, 'sw')
print rc.ray_casting(x_star, m, 's')
print rc.ray_casting(x_star, m, 'se')
print rc.ray_casting(x_star, m, 'e')
print rc.ray_casting(x_star, m, 'ne')

for t in None:# T[1:]:
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> t=", t
    # _Simulate_ an action
    u = U[t]
    print 'u_star=', u
    
    #x_star = action.move(u, x_star, m)
    x_star = action.move_velocity(u, x_star, grid)
    print 'x_star=', x_star
    
    # _Simulate_ an observation
    #z = sensor.sense_door(x_star, m)
    z = sensor.sense_beam(x_star, grid)
    print 'z_star= ', z
    
    #X = MCL.run(X, u, z, m)
    #plots.append(plotter.plot(X, m, x_star, t))
    
# Closure
#with PdfPages('plot.pdf') as pdf:
#    for p in plots:
#        pdf.savefig(p)

#print "mission accomplished: bye :)"
