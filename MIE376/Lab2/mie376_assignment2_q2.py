#Aaryan Nagpal, 1007792596
#Question 2

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Maximizer
opt_mod = Model(name="Maximizer")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
x_1=opt_mod.addVar(name="x_1",vtype=GRB.CONTINUOUS)
x_2=opt_mod.addVar(name="x_2",vtype=GRB.CONTINUOUS)
x_3=opt_mod.addVar(name="x_3",vtype=GRB.CONTINUOUS)
x_4=opt_mod.addVar(name="x_4",vtype=GRB.CONTINUOUS)
x_5=opt_mod.addVar(name="x_5",vtype=GRB.CONTINUOUS)
x_6=opt_mod.addVar(name="x_6",vtype=GRB.CONTINUOUS)
x_7=opt_mod.addVar(name="x_7",vtype=GRB.CONTINUOUS)
x_8=opt_mod.addVar(name="x_8",vtype=GRB.CONTINUOUS)
x_9=opt_mod.addVar(name="x_9",vtype=GRB.CONTINUOUS)
x_10=opt_mod.addVar(name="x_10",vtype=GRB.CONTINUOUS)

#Defining the objective function to maximize
obj_fn = 3*x_1+2*x_2-x_3-2*x_4+x_5+2*x_6-x_7+3*x_8+4*x_9-3*x_10
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables
c_1=opt_mod.addConstr(2*x_1+x_2+3*x_3+x_4+2*x_5+x_6+4*x_7+x_8-2*x_9+3*x_10<=80, name="c_1")
c_2=opt_mod.addConstr(x_1-4*x_2+x_3+2*x_4+3*x_5+x_6-x_7+4*x_8+x_9+2*x_10<=50, name="c_2")
c_3=opt_mod.addConstr(3*x_1+2*x_2-2*x_3-x_4+x_5+3*x_6+2*x_7+x_8+x_9+x_10<=40, name="c_3")
c_4=opt_mod.addConstr(2*x_1+3*x_2+x_3+x_4+x_5+x_6+x_7+x_8+3*x_9+2*x_10<=90, name="c_4")
c_5=opt_mod.addConstr(x_1+x_2+x_3+x_4+x_5+x_6+x_7+x_8+x_9+x_10<=50, name="c_5")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("maximizer.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
