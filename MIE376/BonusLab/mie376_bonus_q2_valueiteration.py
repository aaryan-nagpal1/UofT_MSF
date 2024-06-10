#Initial guesses
vd = 0
vn = 0

#Scenario wise costs (o = one space, t = two space, p = parking lot, r = repair)
rdo = 9
rdt = 13.5
rdp = 14
rdr = 50
rno = 0
rnt = 4.5
rnp = 5

#Optimal policy
policy = [0, 0]

#Running 100 itetations of value iteration to find the optimal policy
for i in range(100):
    # Bellman equations as formulated
    vd0=0
    vd0 = min(rdo + 0.9 * (vd), rdt + 0.9 * (vd), rdp + 0.9 * (vd), rdr + 0.9 * (vn))
    policy[0] = [rdo + 0.9 * (vd), rdt + 0.9 * (vd), rdp + 0.9 * (vd), rdr + 0.9 * (vn)]\
        .index(min([rdo + 0.9 * (vd), rdt + 0.9 * (vd), rdp + 0.9 * (vd), rdr + 0.9 * (vn)]))
    vn0=0
    vn0 = min(rno + 0.9 * (0.9 * vn + 0.1 * vd), rnt + 0.9 * (0.98 * vn + 0.02 * vd), rnp + 0.9 * (vn))
    policy[1] = [rno + 0.9 * (0.9 * vn + 0.1 * vd), rnt + 0.9 * (0.98 * vn + 0.02 * vd), rnp + 0.9 * (vn)]\
        .index(min([rno + 0.9 * (0.9 * vn + 0.1 * vd), rnt + 0.9 * (0.98 * vn + 0.02 * vd), rnp + 0.9 * (vn)]))
    vd=vd0
    vn=vn0
    
#Displaying the optimal costs and policy
print("Optimal cost of dented stage: ", vd)
print("Optimal cost of non-dented stage: ", vn)
print("Optimal parking policy: ", policy)
