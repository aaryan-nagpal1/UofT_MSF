#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Simple Minimizer
opt_mod = Model(name="Simple Minimizer")

#Defining decision variables and setting the lower bound on all variable values to be 0
#Setting optimization to continuous type to enable usage of real number solutions
y_1=opt_mod.addVar(name="y_1",vtype=GRB.CONTINUOUS, lb=0)
y_2=opt_mod.addVar(name="y_2",vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to minimize
obj_fn = 6*y_1+8*y_2
opt_mod.setObjective(obj_fn, GRB.MINIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(y_1+2*y_2>=2, name="c_1")
c_2=opt_mod.addConstr(2*y_1+y_2>=3, name="c_2")


#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("simple_minimizer.lp")

#Displaying the minimized objective function value and variable values
print('Minimized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))