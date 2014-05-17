#!/usr/bin/python

# @author: vektor dewanto
# @obj: simulate ray-casting on a grid map whose individual grid is a square, note: y+ axis points downward

import math
import decimal
import numpy as np
from shapely.geometry import LineString
from shapely.geometry import box
from shapely.geometry import Point

def get_tip(pose, m):
    '''Obtain the top point of a ray, whose length is the diagonal of a squared grid'''
    r = math.sqrt(2*(m['res']**2))# the longest line segment in a grid
    
    # convert polar to cartesian coord
    dx = r * math.cos(pose[2])
    dy = r * math.sin(pose[2]) 
    dy = -1.0 * dy# the y+ points downward instead of upward, we deliberately invert it
    
    # calculate the tip coord
    x = pose[0] + dx
    y = pose[1] + dy
    
    return (x,y)
    
def get_grid_idx(x, y):
    idx_x = int(math.floor(x))
    idx_y = int(math.floor(y))
    
    return (idx_x, idx_y)
    
def is_valid(pose, m):
    idx = get_grid_idx(pose[0], pose[1])
    return not m['grid'][idx]

def get_adj_grid_idx(hit, grid_idx, grid):
    (minx, miny, maxx, maxy) = grid.bounds 
    
    if Point(hit).within(LineString([(minx, miny), (maxx, miny)])):
        print 'hit the top side'
        return (grid_idx[0], grid_idx[1]-1)
    elif Point(hit).within(LineString([(minx, maxy), (maxx, maxy)])):
        print 'hit the bottom side'
        return (grid_idx[0], grid_idx[1]+1)
    elif Point(hit).within(LineString([(minx, miny), (minx, maxy)])):
        print 'hit the left side'
        return (grid_idx[0]-1, grid_idx[1])
    elif Point(hit).within(LineString([(maxx, miny), (maxx, maxy)])):
        print 'hit the right side'
        return (grid_idx[0]+1, grid_idx[1])
    elif hit == (maxx, miny):
        print 'hit the top right corner'
        return (grid_idx[0]+1, grid_idx[1]-1)
    elif hit == (minx, miny):
        print 'hit the top left corner'
        return (grid_idx[0]-1, grid_idx[1]-1)
    elif hit == (maxx, maxy):
        print 'hit the bottom right corner'
        return (grid_idx[0]+1, grid_idx[1]+1)
    elif hit == (minx, maxy):
        print 'hit the bottom left corner'
        return (grid_idx[0]-1, grid_idx[1]+1)
    else:
        assert False, 'error: erronouos ray hit'
            
def ray_cast(pose, m, grid_idx=None):
    '''Return the hit point at the nearest occupied grid along the ray direction'''
    #
    assert is_valid(pose, m), 'init pose is invalid: on the occupied grid'    
    
    # from the current pose, get the tip of the (trial) ray
    tip = get_tip(pose, m)
    
    # Construct the ray
    ray = LineString([(pose[0], pose[1]), (tip[0], tip[1])])
    
    # Construct the enclosing grid
    if grid_idx==None:
        grid_idx = get_grid_idx(pose[0], pose[1])
    print 'grid_idx=', grid_idx
    
    xmin = float(grid_idx[0])
    xmax = float(grid_idx[0]) + m['res']
    ymin = float(grid_idx[1])
    ymax = float(grid_idx[1]) + m['res']
    
    grid = box(xmin, ymin, xmax, ymax)
    
    # Obtain the intersection points
    hit_raw = ray.intersection(grid)
#    print 'list(hit_raw.coords)=', list(hit_raw.coords)
    
    hit = hit_raw.coords[1]# the first element is the ray origin 
    print 'hit=', hit
    
    #
    adj_grid_idx = get_adj_grid_idx(hit, grid_idx, grid)
    print 'adj_grid_idx=', adj_grid_idx
    
    if m['grid'][adj_grid_idx]==0:
        new_pose = (hit[0], hit[1], pose[2])
        hit = ray_cast(new_pose, m, grid_idx= adj_grid_idx)
    
    return hit

def test():
    # Construct the occupancy grid map
    grid_map = {'size': (5,5), 'res': 1.0}
    
    grid =  [1,1,1,1,1,\
             1,0,0,0,1,\
             1,0,0,0,1,\
             1,0,0,0,1,\
             1,1,1,1,1]
    assert len(grid)==grid_map['size'][0]*grid_map['size'][1], 'grid size is mismatched'
    grid = np.asarray(grid)
    grid = grid.reshape(grid_map['size'][0], grid_map['size'][1])
    grid_map['grid'] = grid

    #
    x = 2.5
    y = 2.5
    theta = math.pi/4*7
    pose = (x, y, theta)
    
    #
    hit = ray_cast(pose, grid_map)
    print '(final) hit=', hit

def test_2():
    '''From: http://www.reddit.com/r/dailyprogrammer/comments/1jz2os/080813_challenge_131_intermediate_simple/'''
    # Construct the occupancy grid map
    grid_map = {'size': (10,10), 'res': 1.0}
    
    grid =  [1,1,1,1,1,1,1,1,1,1,\
             1,0,0,1,0,1,0,0,0,1,\
             1,0,0,1,0,1,0,0,0,1,\
             1,0,0,0,0,1,0,1,1,1,\
             1,1,1,1,0,0,0,0,0,1,\
             1,0,0,1,0,0,0,0,0,1,\
             1,0,0,0,0,0,0,0,0,1,\
             1,0,0,1,0,0,0,0,0,1,\
             1,0,0,1,0,0,0,0,1,1,\
             1,1,1,1,1,1,1,1,1,1]
    assert len(grid)==grid_map['size'][0]*grid_map['size'][1], 'grid size is mismatched'
    grid = np.asarray(grid)
    grid = grid.reshape(grid_map['size'][0], grid_map['size'][1])
    grid_map['grid'] = grid
    
    #
    x = 6.5
    y = 6.5
    theta = 1.571
    pose = (x, y, theta)
    
    #
    hit = ray_cast(pose, grid_map)
    print '(final) hit=', hit
    
    # test output  
    target_hit = (6.500, 1.000)
    
    decimal.getcontext().prec = 2
    if target_hit == (decimal.Decimal(hit[0])/decimal.Decimal(1),decimal.Decimal(hit[1])/decimal.Decimal(1)):
        return True
    else:
        return False

def main():
#    test()

    assert test_2(),'test_2(): failed'
    print 'test_2(): passed'
    
if __name__ == "__main__":
    main()
