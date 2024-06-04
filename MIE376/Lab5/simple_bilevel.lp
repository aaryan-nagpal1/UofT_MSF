\ Model Simple Bi-level
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  x + 2 y
Subject To
 c_1: 2 x - 3 y >= -12
 c_2: x + y <= 14
 c_3: lambda1 + lambda2 = 1
 c_4: - 3 x + y + s1 = -3
 c_5: 3 x + y + s2 = 30
 c_6: [ s1 * lambda1 ] = 0
 c_7: [ s2 * lambda2 ] = 0
Bounds
End
