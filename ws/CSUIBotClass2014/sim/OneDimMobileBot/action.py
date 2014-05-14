# @obj: Simulate robot actions for OneDimMobileBot
# @author: vektor dewanto

import numpy as np

def move(u, x_past, m):
    ''' 
    Move the robot abs(u) to the right if (u>0) or to the left if (u<0) with some movement errors.
    The control u is represented by an odometry delta.
    '''
    # Set the (true) action error model
    mu = 0.0
    std = 0.25
    
    #
    dx_bar = u# the desired delta
    if u > 0.0:
      err = np.random.normal(mu, std)
    else:
      err = 0.0# assume no error if control= do nothing
     
    #
    dx = dx_bar + err
    x = x_past + dx
    
    # Impose the wall constrains
    if x > m['right-wall']:
        x = m['right-wall']
    elif x < m['left-wall']:
        x = m['left-wall']
    
    return x
