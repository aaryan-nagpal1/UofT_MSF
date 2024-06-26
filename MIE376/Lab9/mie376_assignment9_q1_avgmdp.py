#Aaryan Nagpal, 1007792596
#Question 1 pt d

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called MDP1
opt_mod = Model(name="MDP1")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
pi=opt_mod.addVars(range(0,6), name="pi", vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to minimize
obj_fn = 500000*pi[0]+500000*pi[1]+1000000*pi[2]+2500000*pi[3]+2000000*pi[4]+3500000*pi[5]
opt_mod.setObjective(obj_fn, GRB.MINIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(pi[2]+pi[3] == 0.2*pi[0]+0.6*pi[2]+0.2*pi[1]+0.2*pi[3]+0.2*pi[5], name="c_1")
c_2=opt_mod.addConstr(pi[4]+pi[5] == 0.1*pi[0]+0.4*pi[2]+pi[4]+0.1*pi[1]+0.1*pi[3]+0.1*pi[5], name="c_2")
c_3=opt_mod.addConstr(pi[0]+pi[1]+pi[2]+pi[3]+pi[4]+pi[5] == 1, name="c_3")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("MDP1.lp")

#Displaying the minimized objective function value and variable values
print('Minimized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))