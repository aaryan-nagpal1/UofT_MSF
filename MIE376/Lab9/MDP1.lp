\ Model MDP1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  500000 pi[0] + 500000 pi[1] + 1e+06 pi[2] + 2.5e+06 pi[3] + 2e+06 pi[4]
   + 3.5e+06 pi[5]
Subject To
 c_1: - 0.2 pi[0] - 0.2 pi[1] + 0.4 pi[2] + 0.8 pi[3] - 0.2 pi[5] = 0
 c_2: - 0.1 pi[0] - 0.1 pi[1] - 0.4 pi[2] - 0.1 pi[3] + 0.9 pi[5] = 0
 c_3: pi[0] + pi[1] + pi[2] + pi[3] + pi[4] + pi[5] = 1
Bounds
End
