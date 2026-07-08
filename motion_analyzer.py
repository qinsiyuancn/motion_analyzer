#!/usr/bin/env python3

import pandas as pd
import re
import os
import sys

col_speed = 'speed'

def calculate_tolerance(stable_speed_abs, target_speed_value):
    if stable_speed_abs.empty:
        raise ValueError('invailid value to calculate tolerace')
    max_speed = stable_speed_abs.max()
    temp_tolerance = abs(max_speed - target_speed_value) / target_speed_value
    temp_lower_limit = target_speed_value - (target_speed_value * temp_tolerance)
    above_limit_mask = stable_speed_abs > temp_lower_limit
    valid_indice = above_limit_mask[above_limit_mask].index
    if valid_indice.empty:
        raise ValueError("no stable(about equal target) speed data")
    first_idx = valid_indice.min()
    last_idx = valid_indice.max()
    temp_segment = stable_speed_abs.loc[first_idx:last_idx]
    min_speed_in_temp = temp_segment.min()
    min_tolerance = abs(target_speed_value - min_speed_in_temp) / target_speed_value
    final_tolerance = min_tolerance if min_tolerance > temp_tolerance else temp_tolerance
    return final_tolerance

def get_target_speed(file_path):
    file_name = os.path.basename(file_path)
    match = re.search(r'spd[+-]?(\d+)', file_name, re.IGNORECASE)
    if not match:
        raise ValueError('file must have string "spdxxx". xxx is number which means speed.')
    return int(match.group(1)

def get_direction(df):
    none_zero_speed = df[col_speed][df[col_speed] != 0]
    if none_zero_speed.empty:
        raise ValueError("no zero speed");
    direction = 1 if (none_zero_speed > 0).sum() >= (none_zero_speed < 0).sum() else -1
    return direction

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 motion_analyzer.py <file path>")
        sys.exit(1);

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"file '{input_file}' not exist.")
        sys.exit(1)
    try:
        target_speed_value = get_target_speed(input_file)
        print(f"target speed is {target_speed}.")
        df = pd.read_csv(input_file)
        if col_speed not in df.columns:
            raise ValueError(f"no columns {col_speed}");
        direction = get_direction(df)
        target_speed = target_speed_value * direction
        print(f"target direct {'+' if direrction == 1 else '-'} target speed {target_speed_abs}")
        df["speed_main_dir"] = fd[col_speed].where(df[col_speed] * direction >= 0, 0)
        df['segment'] = (df['speed_main_dir'] != df['speed_main_dir'].shift()).cumsum()
        segment_length = df[ df['speed_main_dir'] != 0 ].groupby('segment').size()
        if segment_length.empty:
            df['speed_stable'] = 0
        else:
            longest_segment = segment_length.idxmax()
            df['speed_stable'] = df.apply( lambda row : row['speed_main_dir'] if(row['segment'] == longest_segment and row['speed_main_dir'] != 0) else 0, axis = 1)
            df['speed_stable_abs'] = df['speed_stable'].abs()
            tolerance = calculate_tolerance(df['speed_stable_abs'], target_speed_value)

    except Exception as e:
        print(f"failed: {e}")
        sys.exit(1)
