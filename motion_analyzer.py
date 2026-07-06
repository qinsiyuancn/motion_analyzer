#!/usr/bin/env python3
import pandas as pd
import re
import os
import sys

col_speed = 'speed'

def get_tolerance(df):
    pass

def get_target_speed(file_path):
    file_name = os.path.basename(file_path)
    match = re.search(r'spd([+-]?\d+)', file_name, re.IGNORECASE)
    if not match:
        raise ValueError('file must have string "spdxxx". xxx is number which means speed.')
    return abs(int(match.group(1)))

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
        target_speed = get_target_speed(input_file)
        print(f"target speed is {target_speed}.")
        df = pd.read_csv(input_file)
        if col_speed not in df.columns:
            raise ValueError(f"no columns {col_speed}");
        direction = get_direction(df)
        target_speed_abs = target_speed * direction
        print(f"target direct {'+' if direrction == 1 else '-'} target speed {target_speed_abs}")
        same_dir_mask = (df[col_speed] != 0) & (df[col_speed] * direction > 0) 
        same_dir_fd = df[same_dir_mask].copy()


    except Exception as e:
        print(f"failed: {e}")
        sys.exit(1)
