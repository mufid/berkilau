import matplotlib.pyplot as pl
import numpy as np
import math

from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter

def plot(X, m, x_star, t, z_t):
    fig = pl.figure(figsize=(10,10))

    # Draw the grid first
    ax = pl.axes()

    ax.set_xlim(-4,20)
    ax.set_ylim(-4,20)
    ax.xaxis.set_major_locator(pl.MultipleLocator(5.0))
    ax.xaxis.set_minor_locator(pl.MultipleLocator(1.0))
    ax.yaxis.set_major_locator(pl.MultipleLocator(5.0))
    ax.yaxis.set_minor_locator(pl.MultipleLocator(1.0))
    ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')

    # Draw map
    for y, row in enumerate(m):
        for x, cell in enumerate(row):
            if (cell == 'W'):
                rect = pl.Rectangle((x,y), 1, 1, fill=True,color='#cacaca')
                ax.add_patch(rect)

    # Draw the robot and its direction
    x,y,theta = x_star['x'], x_star['y'], x_star['theta']
    dx = 1 * math.cos(theta)
    dy = 1 * math.sin(theta)
    ax.arrow(x,y,dx,dy, head_width=.4, head_length=0.5, length_includes_head=True)

    circle = pl.Circle((x, y), radius=0.35, fc='y')
    ax.add_patch(circle)

    # Draw information
    directions = 'n nw w sw s se e ne'.split()
    title_arr = []
    print z_t
    for direction in directions:
        print z_t[direction]
        title_arr.append("%s: %4.2f" % (direction, z_t[direction]))

    ax.set_title('; '.join(title_arr))

    print X
    xs = [xx[0]['x'] for xx in X]
    ys = [xx[0]['y'] for xx in X]

    pl.scatter(xs, ys)

    return fig
