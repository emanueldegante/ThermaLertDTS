# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:35:50 2026

@author: emanu
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime as dt, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.signal import butter, filtfilt
from io import BytesIO



def process_dts_file_grad(df: pd.DataFrame, spacing: float = 0.146):
    df_ele = df.iloc[:, 1:]
    elevations = df_ele.columns.astype(float)
    ele = elevations[1:]
    time = df.iloc[:,0]
    time = pd.DataFrame(time)

    date_start = dt.strptime(str(df.iloc[0, 0]), "%Y-%m-%d")
    n_days = df.shape[0]

    gradients = []
    for i in range(n_days):
        current_date = (date_start + timedelta(days=i)).strftime("%Y-%m-%d")
        subset = df[df.iloc[:, 0] == current_date]
        if subset.empty:
            continue
        vals = subset.iloc[0, 1:].to_numpy(dtype=float)
        temp_grad = np.gradient(vals)[1:]
        gradients.append(temp_grad)

    grad_df = pd.DataFrame(gradients).T
    grad_df.index = elevations[1:]
    grad_df.columns = range(grad_df.shape[1])

    medians = grad_df.median(axis=1, skipna=True)
    grad_detrended = grad_df.sub(medians, axis=0)
    grad_detrended = grad_detrended.T.reset_index(drop=True)
    
    df_8 = pd.DataFrame(data=grad_detrended, columns=ele)
    df_final = pd.concat([time, df_8], axis=1)

    return df_final, medians


def df_time_calc_grad(year,month,day, df: pd.DataFrame):

    d_1=dt(year, month, day).strftime("%Y-%m-%d")
    d_1_t=dt.strptime(d_1, "%Y-%m-%d")
    
    temp_day = (
        df.loc[df["Unnamed: 0"] == d_1, df.columns[1:]]
          .reset_index(drop=True)
          .T
          .to_numpy()
    )
    
    
    #============================================Prepare data set for functions
    #============================================
    #============================================
    df.set_index(df.columns[0], inplace=True)
    r = df.iloc[:,:].columns.astype(float).to_numpy()
    
    df.index = pd.to_datetime(df.index)

    return r,df, temp_day, d_1



#========================================Functions to extract Temperature values


def extract_date_across_years_grad(df, month, day):
    mask = (df.index.month == month) & (df.index.day == day)
    return df.loc[mask]




#========================================Remove specific year functions
#========================================Remove specific year functions
#========================================Remove specific year functions
#========================================Remove specific year functions
def remove_years_grad(df, years_to_remove):

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



def stats_min_max_std_dates_grad(df):
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


#=============================Stats for same day, 
#=============================Difference 1 day and difference one week



def alarm_plot_min_max_grad(r,temp_day, d_1, Min_D, Min_Year, Max_D, Max_Year, Mean, j_n, separate_figures):
    
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
    
        val = np.asarray(value).item()   # convert to scalar
    
        if val >= threshold_pos[i]:
            diff = val - threshold_pos[i]
    
        elif val <= treshold_neg[i]:
            diff = val - treshold_neg[i]
    
        else:
            continue
    
        data.append([
            float(r[i]),
            float(val),
            float(diff),
            Max_Year.iloc[i]   # FIXED
        ])
    
    df_alarm_analysis = pd.DataFrame(
        data,
        columns=["Elev (m)", "∇T", "Δ-∇T(⁰C/m)", "Year"]
    )
    
    df_alarm = df_alarm_analysis[["Elev (m)", "Δ-∇T(⁰C/m)", "Year"]].copy()
    
    df_alarm["Δ-∇T(⁰C/m)"] = np.round(df_alarm["Δ-∇T(⁰C/m)"], 4)
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
    
        fig, (ax1, ax_alarm) = plt.subplots(1,2,figsize=(total_width, 10),dpi=160,
            gridspec_kw={'width_ratios': [main_width, alarm_width]
            }
        )
   
    #fig, (ax1, ax_alarm) = plt.subplots(1, 2, figsize=(12, 10), dpi=160, gridspec_kw={'width_ratios': [3, 1]})
    # ------------------- Combined Figure -------------------
    # ------------------- MAIN PLOT -------------------
    y_slan_min = (50.0684 - (1.19585 * r[-1]))
    y_slan_max = (50.0684 - (1.19585 * r[0]))
    
    ax2 = ax1.twinx()
    ax1.set_ylabel('Elevation (m)', fontsize=18)
    ax2.set_ylim(y_slan_min, y_slan_max)
    ax1.set_ylim(2, r[j_n])
    ax1.set_xlim(-0.2, .20)
    ax1.yaxis.set_tick_params(labelsize=18)
    ax2.yaxis.set_tick_params(labelsize=.1)
    ax1.xaxis.set_tick_params(labelsize=15)
    ax1.grid(True, linestyle=':', linewidth=0.6, color='grey')
    
    ax1.plot(temp_day, r, label='∇T', color='blue', linewidth=4)
    ax1.plot(threshold_pos, r, '--', label='∇T Historical Max', color='brown', linewidth=2)
    ax1.plot(treshold_neg, r, '--', label='∇T Historical Min', color='red', linewidth=2)
    ax1.plot(Mean, r, '--',label='Mean ∇T', color='green', linewidth=2)
    
    ax1.fill_betweenx(r, threshold_pos, temp_day,where=temp_day > threshold_pos, color='#c0392b', alpha=0.15, zorder=0 )
    ax1.fill_betweenx(r, treshold_neg,temp_day ,where=temp_day < treshold_neg, color='#c0392b', alpha=0.15, zorder=0 )    
    ax1.fill_betweenx(r, threshold_pos,Mean ,where=Mean < threshold_pos, color='#2ecc71', alpha=0.15, zorder=0 )
    ax1.fill_betweenx(r, treshold_neg ,Mean ,where=Mean > treshold_neg, color='#2ecc71', alpha=0.15, zorder=0 )
    
    ax1.set_title('Historical Max. and Min. ∇T\n Date: ' + d_1, fontsize=20)
    ax1.set_xlabel('Temperature Gradient (°C/m)', fontsize=18)
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

