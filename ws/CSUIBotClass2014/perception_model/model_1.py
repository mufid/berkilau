import scipy.stats as stat

def measurement_model(z, x, m):
    ''' The door sensor model is represented by a mixture distribution of three Gaussian distributions forming a multimodal distribution with three peaks on the doors' locations
    '''
    # Set the (true) perception model
    multimodal = [(m['left-door'], 0.25), (m['middle-door'], 0.25), (m['right-door'], 0.25)]
    door_width = m['door-width']
    
    # lamdas contains the weight to each element in probs
    # lamdas is normalized to sum up to one
    dists = [abs(modal[0]-x) for modal in multimodal]
    lamdas = [1.0 if d==min(dists) else 0.0 for d in dists]
    
    p_total = 0;
    for i, modal in enumerate(multimodal):
        cdf_lo = stat.norm(loc= modal[0], scale= modal[1]).cdf(x-door_width/2)
        cdf_hi = stat.norm(loc= modal[0], scale= modal[1]).cdf(x+door_width/2)
        p = cdf_hi - cdf_lo
        
        p_total = p_total + (lamdas[i] * p)
            
    if z == False:
        p_total = 1.0 - p_total#since the defined model is for z=True, i.e. p(z=True|x)
                
    return p_total
