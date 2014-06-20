import CSUIBotClass2014.util.ray_casting2 as rc 

def beam_range_finder_model(z_t, x_t, m):
  q = 1
  # K: banyaknya sensor
  sensors = 'n nw w sw s se e ne'.split()
  for sensor_direction in sensors: 
    z_tk = rc.ray_casting(x_t, sensor_direction, m)
    p = 0.7 # dummy
    q = q * p
  return q