\ Model MDP
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  200 pi[0] + 500 pi[1] + 400 pi[2] + 700 pi[3] + 600 pi[4] + 900 pi[5]
Subject To
 c_1: 0.2 pi[0] + 0.1 pi[1] - 0.2 pi[3] - 0.05 pi[5] = 0
 c_2: - 0.4 pi[2] - 0.1 pi[3] + 0.2 pi[5] = 0
 c_3: pi[0] + pi[1] + pi[2] + pi[3] + pi[4] + pi[5] = 1
Bounds
End
