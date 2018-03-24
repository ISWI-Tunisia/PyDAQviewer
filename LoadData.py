# -*- coding: utf-8 -*-
'''
Author: Ahmed Ammar, ahmed.ammar@fst.utm.tn
Purpose: Load NarrowBand data
Inputs: - - -
Outputs:  - - -
Date Created: Sat Mar 10 19:10:30 2018
Date Modified: M D, Y
Date Released: M D, Y
Versions:
    V0.01: ---
'''
import scipy.io as mat
import numpy as np
import glob

import matplotlib.pyplot as plt
global DataLoaded
DataLoaded_list=[]
DataError_List=[]
def Load_DAQ_Data(path="",fname=""):
    """
    Load DAQ Data from raw files
    """
    
    FileList=glob.glob(path+fname)
    Data=[]
    StartTimes=[]    
    for filename in FileList:
        
        LoadData = mat.loadmat(filename, struct_as_record=False,
                                   squeeze_me=True)
        
        file=filename.split("\\")
        # Add loaded filenames into DataLoaded_list
        DataLoaded_list.append(file[-1])
        print("Data Loaded:", file[-1])
        
        data = LoadData['data']
        data_type= LoadData['is_amp']
        station_lat= LoadData['latitude']
        station_lon= LoadData['longitude']
        direction=LoadData['adc_channel_number']
        fs = LoadData['Fs']
        year = LoadData['start_year']
        month= LoadData['start_month']
        day = LoadData['start_day']
        hr = LoadData['start_hour']
        mn = LoadData['start_minute']
        sec= LoadData['start_second']
        StationInfo={'data_type':data_type, 'station_lat':station_lat,
                     'station_lon':station_lon, 'direction':direction, 'fs':fs}
        
        Tstart = [float(year),float(month),float(day),float(hr),float(mn),float(sec)] # vector of time.
    #    print("Tstart: ", Tstart)
        S= np.array([1, 1/60., 1/3600.]) * Tstart[3:6]
        startTime =S.sum(axis=0) # star time in hours
#        print("startTime", startTime)
        Data.append(data)
        StartTimes.append(startTime)
    try:
#      Data= np.concatenate(Data)  # all the input arrays must have same number of dimensions!
        Data= np.hstack(Data) # Stack all Data horizontally
    except ValueError:
            # if error in file name
            DataError_List.append("No filename like " +fname +" in this directory: " + path)
            print("No filename like " +fname +" in this directory: " + path)
    
    # Time axis
    time= []
    for i in range(0, len(Data)):
        
        t1= StartTimes[0] + (i/float(fs)/3600)
#        print (t1)
        time.append(t1)
    time=np.array(time)
    
    
    return time, Data, StationInfo

if __name__ == "__main__":
    
    # FOR TEST
    time, Data, StationInfo =Load_DAQ_Data("F:\\NarrowbandData\\Algeria\\2015\\03\\20\\", "*150320*NRK_000B.mat")
    #print(len(Data))
    #for large data
    plt.rcParams['agg.path.chunksize'] = 10000 
    # solution given by: Serenity, 
    #link: https://stackoverflow.com/questions/37470734/matplotlib-giving-error-overflowerror-in-draw-path-exceeded-cell-block-limit
    plt.plot(time, Data, lw=.5, color='r')
    plt.show()
    print("Done!")

