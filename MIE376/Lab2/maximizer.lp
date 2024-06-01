\ Model Maximizer
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3 x_1 + 2 x_2 - x_3 - 2 x_4 + x_5 + 2 x_6 - x_7 + 3 x_8 + 4 x_9 - 3 x_10
Subject To
 c_1: 2 x_1 + x_2 + 3 x_3 + x_4 + 2 x_5 + x_6 + 4 x_7 + x_8 - 2 x_9
   + 3 x_10 <= 80
 c_2: x_1 - 4 x_2 + x_3 + 2 x_4 + 3 x_5 + x_6 - x_7 + 4 x_8 + x_9 + 2 x_10
   <= 50
 c_3: 3 x_1 + 2 x_2 - 2 x_3 - x_4 + x_5 + 3 x_6 + 2 x_7 + x_8 + x_9 + x_10
   <= 40
 c_4: 2 x_1 + 3 x_2 + x_3 + x_4 + x_5 + x_6 + x_7 + x_8 + 3 x_9 + 2 x_10
   <= 90
 c_5: x_1 + x_2 + x_3 + x_4 + x_5 + x_6 + x_7 + x_8 + x_9 + x_10 <= 50
Bounds
End
