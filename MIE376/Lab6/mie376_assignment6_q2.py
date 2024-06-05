import gurobipy as gp
from gurobipy import GRB

# Only Change parameters
NODES = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
         'AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7',
         'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 
         'BC2', 'BC3', 'BC4', 'BC5', 'BC6',
         'C4', 'C5', 'C6', 'C7', 'C8',
         'Sink1', 'Sink2', 'Sink3', 'Sink4', 'Sink5', 'Sink6', 'Sink7', 'Sink8']

inject = {'A1': 100, 'A2': 100, 'A3': 100, 'A4': 100, 'A5': 100, 'A6': 100, 'A7': 100, 'A8': 100,
          'AB1': 0, 'AB2': 0, 'AB3': 0, 'AB4': 0, 'AB5': 0, 'AB6': 0, 'AB7': 0,
          'B2': 0, 'B3': 0, 'B4': 0, 'B5': 0, 'B6': 0, 'B7': 0, 'B8': 0,
          'BC2': 0, 'BC3': 0, 'BC4': 0, 'BC5': 0, 'BC6': 0,
          'C4': 0, 'C5': 0, 'C6': 0, 'C7': 0, 'C8': 0, 
          'Sink1': 0, 'Sink2' : 0, 'Sink3' : 0, 'Sink4' : 0, 'Sink5' : 0, 'Sink6' : 0, 'Sink7' : 0, 'Sink8' : 0}

prices = [20, 22, 25, 30, 25, 20, 20, 20]
efficiencies = [1.5, 4.2, 8.5]
max_energy = [50, 100, 150]

