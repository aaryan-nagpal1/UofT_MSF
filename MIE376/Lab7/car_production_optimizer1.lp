\ Model Car Production Optimizer 1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3 sprint_cars + 4 voyager_cars + 5 titan_cars
Subject To
 steel_limit: 1.5 sprint_cars + 3 voyager_cars + 5 titan_cars <= 600
 labour_limit: 280 sprint_cars + 250 voyager_cars + 320 titan_cars
   <= 60000
Bounds
Generals
 sprint_cars voyager_cars titan_cars
End
