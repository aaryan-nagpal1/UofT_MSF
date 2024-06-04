\ Model Stochastic Maximizer
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3.6 p_vl + 2.4 p_vh + 3.5 p_ml + 3.5 p_mh + 2.4 p_cl + 5.6 p_ch - 2.5 f_v
   - 2.5 f_m - 3 f_c
Subject To
 scenario_1: p_vl + p_ml + p_ch <= 1800
 scenario_2: p_vl + p_mh + p_ch <= 1800
 scenario_3: p_vh + p_ml + p_ch <= 1800
 scenario_4: p_vh + p_mh + p_cl <= 1800
 scenario_5: p_vh + p_ml + p_cl <= 1800
 scenario_6: p_vl + p_mh + p_cl <= 1800
 scenario_7: p_vl + p_ml + p_cl <= 1800
 scenario_8: p_vh + p_mh + p_ch <= 1800
 v_low_flavour: - p_vl + f_v >= 0
 v_high_flavour: - p_vh + f_v >= 0
 m_low_flavour: - p_ml + f_m >= 0
 m_high_flavour: - p_mh + f_m >= 0
 c_low_flavour: - p_cl + f_c >= 0
 c_high_flavour: - p_ch + f_c >= 0
Bounds
 300 <= p_vl <= 500
 300 <= p_vh <= 900
 p_ml = 300
 300 <= p_mh <= 600
 300 <= p_cl <= 700
 300 <= p_ch <= 1100
 f_v >= 300
 f_m >= 300
 f_c >= 300
End
