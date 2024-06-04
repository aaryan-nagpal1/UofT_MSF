#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Simple Bi-Level
opt_mod = Model(name="Simple Bi-level")

#Defining variables and setting the lower bound on all variable values to be 0 except x, y (decision variables)
#Setting optimization to continuous type to enable usage of real number solutions
x=opt_mod.addVar(name="x",vtype=GRB.CONTINUOUS)
y=opt_mod.addVar(name="y",vtype=GRB.CONTINUOUS)
s1=opt_mod.addVar(name="s1",vtype=GRB.CONTINUOUS, lb=0)
s2=opt_mod.addVar(name="s2",vtype=GRB.CONTINUOUS, lb=0)
lambda1=opt_mod.addVar(name="lambda1",vtype=GRB.CONTINUOUS, lb=0)
lambda2=opt_mod.addVar(name="lambda2",vtype=GRB.CONTINUOUS, lb=0)


#Defining the objective function to maximize
obj_fn = x+2*y
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables for the bilevel problem
c_1=opt_mod.addConstr(2*x-3*y>=-12, name="c_1")
c_2=opt_mod.addConstr(x+y<=14, name="c_2")
c_3=opt_mod.addConstr(lambda1+lambda2==1, name="c_3")
c_4=opt_mod.addConstr(-3*x+y+s1==-3, name="c_4")
c_5=opt_mod.addConstr(3*x+y+s2==30, name="c_5")
c_6=opt_mod.addConstr(lambda1*s1==0, name="c_6")
c_7=opt_mod.addConstr(lambda2*s2==0, name="c_7")


#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("simple_bilevel.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))