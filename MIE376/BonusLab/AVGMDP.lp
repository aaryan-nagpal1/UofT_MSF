\ Model AVGMDP
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  9 pi[0] + 13.5 pi[1] + 14 pi[2] + 50 pi[3] + 4.5 pi[5] + 5 pi[6]
Subject To
 c_1: - pi[3] + 0.1 pi[4] + 0.02 pi[5] = 0
 c_2: pi[0] + pi[1] + pi[2] + pi[3] + pi[4] + pi[5] + pi[6] = 1
Bounds
End
