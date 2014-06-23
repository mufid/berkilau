#!/usr/bin/python

# @obj: to reproduce figure 8.11 from the book Prob. Robotics by S. Thrun
# @author: vektor dewanto

import numpy as np

import matplotlib.pyplot as plt
import math
import matplotlib.cm as cmx
import CSUIBotClass2014.util.plotter2 as plotter
import CSUIBotClass2014.sim.SimulationExtreme.action as action
import CSUIBotClass2014.sim.SimulationExtreme.perception as sensor
#import CSUIBotClass2014.sim.OneDimMobileBot.xaction as action
import CSUIBotClass2014.MCL.standard as MCL
import CSUIBotClass2014.MCL.kldmcl as KLD
import sys

from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages

# Init
print 'hello :)'
plots = []

# wall = 'W'
# woodenFlood = ' '
# softCarpet = 'S'
# hardCarpet = 'H'
size = {'width': 20, 'height': 20}

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

import math

# Localize!
import CSUIBotClass2014.util.ray_casting2 as rc

def do_nothing():
    # Actually doing nothing
    return None

def main(particle_init, action_fun, percept_fun, u_star, x_star, the_map, time_array, localization_algorithm, forced_state=None, at_time=None):
    T = time_array
    m = the_map
    plots = []
    X = particle_init
    for t in T[1:]:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> t=", t
        # _Simulate_ an action
        if (forced_state and at_time == t):
            u = U[t]
            print "Kidnap!"
            x_star = forced_state
        else:
            u = U[t]
            print 'u_star=', u
            x_star = action_fun(u, x_star, m)
        
        print 'x_star=', x_star
        
        z = percept_fun(x_star, m)
        print 'z_star= ', z
        
        X = localization_algorithm(X, u, z, m)
        plots.append(plotter.plot(X, m, x_star, t, z))
    
    return plots

if __name__ == "__main__":
    # Choose localization algorithm:
    print "Using localization algorithm: %s" % sys.argv[1]
    if (sys.argv[1] == 'kld'):
        alg = KLD.run
    else:
        alg = MCL.run

    # Choose case. Define action, perception
    print "Using case: %s" % sys.argv[2]
    X = []
    t_max = 12
    T = range(t_max+1) # contains a seq. of discrete time step from 0 to t_max
    n_particle = 200    # fixed, hardcoded
    U = [
            None, 
            {'v': .1, 'w': 0}, 
            {'v': .2, 'w': 0}, 
            {'v': .1, 'w': math.pi / 8 },
            {'v': .1, 'w': 0}, 
            {'v': .1, 'w': 0},
            {'v': .1, 'w': 0},   # sec 6
            {'v': .5, 'w': math.pi / 8},
            {'v': .1, 'w': 0},    # sec 8
            {'v': .5, 'w': 0},
            {'v': .5, 'w': 0},    # sec 10
            {'v': .5, 'w': math.pi / 8},
            {'v': .5, 'w': math.pi / 8}
        ]

    x_star = {'x': 8.1, 'y': 10.1, 'theta': -math.pi/4 }

    action_fun  = action.move_velocity
    percept_fun = sensor.sense_beam
    kn_state = None
    kn_time = None

    if (sys.argv[2] == 'global'):
        xs = np.random.uniform(0, 20, n_particle)
        ys = np.random.uniform(0, 20, n_particle)
        theta = np.random.uniform(0, math.pi * 2, n_particle)
    elif (sys.argv[2] == 'local'):
        xs = np.random.normal(x_star['x'], .5, n_particle)
        ys = np.random.normal(x_star['y'], .5, n_particle)
        theta = np.random.normal(x_star['theta'], math.pi/8, n_particle)
    else:
        xs = np.random.normal(x_star['x'], .5, n_particle)
        ys = np.random.normal(x_star['y'], .5, n_particle)
        theta = np.random.normal(x_star['theta'], math.pi/8, n_particle)
        kn_state = {'x': 8.5, 'y': 1.7, 'theta': math.pi/16}
        kn_time = 6
        do_nothing()

    for ii in range(n_particle):
        X.append(({'x': xs[ii], 'y': ys[ii], 'theta': theta[ii]}, 1./n_particle))

    # Use the map
    the_map = m

    plots = main(X, action_fun, percept_fun, U, x_star, the_map, T, alg, kn_state, kn_time)

    file_name = "plot-%s-%s.pdf" % (sys.argv[1], sys.argv[2])
    with PdfPages(file_name) as pdf:
        for p in plots:
            pdf.savefig(p)

    # Done!
    print "All done!"



# END OF FILE
# DO NOT DELETE THIS LINE
# KEEP 3 SPACES ABOVE