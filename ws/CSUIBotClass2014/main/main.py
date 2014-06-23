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

def distance(robot, target):
    delta_x = robot['x'] - target['x']
    delta_y = robot['y'] - target['y']
    return math.sqrt(delta_x**2 + delta_y**2)

def main(particle_init, action_fun, percept_fun, u_star, x_star, the_map, time_array, localization_algorithm, forced_state=None, at_time=None):
    T = time_array
    m = the_map
    plots = []
    X = particle_init
    kk = 0
    start = True
    t = 0
    while start:
        t+=1
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> start t=", t

        cp = U[kk]

        delta_x = x_star['x'] - cp['x']
        delta_y = x_star['y'] - cp['y']

        print 'robot: ',x_star['x'], x_star['y'], x_star['theta']
        print 'target: ',cp['x'], cp['y']
        print 'delta xy: ',delta_x, delta_y

        print "---"
        delta_th = (math.atan2(-delta_y, -delta_x)) - x_star['theta']

        print 'delta_theta', delta_th, ' deg: ', delta_th*180/math.pi
        print 'distance', distance(x_star, cp)
        # delta_th = x_star['theta'] + math.atan(delta_y / delta_x)

        delta_x = abs(delta_x)
        delta_y = abs(delta_y)

        delta_deg = abs(delta_th*180/math.pi)
        if(delta_deg < 10.0):
            if(distance(x_star, cp) > 1.0):
                u = {'v': 1.0, 'w': 0}
            else:
                u = {'v': distance(x_star, cp), 'w': 0}
        else:
            u = {'v': 0, 'w':delta_th/2}
        
        if(sys.argv[2] == 'kidnap'):
            u = knpU[t]
            if(t == len(knpU)-1):
                start = False
        print "--- ---"
        print 'action v: ', u['v'], 'action w: ', u['w']
        #if (delta_x <= 1 and delta_y <= 1):
        #    u = {'v': 0.2, 'w': delta_th}
        #else:
        #    u = {'v': 1, 'w': delta_th}

        if (distance(x_star, cp) < 1.0):
            if(kk == 3):
                start = False
            else:
                kk += 1

        # print delta_th
        #if(t == 8): start = False
        # _Simulate_ an action
        if (forced_state and at_time == t):
            # u = U[t]
            print "Kidnap!"
            x_star = forced_state
        else:
            #u = U[t]
            print 'u_star=', u
            x_star = action_fun(u, x_star, m)

        print 'x_star=', x_star
        
        z = percept_fun(x_star, m)
        print 'z_star= ', z
        
        X = localization_algorithm(X, u, z, m)
        plots.append(plotter.plot(X, m, x_star, t, z))
        
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end of t=", t
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
    t_max = 40
    T = range(t_max+1) # contains a seq. of discrete time step from 0 to t_max
    n_particle = 200    # fixed, hardcoded
    degree = math.pi/180

    U = [ #for local and global problem
        {'x': 18.0, 'y': 11.0},
        {'x': 18.0, 'y':  2.5},
        {'x':  8.5, 'y':  2.0},
        {'x':  8.5, 'y': 11.0}
        ]

    knpU = [
        None,
        {'v': 0.0, 'w': -math.pi/32},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 0.0, 'w': math.pi/24},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 0.0, 'w': math.pi/64},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 0.0, 'w': math.pi/32},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': 0.0},
        {'v': 1.0, 'w': -math.pi/32}
    ]

    x_star = {'x': 8.5, 'y': 10.5, 'theta': math.pi/16 }

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
        kn_state = {'x': 8.5, 'y': 1.5, 'theta': 0}
        kn_time = 8
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