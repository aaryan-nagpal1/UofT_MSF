#Aaryan Nagpal, 1007792596
#Question 1

#Importing all functions from the gurobipy library
from gurobipy import *

#Creating an optimization model called Simple Maximizer
opt_mod = Model(name="Stochastic Maximizer")

#Defining decision variables and setting the lower bound on all variable values to be 0 except for
#flavour concentrates and raw syrup which have to be 300 atleast in order to meet minimum production requirements
#Setting upper bound constraints on low and high production cases for each syrup based on probabilities
#Setting optimization to continuous type to enable usage of real number solutions
p_vl=opt_mod.addVar(name="p_vl",vtype=GRB.CONTINUOUS, lb=300, ub=500)
p_vh=opt_mod.addVar(name="p_vh",vtype=GRB.CONTINUOUS, lb=300, ub=900)
p_ml=opt_mod.addVar(name="p_ml",vtype=GRB.CONTINUOUS, lb=300, ub=300)
p_mh=opt_mod.addVar(name="p_mh",vtype=GRB.CONTINUOUS, lb=300, ub=600)
p_cl=opt_mod.addVar(name="p_cl",vtype=GRB.CONTINUOUS, lb=300, ub=700)
p_ch=opt_mod.addVar(name="p_ch",vtype=GRB.CONTINUOUS, lb=300, ub=1100)
f_v=opt_mod.addVar(name="f_v",vtype=GRB.CONTINUOUS, lb=300)
f_m=opt_mod.addVar(name="f_m",vtype=GRB.CONTINUOUS, lb=300)
f_c=opt_mod.addVar(name="f_c",vtype=GRB.CONTINUOUS, lb=300)

#Definining low and high case probabilities for each syrups production, and also the syrup specific objective
#as well as the costs associated with production
prob_v=[0.4, 0.6]
prob_m=[0.5, 0.5]
prob_c=[0.7, 0.3]

obj_lll = prob_v[1]*prob_m[1]*prob_c[1]*(6*p_vl+7*p_ml+8*p_cl)
obj_llh = prob_v[1]*prob_m[1]*prob_c[0]*(6*p_vl+7*p_ml+8*p_ch)
obj_lhh = prob_v[1]*prob_m[0]*prob_c[0]*(6*p_vl+7*p_mh+8*p_ch)
obj_hlh = prob_v[0]*prob_m[1]*prob_c[0]*(6*p_vh+7*p_ml+8*p_ch)
obj_lhl = prob_v[1]*prob_m[0]*prob_c[1]*(6*p_vl+7*p_mh+8*p_cl)
obj_hll = prob_v[0]*prob_m[1]*prob_c[1]*(6*p_vh+7*p_ml+8*p_cl)
obj_hhl = prob_v[0]*prob_m[0]*prob_c[1]*(6*p_vh+7*p_mh+8*p_cl)
obj_hhh = prob_v[0]*prob_m[0]*prob_c[0]*(6*p_vh+7*p_mh+8*p_ch)
obj_costs = 2.5*f_v+2.5*f_m+3.0*f_c


#Defining the objective function to maximize
obj_fn = obj_lll+obj_llh+obj_lhh+obj_hlh+obj_lhl+obj_hll+obj_hhl+obj_hhh-obj_costs
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

#Setting constraints on the defined variables
case_llh=opt_mod.addConstr(p_vl+p_ml+p_ch<=1800, name="scenario_1")
case_lhh=opt_mod.addConstr(p_vl+p_mh+p_ch<=1800, name="scenario_2")
case_hlh=opt_mod.addConstr(p_vh+p_ml+p_ch<=1800, name="scenario_3")
case_hhl=opt_mod.addConstr(p_vh+p_mh+p_cl<=1800, name="scenario_4")
case_hll=opt_mod.addConstr(p_vh+p_ml+p_cl<=1800, name="scenario_5")
case_lhl=opt_mod.addConstr(p_vl+p_mh+p_cl<=1800, name="scenario_6")
case_lll=opt_mod.addConstr(p_vl+p_ml+p_cl<=1800, name="scenario_7")
case_hhh=opt_mod.addConstr(p_vh+p_mh+p_ch<=1800, name="scenario_8")
flavour_vl=opt_mod.addConstr(f_v>=p_vl, name="v_low_flavour")
flavour_vh=opt_mod.addConstr(f_v>=p_vh, name="v_high_flavour")
flavour_ml=opt_mod.addConstr(f_m>=p_ml, name="m_low_flavour")
flavour_mh=opt_mod.addConstr(f_m>=p_mh, name="m_high_flavour")
flavour_cl=opt_mod.addConstr(f_c>=p_cl, name="c_low_flavour")
flavour_ch=opt_mod.addConstr(f_c>=p_ch, name="c_high_flavour")


#Calling the optimizer to optimize based on the constraints set above, and writing the LP model to a file
opt_mod.optimize()  
opt_mod.write("stochastic_maximizer.lp")

#Displaying the maximized objective function value and variable values
for v in opt_mod.getVars():
    print('%s: %g' %(v.varName, v.x))
print(" ")
print('Profit for weekly production and sales of syrups: $%f' %opt_mod.ObjVal)
print(" ")
print("The amount of syrup of each type produced is :")
print('Vanilla syrup produced : ', max(p_vh.x, p_vl.x) , 'litres')
print('Maple syrup produced : ', max(p_mh.x, p_ml.x) , 'litres')
print('Cherry syrup produced : ', max(p_ch.x, p_cl.x) , 'litres')