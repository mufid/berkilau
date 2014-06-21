import CSUIBotClass2014.util.ray_casting2 as rc 
import math
from scipy.integrate import quad

def phit(ztk, x_t, m, sensor_direction):
  sigmasq = 0.1
  zmax = 3.0

  result_raycast = rc.ray_casting(x_t, m, sensor_direction)
  ztk_star = rc.range((x_t['x'], x_t['y']),
    result_raycast)

  if (ztk >= 0 and ztk < zmax):
    funct = (1/math.sqrt(2*math.pi*sigmasq))*math.exp(
      -0.5*((ztk - ztk_star)**2)/sigmasq)
    
    nu = integrate.quad(lambda ztk: (1/math.sqrt(2*math.pi*sigmasq))*math.exp(
      -0.5*((ztk - ztk_star)**2)/sigmasq),
     0, zmax)**-1
     
    return nu*funct
  else:
    return 0 

def pshort(ztk, x_t, m, sensor_direction):
  lambdashort = 0.5 #intrinsic parameter
  result_raycast = rc.ray_casting(x_t, m, sensor_direction)
  ztk_star = rc.range((x_t['x'], x_t['y']),
    result_raycast)
  if(ztk >= 0 and ztk_star >= ztk):
    nu = 1/(1-math.exp(-lambdashort*ztk_star))
    expval = nu*lambdashort*math.exp(-lambdashort*ztk)
    return expval
  else:
    return 0

def pfail(ztk):
  zmax = 3.0
  return ztk == zmax #max range = 3

def prand(ztk):
  zmax = 3.0
  if(0 <= ztk and ztk < zmax):
    return 1/zmax
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
    
    #intrinsic parameter, totalnya harus = 1
    zhit = 0.25
    zshort = 0.25
    zfail = 0.25
    zrand = 0.25

    p = (zhit * phit(z_tk, x_t, m, sensor_direction))*
        (zshort * pshort(z_tk, x_t, m, sensor_direction))*
        (zfail * pfail(z_tk))*
        (zrand * prand(z_tk))
    q = q * p

  return q