Arcs, lower, upper, value = gp.multidict({
    ('Source', 'A1'): [100, 100, 0],
    ('Source', 'A2'): [100, 100, 0],
    ('Source', 'A3'): [100, 100, 0],
    ('Source', 'A4'): [100, 100, 0],
    ('Source', 'A5'): [100, 100, 0],
    ('Source', 'A6'): [100, 100, 0],
    ('Source', 'A7'): [100, 100, 0],
    ('Source', 'A8'): [100, 100, 0],
    ('A1', 'AB1'): [0, GRB.INFINITY, 0],
    ('A2', 'AB2'): [0, GRB.INFINITY, 0],
    ('A3', 'AB3'): [0, GRB.INFINITY, 0],
    ('A4', 'AB4'): [0, GRB.INFINITY, 0],
    ('A5', 'AB5'): [0, GRB.INFINITY, 0],
    ('A6', 'AB6'): [0, GRB.INFINITY, 0],
    ('A7', 'AB7'): [0, GRB.INFINITY, 0],
    ('AB1', 'B2'): [0, GRB.INFINITY, 0],
    ('AB2', 'B3'): [0, GRB.INFINITY, 0],
    ('AB3', 'B4'): [0, GRB.INFINITY, 0],
    ('AB4', 'B5'): [0, GRB.INFINITY, 0],
    ('AB5', 'B6'): [0, GRB.INFINITY, 0],
    ('AB6', 'B7'): [0, GRB.INFINITY, 0],
    ('AB7', 'B8'): [0, GRB.INFINITY, 0],
    ('A1', 'B2'): [0, max_energy[0]/efficiencies[0], prices[0]*efficiencies[0]],
    ('A2', 'B3'): [0, max_energy[0]/efficiencies[0], prices[1]*efficiencies[0]],
    ('A3', 'B4'): [0, max_energy[0]/efficiencies[0], prices[2]*efficiencies[0]],
    ('A4', 'B5'): [0, max_energy[0]/efficiencies[0], prices[3]*efficiencies[0]],
    ('A5', 'B6'): [0, max_energy[0]/efficiencies[0], prices[4]*efficiencies[0]],
    ('A6', 'B7'): [0, max_energy[0]/efficiencies[0], prices[5]*efficiencies[0]],
    ('A7', 'B8'): [0, max_energy[0]/efficiencies[0], prices[6]*efficiencies[0]],
    ('A1', 'A2'): [0, GRB.INFINITY, 0],
    ('A2', 'A3'): [0, GRB.INFINITY, 0],
    ('A3', 'A4'): [0, GRB.INFINITY, 0],
    ('A4', 'A5'): [0, GRB.INFINITY, 0],
    ('A5', 'A6'): [0, GRB.INFINITY, 0],
    ('A6', 'A7'): [0, GRB.INFINITY, 0],
    ('A7', 'A8'): [0, GRB.INFINITY, 0],
    ('B2', 'BC2'): [0, GRB.INFINITY, 0],
    ('B3', 'BC3'): [0, GRB.INFINITY, 0],
    ('B4', 'BC4'): [0, GRB.INFINITY, 0],
    ('B5', 'BC5'): [0, GRB.INFINITY, 0],
    ('B6', 'BC6'): [0, GRB.INFINITY, 0],
    ('BC2', 'C4'): [0, GRB.INFINITY, 0],
    ('BC3', 'C5'): [0, GRB.INFINITY, 0],
    ('BC4', 'C6'): [0, GRB.INFINITY, 0],
    ('BC5', 'C7'): [0, GRB.INFINITY, 0],
    ('BC6', 'C8'): [0, GRB.INFINITY, 0],
    ('B2', 'C4'): [0, max_energy[1]/efficiencies[1], prices[1]*efficiencies[1]],
    ('B3', 'C5'): [0, max_energy[1]/efficiencies[1], prices[2]*efficiencies[1]],
    ('B4', 'C6'): [0, max_energy[1]/efficiencies[1], prices[3]*efficiencies[1]],
    ('B5', 'C7'): [0, max_energy[1]/efficiencies[1], prices[4]*efficiencies[1]],
    ('B6', 'C8'): [0, max_energy[1]/efficiencies[1], prices[5]*efficiencies[1]],
    ('B2', 'B3'): [0, GRB.INFINITY, 0],
    ('B3', 'B4'): [0, GRB.INFINITY, 0],
    ('B4', 'B5'): [0, GRB.INFINITY, 0],
    ('B5', 'B6'): [0, GRB.INFINITY, 0],
    ('B6', 'B7'): [0, GRB.INFINITY, 0],
    ('B7', 'B8'): [0, GRB.INFINITY, 0],
    ('C4', 'C5'): [0, GRB.INFINITY, 0],
    ('C5', 'C6'): [0, GRB.INFINITY, 0],
    ('C6', 'C7'): [0, GRB.INFINITY, 0],
    ('C7', 'C8'): [0, GRB.INFINITY, 0],
    ('C4', 'Sink'): [0, max_energy[2]/efficiencies[2], prices[3]*efficiencies[2]],
    ('C5', 'Sink'): [0, max_energy[2]/efficiencies[2], prices[4]*efficiencies[2]],
    ('C6', 'Sink'): [0, max_energy[2]/efficiencies[2], prices[5]*efficiencies[2]],
    ('C7', 'Sink'): [0, max_energy[2]/efficiencies[2], prices[6]*efficiencies[2]],
    ('C8', 'Sink'): [0, max_energy[2]/efficiencies[2], prices[7]*efficiencies[2]],
    ('A8', 'Sink'): [0, max_energy[0]/efficiencies[0], prices[7]*efficiencies[0]],
    ('B7', 'Sink'): [0, max_energy[1]/efficiencies[1], prices[6]*efficiencies[1]],
    ('B8', 'Sink'): [0, max_energy[1]/efficiencies[1], prices[7]*efficiencies[1]],
    ('C4', 'Sink1'): [0, GRB.INFINITY, 0],
    ('C5', 'Sink2'): [0, GRB.INFINITY, 0],
    ('C6', 'Sink3'): [0, GRB.INFINITY, 0],
    ('C7', 'Sink4'): [0, GRB.INFINITY, 0],
    ('C8', 'Sink5'): [0, GRB.INFINITY, 0],
    ('B7', 'Sink6'): [0, GRB.INFINITY, 0],
    ('B8', 'Sink7'): [0, GRB.INFINITY, 0],
    ('A8', 'Sink8'): [0, GRB.INFINITY, 0],
    ('Sink1', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink2', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink3', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink4', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink5', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink6', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink7', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink8', 'Sink'): [0, GRB.INFINITY, 0],
    ('Sink', 'Source'): [0, GRB.INFINITY, 0]})

######### Do not change rest of the code
m = gp.Model("Network_Programming")
Flows = {}

for i in Arcs:
    Flows[i] = m.addVar(vtype=GRB.CONTINUOUS)
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

