import CSUIBotClass2014.util.ray_casting2 as rc 

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
    p = 0.7 # dummy
    q = q * p

  return q