#!/usr/bin/awk -f
BEGIN {
  for (asic = 0; asic < 6; asic++) {
    asic_temp[asic] = "";
    asic_type[asic] = "OFF";
    for (die = 0; die < 4; die++) {
        asic_freq[asic, die] = 0;
    }
    for (dcdc = 0; dcdc < 8; dcdc++)
      asic_dcdctemp[asic, dcdc] = "";
  }
  cur_asic = 0;
 }

/"asic_1"/ { cur_asic = 0 }
/"asic_2"/ { cur_asic = 1 }
/"asic_3"/ { cur_asic = 2 }
/"asic_4"/ { cur_asic = 3 }
/"asic_5"/ { cur_asic = 4 }
/"asic_6"/ { cur_asic = 5 }

/"die0_Freq"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_freq[cur_asic, 0] = $2 }
/"die1_Freq"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_freq[cur_asic, 1] = $2 }
/"die2_Freq"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_freq[cur_asic, 2] = $2 }
/"die3_Freq"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_freq[cur_asic, 3] = $2 }

/"dcdc0_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 0] = $2 }
/"dcdc1_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 1] = $2 }
/"dcdc2_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 2] = $2 }
/"dcdc3_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 3] = $2 }
/"dcdc4_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 4] = $2 }
/"dcdc5_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 5] = $2 }
/"dcdc6_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 6] = $2 }
/"dcdc7_Temp"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_dcdctemp[cur_asic, 7] = $2 }

/BOARD0=/ { gsub(/BOARD0=/, "", $1); asic_type[0] = $1 }
/BOARD1=/ { gsub(/BOARD1=/, "", $1); asic_type[1] = $1 }
/BOARD2=/ { gsub(/BOARD2=/, "", $1); asic_type[2] = $1 }
/BOARD3=/ { gsub(/BOARD3=/, "", $1); asic_type[3] = $1 }
/BOARD4=/ { gsub(/BOARD4=/, "", $1); asic_type[4] = $1 }
/BOARD5=/ { gsub(/BOARD5=/, "", $1); asic_type[5] = $1 }

/"temperature"/ { gsub(/"/, "", $2); gsub(/,/, "", $2); asic_temp[cur_asic] = $2 }

END {
  for (asic = 0; asic < 6; asic++) {
    num = asic + 1;
    temp = "---";
    if ("" != asic_temp[asic])
      temp = (0.0 + asic_temp[asic]);
    freq = 0.0;
    for (die = 0; die < 4; die++) {
      freq += asic_freq[asic, die];
    }
    freq /= 4.0;
    if (freq <= 0)
      freq = "---";
    dcdctemp = 0;
    dcdcnum = 0;
    for (dcdc = 0; dcdc < 8; dcdc++) {
      if ("" == asic_dcdctemp[asic, dcdc])
        continue;
      dcdctemp += asic_dcdctemp[asic, dcdc];
      dcdcnum++;
    }
    if (0 == dcdcnum)
      dcdctemp = "---";
    else
      dcdctemp = sprintf("%.1f", dcdctemp / dcdcnum);
    print num, temp, dcdctemp, freq, asic_type[asic];
  }
}
