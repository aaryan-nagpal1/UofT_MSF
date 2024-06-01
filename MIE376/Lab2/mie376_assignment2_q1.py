#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Simple Minimizer
opt_mod = Model(name="Simple Minimizer")

#Defining variables and setting the lower bound on all variable values to be 0
#Setting optimization to continuous type to enable usage of real number solutions
x_1=opt_mod.addVar(name="x_1",vtype=GRB.CONTINUOUS, lb=0)
x_2=opt_mod.addVar(name="x_2",vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to minimize
obj_fn = -3*x_1+8*x_2
opt_mod.setObjective(obj_fn, GRB.MINIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(4*x_1+2*x_2<=12, name="c_1")
c_2=opt_mod.addConstr(2*x_1+3*x_2<=6, name="c_2")


#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("simple_minimizer.lp")

#Displaying the minimized objective function value and variable values
print('Minimized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
