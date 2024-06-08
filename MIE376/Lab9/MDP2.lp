\ Model MDP2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  - pi[0] + 15 pi[1] - pi[2] + 25 pi[3] - pi[4] + 40 pi[5] - pi[6]
   + 44 pi[7]
Subject To
 c_1: - 0.2 pi[0] - 0.2 pi[1] + pi[2] + 0.8 pi[3] - 0.2 pi[5] - 0.2 pi[7]
   = 0
 c_2: - 0.9 pi[2] + 0.3 pi[4] + pi[5] = 0
 c_3: - 0.1 pi[2] - 0.3 pi[4] + pi[7] = 0
 c_4: pi[0] + pi[1] + pi[2] + pi[3] + pi[4] + pi[5] + pi[6] + pi[7] = 1
Bounds
End
