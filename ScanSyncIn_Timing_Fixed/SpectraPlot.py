from __future__ import division
import numpy as np
import matplotlib.pyplot as plt   

def SpectraPlot(Data, WavelengthArray,label):
    Spectra = np.sum(np.sum(np.sum(Data,axis=1),axis=1),axis=1)
    plt.plot(WavelengthArray,Spectra,marker='o')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Counts per pixel')
    plt.title(label)
    plt.savefig('results/Spectra_'+label,dpi=200)
    # plt.show()
    
    
    