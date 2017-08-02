from __future__ import division
import glob, os
import numpy as np
import matplotlib.pyplot as plt 
import TimeArray, WavelengthArray, SpectraPlot, LogPlots
import MonoExpFit, BiExpFit, TriExpFit

############################################################################################################################################################

'''
This script takes a .asc file and plots of the spectra, log plot of curve and fits with residual (mono, bi, and tri).

Things to consider when using this file

1. The data file needs to be in the data folder
2. A results folder need to be created so the data can be saved in that folder
3. This assumes 16 PMTs are used
4. This program assumes the first 20 data points are good enough to zero the baseline 
5. The fits don't seem overly dependent on the intial guesses used 
6. The spectra have no background subtraction
7. The fits do not account for the IRF

'''

############################################################################################################################################################

# inputs

GratPos = 2.8 # Set Grating Position
label = 'Sample Name' # Define Region
PMTarray = np.array([(3,5),(9,12),(13,15)])  
ADCres = 256

## toggle functions on and off
ShowPlots   = False # if True the plots will be displayed as separate windows (if generating many plots consider turning to False)
PlotSpectra = True
TryMonoFit  = True
TryBiFit    = True
TryTriFit   = True
PlotLog     = True



############################################################################################################################################################

# stuff not needed to be changed
NumPMTs = 16

## Load Data Set ##
data = np.genfromtxt(glob.glob('data/*.asc')[0],skip_header=10,skip_footer=1)
data= np.reshape(data,(NumPMTs,ADCres))



# start making calculations
TimeArray = TimeArray.TimeArray(ADCres)
WavelengthArray = WavelengthArray.WavelengthArray(GratPos)
if PlotSpectra == True:
    print('Making Spectrum Plot')
    SpectraPlot.SpectraPlot(data,WavelengthArray,label)
if TryMonoFit == True:
    print('Doing Mono-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        MonoExpFit.MonoExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)
if TryBiFit == True:
    print('Doing Bi-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        BiExpFit.BiExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)
if TryTriFit == True:
    print('Doing Tri-Fits')
    for idx in range(0,np.shape(PMTarray)[0]):
        TriExpFit.TriExpFit(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)
if PlotLog == True:
    print('Making Log Plots')
    for idx in range(0,np.shape(PMTarray)[0]):
        LogPlots.LogPlots(data,PMTarray[idx][0],PMTarray[idx][1],TimeArray,label)

if ShowPlots == True:
    plt.show()
