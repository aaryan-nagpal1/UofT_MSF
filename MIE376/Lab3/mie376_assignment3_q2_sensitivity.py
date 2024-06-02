#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Simple Maximizer
opt_mod = Model(name="Simple Maximizer")

#Defining variables and setting the lower bound on all variable values to be 0
x=opt_mod.addVars(range(1,3), name="x", lb=0)

#Defining the objective function to minimize
obj_fn = 2*x[1]+3*x[2]
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(x[1]+2*x[2]<=6, name="c_1")
c_2=opt_mod.addConstr(2*x[1]+x[2]<=8, name="c_2")


#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("simple_maximizer_2.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
print(" ")
    
#Reduced costs
print("Reduced cost:")
print("x1: {:.2f}".format(x[1].Rc))
print("x2: {:.2f}".format(x[2].Rc))
print(" ")

#Range of objective coefficients
print("Objective coefficient ranges that basis remains optimal:")
delta1_lb = x[1].SAObjLow - x[1].Obj
delta1_ub = x[1].SAObjUp - x[1].Obj
delta2_lb = x[2].SAObjLow - x[2].Obj
delta2_ub = x[2].SAObjUp - x[2].Obj
print("x1: The change of coefficient is from {:.2f} to {:.2f}".format(delta1_lb, delta1_ub))
print("x2: The change of coefficient is from {:.2f} to {:.2f}".format(delta2_lb, delta2_ub))
print(" ")

#Shadow prices
print("Shadow price:")
print("y1: {:.2f}".format(c_1.Pi))
print("y2: {:.2f}".format(c_2.Pi))
print(" ")

#Range of rhs values
print("RHS ranges that basis remains optimal:")
delta1_lb = c_1.SARHSLow - c_1.RHS
delta1_ub = c_1.SARHSUp - c_1.RHS
delta2_lb = c_2.SARHSLow - c_2.RHS
delta2_ub = c_2.SARHSUp - c_2.RHS
print("y1: The change of value is from {:.2f} to {:.2f}".format(delta1_lb, delta1_ub))
print("y1: The change of value is from {:.2f} to {:.2f}".format(delta2_lb, delta2_ub))