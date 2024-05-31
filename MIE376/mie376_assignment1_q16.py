#Aaryan Nagpal, 1007792596
#Question 16 from LP Problem Set

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Transport Cargo Optimizer
opt_mod = Model(name="Transport Cargo Optimizer")

#Defining variables for all cargo units in front, center, and back compartments of the place
#Also setting the lower bound on all variable values to be 0 to have 0 or more units of cargo
#Setting optimization to continuous type to enable usage of part of cargo instead of just whole cargo
x_a=opt_mod.addVar(name="front_cargoA",vtype=GRB.CONTINUOUS, lb=0)
x_b=opt_mod.addVar(name="front_cargoB",vtype=GRB.CONTINUOUS, lb=0)
x_c=opt_mod.addVar(name="front_cargoC",vtype=GRB.CONTINUOUS, lb=0)
x_d=opt_mod.addVar(name="front_cargoD",vtype=GRB.CONTINUOUS, lb=0)
y_a=opt_mod.addVar(name="center_cargoA",vtype=GRB.CONTINUOUS, lb=0)
y_b=opt_mod.addVar(name="center_cargoB",vtype=GRB.CONTINUOUS, lb=0)
y_c=opt_mod.addVar(name="center_cargoC",vtype=GRB.CONTINUOUS, lb=0)
y_d=opt_mod.addVar(name="center_cargoD",vtype=GRB.CONTINUOUS, lb=0)
z_a=opt_mod.addVar(name="back_cargoA",vtype=GRB.CONTINUOUS, lb=0)
z_b=opt_mod.addVar(name="back_cargoB",vtype=GRB.CONTINUOUS, lb=0)
z_c=opt_mod.addVar(name="back_cargoC",vtype=GRB.CONTINUOUS, lb=0)
z_d=opt_mod.addVar(name="back_cargoD",vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to maximize the profit in transporting cargo types in plane compartments
obj_fn = 220*20*(x_a+y_a+z_a)+280*16*(x_b+y_b+z_b)+250*25*(x_c+y_c+z_c)+200*13*(x_d+y_d+z_d)
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on compartment wise weight and space limits, as well as compartment weight  
#balancing ratios for all compartments on the plane regardless of cargo limit as mentioned in the problem
front_cargo=opt_mod.addConstr((20*x_a+16*x_b+25*x_c+13*x_d)<=120, name="front_cargo")
center_cargo=opt_mod.addConstr((20*y_a+16*y_b+25*y_c+13*y_d)<=180, name="center_cargo")
back_cargo=opt_mod.addConstr((20*z_a+16*z_b+25*z_c+13*z_d)<=100, name="back_cargo")
front_space=opt_mod.addConstr((500*x_a+700*x_b+600*x_c+400*x_d)<=7000, name="front_space")
center_space=opt_mod.addConstr((500*y_a+700*y_b+600*y_c+400*y_d)<=9000, name="center_space")
back_space=opt_mod.addConstr((500*z_a+700*z_b+600*z_c+400*z_d)<=5000, name="back_space")
front_center_weight_ratio=opt_mod.addConstr(((20*x_a+16*x_b+25*x_c+13*x_d)/120)==
                                           ((20*y_a+16*y_b+25*y_c+13*y_d)/180), name="front_center_weight_ratio")
center_back_weight_ratio=opt_mod.addConstr(((20*y_a+16*y_b+25*y_c+13*y_d)/180)==
                                           ((20*z_a+16*z_b+25*z_c+13*z_d)/100), name="center_back_weight_ratio")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("transport_cargo_optimizer.lp")

#Displaying the maximized profit for transport company in $, and all the optimized variable values in 
#number of units of each type of cargo in each type of compartment
print('Profit in $ for transport company: $%f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g units' %(v.varName, v.x))