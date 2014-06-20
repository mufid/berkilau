# @obj: Simulate robot perceptions/observations for OneDimMobileBot whose sensor is merely a door sensor returning either door(=True=1) or not-door(=False=0)
# @author: vektor dewanto

import numpy as np
import scipy.stats as stat
import CSUIBotClass2014.util.ray_casting2 as rc
def get_noise():
  # all in meters
  mu = 0
  sigma = .5
  return np.random.normal(mu, sigma, 1)[0]

def sense_beam(state, m):
  # Direction 
  directions = 'n nw w sw s se e ne'.split()
  z_t = [rc.ray_casting(state, m, direction) for direction in directions]

  z_t = [i + get_noise() for i in z_t]
  return z_t;
