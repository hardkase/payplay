import pandas as pd 
import numpy as np 
import datetime as dt
import constants as con

def fix_columns(data):
    data.columns = con.COLUMN_NAMES
    return data

def insert_column(data, index_pos, col_name, value):
    data = data.insert(index_pos, col_name, value)
    return data

def to_lower(data):
    # there has to be an easier way to do this ...
    for i in range(len(data.index)):
        series = data.iloc[i]
        series.str.lower
        for j in range(len(series.index)):
            val = series[j]
            if isinstance(val, str):
                series[j] = val.lower()
        data.iloc[i] = series
        print("DEBUG: ", series)
    return data


