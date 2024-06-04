#Aaryan Nagpal, 1007792596
#Question 2

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Iterative Bi-Level 1
opt_mod = Model(name="Iterative Bi-level 1")

#Defining decision variables and setting optimization to continuous type to enable usage of real number solutions
x=opt_mod.addVar(name="x",vtype=GRB.CONTINUOUS)
y=opt_mod.addVar(name="y",vtype=GRB.CONTINUOUS)

#Defining the objective function to maximize
obj_fn = x+2*y
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables for the bilevel problem
c_1=opt_mod.addConstr(2*x-3*y>=-12, name="c_1")
c_2=opt_mod.addConstr(x+y<=14, name="c_2")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("iterative_bilevel1.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))

#setting a new variable to be equal to the x-value from upper level problem iteration 1 solution
#to be used in lower level problem (iteration 2)
iter1_x=x.X

#Creating an optimization model called Iterative Bi-Level 2
opt_mod = Model(name="Iterative Bi-level 2")

#Defining decision variable and setting optimization to continuous type to enable usage of real number solutions
y=opt_mod.addVar(name="y",vtype=GRB.CONTINUOUS)

#Defining the objective function to maximize
obj_fn = y
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables for the bilevel problem and using the variable for x-value
#we defined earlier from iteration 1 to set constraints
c_1=opt_mod.addConstr(3*iter1_x-y>=3, name="c_1")
c_2=opt_mod.addConstr(3*iter1_x+y<=30, name="c_2")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("iterative_bilevel2.lp")

#Displaying the maximized objective function value and variable values
print('Maximized objective function: %f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
print("x:", int(iter1_x))

#setting a new variable to be equal to the y-value from lower level problem iteration 2 solution
#to be used in upper level problem (iteration 3)
iter2_y=y.X

#Creating an optimization model called Iterative Bi-Level 3
opt_mod = Model(name="Iterative Bi-level 3")

#Defining variables and setting optimization to continuous type to enable usage of real number solutions
x=opt_mod.addVar(name="x",vtype=GRB.CONTINUOUS)

#Defining the objective function to maximize and using the variable for y-value
#we defined earlier from iteration 2 to set objective function and contraints below
obj_fn = x+2*iter2_y
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables for the bilevel problem
c_1=opt_mod.addConstr(2*x-3*iter2_y>=-12, name="c_1")
c_2=opt_mod.addConstr(x+iter2_y<=14, name="c_2")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("iterative_bilevel3.lp")

#Problem at this point becomes infeasible as seen in the output when run, so nothing is printed for
#variable values to avoid raising exceptions and errors




