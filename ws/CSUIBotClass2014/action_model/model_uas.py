import numpy as np
import math

def sample(b):
    mu    = .0
    sigma = b
    if b == 0:
        return 0
    return np.random.normal(mu, sigma, 1)[0]

def sample_motion_model(u, pose, m):
    # Set the odometry error model
    x, y, theta = pose['x'], pose['y'], pose['theta']

    dt = 1 # For now, one second difference only

    a = [0, 
        .025, 
        math.pi/135, 
        .025, 
        math.pi/135, 
        .025, 
        math.pi/135
    ]

    v_desired = u['v']
    w_desired = u['w']

    v = v_desired
    w = w_desired

    v_t = v + sample(a[1] * abs(v) + a[2] * abs(w))
    w_t = w + sample(a[3] * abs(v) + a[4] * abs(w))
    gamma = w + sample(a[5] * abs(v) + a[6] * abs(w))
    x_a = x - v_t / w_t * math.sin(theta) + v_t / w_t * math.sin(theta + w_t * dt)
    y_a = y + v_t / w_t * math.cos(theta) - v_t / w_t * math.cos(theta + w_t * dt)
    theta_a = theta + w_t * dt + gamma * dt

    return {'x': x_a, 'y': y_a, 'theta': theta_a}