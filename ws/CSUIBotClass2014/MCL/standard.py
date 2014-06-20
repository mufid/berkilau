# @obj: implement the standard MCL alg.; table 8.2 on the book Prob. Robotics by S. Thrun
# @author: vektor dewanto

import numpy as np
import CSUIBotClass2014.action_model.model_uas as act_model
import CSUIBotClass2014.perception_model.beam_range_finder_model as obs_model

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
            X.append(X_bar[candidate_idx])
            
    return X
    
def run(X_past, u, z, m):
    ''' 
    \param X: is a list of tuples (x, w)
    \param u: the control/action
    \param z: the observation
    \param m: the given map
    '''
    X_bar = []
    X = []
    n_particle = len(X_past)# fixed #particle for ever :(

    for i in range(n_particle):
        x = act_model.sample_motion_model(u, X_past[i][0])
        w = obs_model.beam_range_finder_model(z, x, m)
        X_bar.append((x, w))
    
    X = resample(X_bar)

    return X
