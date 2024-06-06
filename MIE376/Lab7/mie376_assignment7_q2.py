#Aaryan Nagpal, 1007792596
#Question 2

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Car Production Optimizer
opt_mod = Model(name="Car Production Optimizer 2")

#Defining variables for all types of cars to be produced, and setting the lower bound on all variable values to be 0
#Also setting the production binary variables to be binary type to have a minimum production of 70 cars
#Setting optimization to integer type to have just integer number of cars
u_s=opt_mod.addVar(name="sprint_cars",vtype=GRB.INTEGER, lb=0)
u_v=opt_mod.addVar(name="voyager_cars",vtype=GRB.INTEGER, lb=0)
u_t=opt_mod.addVar(name="titan_cars",vtype=GRB.INTEGER, lb=0)
p_s=opt_mod.addVar(name="sprint_production_binary",vtype=GRB.BINARY)
p_v=opt_mod.addVar(name="voyager_production_binary",vtype=GRB.BINARY)
p_t=opt_mod.addVar(name="titan_production_binary",vtype=GRB.BINARY)

#Defining the objective function to maximize the profit in car production
obj_fn = (11*u_s*p_s+14*u_v*p_v+16*u_t*p_t)-(8*u_s*p_s+10*u_v*p_v+11*u_t*p_t)
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on steel and labor availability, as well as the minimum production of 70 cars if
#the production binary variable is set to 1
steel_limit=opt_mod.addConstr(1.5*u_s+3*u_v+5*u_t <= 600, name="steel_limit")
labour_limit=opt_mod.addConstr(280*u_s+250*u_v+320*u_t <= 60000, name="labour_limit")
sprint_production_lower_limit=opt_mod.addConstr(70*p_s <= u_s, name="sprint_production_lower_limit")
sprint_production_upper_limit=opt_mod.addConstr(u_s <= GRB.INFINITY*p_s, name="sprint_production_upper_limit")
voyager_production_lower_limit=opt_mod.addConstr(70*p_v <= u_v, name="voyager_production_lower_limit")
voyager_production_upper_limit=opt_mod.addConstr(u_v <= GRB.INFINITY*p_v, name="voyager_production_upper_limit")
titan_production_lower_limit=opt_mod.addConstr(70*p_t <= u_t, name="titan_production_lower_limit")
titan_production_upper_limit=opt_mod.addConstr(u_t <= GRB.INFINITY*p_t, name="titan_production_upper_limit")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("car_production_optimizer2.lp")

#Displaying the maximized profit for the production in $, and all the optimized variable values in number of cars
print('Profit in k$ for car production: $%f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g cars' %(v.varName, v.x))