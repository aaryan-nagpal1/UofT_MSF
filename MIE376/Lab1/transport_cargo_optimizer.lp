\ Model Transport Cargo Optimizer
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  4400 front_cargoA + 4480 front_cargoB + 6250 front_cargoC
   + 2600 front_cargoD + 4400 center_cargoA + 4480 center_cargoB
   + 6250 center_cargoC + 2600 center_cargoD + 4400 back_cargoA
   + 4480 back_cargoB + 6250 back_cargoC + 2600 back_cargoD
Subject To
 front_cargo: 20 front_cargoA + 16 front_cargoB + 25 front_cargoC
   + 13 front_cargoD <= 120
 center_cargo: 20 center_cargoA + 16 center_cargoB + 25 center_cargoC
   + 13 center_cargoD <= 180
 back_cargo: 20 back_cargoA + 16 back_cargoB + 25 back_cargoC
   + 13 back_cargoD <= 100
 front_space: 500 front_cargoA + 700 front_cargoB + 600 front_cargoC
   + 400 front_cargoD <= 7000
 center_space: 500 center_cargoA + 700 center_cargoB + 600 center_cargoC
   + 400 center_cargoD <= 9000
 back_space: 500 back_cargoA + 700 back_cargoB + 600 back_cargoC
   + 400 back_cargoD <= 5000
 front_center_weight_ratio: 0.1666666666666667 front_cargoA
   + 0.1333333333333333 front_cargoB + 0.2083333333333333 front_cargoC
   + 0.1083333333333333 front_cargoD - 0.1111111111111111 center_cargoA
   - 0.0888888888888889 center_cargoB - 0.1388888888888889 center_cargoC
   - 0.0722222222222222 center_cargoD = 0
 center_back_weight_ratio: 0.1111111111111111 center_cargoA
   + 0.0888888888888889 center_cargoB + 0.1388888888888889 center_cargoC
   + 0.0722222222222222 center_cargoD - 0.2 back_cargoA - 0.16 back_cargoB
   - 0.25 back_cargoC - 0.13 back_cargoD = 0
Bounds
End
