#Initial guesses
vs = 0
vm = 0
vi = 0

#Scenario wise costs (m = mild, i = intermediate, s = severe, b = basic, a = advanced)
rmb = 200
rma = 500
rib = 400
ria = 700
rsb = 600
rsa = 900

#Optimal policy
policy = [0, 0, 0]

#Running 100 itetations of value iteration to find the optimal policy
for i in range(100):
    # Bellman equations as formulated
    vm0=0
    vm0 = min(rmb + 0.9 * (0.8 * vm + 0.2 * vi), rma + 0.9 * (0.9 * vm + 0.1 * vi))
    policy[0] = [rmb + 0.9 * (0.8 * vm + 0.2 * vi), rma + 0.9 * (0.9 * vm + 0.1 * vi)]\
        .index(min([rmb + 0.9 * (0.8 * vm + 0.2 * vi), rma + 0.9 * (0.9 * vm + 0.1 * vi)]))
    vi0=0
    vi0 = min(rib + 0.9 * (0.6 * vi + 0.4 * vs), ria + 0.9 * (0.7 * vi + 0.2 * vm + 0.1 * vs))
    policy[1] = [rib + 0.9 * (0.6 * vi + 0.4 * vs), ria + 0.9 * (0.7 * vi + 0.2 * vm + 0.1 * vs)]\
        .index(min([rib + 0.9 * (0.6 * vi + 0.4 * vs), ria + 0.9 * (0.7 * vi + 0.2 * vm + 0.1 * vs)]))
    vs0=0
    vs0 = min(rsb + 0.9 * vs, rsa + 0.9 * (0.8 * vs + 0.15 * vi + 0.05 * vm))
    policy[2] = [rsb + 0.9 * vs, rsa + 0.9 * (0.8 * vs + 0.15 * vi + 0.05 * vm)]\
        .index(min([rsb + 0.9 * vs, rsa + 0.9 * (0.8 * vs + 0.15 * vi + 0.05 * vm)]))
    vm=vm0
    vi=vi0
    vs=vs0
#Displaying the optimal costs and policy
print("Optimal cost of mild stage treatment: ", vm)
print("Optimal cost of intermediate stage treatment: ", vi)
print("Optimal cost of severe stage treatment: ", vs)
print("Optimal treatment policy: ", policy)

