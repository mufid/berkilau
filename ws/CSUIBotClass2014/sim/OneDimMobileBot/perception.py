# @obj: Simulate robot perceptions/observations for OneDimMobileBot whose sensor is merely a door sensor returning either door(=True=1) or not-door(=False=0)
# @author: vektor dewanto

import numpy as np
import scipy.stats as stat
import CSUIBotClass2014.util.ray_casting as RayCast
def get_noise():
    # all in meters
    mu = 0
    sigma = .5
    return np.random.normal(mu, sigma, 1)[0]

def sense_beam(state, m):
    arahs = ['n', 'nw', 'w', 'sw', 's', 'se', 'e', 'ne']
    z_t = [RayCast.ray_cas(state, m) for state in arahs]
    z_t = [i + get_noise() for i in z_t]
    return z_t;

'''
def sense_door(x, m):
    ''' 
    #A door sensor returns either True (=door) or False (=no door) with some perception errors
    '''
    # Set the (true) perception model: a gaussian mixture model with three modals (=peaks=models)
    multimodal = [(m['left-door'], 0.25), (m['middle-door'], 0.25), (m['right-door'], 0.25)]
    door_width = m['door-width']
    
    # lamdas contains the weight to each element in probs
    # lamdas is normalized to sum up to one
    dists = [abs(modal[0]-x) for modal in multimodal]
    lamdas = [1.0 if d==min(dists) else 0.0 for d in dists]# for now, lamda is one for the nearest modal, otherwise zero
    
    p_total = 0;
    for i, modal in enumerate(multimodal):
        cdf_lo = stat.norm(loc= modal[0], scale= modal[1]).cdf(x-door_width/2)
        cdf_hi = stat.norm(loc= modal[0], scale= modal[1]).cdf(x+door_width/2)
        p = cdf_hi - cdf_lo
        
        p_total = p_total + (lamdas[i] * p)
        
    # This is a bernoulli dist.
    door = np.random.binomial(n=1, p=p_total)
    
    return door
'''