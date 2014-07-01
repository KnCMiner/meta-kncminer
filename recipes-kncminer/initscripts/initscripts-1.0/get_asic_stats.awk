#!/usr/bin/awk -f
BEGIN {
  for (asic = 0; asic < 6; asic++) {
    asic_temp[asic] = "";
    asic_type[asic] = "OFF";
    asic_freq[asic, 0] = 0;
    asic_freq[asic, 1] = 0;
    asic_freq[asic, 2] = 0;
    asic_freq[asic, 3] = 0;
  }
  cur_asic=0;
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
      temp = (0.0+asic_temp[asic]);
    freq = ((0.0+asic_freq[asic, 0]+asic_freq[asic, 1]+asic_freq[asic, 2]+asic_freq[asic, 3])/4);
    if (freq <= 0)
      freq = "---";
    print num, temp, freq, asic_type[asic];
  }
}
