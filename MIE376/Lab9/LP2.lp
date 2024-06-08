\ Model LP2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  v[0] + v[1] + v[2] + v[3]
Subject To
 c_1: 0.28 v[0] - 0.18 v[1] >= -1
 c_2: 0.28 v[0] - 0.18 v[1] >= 15
 c_3: v[1] - 0.81 v[2] - 0.09 v[3] >= -1
 c_4: - 0.72 v[0] + 0.82 v[1] >= 25
 c_5: 0.37 v[2] - 0.27 v[3] >= -1
 c_6: - 0.72 v[0] - 0.18 v[1] + v[2] >= 40
 c_7: 0.1 v[3] >= -1
 c_8: - 0.72 v[0] - 0.18 v[1] + v[3] >= 44
Bounds
End
