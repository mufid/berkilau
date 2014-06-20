#!/usr/bin/python

from mdp import *
import numpy as np
import sys

# INIT
#Fig[17,1] = GridMDP([[-0.02, -0.02, -0.02, +1],
#                     [-0.02, None,  -0.02, -1],
#                     [-0.02, -0.02, -0.02, -0.02]], 
#                    terminals=[(3, 2), (3, 1)], gamma=.99)

#Ricky = GridMDP([[-0.02, -0.02, -0.02, -0.02, -0.02],
 #                [-0.02, -0.02, -0.02, -0.02, -0.02],
  #               [-0.02, -0.02, -0.02, -0.02, -0.02],
   #              [-0.02, -0.02, -0.02, -0.02, -0.02],
    #             [+1.00, -0.02, -0.02, -0.02, -0.02]], 
     #            terminals=[(0, 0)], gamma=.99)
epsilon = 0.001# converge criterion

Ricky = GridMDP([[-0.02, -0.02, -0.02, -0.02, -0.02, +1.00, +1.00, +1.00],
                 [-0.02, -0.02, -0.02, -0.02, -0.02, +1.00, None, +1.00],
                 [-0.02, -0.02, -0.02, None, -0.02, +1.00, +1.00, +1.00],
                 [-0.02, -0.02, -0.02, -0.02, -1.00, -1.00, -1.00, -0.02],
                 [-0.02, -0.02, -0.02, -0.02, -1.00, None, -1.00, -0.02],
                 [-0.02, -0.02, -0.02, -0.02, -1.00, -1.00, -1.00, -0.02]], 
                 terminals=[(4, 0), (5, 0), (6, 0),
                            (4, 1), (6, 1),
                            (4, 2), (5, 2), (6, 2),
                            (5, 3), (5, 4), (5, 5),
                            (6, 3), (6, 5),
                            (7, 3), (7, 4), (7, 5)], gamma=.99)

##################################################
#print '>>> For the example shown in the class <<<'
#m = Fig[17,1]
#V = value_iteration(m, epsilon)

#n_row, n_col = m.grid_shape()
#V_arr = np.zeros((n_row,n_col))
#for i in range(n_row):# over rows of the matrix
#    for j in range(n_col):# over columns of the matrix
#        y = abs(i-(n_row-1))
#        x = j
#        grid_idx = (x,y)
                
#        if grid_idx in V:
#            V_arr[i,j] = V[grid_idx]
#        else:
#            V_arr[i,j] = None
            
#print 'V* (epsilon=', epsilon,')='
#print V_arr

#print 'Best policy:'

#pi = best_policy(m, V)
#print_table(m.to_arrows(pi))

print " >>> Exam's Answer <<<"
m = Ricky
V = value_iteration(m, epsilon)

n_row, n_col = m.grid_shape()
V_arr = np.zeros((n_row,n_col))
for i in range(n_row):# over rows of the matrix
    for j in range(n_col):# over columns of the matrix
        y = abs(i-(n_row-1))
        x = j
        grid_idx = (x,y)
                
        if grid_idx in V:
            V_arr[i,j] = V[grid_idx]
        else:
            V_arr[i,j] = None
            
print 'V* (epsilon=', epsilon,')='
print V_arr

print 'Best policy:'

pi = best_policy(m, V)
print_table(m.to_arrows(pi))

