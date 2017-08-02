from __future__ import division
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit


def MonoExpFit(data,PMTstart,PMTstop,MonoTime,TimeArray,label):
    
    def ExpFun_mono(x):
        return np.exp(-(1/MonoTime)*x)
    
    ## define the data points used for zeroing the basline
    StartZero = 0
    StopZero = 20
    
    # sum over all pixels
    data = np.sum(np.sum(data,axis=1),axis=1)
    # select the wavelengths
    data = data[PMTstart:PMTstop+1,:]
    LTcurve = np.sum(data,axis=0)
    # zero the baseline off negative times 
    LTcurve_zeroed = np.mean(LTcurve[StartZero:StopZero])
    LTcurve = LTcurve - LTcurve_zeroed
    # find Total Yield of the curve (used in plot anotation later)
    TotalYield = np.sum(LTcurve)
    # normalize max value to one
    LTcurve = LTcurve / np.max(LTcurve)
    # shift some max is at zero
    MaxPix = np.argmax(LTcurve)
    TimeArray = TimeArray - TimeArray[MaxPix]
    # select the part to fit
    LTcurve_to_fit = LTcurve[MaxPix:]
    TimeArray_to_fit = TimeArray[MaxPix:]
    
    
            
    # find residuals
    residuals = LTcurve_to_fit - ExpFun_mono(TimeArray_to_fit)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((LTcurve_to_fit-np.mean(LTcurve_to_fit))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # make the fit figure
    fig1, ax1 = plt.subplots(1)
    ax1.plot(TimeArray,LTcurve,c='b',lw=1)
    ax1.plot(TimeArray_to_fit,LTcurve_to_fit,c='k',lw=3)
    ax1.plot(TimeArray_to_fit,ExpFun_mono(TimeArray_to_fit),c='y',lw=2,ls='dashed')
    ## annotate the title and axis ##
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Counts (normalized)')
    ax1.set_title('MonoFit_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop))
    # annotate the total yield of the lifetime curve
    ax1.annotate('Total Yield\n%.f'%TotalYield, xy=(0.7, 0.6), xycoords='axes fraction', color='k', fontsize=14,horizontalalignment='center')
    ## make annotations of fit values ##
    ax1.annotate('$t_1$ = %.3f'%MonoTime, xy=(0.45, 0.85), xycoords='axes fraction', color='k', fontsize=14)
    ax1.annotate('Fixed', xy=(0.7, 0.85), xycoords='axes fraction', color='k', fontsize=14)
    ax1.annotate('$R^2$ = %.3f'%r_squared, xy=(0.6, 0.75), xycoords='axes fraction', color='k', fontsize=14)
    
    
    ## make the residual figure
    fig2, ax2 = plt.subplots(1)
    ax2.scatter(TimeArray_to_fit,residuals,s=10,c='b')
    ax2.axhline(0,c='k',ls='dashed')
    ax2.set_xlabel('Time (ns)')
    ax2.set_xlabel('Residuals')
    ax2.set_title('MonoFit_Residual_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop))
    ax2.set_ylim(-0.15,0.15)
    
    ## save the figures ##
    fig1.savefig('results/MonoFit_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop),dpi=200)
    fig2.savefig('results/MonoFit_Residual_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop),dpi=200)
