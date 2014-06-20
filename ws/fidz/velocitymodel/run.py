__author__ = 'Mufid'

# Every import needed, listed
import numpy as np
import pylab as pl
import random
import math
from matplotlib.backends.backend_pdf import PdfPages

# ------------------------
# All configuration.
# ------------------------
# Alpha: manufacture-specific variable
# Please use 1 as its base bound
alpha = [0, .5, .5, .5, .5, .5, .5]
sample_count = 100
# sigma: variance
# Generate a set of random distribution
sigma = 1.5
v  = 5
w  = -10
x  = 1
y  = 1   # y from bottom, because we use scatter plot
dt = 1  # time difference
theta = math.pi / 4 # 45 degree
dist = np.random.normal(0, sigma, 1000)
# The mu need to be zero since the equation
# require zero-centered normal distribution
# The 1000 total number of entries are
# customizable. By default, no need to change this.

# ---- code start -----

def sample(b, dist):
  '''
  Sample algorithm, as previewed in algorithm
  Table 5.4 in Thurn's Book. Please note that
  we use internal Python's normal distribution
  array, so no need to use equation in 5.4
  '''
  # Uncomment if you want to use static distribution
  # random.choice(dist)
  return np.random.normal(0, b, 1)[0]

def sample_motion_model_velocity(v, w, x, y, theta, a, dt, dist):
  '''
  Get the sample motion model, as suggested
  in algorithm Table 5.3 in Probabilistic
  Robotics by Sebastian Thrun. For reference, please
  see CSUIBotClass2014/action_model/model_1.py
  All unit in meter. Theta and omega (w) in radian
  '''
  #print sample(a[1] * abs(v) + a[2] * abs(w), dist)

  v_t = v + sample(a[1] * abs(v) + a[2] * abs(w), dist)
  w_t = w + sample(a[3] * abs(v) + a[4] * abs(w), dist)
  gamma = w + sample(a[5] * abs(v) + a[6] * abs(w), dist)
  x_a = x - v_t / w_t * math.sin(theta) + v_t / w_t * math.sin(theta + w_t * dt)
  y_a = y + v_t / w_t * math.cos(theta) - v_t / w_t * math.cos(theta + w_t * dt)
  theta_a = theta + w_t * dt + gamma * dt
  return (x_a, y_a, theta_a)

result = []

for i in range(1, sample_count):
  # Sample
  r = sample_motion_model_velocity(v, w, x, y, theta, alpha, dt, dist)
  # Then add to result list
  result.append(r)

xs = [i[0] for i in result]
ys = [i[1] for i in result]

with PdfPages('plot.pdf') as pdf:
  # Define a graph
  pl.figure(figsize=(10,10))

  # Draw the grid first
  ax = pl.axes()

  ax.set_xlim(-4,20)
  ax.set_ylim(-4,20)
  ax.xaxis.set_major_locator(pl.MultipleLocator(5.0))
  ax.xaxis.set_minor_locator(pl.MultipleLocator(0.5))
  ax.yaxis.set_major_locator(pl.MultipleLocator(5.0))
  ax.yaxis.set_minor_locator(pl.MultipleLocator(0.5))
  ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
  ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
  ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
  ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')

  # Draw the velocity
  dx = v * math.cos(theta)
  dy = v * math.sin(theta)
  ax.arrow(x,y,dx,dy, head_width=.4, head_length=0.5, length_includes_head=True)

  circle = pl.Circle((x, y), radius=0.35, fc='y')
  ax.add_patch(circle)

  # First, draw the current location
  
  pl.scatter(xs, ys)
  pdf.savefig()
