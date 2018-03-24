# -*- coding: utf-8 -*-
'''
Author: Ahmed Ammar, ahmed.ammar@fst.utm.tn
Purpose: Fix AWESOME DATA Phase
Inputs: 
    Path to Data Phase Files : path
    Phase Files Names
    Phase Data: Loaded by LoadData module (see LoadData.py)
    
Outputs: Unwrapped AWESOME Phase
Date Created: Sun Mar 11 19:28:53 2018
Aknowlegment: Many thanks to nandhos on Stack Overflow.
Source: https://stackoverflow.com/questions/34722985/matlab-fftfilt-equivalent-for-python
'''
import scipy.signal as sg
import numpy as np

class FixDAQ_DataPhase():
    """
    Fix DAQ data
    """
    def __init__(self, path="", filename=""):
        self.path= path
        self.filename= filename

        
    def fix_phasedata180(self, Data, averaging_length):
        Data = np.reshape(Data,len(Data))
        x = np.exp(1j*Data*2./180.*np.pi)
        N = float(averaging_length)
        b, a = sg.butter(10, 1./np.sqrt(N))
        y = sg.filtfilt(b, a, x)
        output_phase = Data - np.array(list(map(round,((Data/180*np.pi-np.unwrap(np.angle(y))/2)%(2*np.pi))*180/np.pi/180)))*180
        temp = output_phase[0]%90
        output_phase = output_phase-output_phase[0]+temp
        s = output_phase[output_phase >= 180]
        for s in range(len(output_phase)):
            output_phase[s] = output_phase[s]-360
        return output_phase
    
    def fix_phasedata90(self, Data, averaging_length):
        Data = np.reshape(Data,len(Data))
        x = np.exp(1j*Data*4./180.*np.pi)
        N = float(averaging_length)
        b, a = sg.butter(10, 1./np.sqrt(N))
        y = sg.filtfilt(b, a, x)
        output_phase = Data - np.array(list(map(round,((Data/180*np.pi-np.unwrap(np.angle(y))/4)%(2*np.pi))*180/np.pi/90)))*90
        temp = output_phase[0]%90
        output_phase = output_phase-output_phase[0]+temp
        output_phase = output_phase%360
        s = output_phase[output_phase >= 180]
        for s in range(len(output_phase)):
            output_phase[s] = output_phase[s]-360
        return output_phase
 