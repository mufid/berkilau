import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter

def plot(X, m, x_star, t):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_xlim((m['left-wall'],m['right-wall']))
    ax.set_xticks(np.linspace(m['left-wall'],m['right-wall'],11))
    ax.set_ylim((0.0, 0.1))
    ax.set_yticks(np.linspace(0.0,0.1,5))
    
    ax.set_xlabel('robot position: x')
    ax.set_ylabel('bel(x)')
    fig.suptitle('Localization at t= ' + str(t))

    coords = [[(x[0],0),(x[0],x[1])] for x in X]
    line_segments = LineCollection(coords, linewidths = 1.5, colors = colorConverter.to_rgba('r'), linestyle = 'solid')
    ax.add_collection(line_segments)
    
    ax.annotate('The BOT', xy=(x_star, 0.0), xytext=(5.0, 0.050), arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='center', verticalalignment='center')
    ax.annotate('left-door', xy=(m['left-door'], 0.0), xytext=(m['left-door'], 0.075), arrowprops=dict(facecolor='blue', shrink=0.05), horizontalalignment='center', verticalalignment='center')    
    ax.annotate('middle-door', xy=(m['middle-door'], 0.0), xytext=(m['middle-door'], 0.075), arrowprops=dict(facecolor='blue', shrink=0.05), horizontalalignment='center', verticalalignment='center') 
    ax.annotate('right-door', xy=(m['right-door'], 0.0), xytext=(m['right-door'], 0.075), arrowprops=dict(facecolor='blue', shrink=0.05), horizontalalignment='center', verticalalignment='center') 
    
    return fig
