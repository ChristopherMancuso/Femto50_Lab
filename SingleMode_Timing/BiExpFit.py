from __future__ import division
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

def ExpFun_bi(x,a1,t1,t2):
    return a1*np.exp(-(1/t1)*x) + (1-a1)*np.exp(-(1/t2)*x)

def BiExpFit(data,PMTstart,PMTstop,TimeArray,label):
    
    ## define the data points used for zeroing the basline
    StartZero = 0
    StopZero = 20
    

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
    
            
    try:
        
        # try to get a fit to work
        popt, pcov = curve_fit(ExpFun_bi, TimeArray_to_fit, LTcurve_to_fit, p0=[0.5,0.3,1.3])
        y_fit = ExpFun_bi(TimeArray_to_fit,*popt)
        ## get the error arrays ##
        perr = np.sqrt(np.diag(pcov))
        ## get r_sqaured (https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit)
        residuals = LTcurve_to_fit - ExpFun_bi(TimeArray_to_fit, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((LTcurve_to_fit-np.mean(LTcurve_to_fit))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        
        # make the fit figure
        fig1, ax1 = plt.subplots(1)
        ax1.plot(TimeArray,LTcurve,c='b',lw=1)
        ax1.plot(TimeArray_to_fit,LTcurve_to_fit,c='k',lw=3)
        ax1.plot(TimeArray_to_fit,y_fit,c='y',lw=2,ls='dashed')
        ## annotate the title and axis ##
        ax1.set_xlabel('Time (ns)')
        ax1.set_ylabel('Counts (normalized)')
        ax1.set_title('BiFit_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop))
        # annotate the total yield of the lifetime curve
        ax1.annotate('Total Yield\n%.f'%TotalYield, xy=(0.8, 0.5), xycoords='axes fraction', color='k', fontsize=14,horizontalalignment='center')
        ## make annotations of fit values ##
        ax1.annotate('$a_1$ = %.3f'%popt[0], xy=(0.45, 0.9), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('$t_1$ = %.3f'%popt[1], xy=(0.45, 0.85), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('$a_2$ = %.3f'%(1-popt[0]), xy=(0.45, 0.8), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('$t_2$ = %.3f'%popt[2], xy=(0.45, 0.75), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('($\sigma_1$ = %.3f)'%perr[0], xy=(0.65, 0.9), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('($\sigma_1$ = %.3f)'%perr[1], xy=(0.65, 0.85), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('($\sigma_1$ = %.3f)'%perr[0], xy=(0.65, 0.8), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('($\sigma_1$ = %.3f)'%perr[2], xy=(0.65, 0.75), xycoords='axes fraction', color='k', fontsize=12)
        ax1.annotate('$R^2$ = %.3f'%r_squared, xy=(0.7, 0.65), xycoords='axes fraction', color='k', fontsize=14)
        
        ## make the residual figure
        fig2, ax2 = plt.subplots(1)
        ax2.scatter(TimeArray_to_fit,residuals,s=10,c='b')
        ax2.axhline(0,c='k',ls='dashed')
        ax2.set_xlabel('Time (ns)')
        ax2.set_xlabel('Residuals')
        ax2.set_title('BiFit_Residual_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop))
        ax2.set_ylim(-0.15,0.15)
        
        ## save the figures ##
        fig1.savefig('results/BiFit_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop),dpi=200)
        fig2.savefig('results/BiFit_Residual_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop),dpi=200)
        
        
    except RuntimeError:
        print('passed on the run time error')