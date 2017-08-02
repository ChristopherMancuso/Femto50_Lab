from __future__ import division
import numpy as np

def TimeArray(ADCres,Range=50,TACGain=4):
    TimesPerCh_pix = Range/(TACGain*ADCres)
    return np.linspace(0,TimesPerCh_pix*ADCres,ADCres)
    
    