#Aaryan Nagpal, 1007792596
#Question 2

#Importing all functions from the gurobipy and numpy libraries
from gurobipy import *
import numpy as np

#Creating an optimization model called Simple Maximizer
opt_mod = Model(name="Quadratic Optimizer")

#Defining the A matrix and b vector for sensor measurements and projections as given in the question
b = np.array([0.3, 1.0, 0.8, 0.7, 0.5])
#Transposing b to match Ax=b setup
b=b.T

A = np.array([[1.0, 0.5, 0.3, 0.2, 0.1, 0.7, 0.2, 0.1], 
              [0.5, 1.0, 0.4, 0.3, 0.2, 0.1, 0.3, 0.9], 
              [0.4, 0.4, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1], 
              [0.3, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2], 
              [0.2, 0.2, 0.5, 0.8, 1.0, 0.8, 0.6, 0.4]])

#Defining variables and setting the lower bound on all variable values to be 0 as the only constraint
x=opt_mod.addMVar((8,), name="x", lb=0)

#Creating the objective function using the Q and q^T as formulated in the writeup for this question
#This models 1/2x^tQx + q^tx
opt_mod.setObjective(x.T@A.T@A@x - 2*b.T@A@x + b.T@b)

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("quadratic_optimizer.lp")

#Displaying the minimized least squares objective function value and variable values
print('Minimized non-negative least squares fit error: %f' % round(opt_mod.ObjVal,2))
print(" ")
print("Optimal NNLS transfer function values in x vector")
for v in range(len(opt_mod.getVars())):
    print('x_' + str(v+1), ': %g' %(round(opt_mod.getVars()[v].x, 2)))