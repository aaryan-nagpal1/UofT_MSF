\ Model Car Production Optimizer 3
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  - 180 sprint_production_case_binary - 240 voyager_production_case_binary
   - 240 titan_production_case_binary
   - 300 sprint_voyager_production_case_binary
   - 400 voyager_titan_production_case_binary
   - 420 sprint_titan_production_case_binary
   - 450 sprint_voyager_titan_production_case_binary + [
   6 sprint_cars * sprint_production_case_binary
   + 6 sprint_cars * sprint_voyager_production_case_binary
   + 6 sprint_cars * sprint_titan_production_case_binary
   + 6 sprint_cars * sprint_voyager_titan_production_case_binary
   + 8 voyager_cars * voyager_production_case_binary
   + 8 voyager_cars * sprint_voyager_production_case_binary
   + 8 voyager_cars * voyager_titan_production_case_binary
   + 8 voyager_cars * sprint_voyager_titan_production_case_binary
   + 10 titan_cars * titan_production_case_binary
   + 10 titan_cars * voyager_titan_production_case_binary
   + 10 titan_cars * sprint_titan_production_case_binary
   + 10 titan_cars * sprint_voyager_titan_production_case_binary ] / 2 
Subject To
 steel_limit: 1.5 sprint_cars + 3 voyager_cars + 5 titan_cars <= 600
 labour_limit: 280 sprint_cars + 250 voyager_cars + 320 titan_cars
   <= 60000
 case_pick: sprint_production_case_binary + voyager_production_case_binary
   + titan_production_case_binary + sprint_voyager_production_case_binary
   + voyager_titan_production_case_binary
   + sprint_titan_production_case_binary
   + sprint_voyager_titan_production_case_binary = 1
Bounds
Binaries
 sprint_production_case_binary voyager_production_case_binary
 titan_production_case_binary sprint_voyager_production_case_binary
 voyager_titan_production_case_binary sprint_titan_production_case_binary
 sprint_voyager_titan_production_case_binary
Generals
 sprint_cars voyager_cars titan_cars
End
