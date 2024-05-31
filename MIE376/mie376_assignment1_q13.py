#Aaryan Nagpal, 1007792596
#Question 13 from LP Problem Set

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Gasoline Blend Optimizer
opt_mod = Model(name="Gasoline Blend Optimizer")

#Defining variables for all components used in Lo-lead and premium blends, as well as those unused
#Also setting the lower bound on all variable values to be 0 to have 0 or more barrels used
#Setting optimization to continuous type to enable usage of part of barrels instead of just whole barrels
x_1=opt_mod.addVar(name="cat_cracked_barrels_for_lolead",vtype=GRB.CONTINUOUS, lb=0)
x_2=opt_mod.addVar(name="isopentane_barrels_for_lolead",vtype=GRB.CONTINUOUS, lb=0)
x_3=opt_mod.addVar(name="straight_gas_barrels_for_lolead",vtype=GRB.CONTINUOUS, lb=0)
y_1=opt_mod.addVar(name="cat_cracked_barrels_for_premium",vtype=GRB.CONTINUOUS, lb=0)
y_2=opt_mod.addVar(name="isopentane_barrels_for_premium",vtype=GRB.CONTINUOUS, lb=0)
y_3=opt_mod.addVar(name="straight_gas_barrels_for_premium",vtype=GRB.CONTINUOUS, lb=0)
z_1=opt_mod.addVar(name="cat_cracked_barrels_unused",vtype=GRB.CONTINUOUS, lb=0)
z_2=opt_mod.addVar(name="isopentane_barrels_unused",vtype=GRB.CONTINUOUS, lb=0)
z_3=opt_mod.addVar(name="straight_gas_barrels_unused",vtype=GRB.CONTINUOUS, lb=0)

#Defining the objective function to maximize the profit in a weeks gasoline blend production
obj_fn = 19.8*(x_1+x_2+x_3)+22*(y_1+y_2+y_3)+19*(z_1+z_2+z_3)
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on vapour pressure, octane number and barrel availability for components and blends
#as defined in the problem statement
vapour_pressure_lolead=opt_mod.addConstr((8*x_1+20*x_2+4*x_3)<=7*(x_1+x_2+x_3), name="vapour_pressure_lolead")
vapour_pressure_premium=opt_mod.addConstr((8*y_1+20*y_2+4*y_3)<=6*(y_1+y_2+y_3), name="vapour_pressure_premium")
octane_lolead=opt_mod.addConstr((83*x_1+109*x_2+74*x_3)>=80*(x_1+x_2+x_3), name="octane_lolead")
octane_premium=opt_mod.addConstr((83*y_1+109*y_2+74*y_3)>=100*(y_1+y_2+y_3), name="octane_premium")
cat_cracked_limit=opt_mod.addConstr(x_1+y_1<=2700, name="cat_cracked_limit")
isopentane_limit=opt_mod.addConstr(x_2+y_2<=1350, name="isopentane_limit")
straight_gas_limit=opt_mod.addConstr(x_3+y_3<=4100, name="straight_gas_limit")
unused_cat_cracked=opt_mod.addConstr(z_1==2700-x_1-y_1, name="unused_cat_cracked")
unused_isopentane=opt_mod.addConstr(z_2==1350-x_2-y_2, name="unused_isopentane")
unused_straight_gas=opt_mod.addConstr(z_3==4100-x_3-y_3, name="unused_straight_gas")

#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()
opt_mod.write("gasoline_blend_optimizer.lp")

#Displaying the maximized profit for the week in $, and all the optimized variable values in number of barrels
#of each component in each type of blend, as well as those unused
print('Profit in $ for weeks gasoline blend production: $%f' %opt_mod.ObjVal)
for v in opt_mod.getVars():
    print('%s: %g barrels' %(v.varName, v.x))