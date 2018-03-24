# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 22:47:40 2016

@author: ahmed
"""

import os
directory = os.chdir('data/')
import scipy.io as matlab
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

#Ampfilename= raw_input('Write de name of AWESOME narrow band data: ')
Ampfilename = 'TN160924000000ICV_000A.mat'
Phifilename = 'TN160924000000ICV_000B.mat'

if Ampfilename[-8:-5]=='000':
    CH='N/S'
else:
    CH='E/W'
station= Ampfilename[14:17]

mat_a = matlab.loadmat(Ampfilename, struct_as_record=False, squeeze_me=True)
mat_p = matlab.loadmat(Phifilename, struct_as_record=False, squeeze_me=True)
amp = mat_a['data']
phi =mat_p['data']
fsL = mat_a['Fs']
year = mat_a['start_year']

month= mat_a['start_month']
day = mat_a['start_day']
hr = mat_a['start_hour']
mn = mat_a['start_minute']
sec= mat_a['start_second']

Tstart = [float(year),float(month),float(day),float(hr),float(mn),float(sec)] # vector of time.
#print Tstart
S= np.array([1, 1/60., 1/3600.]) * Tstart[3:6]
startTime =S.sum(axis=0) # star time in hours
#print startTime


step =[]
tLo= []
for i in range(0, len(amp), 1):
    t = i
    step.append(t)
    t1= startTime + (step[i]/float(fsL)/3600.)
    #print (t1)
    tLo.append(t1)
    


#f = open("%s%s%s%s.txt"%(year,month,day,station), 'w')
#f.write("# time  Amplitude  Phase\n")
#for i in range(0,len(tLo)-1):
#    f.write(str(tLo[i]) + " " + str(amp[i]) + " " + str(phi[i]) + "\n")
#
#f.close()

fig=plt.figure(figsize=(8,5))
ax1=plt.subplot(2, 1, 1)
plt.grid()
plt.plot(tLo, 20*np.log10(amp), '-b')
ax1.set_ylabel('Amplitude [dB]', fontsize=12)
#ax1.set_xticks([])
#plt.xlabel('Time (UT)', fontsize=12)
ax1.set_title ('Tunisia %.0f-%.0f-%.0f %s   %s Antenna'%(float(year),float(month),float(day),station,CH),
           fontsize=14, weight='bold')


ax2=plt.subplot(2, 1, 2, sharex=ax1)
ax2.grid()
ax2.plot(tLo[:len(phi)], phi, '-b')
ax2.set_ylabel(r'Phase [$^\circ$]', fontsize=12)
ax2.set_xlabel('Time (UT)', fontsize=12)

plt.savefig("%s%s%s%s.png"%(year,month,day,station))
plt.savefig("%s%s%s%s.eps"%(year,month,day,station))

'''
## correction to the signal from NarrowQplot.m
fix_phasedata function are from:
http://stackoverflow.com/questions/34722985/matlab-fftfilt-equivalent-for-python
'''
##phase unwrapped
PhaseFixLength90 = 60
PhaseFixLength180 =60
averaging_length=fsL*PhaseFixLength180
def fix_phasedata180(phi, averaging_length):
    phi = np.reshape(phi,len(phi))
    x = np.exp(1j*phi*2./180.*np.pi)
    N = float(averaging_length)
    b, a = sg.butter(10, 1./np.sqrt(N))
    y = sg.filtfilt(b, a, x)
    output_phase = phi - np.array(list(map(round,((phi/180*np.pi-np.unwrap(np.angle(y))/2)%(2*np.pi))*180/np.pi/180)))*180
    temp = output_phase[0]%90
    output_phase = output_phase-output_phase[0]+temp
    s = output_phase[output_phase >= 180]
    for s in range(len(output_phase)):
        output_phase[s] = output_phase[s]-360
    return output_phase
    
data_phase_fixed180 = fix_phasedata180(phi, averaging_length)

def fix_phasedata90(phi, averaging_length):
    phi = np.reshape(phi,len(phi))
    x = np.exp(1j*phi*4./180.*np.pi)
    N = float(averaging_length)
    b, a = sg.butter(10, 1./np.sqrt(N))
    y = sg.filtfilt(b, a, x)
    output_phase = phi - np.array(list(map(round,((phi/180*np.pi-np.unwrap(np.angle(y))/4)%(2*np.pi))*180/np.pi/90)))*90
    temp = output_phase[0]%90
    output_phase = output_phase-output_phase[0]+temp
    output_phase = output_phase%360
    s = output_phase[output_phase >= 180]
    for s in range(len(output_phase)):
        output_phase[s] = output_phase[s]-360
    return output_phase


data_phase_fixed90 = fix_phasedata90(data_phase_fixed180, averaging_length)

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
AveragingLengthAmp = 10
AveragingLengthPhase = 10
data_amp_averaged = np.zeros((len(amp) - AveragingLengthAmp + 1,1),float)
data_phase_averaged = np.zeros((len(data_phase_unwrapped) - AveragingLengthPhase + 1,1),float)

for jj in range(0, (len(amp)-AveragingLengthAmp+1)):
    data_amp_averaged[jj] = np.mean(amp[jj:(jj+AveragingLengthAmp-1)])


for jj in range(0, (len(data_phase_unwrapped) - AveragingLengthPhase + 1)):
    data_phase_averaged[jj] = np.mean(data_phase_unwrapped[jj:(jj+AveragingLengthPhase-1)])

##Figure
    
fig=plt.figure(figsize=(8,5))
ax1=plt.subplot(2, 1, 1)
plt.grid()
plt.plot(tLo[:len(data_amp_averaged)], 20*np.log10(data_amp_averaged),'-k',linewidth=1.)
ax1.set_ylabel('Amplitude [dB]', fontsize=12)
#ax1.set_xticks([])
#plt.xlabel('Time (UT)', fontsize=12)
ax1.set_title ('Tunisia %.0f-%.0f-%.0f %s   %s Antenna'%(float(year),float(month),float(day),station,CH),
           fontsize=14, weight='bold')


ax2=plt.subplot(2, 1, 2, sharex=ax1)
ax2.grid()
ax2.plot(tLo[:len(data_phase_averaged)], data_phase_averaged, '-k',linewidth=1.)
ax2.set_ylabel(r'Phase [$^\circ$]', fontsize=12)
ax2.set_xlabel('Time (UT)', fontsize=12)


plt.savefig("%s%s%s%s_average.png"%(year,month,day,station))
plt.savefig("%s%s%s%s_average.eps"%(year,month,day,station))             
                


plt.show()
 


