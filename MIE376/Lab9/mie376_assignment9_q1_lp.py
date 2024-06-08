#Aaryan Nagpal, 1007792596
#Question 1 pt b

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called LP1
opt_mod = Model(name="LP1")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
v=opt_mod.addVars(range(0,3), name="v", vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to maximize
obj_fn = v[0]+v[1]+v[2]
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(v[0] <= 500000+0.9*(0.7*v[0]+0.2*v[1]+0.1*v[2]), name="c_1")
c_2=opt_mod.addConstr(v[1] <= 1000000+0.9*(0.6*v[1]+0.4*v[2]), name="c_2")
c_3=opt_mod.addConstr(v[1] <= 2500000+0.9*(0.7*v[0]+0.2*v[1]+0.1*v[2]), name="c_3")
c_4=opt_mod.addConstr(v[2] <= 2000000+0.9*(v[2]), name="c_4")
c_5=opt_mod.addConstr(v[2] <= 3500000+0.9*(0.7*v[0]+0.2*v[1]+0.1*v[2]), name="c_5")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("LP1.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
    
#Shadow prices
print("Shadow price:")
print("y1: {:.2f}".format(c_1.Pi))
print("y2: {:.2f}".format(c_2.Pi))
print("y3: {:.2f}".format(c_3.Pi))
print("y4: {:.2f}".format(c_4.Pi))
print("y5: {:.2f}".format(c_5.Pi))
print(" ")