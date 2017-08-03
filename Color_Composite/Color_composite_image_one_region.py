from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


'''
In this program you specfiy different files, PMTs, normalization and give a lable to the channel, and the program saves a color composite image.

The Files to be used in the composite image need to be in the data folder
This will only separate images by the wavelength and not timing
Need to create a folder called 'composite_images' in the folder where this script is, as this is where the data is saved to
The brightness and contrast need to be adjusted in an external program (i.e. ImageJ, PowerPoint , etc.)
The files are saved as .png

'''

######### Inputs #########################################################################################################################################

# Add the File Names
# must use 'none' as file name if you don't want that color channel included
File1 = 'Summed_FullImages_Scan01_Retina_55_g90_g1.86_6.9mW_Sclera-ONL_512x512_30s.asc_.npy'  # first grating position
File2 = 'Summed_FullImages_Scan02_Retina_55_g90_g2.8_6.9mW_Sclera-ONL_512x512_30s.asc_.npy'  # second grating position
File3 = 'none'  # third grating position
File4 = 'none' # use this for no image in that color channel


# Select the paremeter for each color channel 
# (WL_start and WL_stop are the PMTs to look at, and will include the start and stop values)

# red channel 
datafile_red = File2 
WL_start_red = 10
WL_stop_red = 12
Rlabel = 'A2E'
# green channel
datafile_green = File2
WL_start_green =3
WL_stop_green = 5
Glabel = 'SHG'
# blue channel
datafile_blue = File1
WL_start_blue = 3
WL_stop_blue = 5
Blabel = 'THG'


# chose the normalization to be used in the image
# NORMsingle find the maximum from all the channels and sets the image max to that (accurately shows the yields for the different channels)
# NORMeachCHANNEL finds the maximum for each channel indiviually (put all channels on equal footing)
Normalization = 'NORMsingle' # The options are: 'NORMeachCHANNEL', 'NORMsingle'






####################### start making the composite image ##################################################################################################
print('This program has started')

# for red channel
if datafile_red == 'none':
    r = 0
else:
    data_red = np.load('data/'+datafile_red)
    r = np.sum(np.sum(data_red,axis=3)[WL_start_red:WL_stop_red+1,:,:],axis=0)  
# for green channel
if datafile_green == 'none':
    g = 0
else:
    data_green = np.load('data/'+datafile_green)
    g = np.sum(np.sum(data_green,axis=3)[WL_start_green:WL_stop_green+1,:,:],axis=0) 
# for blue channel
if datafile_blue == 'none':
    b = 0
else:
    data_blue = np.load('data/'+datafile_blue)
    b = np.sum(np.sum(data_blue,axis=3)[WL_start_blue:WL_stop_blue+1,:,:],axis=0)
    
    
if Normalization == 'NORMeachCHANNEL':
    r = r/np.max(r)
    g = g/np.max(g)
    b = b/np.max(b)
if Normalization == 'NORMsingle':
        maxs = []
        for idx in r,g,b:
            mymax = np.max(idx)
            maxs.append(mymax)
        r = r/np.max(maxs)
        g = g/np.max(maxs)
        b = b/np.max(maxs)
    
# merge RGB colors
rgbArray = np.zeros((512,512,3), 'uint8')
rgbArray[..., 0] = r*256
rgbArray[..., 1] = g*256
rgbArray[..., 2] = b*256

img  = Image.fromarray(rgbArray)
plt.imshow(rgbArray)
img.save('composite_images/Image_Red_'+Rlabel+'_Green_'+Glabel+'_Blue_'+Blabel+'_'+Normalization+'.png')
print('This file has been saved')