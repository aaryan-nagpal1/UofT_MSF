#Aaryan Nagpal, 1007792596
#Question 3

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Car Production Optimizer
opt_mod = Model(name="Car Production Optimizer 3")

#Defining variables for all types of cars to be produced, and setting the lower bound on all variable values to be 0
#Creating binary variables to account for the different production cases
#Setting optimization to integer type to have just integer number of cars
u_s=opt_mod.addVar(name="sprint_cars",vtype=GRB.INTEGER, lb=0)
u_v=opt_mod.addVar(name="voyager_cars",vtype=GRB.INTEGER, lb=0)
u_t=opt_mod.addVar(name="titan_cars",vtype=GRB.INTEGER, lb=0)
c_s=opt_mod.addVar(name="sprint_production_case_binary",vtype=GRB.BINARY)
c_v=opt_mod.addVar(name="voyager_production_case_binary",vtype=GRB.BINARY)
c_t=opt_mod.addVar(name="titan_production_case_binary",vtype=GRB.BINARY)
c_sv=opt_mod.addVar(name="sprint_voyager_production_case_binary",vtype=GRB.BINARY)
c_vt=opt_mod.addVar(name="voyager_titan_production_case_binary",vtype=GRB.BINARY)
c_st=opt_mod.addVar(name="sprint_titan_production_case_binary",vtype=GRB.BINARY)
c_svt=opt_mod.addVar(name="sprint_voyager_titan_production_case_binary",vtype=GRB.BINARY)

#Defining the objective function to maximize the profit in car production for possible production cases
obj_fn = c_s*((11*u_s)-(8*u_s)-180) + \
         c_v*((14*u_v)-(10*u_v)-240) + \
         c_t*((16*u_t)-(11*u_t)-240) + \
         c_sv*((11*u_s+14*u_v)-(8*u_s+10*u_v)-300) + \
         c_vt*((14*u_v+16*u_t)-(10*u_v+11*u_t)-400) + \
         c_st*((11*u_s+16*u_t)-(8*u_s+11*u_t)-420) + \
         c_svt*((11*u_s+14*u_v+16*u_t)-(8*u_s+10*u_v+11*u_t)-450)

opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on steel and labor availability as well as the production case
steel_limit=opt_mod.addConstr(1.5*u_s+3*u_v+5*u_t <= 600, name="steel_limit")
labour_limit=opt_mod.addConstr(280*u_s+250*u_v+320*u_t <= 60000, name="labour_limit")
case_pick=opt_mod.addConstr(c_s+c_v+c_t+c_sv+c_vt+c_st+c_svt==1, name="case_pick")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("car_production_optimizer3.lp")

#Displaying the maximized profit for the production in $, and all the optimized variable values in number of cars
print('Profit in k$ for car production: $%f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g cars' %(v.varName, v.x))