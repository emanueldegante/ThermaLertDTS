# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 22:34:50 2026

@author: emanu
"""

import pandas as pd
import numpy as np



#dataframe=pd.read_csv('"F:\\0_Mactaquac_Data_Bases\\DTS_daily_Total.csv')
#nodes_from_bottom=10
#win=10

def data_jitter_correction(dataframe, nodes_from_bottom, win):

    df=dataframe
    time=df.iloc[:,0]
    column=df.columns
    column=column[1:]
    
    data=df.iloc[:,1:]
    data=np.array(data)
    
    a=data.shape[1]
    deeper_nodes=data[:,a-nodes_from_bottom:]
    
    median_deeper_nodes=np.nanmedian(deeper_nodes, axis=1)
    
    s = pd.Series(median_deeper_nodes)
    rolling_medians = s.rolling(window=win).median().to_numpy()
    
    diff=rolling_medians-median_deeper_nodes
    diff=diff.reshape(len(diff),1)
    
    chatter = np.where(np.isnan(diff), data, diff + data)
    
    df_final=pd.DataFrame(data=chatter,index=time, columns=column)
    
    df_final.to_csv('F:\\0_Mactaquac_Data_Bases\\DTS_daily_Total_Jitter.csv')
    
    
    return df_final


#df_final=data_jitter_correction(dataframe, nodes_from_bottom, win)

