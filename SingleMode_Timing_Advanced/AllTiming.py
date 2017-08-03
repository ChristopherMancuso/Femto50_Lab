from __future__ import division
import numpy as np
import matplotlib.pyplot as plt   

def AllTiming(Data, TimeArray, StartZero, StopZero, label):
    for idx in range(16):
        mymean = np.mean(Data[idx,StartZero:StopZero])
        Data[idx,:] = Data[idx,:] - mymean
    fig, ax = plt.subplots(1)
    for idx in range(16):
        ax.plot(TimeArray,Data[idx,:],label='Channel %.i'%(idx+1))
    ax.legend(loc='upper right', frameon=False, ncol=1, fontsize=8)
    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Counts')
    ax.set_title(label)
    fig.savefig('results/AllTiming_'+label,dpi=200)
    
    
    