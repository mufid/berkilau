import numpy as np

def sample_motion_model(u, x_past):
    ''' Assumptions:
    1) Use the odometry motion model, u = (desired) dx
    2) Odometry error is modeled using gaussian distribution'''
    # Set the odometry error model
    mu = 0.
    std = 0.25
    
    dx_bar = u
    err = np.random.normal(mu, std)

    dx = dx_bar + err
    x = x_past + dx
    
    return x
