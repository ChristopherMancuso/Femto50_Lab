from __future__ import division
import numpy as np
import matplotlib.pyplot as plt 

def LogPlots(data,PMTstart,PMTstop,TimeArray,label):


    # select the wavelengths
    data = data[PMTstart:PMTstop+1,:]
    LTcurve = np.sum(data,axis=0)
    
    # make the two panel figure
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(8,5))
    ax1.plot(TimeArray,LTcurve)
    ax2.plot(TimeArray,LTcurve)
    ax2.set_yscale('log')
    # annotate the plot
    ax1.set_xlabel('Time (ns)')
    ax2.set_xlabel('Time (ns)')
    ax1.set_ylabel('Counts')
    ax2.set_ylabel('Counts')
    fig.suptitle(label+'_PMTs%.fto%.f'%(PMTstart,PMTstop))
    fig.subplots_adjust(left=0.12,bottom=0.11,right=0.97,top=0.91,wspace=0.27,hspace=0.20)
    #save the figure
    fig.savefig('results/Log_'+label+'_PMTs%.fto%.f'%(PMTstart,PMTstop),dpi=200)