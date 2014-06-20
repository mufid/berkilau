import matplotlib.pyplot as pl
import numpy as np
import math

from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter

def plot(X, m, x_star, t):
    fig = pl.figure(figsize=(10,10))

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

    return fig
