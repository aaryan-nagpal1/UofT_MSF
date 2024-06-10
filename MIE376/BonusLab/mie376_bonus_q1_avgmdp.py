#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called AVGMDP
opt_mod = Model(name="AVGMDP")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
pi=opt_mod.addVars(range(0,7), name="pi", vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to minimize
obj_fn = 9*pi[0]+13.5*pi[1]+14*pi[2]+50*pi[3]+0*pi[4]+4.5*pi[5]+5*pi[6]
opt_mod.setObjective(obj_fn, GRB.MINIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(pi[4]+pi[5]+pi[6] == pi[6]+pi[3]+0.98*pi[5]+0.9*pi[4], name="c_1")
c_2=opt_mod.addConstr(pi[0]+pi[1]+pi[2]+pi[3]+pi[4]+pi[5]+pi[6] == 1, name="c_2")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("AVGMDP.lp")

#Displaying the minimized objective function value and variable values
print('Minimized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))