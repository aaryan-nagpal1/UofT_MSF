\ Model Gasoline Blend Optimizer
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  19.8 cat_cracked_barrels_for_lolead + 19.8 isopentane_barrels_for_lolead
   + 19.8 straight_gas_barrels_for_lolead
   + 22 cat_cracked_barrels_for_premium + 22 isopentane_barrels_for_premium
   + 22 straight_gas_barrels_for_premium + 19 cat_cracked_barrels_unused
   + 19 isopentane_barrels_unused + 19 straight_gas_barrels_unused
Subject To
 vapour_pressure_lolead: cat_cracked_barrels_for_lolead
   + 13 isopentane_barrels_for_lolead - 3 straight_gas_barrels_for_lolead
   <= 0
 vapour_pressure_premium: 2 cat_cracked_barrels_for_premium
   + 14 isopentane_barrels_for_premium - 2 straight_gas_barrels_for_premium
   <= 0
 octane_lolead: 3 cat_cracked_barrels_for_lolead
   + 29 isopentane_barrels_for_lolead - 6 straight_gas_barrels_for_lolead
   >= 0
 octane_premium: - 17 cat_cracked_barrels_for_premium
   + 9 isopentane_barrels_for_premium - 26 straight_gas_barrels_for_premium
   >= 0
 cat_cracked_limit: cat_cracked_barrels_for_lolead
   + cat_cracked_barrels_for_premium <= 2700
 isopentane_limit: isopentane_barrels_for_lolead
   + isopentane_barrels_for_premium <= 1350
 straight_gas_limit: straight_gas_barrels_for_lolead
   + straight_gas_barrels_for_premium <= 4100
 unused_cat_cracked: cat_cracked_barrels_for_lolead
   + cat_cracked_barrels_for_premium + cat_cracked_barrels_unused = 2700
 unused_isopentane: isopentane_barrels_for_lolead
   + isopentane_barrels_for_premium + isopentane_barrels_unused = 1350
 unused_straight_gas: straight_gas_barrels_for_lolead
   + straight_gas_barrels_for_premium + straight_gas_barrels_unused = 4100
Bounds
End
