\ Model Car Production Optimizer 2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
 [ 6 sprint_cars * sprint_production_binary
   + 8 voyager_cars * voyager_production_binary
   + 10 titan_cars * titan_production_binary ] / 2 
Subject To
 steel_limit: 1.5 sprint_cars + 3 voyager_cars + 5 titan_cars <= 600
 labour_limit: 280 sprint_cars + 250 voyager_cars + 320 titan_cars
   <= 60000
 sprint_production_lower_limit: - sprint_cars + 70 sprint_production_binary
   <= 0
 sprint_production_upper_limit: sprint_cars
   - 1e+100 sprint_production_binary <= 0
 voyager_production_lower_limit: - voyager_cars
   + 70 voyager_production_binary <= 0
 voyager_production_upper_limit: voyager_cars
   - 1e+100 voyager_production_binary <= 0
 titan_production_lower_limit: - titan_cars + 70 titan_production_binary
   <= 0
 titan_production_upper_limit: titan_cars - 1e+100 titan_production_binary
   <= 0
Bounds
Binaries
 sprint_production_binary voyager_production_binary titan_production_binary
Generals
 sprint_cars voyager_cars titan_cars
End
