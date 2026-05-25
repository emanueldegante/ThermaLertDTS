# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:37:21 2026

@author: ede7
"""


import pandas as pd
import os
import os.path
import datetime as dt
from IPython.display import clear_output


import numpy as np
#from datetime import datetime as dt
from datetime import timedelta




#now = dt.datetime.now()
#year_db = str(now.year)
#month_db = now.strftime("%b").lower()

#year_db=str(2026)
#month_db=str('feb')    


#==============================================================

  

def data_creation(year_db,month_db):

    hdf_root = "F:\\0_Mactaquac_Data_Bases\\FibreOptics_BoreHole\\" + year_db +"\\"+ month_db
        
    
    
    hdffilename='data_ch1_'+ year_db + '_' + month_db +'.h5'
    hdffile=hdf_root + "\\" + hdffilename
    
    hdf_fullpath = os.path.join(hdf_root, hdffilename)     
    #folder to search for DDF files.
    fileDir = hdf_root
    
    df=pd.DataFrame() #create blank data frame
    h=0
    for dirpath, dirnames, filenames in os.walk(fileDir):                     #directory crawler
        for filename in [f for f in filenames if f.endswith(".ddf")]:
            clear_output()
            print("\r"), filename,
            #read temperature and spatial values
            
            dts=pd.read_csv(str(dirpath + '\\' + filename), delimiter='\t', skiprows=26, usecols=[0,1], index_col=[0], header=None, encoding='latin1')
            
            #take datetime values from file
            date=pd.read_csv(str(dirpath + '\\' + filename), nrows=1, skiprows=8, encoding='latin1')
            X2=date.values.T
            date=str(X2)[9:19]
            
            time=pd.read_csv(str(dirpath + '\\' + filename), nrows=1, skiprows=9, encoding='latin1')
            X1=time.values.T
            time=str(X1)[9:17]
            
            tm=date + ' ' + time
            
            file_date=dt.datetime.strptime(tm, "%Y/%m/%d %H:%M:%S")
            datetime=pd.date_range(file_date,file_date)
            
            dts2 = pd.DataFrame(index=datetime, data=dts.values.T, columns=dts.index)
            
            df=pd.concat([df,dts2])
            
            h+=1
    
      
    print(df)
    store = pd.HDFStore(hdf_fullpath)
    store['sepi3_halodts']=df
    store.close()
    
    #==========================================================================================================
    #==========================================================================================================
    #============================================ Dayly Average
    #==========================================================================================================
    #==========================================================================================================
    
    
    year_db_1=int(year_db)
    year_db_2=year_db_1+1
    
    sd=dt.datetime(year_db_1,1,1)         # Start date of plot(type in the desired start date of plot as yyyy,m, dd)
    ed=dt.datetime(year_db_2,1,1)         # end date of plot (type in the desired end date of plot as yyyy,m,dd)
    
    
    directory = [hdf_root + "\\" + hdffilename ,"sepi3_halodts"]  
    
    
    
    #--------------------------Reading HDF5 File------------------------------------------------------------
    
    
    def readhdf(directory, sd, ed):
        raw_data = pd.read_hdf(directory[0],directory[1])   
        sort_data=raw_data.sort_index()
        tr_data=sort_data.truncate(sd,ed)                    
        
        return tr_data
    
    tr_data = readhdf(directory, sd, ed)  # truncated data
    
    
    #============================================= Calculating elevation 
    
    
    elevation = pd.read_csv('F:\\0_Mactaquac_Data_Bases\\elevation_list.csv').squeeze("columns")
    
    #--------------------------------------Averaging Functions----------------------------------------------------------
    
    def dailymean(tr_data):
        rs_data=tr_data.resample('1D', closed='left', label='left').mean()   #Resample data by daily mean
        table = rs_data.transpose()
        table.index=(621.8-np.array(table.index, dtype=float))/11.8          #slant height (m) above bottom of hole
        #            619.3
        return table
    
    ###------------------------------- Callig the function to plot ###
    
    resampled_data=dailymean(tr_data)
    
    
    date=resampled_data.columns
    
    
    
    #============================================================== Getting Temperatures to Measure
    temp_data=resampled_data.iloc[320:606]
    
    temp_data=np.array(temp_data)
    temp_data_t= np.transpose(temp_data)
    
    #=============================================================== Creating new data frame
    
    
    
    df_new_t = pd.DataFrame(temp_data_t, columns=[elevation], index=[date])
    
    
    csv_filename = 'DTS_BH_daily_ch1_' + year_db + '_' + month_db + '.csv'
    
    
    csv_fullpath = os.path.join(hdf_root, csv_filename)
    
    df_daily=df_new_t.to_csv(csv_fullpath)
    
    
    #==========================================================================================================
    #==========================================================================================================
    #============================================ Hourly Average
    #==========================================================================================================
    #==========================================================================================================
    
    
    #--------------------------------------Averaging Functions----------------------------------------------------------
    
    def hourlymean(tr_data):
        rs_data = tr_data.resample('H', closed='left', label='left').mean()     
        table = rs_data.transpose()
        table.index = (621.8-np.array(table.index, dtype=float))/11.8            
        
        return table
    
    
    
    resampled_data_h=hourlymean(tr_data)
    
    
    date_h=resampled_data_h.columns
    
    #============================================= Getting Temperature
    temp_data_h=resampled_data_h.iloc[320:606]
    
    temp_data_h=np.array(temp_data_h)
    temp_data_t_h= np.transpose(temp_data_h)
    
    
    
    
    #=============================================================== Creating new data frame
    
    df_new_t_h = pd.DataFrame(temp_data_t_h, columns=[elevation], index=[date_h])
    
    
    csv_filename_h = 'DTS_BH_hourly_ch1_' + year_db + '_' + month_db + '.csv'
    
    csv_fullpath_h = os.path.join(hdf_root, csv_filename_h)
    
    df_hourly=df_new_t_h.to_csv(csv_fullpath_h)
    
    
    #==========================================================================================================
    #==========================================================================================================
    #============================================ Real_Data
    #==========================================================================================================
    #==========================================================================================================
    
    
    #--------------------------------------Averaging Functions----------------------------------------------------------
    
    def real(tr_data):
        rs_data = tr_data                                                        # resample data by weekly mean
        table = rs_data.transpose()
        table.index = (621.8-np.array(table.index, dtype=float))/11.8            # slant height (m) above bottom of hole
        
        return table
    
    
    resampled_data_r=real(tr_data)
    
    
    date_r=resampled_data_r.columns
    
    #============================================= Getting Temperature
    temp_data_r=resampled_data_r.iloc[320:606]
    
    temp_data_r=np.array(temp_data_r)
    temp_data_t_r= np.transpose(temp_data_r)
    
    
    
    
    #=============================================================== Creating new data frame
    
    df_new_t_r = pd.DataFrame(temp_data_t_r, columns=[elevation], index=[date_r])
    
    
    csv_filename_r = 'DTS_BH_raw_ch1_' + year_db + '_' + month_db + '.csv'
    
    csv_fullpath_r = os.path.join(hdf_root, csv_filename_r)
    
    df_raw=df_new_t_r.to_csv(csv_fullpath_r)
    
    
    return df_daily, df_hourly, df_raw

#df_daily, df_hourly, df_raw = data_creation(year_db,month_db)