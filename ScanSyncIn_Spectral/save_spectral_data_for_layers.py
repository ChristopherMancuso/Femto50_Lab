from __future__ import division
import numpy as np
import matplotlib.pyplot as plt      # for graphs
import os, glob
import matplotlib.patches as patches
import WavelengthArray


'''
This program will plot the spectral data for each layer as well as an image of the regio depicting where the layers were
taken from. Additionally, three files are saved: the first saves the labels for the layers, the second saves the calibrated wavelength at
the given grating position, and the last file saves the emission spectra from all the layers. This program only does one data file at a time.

Things to consider:
1. This assumes 16 PMTs were used.
2. The data file must be in the data folder
3. The results will go in the results folder.

'''

###########################################################################################################################################################

# inputs

# the grating position
GratPos = 2.8

# a dictionaryof the boundaries where each layer is of the form 'Layer':[x_min,x_max,y_min,y_max]. 
# Remember y_min is the top of the image, which is the same convention used in plot_whole_image
LayerRegions = {'IPL':[6,30,188,404],
                'INL':[71,106,150,375],
                'OPL':[142,165,170,375],
                'ONL':[215,300,170,400],
                'IRL':[345,385,140,350],
                'ORL':[416,443,65,234],
                'RPE':[472,486,124,283],
                'Choroid':[482,503,133,335]}


#########################################################################################################################################################
print('The program has started')

# load the data
FileName = glob.glob('data/*.npy')[0]
data = np.load(FileName)

# change the file name for saving
FileName = FileName.split('data/')[-1]

# create the wavelength array
WavelengthArray = WavelengthArray.WavelengthArray(GratPos)

#create a tuple of the dictionary
Items = LayerRegions.items()


print('Making plot with ROI boxes')
# make a plot of all the PMTs and pixels with boxes of regions of interest
SummedIm = np.sum(np.sum(data,axis=3),axis=0)
# Create figure and axes
fig = plt.figure(figsize=(4,4))
ax  = plt.subplot(111)
ax.imshow(SummedIm[:,:],cmap='gray',aspect='auto')
ax.set_xticklabels([])
ax.set_yticklabels([])
for idx in range(len(LayerRegions)):
    # Create a Rectangle patch
    left    = Items[idx][1][0]
    right   = Items[idx][1][1]
    top     = Items[idx][1][2]
    bottom  = Items[idx][1][3]
    width = right - left
    height = bottom - top
    rect = patches.Rectangle((left,top),width,height,linewidth=1,edgecolor='w',facecolor='none')
    ax.add_patch(rect)
fig.savefig('results/Region_with_boxes.png',dpi=200)

print('Making spectra plots for all the layers')
# make a plot of the wavelengths - individual plots
Emission_of_Layers = []
for idx in range(len(LayerRegions)):
    label   = Items[idx][0]
    left    = Items[idx][1][0]
    right   = Items[idx][1][1]
    top     = Items[idx][1][2]
    bottom  = Items[idx][1][3]
    NumPixs_tot = (right - left) + (bottom - top)

    EmissionIm = data[:,top:bottom,left:right,:]
    EmissionIm = np.sum(np.sum(np.sum(EmissionIm,axis=1),axis=1),axis=1)
    Emission_of_Layers.append(EmissionIm)

    fig,ax = plt.subplots(1)
    ax.plot(WavelengthArray, EmissionIm,marker='o')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Counts per pixel')
    ax.set_title(label)
    fig.savefig('results/'+label,dpi=200)

Emission_of_Layers = np.array(Emission_of_Layers)

# save the files
np.save('results/Emission_'+FileName, Emission_of_Layers)
np.save('results/Labels_'+FileName, LayerRegions.keys())
np.save('results/WavelengthArray_'+FileName, WavelengthArray)

print('The files have been saved')