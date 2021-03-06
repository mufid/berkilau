# @obj: Simulate robot actions for Simulation
# @author: -

import numpy as np

def sample(b):
    mu    = .0 # assume zero mean 
    sigma = b
    return np.random.normal(mu, sigma, 1)[0]

def move_velocity(u, pose, m):
    # assume fixed one second time different
    dt = 1

    # Set the odometry error model
    alpha = [0, 
        .1, 
        math.pi/8, 
        1, 
        math.pi/8, 
        1, 
        math.pi/8
    ]
    a = alpha
    v_desired = u['v']
    w_desired = u['w']

    v = v_desired
    w = w_desired

    v_h = v + sample(a[1] * abs(v) + a[2] * abs(w))
    w_h = w + sample(a[3] * abs(v) + a[4] * abs(w))
    gamma_h = w + sample(a[5] * abs(v) + a[6] * abs(w))

    x_a = x - v_h / w_h * math.sin(theta) + v_h / w_h * math.sin(theta + w_t * dt)
    y_a = y + v_h / w_h * math.cos(theta) - v_h / w_h * math.cos(theta + w_t * dt)
    theta_a = theta + w_h * dt + gamma_h * dt

    return (x_a, y_a, theta_a)