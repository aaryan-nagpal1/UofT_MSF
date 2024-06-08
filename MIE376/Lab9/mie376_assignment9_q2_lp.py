#Aaryan Nagpal, 1007792596
#Question 2 pt b

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called LP2
opt_mod = Model(name="LP2")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
v=opt_mod.addVars(range(0,4), name="v", vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to minimize
obj_fn = v[0]+v[1]+v[2]+v[3]
opt_mod.setObjective(obj_fn, GRB.MINIMIZE)


#Setting constraints on the defined variables
c_1=opt_mod.addConstr(v[0] >= -1+0.9*(0.8*v[0]+0.2*v[1]), name="c_1")
c_2=opt_mod.addConstr(v[0] >= (20-5)+0.9*(0.8*v[0]+0.2*v[1]), name="c_2")
c_3=opt_mod.addConstr(v[1]>= -1+0.9*(0.9*v[2]+0.1*v[3]), name="c_3")
c_4=opt_mod.addConstr(v[1] >= (30-5)+0.9*(0.8*v[0]+0.2*v[1]), name="c_4")
c_5=opt_mod.addConstr(v[2] >= -1+0.9*(0.7*v[2]+0.3*v[3]), name="c_5")
c_6=opt_mod.addConstr(v[2] >= (45-5)+0.9*(0.8*v[0]+0.2*v[1]), name="c_6")
c_7=opt_mod.addConstr(v[3] >= -1+0.9*(v[3]), name="c_7")
c_8=opt_mod.addConstr(v[3] >= (49-5)+0.9*(0.8*v[0]+0.2*v[1]), name="c_8")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("LP2.lp")

#Displaying the minimized objective function value and variable values
print('Minimized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
    
#Shadow prices
print("Shadow price:")
print("y1: {:.2f}".format(c_1.Pi))
print("y2: {:.2f}".format(c_2.Pi))
print("y3: {:.2f}".format(c_3.Pi))
print("y4: {:.2f}".format(c_4.Pi))
print("y5: {:.2f}".format(c_5.Pi))
print("y6: {:.2f}".format(c_6.Pi))
print("y7: {:.2f}".format(c_7.Pi))
print("y8: {:.2f}".format(c_8.Pi))
print(" ")