from __future__ import division
import numpy as np
import matplotlib.pyplot as plt   

def SpectraPlot(Data, WavelengthArray,StartZero,StopZero,label):
    for idx in range(16):
        mymean = np.mean(Data[idx,StartZero:StopZero])
        Data[idx,:] = Data[idx,:] - mymean
    Spectra = np.sum(Data,axis=1)
    fig, ax = plt.subplots(1)
    ax.plot(WavelengthArray,Spectra,marker='o')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Counts per pixel')
    ax.set_title(label)
    fig.savefig('results/Spectra_'+label,dpi=200)
    
    
    