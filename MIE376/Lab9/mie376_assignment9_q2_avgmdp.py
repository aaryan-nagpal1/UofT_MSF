#Aaryan Nagpal, 1007792596
#Question 2 pt d

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called MDP2
opt_mod = Model(name="MDP2")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
pi=opt_mod.addVars(range(0,8), name="pi", vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to maximize
obj_fn = -pi[0]+15*pi[1]-pi[2]+25*pi[3]-pi[4]+40*pi[5]-pi[6]+44*pi[7]
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(pi[2]+pi[3] == 0.2*pi[0]+0.2*pi[5]+0.2*pi[7]+0.2*pi[1]+0.2*pi[3], name="c_1")
c_2=opt_mod.addConstr(pi[4]+pi[5] == 0.9*pi[2]+0.7*pi[4], name="c_2")
c_3=opt_mod.addConstr(pi[6]+pi[7] == 0.1*pi[2]+0.3*pi[4]+pi[6], name="c_3")
c_4=opt_mod.addConstr(pi[0]+pi[1]+pi[2]+pi[3]+pi[4]+pi[5]+pi[6]+pi[7] == 1, name="c_4")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("MDP2.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))