# -*- coding: utf-8 -*-
'''
Author: Ahmed Ammar, ahmed.ammar@fst.utm.tn
Purpose: - - - 
Inputs: - - -
Outputs:  - - -
Date Created: Thu Apr 12 20:12:48 2018
Date Modified: M D, Y
Date Released: M D, Y
Versions:
    V0.01: ---
    
'''
from PyQt5.QtCore import pyqtSlot, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
from Ui_PlotNarrowband import Ui_MainWindow
from LoadData import Load_DAQ_Data
from DAQ_DataPhase import FixDAQ_DataPhase
import numpy as np

class PlotNarrowband(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
#        self.pathnames=["H:\\NarrowbandData\\Tunisia\\2017\\09\\06\\",
#                         "H:\\NarrowbandData\\Tunisia\\2017\\09\\06\\" ]
#        self.filenames=["*170906*NRK_001A.mat","*170906*NRK_001B.mat"]
#        self.TitlePlot=["1","2"]
            
        self.time_interval()
#        self.Plot_Data(pathnames=self.pathnames,filenames=self.filenames, TitlePlot=self.TitlePlot)
        
    def Plot_Data(self, pathnames, filenames, TitlePlot): 
        """
        Plot Amplitude and Phase from AWESOME DATA
        """
        max_nsp=len(pathnames)
        
        nsp=0 # number of subplots
        plt=self.mplwidget.canvas
        plt.ax.clear()
        plt.ax.axis('off')
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
                ax1= plt.fig.add_subplot(max_nsp, 1, nsp)
                if self.view_raw.isChecked() and  self.view_average.isChecked() == True: 
                    ax1.plot(time[:len(data_amp_averaged)], 20*np.log10(data_amp_averaged), lw=1, color='r')
                    ax1.plot(time, 20*np.log10(Data_amp), ls='-', lw=.5, color='b', alpha=.5)                    
                elif self.view_raw.isChecked() == True and  self.view_average.isChecked() == False:
                    ax1.clear()
                    ax1.plot(time, 20*np.log10(Data_amp), ls='-', lw=.5, color='b', alpha=.5)
                elif self.view_raw.isChecked() == False and  self.view_average.isChecked() == True: 
                    ax1.clear()
                    ax1.plot(time[:len(data_amp_averaged)], 20*np.log10(data_amp_averaged), lw=1, color='r')
                else:
                    ax1.clear()
                    
                ax1.set_title(title, fontsize=10, weight = 'bold')
                ax1.set_xlabel("Time (UT)", fontsize=8, weight = 'bold')
                ax1.set_ylabel("Amplitude (dB)", fontsize=8, weight = 'bold')
                ax1.set_xlim(self.start, self.end)
        
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
                ax2= plt.fig.add_subplot(max_nsp, 1, nsp, sharex=ax1)
                if self.view_raw.isChecked() and  self.view_average.isChecked() == True: 
                    ax2.plot(time[:len(data_phase_averaged)], data_phase_averaged, lw=1, color='r')
                    ax2.plot(time, data_phase_unwrapped, lw=.5, color='b', alpha=.5)       
                elif self.view_raw.isChecked() == True and  self.view_average.isChecked() == False:
                    ax2.clear()
                    ax2.plot(time, data_phase_unwrapped, lw=.5, color='b', alpha=.5)
                elif self.view_raw.isChecked() == False and  self.view_average.isChecked() == True: 
                    ax2.clear()
                    ax2.plot(time[:len(data_phase_averaged)], data_phase_averaged, lw=1, color='r')
                else:
                    ax2.clear()
#                ax2.plot(time[:len(data_phase_averaged)], data_phase_averaged, lw=1, color='r')
#                ax2.plot(time, data_phase_unwrapped, lw=.5, color='b', alpha=.5)
                ax2.set_title(title, fontsize=10, weight = 'bold')
                ax2.set_xlabel("Time (UT)", fontsize=8, weight = 'bold')
                ax2.set_ylabel("Phase (deg)", fontsize=8, weight = 'bold')
                ax2.set_xlim(self.start,self.end)
                
#        plt.fig.tight_layout()     
        plt.draw()

       
    @pyqtSlot()
    def on_view_raw_clicked(self):
        
        self.Plot_Data(pathnames=self.pathnames, filenames=self.filenames, TitlePlot=self.TitlePlot)
        
    @pyqtSlot()
    def on_view_average_clicked(self):
        self.Plot_Data(pathnames=self.pathnames, filenames=self.filenames, TitlePlot=self.TitlePlot)
        
    @pyqtSlot()
    def on_replot_clicked(self):
        self.Plot_Data(pathnames=self.pathnames, filenames=self.filenames, TitlePlot=self.TitlePlot)
        
    def time_interval(self):
        ts = self.startTime.time().toString()
        (h, m, s) = ts.split(':')
        self.start = int(h) + int(m) / 60 + int(s)/3600
        
        te = self.endTime.time().toString()
        (h, m, s) = te.split(':')
        self.end = int(h) + int(m) / 60 + int(s)/3600
                      
    @pyqtSlot(QTime)
    def on_startTime_timeChanged(self, QTime):
        '''
        Start time
        '''
        self.time_interval()
        
    @pyqtSlot(QTime)
    def on_endTime_timeChanged(self, QTime):
        '''
         End Time
        '''
        self.time_interval()
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    MyApplication = PlotNarrowband()
    MyApplication.show()
    sys.exit(app.exec_())
