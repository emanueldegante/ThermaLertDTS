# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 18:17:39 2026

@author: emanu
"""


import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
#import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date, timedelta
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from scipy.signal import butter, filtfilt
from scipy.stats import linregress
import requests
from io import BytesIO
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from dash import Dash, dcc, html, Output, Input, State

#============================Day Calculator

def df_time_calc_tempdiff(year,month,day,day_diff, df: pd.DataFrame):

    d_1=dt(year, month, day).strftime("%Y-%m-%d")
    d_1_t=dt.strptime(d_1, "%Y-%m-%d")
    
    
    d_7 = d_1_t - timedelta(days=day_diff)
    d_7_s=d_7.strftime("%Y-%m-%d")
    
    
    
    #===========================================================historical p
    
    #============================================Prepare data set for functions
    #============================================
    #============================================
    
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    df.set_index(df.columns[0], inplace=True)
    
    r = df.iloc[:, :].columns.astype(float).to_numpy()
    
    df.index = pd.to_datetime(df.index)

    return df, r, d_1, d_7, d_1_t, d_7_s

#========================================Functions to extract Temperature values


def extract_date_across_years_tempdiff(df, month, day):
    mask = (df.index.month == month) & (df.index.day == day)
    return df.loc[mask]



def eday_minus_week_tempdiff(df, d_7):
    month_7 = d_7.month
    day_7   = d_7.day
    mask = (df.index.month == month_7) & (df.index.day == day_7)
    return df.loc[mask]

#========================================Remove specific year functions
#========================================Remove specific year functions
#========================================Remove specific year functions
#========================================Remove specific year functions
def remove_years_tempdiff(df, years_to_remove):

    df2 = df.copy()
    df2.index = pd.to_datetime(df2.index)

    if isinstance(years_to_remove, int):
        years_to_remove = [years_to_remove]

    return df2[~df2.index.year.isin(years_to_remove)]


#===========================================Difference computations
#===========================================Difference computations
#===========================================Difference computations
#===========================================Difference computations




#============================= Statistics Computation
#============================= Statistics Computation
#============================= Statistics Computation
#============================= Statistics Computation
#============================= Statistics Computation

def stats_min_max_std_tempdiff(df):
    lenght_df=df.shape[1]

    #min calculation
    min_val_df=[]
    for i in range(lenght_df):
        min_val=min(df.iloc[:,i])
        min_val_df.append(min_val)
    min_val_df=pd.DataFrame(min_val_df)
    
    #Max Calculation
    max_val_df=[]
    for i in range(lenght_df):
        max_val=max(df.iloc[:,i])
        max_val_df.append(max_val)
    max_val_df=pd.DataFrame(max_val_df)
    
    #mean Calculation
    mean_val_df=[]
    for i in range(lenght_df):
        mean_val=np.nanmean(df.iloc[:,i])
        mean_val_df.append(mean_val)
    mean_val_df=pd.DataFrame(mean_val_df)
    
    #Std Calculation
    std_val_df=[]
    for i in range(lenght_df):
        std_val=np.nanstd(df.iloc[:,i])
        std_val_df.append(std_val)
    std_val_df=pd.DataFrame(std_val_df)
    
    per_5_df=[]
    for i in range(lenght_df):
        per_5=np.nanpercentile((df.iloc[:,i]),5)
        per_5_df.append(per_5)
    per_5_df=pd.DataFrame(per_5_df)
    
    per_10_df=[]
    for i in range(lenght_df):
        per_10=np.nanpercentile((df.iloc[:,i]),10)
        per_10_df.append(per_10)
    per_10_df=pd.DataFrame(per_10_df)
    
    per_50_df=[]
    for i in range(lenght_df):
        per_50=np.nanpercentile((df.iloc[:,i]),50)
        per_50_df.append(per_50)
    per_50_df=pd.DataFrame(per_50_df)
    
    per_90_df=[]
    for i in range(lenght_df):
        per_90=np.nanpercentile((df.iloc[:,i]),90)
        per_90_df.append(per_90)
    per_90_df=pd.DataFrame(per_90_df)
    
    per_95_df=[]
    for i in range(lenght_df):
        per_95=np.nanpercentile((df.iloc[:,i]),95)
        per_95_df.append(per_95)
    per_95_df=pd.DataFrame(per_95_df)
    
    per_99_df=[]
    for i in range(lenght_df):
        per_99=np.nanpercentile((df.iloc[:,i]),99)
        per_99_df.append(per_99)
    per_99_df=pd.DataFrame(per_99_df)
    
    r_2_df=[]
    slope_df=[]
    intercept_df=[]
    for i in range(lenght_df):
        # Create x as the index
        val=(df.iloc[:,i])
        x = np.arange(len(val))
        # Remove NaN values
        mask = ~np.isnan(val)
        x_clean = x   [mask]
        y_clean = val [mask]
        res = linregress(x_clean, y_clean)
        r_2_df.append(res.rvalue**2)
        slope_df.append(res.slope)
        intercept_df.append(res.intercept)
    r_2_df=pd.DataFrame(r_2_df)
    slope_df=pd.DataFrame(slope_df)
    intercept_df=pd.DataFrame(intercept_df)
    #=====================================Data Frame Creation   INI
    
    min_val_t=min_val_df.transpose()
    max_val_t=max_val_df.transpose()
    mean_val_t=mean_val_df.transpose()
    std_val_t=std_val_df.transpose()
    per_5_df=per_5_df.transpose()
    per_10_df=per_10_df.transpose()
    per_50_df=per_50_df.transpose()
    per_90_df=per_90_df.transpose()
    per_95_df=per_95_df.transpose()
    per_99_df=per_99_df.transpose()
    r_2_df=r_2_df.transpose()
    slope_df=slope_df.transpose()
    intercept_df=intercept_df.transpose()
    
    df_1 = pd.concat([min_val_t, max_val_t])
    df_2 = pd.concat([mean_val_t, std_val_t])
    df_3 = pd.concat([df_1, df_2])
    df_4=  pd.concat([per_5_df,per_10_df,per_50_df,per_90_df, per_95_df,per_99_df,r_2_df,slope_df,intercept_df ])
    df_5= pd.concat([df_3,df_4])
    #==================================Data Frame Creaetion  - Close
    
    values=['Min', 'Max', 'Mean', 'STD', 'P_5', 'P_10', 'P_50', 'P_90', 'P_95', 'P_99', 'R2','Slope','Intercept']
    
    elevation=df.columns[:]
    
    
    df_final=pd.DataFrame(data=df_5)
    df_final.index=values
    df_final.columns=elevation
    
    df_final_t=df_final.transpose()
    
    Mean=df_final_t['Mean'].reset_index(drop=True)
    Min= df_final_t['Min'].reset_index(drop=True)
    Max= df_final_t['Max'].reset_index(drop=True)
    STD= df_final_t['STD'].reset_index(drop=True)
    
    
    return df_final_t, Mean, STD


#=============================Stats for same day, 
#=============================Difference 1 day and difference one week


def stats_min_max_std_dates_tempdiff(df):
    # Number of columns (elevations)
    length_df = df.shape[1]

    # Prepare lists
    min_val_list = []
    max_val_list = []
    mean_val_list = []
    std_val_list = []
    min_year_list = []
    max_year_list = []

    # Loop through each elevation column
    for i in range(length_df):
        col = df.iloc[:, i]

        # MIN
        min_val = col.min()
        min_val_list.append(min_val)
        # Get the year where MIN occurs
        min_year = col.idxmin().year
        min_year_list.append(min_year)

        # MAX
        max_val = col.max()
        max_val_list.append(max_val)
        # Get the year where MAX occurs
        max_year = col.idxmax().year
        max_year_list.append(max_year)

        # MEAN
        mean_val = np.nanmean(col)
        mean_val_list.append(mean_val)

        # STD
        std_val = np.nanstd(col)
        std_val_list.append(std_val)

    # Create dataframe
    df_final = pd.DataFrame({
        "Min": min_val_list,
        "Min_Year": min_year_list,
        "Max": max_val_list,
        "Max_Year": max_year_list,
        "Mean": mean_val_list,
        "STD": std_val_list
    }, index=df.columns)

    # Transpose so rows become Min/Max/…
    df_final_t = df_final.transpose()

    Mean = df_final["Mean"].reset_index(drop=True)
    Min = df_final["Min"].reset_index(drop=True)
    Min_Year = df_final["Min_Year"].reset_index(drop=True)
    Max = df_final["Max"].reset_index(drop=True)
    Max_Year = df_final["Max_Year"].reset_index(drop=True)
    STD = df_final["STD"].reset_index(drop=True)
 
    
    return Min, Min_Year, Max, Max_Year, Mean

#===========================================================plotting
#===========================================================same day
#===========================================================difference



def alarm_plot_min_max_tempdiff(r,temp_day,d_1, Min_D, Min_Year, Max_D, Max_Year, Mean, j_n, day_diff, d_7_s, separate_figures):
    
    r = r[j_n:]
    temp_day = temp_day[j_n:].ravel()
    Min_D = Min_D[j_n:]
    Min_Year = Min_Year[j_n:]
    Max_D = Max_D[j_n:]
    Max_Year = Max_Year[j_n:]
    Mean = Mean[j_n:]
    
    threshold_pos = np.array(Max_D)
    treshold_neg = np.array(Min_D)
    
    temp_day_r =  np.round(temp_day, 3)
    temp_day=temp_day_r
    # ------------------- Identify anomalies -------------------
    data = []
    
    for i, value in enumerate(temp_day):
    
        if value >= threshold_pos[i]:
            diff = value - threshold_pos[i]
    
        elif value <= treshold_neg[i]:
            diff = value - treshold_neg[i]
        else:
            continue
        data.append([
            float(r[i]),
            float(value),
            float(diff),
            Max_Year.iloc[i]
        ]) 
    df_alarm_analysis = pd.DataFrame(
        data,
        columns=["Elev (m)", "Temp", "ΔT (⁰C)", "Year"]
    )
    
    df_alarm=df_alarm_analysis[["Elev (m)", "ΔT (⁰C)", "Year"]]
    df_alarm["ΔT (⁰C)"] = np.round(df_alarm["ΔT (⁰C)"], 4)
    df_alarm["Year"] = df_alarm["Year"] % 100
    
    anomaly = 'Y' if not df_alarm.empty else 'N'
    
    alarm_text = "Historical Norms Exceeded" if not df_alarm.empty else "Within Historical Norms"
    dot_color = 'red' if not df_alarm.empty else 'green'
    
    # ------------------- Build horizontal multi-column text with dynamic widths -------------------
    n_cols=0
    
    if not df_alarm.empty:
        rows = df_alarm.shape[0]
        rows_per_col = 40
        n_cols = (rows + rows_per_col - 1) // rows_per_col
    
        col_blocks = []
        col_widths = []
    
        for c in range(n_cols):
            start = c * rows_per_col
            end = min((c + 1) * rows_per_col, rows)
            block = df_alarm.iloc[start:end]
            block_text = block.to_string(index=False).split("\n")
            col_blocks.append(block_text)
    
            # Determine max width in this block for proper padding
            max_width = max(len(line) for line in block_text)
            col_widths.append(max_width)
    
        # Normalize height (pad shorter columns with empty strings)
        max_height = max(len(col) for col in col_blocks)
        for col in col_blocks:
            if len(col) < max_height:
                col += [""] * (max_height - len(col))
    
        # Build rows by concatenating column strings horizontally with dynamic spacing
        df_text = ""
        for row_i in range(max_height):
            row_parts = []
            for col_idx, col in enumerate(col_blocks):
                row_parts.append(col[row_i].ljust(col_widths[col_idx] + 2))  # 2 spaces between columns
            df_text += "".join(row_parts) + "\n"
    else:
        df_text = ""
    
    print(df_alarm)
    print(alarm_text)
    
    # ------------------- Combined Figure -------------------
    
    separate_figures = separate_figures
    
    # ============================================
    # Dynamic alarm width
    # ============================================
    
    # Example:
    # number of alarm columns
    n_alarm_cols = n_cols
    
    # Main plot fixed width
    main_width = 10
    
    # Dynamic alarm width
    alarm_width = max(4, n_alarm_cols * 2.5)
    
    # ============================================
    # Create figures
    # ============================================
    
    if separate_figures:
    
        fig1, ax1 = plt.subplots(
            figsize=(main_width, 10),
            dpi=160
        )
    
        fig_alarm, ax_alarm = plt.subplots(figsize=(alarm_width, 10),dpi=160
        )
    
    else:
    
        total_width = main_width + alarm_width
    
        fig, (ax1, ax_alarm) = plt.subplots(1,2,figsize=(total_width, 10),dpi=260,
            gridspec_kw={'width_ratios': [main_width, alarm_width]
            }
        )
    
    day_diff_str=str(day_diff)
    #fig, (ax1, ax_alarm) = plt.subplots(1, 2, figsize=(12, 10), dpi=160, gridspec_kw={'width_ratios': [3, 1]})
    # ------------------- Combined Figure -------------------
    # ------------------- MAIN PLOT -------------------
    y_slan_min = (50.0684 - (1.19585 * r[-1]))
    y_slan_max = (50.0684 - (1.19585 * r[0]))
    
    ax2 = ax1.twinx()
    ax1.set_ylabel('Elevation (m)', fontsize=18)
    ax2.set_ylim(y_slan_min, y_slan_max)
    ax1.set_ylim(2, r[j_n])
    ax1.set_xlim(-.20, .40)
    ax1.yaxis.set_tick_params(labelsize=18)
    ax2.yaxis.set_tick_params(labelsize=.1)
    ax1.xaxis.set_tick_params(labelsize=15)
    ax1.grid(True, linestyle=':', linewidth=0.6, color='grey')
    
    ax1.plot(temp_day, r, label='Temperature Change '+ day_diff_str, color='blue', linewidth=4)
    ax1.plot(threshold_pos, r, '--', label='Historical Max', color='brown', linewidth=2)
    ax1.plot(treshold_neg, r, '--', label='Historical Min', color='red', linewidth=2)
    ax1.plot(Mean, r, '--',label='Mean Temperature Change ', color='green', linewidth=2)
    
    ax1.fill_betweenx(r, threshold_pos, temp_day,where=temp_day > threshold_pos, color='#c0392b', alpha=0.15, zorder=0 )
    ax1.fill_betweenx(r, treshold_neg,temp_day ,where=temp_day < treshold_neg, color='#c0392b', alpha=0.15, zorder=0 )
    ax1.fill_betweenx(r, threshold_pos,Mean ,where=Mean < threshold_pos, color='#2ecc71', alpha=0.15, zorder=0 )
    ax1.fill_betweenx(r, treshold_neg ,Mean ,where=Mean > treshold_neg, color='#2ecc71', alpha=0.15, zorder=0 )
    
    ax1.set_title('Historical Max. and Min. \n Day 1: ' + d_1+ ' - Day '+day_diff_str +": "+ d_7_s , fontsize=20)
    ax1.set_xlabel('Temperature (°C)', fontsize=18)
    ax1.legend(loc='lower right', fontsize=14)
    
    # ------------------- ALARM PANEL -------------------
    ax_alarm.axis('off')
    ax_alarm.set_xlim(0, 1)
    ax_alarm.set_ylim(0, 1)
    
    ax_alarm.text(
        0.7, 0.96, alarm_text,
        fontsize=14,
        verticalalignment='top',
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
    )
    
    dot_y =  0.96
    ax_alarm.scatter(0.25, dot_y, s=1500, color=dot_color, zorder=5)
    
    if df_text:
        ax_alarm.text(
            0.02, dot_y - 0.09, df_text,
            fontsize=11,
            verticalalignment='top',
            horizontalalignment='left',
            family="monospace",
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
        )
    
    plt.tight_layout()
    
    # Save figure to memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    img_bytes = buf.read()

    # Optional for Dash/web display
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    plt.close(fig)

    return fig, img_bytes, img_base64, anomaly

