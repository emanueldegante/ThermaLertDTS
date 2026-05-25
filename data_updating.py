# -*- coding: utf-8 -*-
"""
Created on Mon May 18 23:34:46 2026

@author: emanu
"""

import pandas as pd
import numpy as np
import os
import os.path
from datetime import datetime as dt
from datetime import timedelta




def data_updating(year_db, month_db):

    final_root = "F:\\0_Mactaquac_Data_Bases"

    df_final = pd.read_csv(final_root + '/DTS_daily_Total.csv')

    df_final.columns = [
        str(int(float(c))) if c.replace('.', '', 1).isdigit() and float(c) == int(float(c))
        else str(float(c)) if c.replace('.', '', 1).isdigit()
        else c
        for c in df_final.columns
    ]


    current_root = (
        "F:\\0_Mactaquac_Data_Bases\\FibreOptics_BoreHole\\"
        + year_db + "\\" + month_db
    )

    df_year = pd.read_csv(
        current_root +
        '/DTS_BH_daily_ch1_' + year_db + '_' + month_db + '.csv'
    )

    df_year.columns = [
        str(int(float(c))) if c.replace('.', '', 1).isdigit() and float(c) == int(float(c))
        else str(float(c)) if c.replace('.', '', 1).isdigit()
        else c
        for c in df_year.columns
    ]


    # Convert datetime columns
    df_final['Unnamed: 0'] = pd.to_datetime(df_final['Unnamed: 0'])
    df_final = df_final.set_index('Unnamed: 0')

    df_year['Unnamed: 0'] = pd.to_datetime(df_year['Unnamed: 0'])
    df_year = df_year.set_index('Unnamed: 0')


    # Remove only overlapping dates
    df_final = df_final[~df_final.index.isin(df_year.index)]

    # Append new data
    df_final = pd.concat([df_final, df_year])

    # Remove duplicates if any
    df_final = df_final[~df_final.index.duplicated(keep='last')]

    # Sort chronologically
    df_final = df_final.sort_index()


    # Save updated database
    df_final.to_csv(final_root + "/DTS_daily_Total.csv")

    return df_final