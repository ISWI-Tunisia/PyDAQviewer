# -*- coding: utf-8 -*-
'''
Author: Ahmed Ammar, ahmed.ammar@fst.utm.tn
Purpose: - - - 
Inputs: - - -
Outputs:  - - -
Date Created: Sun Mar 11 22:50:48 2018
Date Modified: M D, Y
Date Released: M D, Y
Versions:
    V0.01: ---
    
'''
from LoadData import Load_DAQ_Data
from DAQ_DataPhase import FixDAQ_DataPhase
import numpy as np
import matplotlib.pyplot as plt

def Plot_Data(pathnames=[], filenames=[], TitlePlot=[]):
    """
    Plot Amplitude and Phase from AWESOME DATA
    """
    max_nsp=len(pathnames)
    
    nsp=0 # number of subplots
    fig=plt.figure(figsize=(7.5, 5+max_nsp/4))
    plt.gcf().canvas.set_window_title('PyDAQviewer: Plot Narrowband Data')
    for pathname, filename,title in zip(pathnames,filenames,TitlePlot):
        nsp+=1
        
        FixData=FixDAQ_DataPhase(pathname, filename)
        time, Data, StationInfo =Load_DAQ_Data(FixData.path, FixData.filename)
        
        fs=StationInfo['fs']
        
        if StationInfo['data_type']==1.0:
            Data_amp= Data
            ##Averaging
            AveragingLengthAmp = 10
            data_amp_averaged = np.zeros((len(Data_amp) - AveragingLengthAmp + 1,1),float)
            for jj in range(0, (len(Data_amp)-AveragingLengthAmp+1)):
                data_amp_averaged[jj] = np.mean(Data_amp[jj:(jj+AveragingLengthAmp-1)])
            ## Figure
            ax1= fig.add_subplot(max_nsp, 1, nsp)
            plt.plot(time[:len(data_amp_averaged)], 20*np.log10(data_amp_averaged), lw=1, color='r')
            plt.plot(time, 20*np.log10(Data_amp), ls='-', lw=.5, color='b', alpha=.5)
            plt.title(title, fontsize=10, weight = 'bold')
            plt.xlabel("Time (UT)", fontsize=8, weight = 'bold')
            plt.ylabel("Amplitude (dB)", fontsize=8, weight = 'bold')
            plt.xlim(0,24)
    
        else:
            Data_phi= Data
        
            ##phase unwrapped
            PhaseFixLength90 = 3000
            PhaseFixLength180 =3000
            averaging_length=fs*PhaseFixLength180
        #    print(averaging_length)
            data_phase_fixed180 = FixData.fix_phasedata180(Data_phi, averaging_length)
        #    print(data_phase_fixed180)
            data_phase_fixed90 = FixData.fix_phasedata90(data_phase_fixed180, averaging_length)
            data_phase_unwrapped = np.zeros((len(data_phase_fixed90),1),float)
            data_phase_unwrapped[0] = data_phase_fixed90[0]
            
            offset = 0
            for jj in range(1, (len(data_phase_fixed90))):
                if data_phase_fixed90[jj]-data_phase_fixed90[jj-1] > 180:
                    offset = offset + 360
                elif data_phase_fixed90[jj]-data_phase_fixed90[jj-1] < -180:
                    offset = offset - 360
                data_phase_unwrapped[jj] = data_phase_fixed90[jj] - offset
            
            ##Averaging
            AveragingLengthPhase = 10           
            data_phase_averaged = np.zeros((len(data_phase_unwrapped) - AveragingLengthPhase + 1,1),float)
            for jj in range(0, (len(data_phase_unwrapped) - AveragingLengthPhase + 1)):
                data_phase_averaged[jj] = np.mean(data_phase_unwrapped[jj:(jj+AveragingLengthPhase-1)])
            
            ## Figure
            ax2= fig.add_subplot(max_nsp, 1, nsp, sharex=ax1)
            plt.plot(time[:len(data_phase_averaged)], data_phase_averaged, lw=1, color='r')
            plt.plot(time, data_phase_unwrapped, lw=.5, color='b', alpha=.5)
            plt.title(title, fontsize=10, weight = 'bold')
            plt.xlabel("Time (UT)", fontsize=8, weight = 'bold')
            plt.ylabel("Phase (deg)", fontsize=8, weight = 'bold')
            plt.xlim(0,24)
            
    plt.tight_layout()       
    plt.show()
if __name__ == "__main__":
    Plot_Data(pathnames=["H:\\NarrowbandData\\Tunisia\\2017\\09\\06\\",
                         "H:\\NarrowbandData\\Tunisia\\2017\\09\\06\\" ],
              filenames=["*170906*NRK_001A.mat","*170906*NRK_001B.mat"],
                        TitlePlot=["1","2"])