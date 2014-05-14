#!/usr/bin/python

# @obj: to reproduce figure 8.11 from the book Prob. Robotics by S. Thrun
# @author: vektor dewanto

import numpy as np
import CSUIBotClass2014.util.plotter as plotter
import CSUIBotClass2014.sim.OneDimMobileBot.action as action
import CSUIBotClass2014.sim.OneDimMobileBot.perception as sensor
import CSUIBotClass2014.MCL.standard as MCL

from matplotlib.backends.backend_pdf import PdfPages

# Init
print 'hello :)'
plots = []

t_max = 3
T = range(t_max+1)# contains a seq. of discrete time step from 0 to t_max
n_particle = 300# fixed, hardcoded

# the world is simply a 1-D straight line in the range of [0.,10.]
m = {'left-wall': 0.0, 'right-wall': 10.0, 'left-door': 2.0, 'middle-door': 4.0, 'right-door': 9.0, 'start-pos': 2.0, 'door-width': 1.0}

U = [None, 0.0, 2.0, 2.5]# hardcoded: a list of desired actions in odometry motion model
assert (len(U)>=len(T)), 'len(U)<len(T)'

# At t=0, initiate X with n_particle particles drawn from a uniform distribution (since this is a global loc. problem)
X_tmp = np.random.uniform(m['left-wall'], m['right-wall'], n_particle)# _without_ weights, drawn from ['left-wall','right-wall')
w = 1.0/n_particle# uniform
X = [(x, w) for x in X_tmp]

# Put the robot now!
x_star = m['start-pos']
plots.append(plotter.plot(X, m, x_star, t=0))

# Localize!
for t in T[1:]:
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> t=", t
    # _Simulate_ an action
    u = U[t]
    print 'u_star=', u
    
    x_star = action.move(u, x_star, m)
    print 'x_star=', x_star
    
    # _Simulate_ an observation
    z = sensor.sense_door(x_star, m)
    print 'z_star= ', z
    
    X = MCL.run(X, u, z, m)
    plots.append(plotter.plot(X, m, x_star, t))
    
# Closure
with PdfPages('plot.pdf') as pdf:
    for p in plots:
        pdf.savefig(p)

print "mission accomplished: bye :)"
