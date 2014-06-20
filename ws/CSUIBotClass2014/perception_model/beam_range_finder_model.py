import CSUIBotClass2014.util.ray_casting2 as rc 
import math
from scipy.integrate import quad

def phit(ztk, x_t, m, sensor_direction):
  sigmasq = 0.1
  zmax = 3.0

  result_raycast = rc.ray_casting(x_t, m, sensor_direction)
  ztk_star = rc.range((x_t['x'], x_t['y']),
    result_raycast)

  if (ztk >= 0 && ztk < zmax):
    funct = (1/math.sqrt(2*math.pi*sigmasq))*math.exp(
      -0.5*((ztk - ztk_star)**2)/sigmasq)
    
    nu = integrate.quad(lambda ztk: (1/math.sqrt(2*math.pi*sigmasq))*math.exp(
      -0.5*((ztk - ztk_star)**2)/sigmasq),
     0, zmax)**-1
     
    return nu*funct
  else:
    return 0 


def beam_range_finder_model(z_t, x_t, m):
  q = 1

  # Automatically zero if is invalid
  if (not rc.is_valid((x_t['x'], x_t['y']), m)):
    return 0

  # K: banyaknya sensor
  sensors = 'n nw w sw s se e ne'.split()
  for sensor_direction in sensors: 
    result_raycast = rc.ray_casting(x_t, m, sensor_direction)
    z_tk = rc.range((x_t['x'], x_t['y']),
      result_raycast)
    p_hit = p_hit(z_tk, x_t, m, sensor_direction)
    p = 0.7 # dummy
    q = q * p

  return q