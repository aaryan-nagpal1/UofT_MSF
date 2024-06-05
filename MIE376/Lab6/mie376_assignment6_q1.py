import gurobipy as gp
from gurobipy import GRB

#####Only Change parameters
NODES = ['PL1', 'PL2', 'PL3', 'SP1', 'SP2', 'SP3', 'WP1', 'WP2', 'WP3', 'P']

inject = {
    'PL1': 0,
    'PL2': 0,
    'PL3': 0,
    'SP1': 1200,
    'SP2': 0,
    'SP3': 0,
    'WP1': 100,
    'WP2': 0,
    'WP3': 0,
    'P': 0}

Arcs, lower, upper, value = gp.multidict({
    ('Source', 'PL1'): [0, 1500, 0],
    ('Source', 'PL2'): [0, 1500, 0],
    ('Source', 'PL3'): [0, 1500, 0],
    ('PL1', 'SP1'): [0, GRB.INFINITY, -6000],
    ('PL1', 'WP1'): [0, GRB.INFINITY, -7500],
    ('PL2', 'SP2'): [0, GRB.INFINITY, -6000],
    ('PL2', 'WP2'): [0, GRB.INFINITY, -7500],
    ('PL3', 'SP3'): [0, GRB.INFINITY, -6000],
    ('PL3', 'WP3'): [0, GRB.INFINITY, -7500],
    ('SP1', 'SP2'): [0, GRB.INFINITY, -150],
    ('SP2', 'SP3'): [0, GRB.INFINITY, -150],
    ('WP1', 'WP2'): [0, GRB.INFINITY, -200],
    ('WP2', 'WP3'): [0, GRB.INFINITY, -200],
    ('SP1', 'P'): [0, 1100, 8000],
    ('SP2', 'P'): [0, 1500, 8000],
    ('SP3', 'P'): [0, 1200, 8000],
    ('WP1', 'P'): [0, 600, 9000],
    ('WP2', 'P'): [0, 700, 9000],
    ('WP3', 'P'): [0, 50, 9000],
    ('P', 'Sink'): [0, GRB.INFINITY, 0]})

######### Do not change rest of the code
m = gp.Model("Network_Programming")
Flows = {}

for i in Arcs:
    Flows[i]= m.addVar( vtype=GRB.INTEGER )
    Flows[i].setAttr("ub", upper[i])
    Flows[i].setAttr("lb", lower[i])
    
m.setObjective( gp.quicksum(Flows[i]*value[i] for i in Arcs) , GRB.MAXIMIZE)
m.addConstrs(gp.quicksum(Flows[k] for k in Arcs.select(i,'*')) -
gp.quicksum(Flows[l] for l in Arcs.select('*',i)) - inject[i] == 0 for i in
NODES)

m.update()
m.optimize()
m.display()

#print variable values
for v in m.getVars():
    print('%s: %g' %(v.varName, v.x))