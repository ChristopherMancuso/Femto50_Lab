from __future__ import division
import glob, os
import numpy as np
import matplotlib.pyplot as plt 
import TimeArray, WavelengthArray
import SpectraPlot, LogPlots, AllTiming
import MonoExpFit, BiExpFit, TriExpFit

'''
This script takes a .asc file and plots of the spectra, log plot of curve and fits with residual (mono, bi, and tri). In this the spectra 
are now background subtracted and you can look at all the timing plots and control which data to remove and where the background subtraction
is done.

Things to consider when using this file
1. The data file needs to be in the data folder
2. A results folder need to be created so the data can be saved in that folder
3. This assumes 16 PMTs are used
4. The fits don't seem overly dependent on the intial guesses used 
5. The fits do not account for the IRF
'''

#########################################################################################################################################################


## inputs ##
GratPos = 2.8 # Set Grating Position
label = 'FAD' # Define Region
PMTarray = np.array([(3,5),(6,8),(10,12)])  
ADCres = 256

# these paramters chose how many data points to remove before analyzing the data
bchop = 12 # the number of points of the beginning of the data
echop = 235 # the number of points of the end of the data

# these paramters select which data points are used from doing the background subtraction
StartZero = 0
StopZero = 20

## toggle functions on and off
ShowPlots    = False # if True the plots will be displayed as separate windows (if generating many plots consider turning to False)
PlotTiming   = True
PlotSpectra  = True
TryMonoFit   = True
TryBiFit     = True
TryTriFit    = True
PlotLog      = True


############################################################################################################################################################
print('This program has started')

# don not change below here

NumPMTs = 16

## Load Data Set ##
data = np.genfromtxt(glob.glob('data/*.asc')[0],skip_header=10,skip_footer=1)
data= np.reshape(data,(NumPMTs,ADCres))

# start making calculations
TimeArray = TimeArray.TimeArray(ADCres)
WavelengthArray = WavelengthArray.WavelengthArray(GratPos)

#chop of the weird stuff at the end
TimeArray = TimeArray[bchop:echop]
data = data[:,bchop:echop]

if PlotTiming == True:
    print('Making AllTiming Plot')
    AllTiming.AllTiming(data,TimeArray,StartZero,StopZero,label)
if PlotSpectra == True:
    print('Making Spectrum Plot')
    SpectraPlot.SpectraPlot(data,WavelengthArray,StartZero,StopZero,label)
if TryMonoFit == True:
    print('Doing Mono-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        MonoExpFit.MonoExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,StartZero,StopZero,label)
if TryBiFit == True:
    print('Doing Bi-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        BiExpFit.BiExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,StartZero,StopZero,label)
if TryTriFit == True:
    print('Doing Tri-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        TriExpFit.TriExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,StartZero,StopZero,label)
if PlotLog == True:
    print('Making Log Plots')
    for idx in range(0,np.shape(PMTarray)[0]):
        LogPlots.LogPlots(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)

if ShowPlots == True:
    plt.show()
print('The files have been saved')