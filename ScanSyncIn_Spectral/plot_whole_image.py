from __future__ import division
import numpy as np
import matplotlib.pyplot as plt      # for graphs
import os, glob


'''
This program plots an image from a ScanSyncIn dataset. This program work in conjunction with save_spectral_data_for_layers. Plot_whole_image
simply plots the data in an interactive matplotlib graph. The idea here is to find the edges of the different layers so they can be input into
the save_spectral_data_for_layers program. 

Things to consider:
1. The convention used here is that the (0,0) pixel is in the top left of the figure. This convention is also used in save_spectral_data_for_layers
2. The x-direction is read left to right, so x_min is the left, and x_max is the right
3. The x-direction is read top to bottom, so y_min is the top, and y_max is far bottom
4. The data must be placed in the data folder to be read

'''

FileName = glob.glob('data/*.npy')[0]
data = np.load(FileName)
data = np.sum(np.sum(data,axis=3),axis=0)

plt.imshow(data,cmap='gray',aspect='auto')

plt.show()