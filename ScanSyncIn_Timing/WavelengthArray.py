from __future__ import division
import numpy as np

def WavelengthArray(GratPos):

    # start the calibration 
    a = (404-365)/np.array([8.33-6,7-4,4-1])
    b = (435-404)/np.array([11-8.33,9.5-7,7-4,5-2,4-1])
    c = (546-435)/np.array([12-4,10-2,9-1])
    d = (577-546)/np.array([13-10,10-7,8-6,7-4,5-2.33,4-1])

    mymeans = []
    for myarray in a,b,c,d:
        mymean = np.mean(myarray)
        mymeans.append(mymean)
    total_mean = np.mean(mymeans)

    WLperPMT = total_mean

    NumPMTs_in_step = 16
    bandwidth = total_mean*NumPMTs_in_step

    p1 = (6-1)/(2.1-1.8)
    p2 = (8.33-1)/(2.3-1.8)
    p3 = (11-1)/(2.5-1.8)
    p4 = (12-1)/(3.0-2.3)
    p5 = (13-4)/(3.0-2.4)

    PMTperGrating = (p1+p2+p3+p4+p5)/5

    WLperGrating = (WLperPMT*PMTperGrating)*0.1 # distance in nm move for every 0.1 on the actuator

    # 2.4 is the base case
    g2p4 = np.linspace(404.5,404.5+bandwidth,16)


    change = (GratPos-2.4)*10
    grat_start = 404.5 + (change*WLperGrating)
    grat_stop = grat_start + bandwidth
    return np.linspace(grat_start,grat_stop,16)

















    


