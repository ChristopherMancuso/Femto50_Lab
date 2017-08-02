from __future__ import division
import glob, os
import numpy as np
import matplotlib.pyplot as plt 
import TimeArray, WavelengthArray, SpectraPlot, LogPlots
import MonoExpFit, BiExpFit, TriExpFit

############################################################################################################################################################

'''
This script takes a .npy of region and will generate plots of the spectra, log plot of curve and fits with residual (mono, bi, and tri), where the
user fixes the lifetimes.

Things to consider when using this file

1. This assumes the data is a 4D .npy file of the form (PMT, PixY, PixX, ADCres). This file needs to be in the data folder
2. A results folder need to be created so the data can be saved in that folder
3. This assumes that the whole image is to be used in the timing infomation 
4. This assumes 16 PMTs are used
5. This assumes a TAC gain of 4 and a Range of 50 ns on the TCSPC software
6. This program assumes the first 20 data points are good enough to zero the baseline 
7. The fits don't seem overly dependent on the intial guesses used 
8. The spectra have no background subtraction
9. The fits do not account for the IRF

'''

############################################################################################################################################################

# inputs

GratPos = 2.8 # Set Grating Position
label = 'NFL' # Define Region
PMTarray = np.array([(6,8),(10,12)]) 

MonoTime = 1.3 # in ns
 
BiShort = 0.39 # in ns
BiLong  = 2.24 # in ns

TriShort = 0.17 # in ns
TriMed   = 0.39 # in ns
TriLong  = 2.24 # in ns

## toggle functions on and off
ShowPlots   = False # if True the plots will be displayed as separate windows (if generating many plots consider turning to False)
PlotSpectra = True
TryMonoFit  = True
TryBiFit    = True
TryTriFit   = True
PlotLog     = True





############################################################################################################################################################

# stuff not needed to be changed

## Load Data Set ##
data = np.load(glob.glob('data/*.npy')[0])


## Get input from the data file ##
NumPMTs = np.shape(data)[0]
TotPixY = np.shape(data)[1]
TotPixX = np.shape(data)[2]
ADCres  = np.shape(data)[3]


# start making calculations
TimeArray = TimeArray.TimeArray(ADCres)
WavelengthArray = WavelengthArray.WavelengthArray(GratPos)
if PlotSpectra == True:
    print('Making Spectrum Plot')
    SpectraPlot.SpectraPlot(data,WavelengthArray,label)
if TryMonoFit == True:
    print('Doing Mono-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        MonoExpFit.MonoExpFit(data,PMTarray[idx][0],PMTarray[idx][1],MonoTime,TimeArray,label)
if TryBiFit == True:
    print('Doing Bi-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        BiExpFit.BiExpFit(data,PMTarray[idx][0],PMTarray[idx][1],BiShort,BiLong,TimeArray,label)
if TryTriFit == True:
    print('Doing Tri-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        TriExpFit.TriExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TriShort,TriMed,TriLong,TimeArray,label)
if PlotLog == True:
    print('Making Log Plots')
    for idx in range(0,np.shape(PMTarray)[0]):
        LogPlots.LogPlots(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)

if ShowPlots == True:
    plt.show()
