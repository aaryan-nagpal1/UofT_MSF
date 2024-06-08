\ Model LP1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  v[0] + v[1] + v[2]
Subject To
 c_1: 0.37 v[0] - 0.18 v[1] - 0.09 v[2] <= 500000
 c_2: 0.46 v[1] - 0.36 v[2] <= 1e+06
 c_3: - 0.63 v[0] + 0.82 v[1] - 0.09 v[2] <= 2.5e+06
 c_4: 0.1 v[2] <= 2e+06
 c_5: - 0.63 v[0] - 0.18 v[1] + 0.91 v[2] <= 3.5e+06
Bounds
End
