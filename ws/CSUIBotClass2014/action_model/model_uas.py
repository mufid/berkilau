import numpy as np

def sample(b):
    mu    = .0
    sigma = 0.25
    return np.random.normal(mu, sigma, 1)[0]

def sample_motion_model_velocity(u, pose, m):
    # Set the odometry error model

    v_desired = u['v']
    w_desired = u['w']

    v = v_desired
    w = w_desired

    v_h = v + sample(a[1] * abs(v) + a[2] * abs(w), dist)
    w_t = w + sample(a[3] * abs(v) + a[4] * abs(w), dist)
    gamma = w + sample(a[5] * abs(v) + a[6] * abs(w), dist)
    x_a = x - v_t / w_t * math.sin(theta) + v_t / w_t * math.sin(theta + w_t * dt)
    y_a = y + v_t / w_t * math.cos(theta) - v_t / w_t * math.cos(theta + w_t * dt)
    theta_a = theta + w_t * dt + gamma * dt

    return (x_a, y_a, theta_a)