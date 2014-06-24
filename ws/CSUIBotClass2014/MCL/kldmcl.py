# @obj: implement the standard MCL alg.; table 8.2 on the book Prob. Robotics by S. Thrun
# @author: vektor dewanto

import numpy as np
import CSUIBotClass2014.action_model.model_uas as act_model
import CSUIBotClass2014.perception_model.beam_range_finder_model as obs_model
from scipy import stats
import math

def normalize_weight(X):
    # Normalize all weights, so that they sum up to one
    total_w = sum([xw[1] for xw in X])
    X = [(xw[0], xw[1]/total_w) for xw in X]
    
    return X
    
def resample(X_bar):
    ''' 
    draw i with probability proportional to w_t^i
    '''
    X_bar = normalize_weight(X_bar)
    X = []

    while len(X) < len(X_bar):
        candidate_idx = np.random.random_integers(low=0, high= len(X_bar)-1) 
        candidate_w = X_bar[candidate_idx][1]

        sampled = np.random.binomial(n=1, p=candidate_w)# a Bernoulli dist.
        
        if sampled==1:
            return X_bar[candidate_idx]
            
    return X
    
def run(X_past, u, z, m):
    ''' 
    \param X: is a list of tuples (x, w)
    \param u: the control/action
    \param z: the observation
    \param m: the given map
    '''
    epsilon = 0.05
    delta = 0.01
    Xt = [] 
    b = [[0]*20]*20
    M = 0
    Mx = 0
    Mxmin = 20
    k = 0
    n_particle = len(X_past)# fixed #particle for ever :(
    
    while True:
        xt1 = resample(X_past)
        xmt = act_model.sample_motion_model(u, xt1[0], m)
        w = 1-obs_model.beam_range_finder_model(z, xmt, m)
        Xt.append((xmt, w))

        idx = int(math.floor(xmt['x']))
        idy = int(math.floor(xmt['y']))
        if(b[idy][idx]==0 and
            (
                (idx < 20) and (idx >= 0) and
                (idy < 20) and (idy >= 0)
            )
            ):
            k += 1
            b[idy][idx] = 1
            if(k>1):
                var1 = 2.0/(9*(k-1))
                Mx = ((k-1)/2.0*epsilon*
                     (1 - var1 + math.sqrt(var1)*stats.norm.ppf(1-delta))**3)
        M+=1
        if not ((M<Mx) or (M<Mxmin)):
            print "particles: %d" % len(Xt)
            return Xt

    return Xt
