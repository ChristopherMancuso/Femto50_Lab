from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

'''
In this program you specfiy different files, PMTs, normalization and give a lable to the channel, and the program saves a color composite image
of both regions.

The Files to be used in the composite image need to be in the data folder
This will only separate images by the wavelength and not timing
Need to create a folder called 'composite_images' in the folder where this script is, as this is where the data is saved to
The brightness and contrast need to be adjusted in an external program (i.e. ImageJ, PowerPoint , etc.)
The files are saved as .png

'''

######### Inputs #########################################################################################################################################

# Add the File Names for the first region
# must use 'none' as file name if you don't want that color channel included
File1 = 'Summed_FullImages_Scan01_Retina_55_g90_g1.86_6.9mW_Sclera-ONL_512x512_30s.asc_.npy'  # first grating position
File2 = 'Summed_FullImages_Scan02_Retina_55_g90_g2.8_6.9mW_Sclera-ONL_512x512_30s.asc_.npy'  # second grating position
File3 = 'none'  # third grating position
File4 = 'none' # use this for no image in that color channel

# Add the File Names for the second region (keep grating position ordering the same as the first region)
# must use 'none' as file name if you don't want that color channel included
File1b = 'Summed_FullImages_Scan61_Retina_55_g90_g1.86_6.9mW_ONL-NFL_512x512_30s.asc_.npy'  # first grating position 
File2b = 'Summed_FullImages_Scan62_Retina_55_g90_g2.8_6.9mW_ONL-NFL_512x512_30s.asc_.npy'  # second grating position
File3b = 'none'  # third grating position
File4b = 'none' # use this for no image in that color channel

# Select the paremeter for each color channel 
# (WL_start and WL_stop are the PMTs to look at, and will include the start and stop values)
# Region 2 images use same values as the Region 1 images

# red channel
datafile_red = File2
WL_start_red = 10
WL_stop_red = 12
Rlabel = 'A2E'
# green channel
datafile_green = File2
WL_start_green = 3
WL_stop_green = 5
Glabel = 'SHG'
# blue channel
datafile_blue = File1
WL_start_blue = 3
WL_stop_blue = 5
Blabel = 'THG'

'''
chose the normalization to be used in the image from the option below
1. 'NORMsingle' : finds the maximum from all the channels and sets the image max to that (accurately shows the yields for all the different channels)
2. 'NORMeachCHANNEL' : finds the maximum for each channel indiviually (put all channels on equal footing)
3. 'NORMeachImage' : finds the maximum from all the channels in one image and sets the image max to that (accurately shows the yields for all the different
    channels in one image)
'''
Normalization = 'NORMeachIMAGE' 



###########################################################################################################################################################
# do not change below here      

print('This program has started')

# red channel image2
if datafile_red   == File1:
    datafile_red2 =  File1b
if datafile_red   == File2:
    datafile_red2 =  File2b
if datafile_red   == File3:
    datafile_red2 =  File3b
# green channel image2
if datafile_green   == File1:
    datafile_green2 =  File1b
if datafile_green   == File2:
    datafile_green2 =  File2b
if datafile_green   == File3:
    datafile_green2 =  File3b
# blue channel image2
if datafile_blue   == File1:
    datafile_blue2 =  File1b
if datafile_blue   == File2:
    datafile_blue2 =  File2b
if datafile_blue   == File3:
    datafile_blue2 =  File3b




####################### start making the composite image ##################################################################################################
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
    

# for red channel
if datafile_red2 == 'none':
    r2 = 0
else:
    data_red2 = np.load('data/'+datafile_red2)
    r2 = np.sum(np.sum(data_red2,axis=3)[WL_start_red:WL_stop_red+1,:,:],axis=0)  
# for green channel
if datafile_green2 == 'none':
    g2 = 0
else:
    data_green2 = np.load('data/'+datafile_green2)
    g2 = np.sum(np.sum(data_green2,axis=3)[WL_start_green:WL_stop_green+1,:,:],axis=0) 
# for blue channel
if datafile_blue2 == 'none':
    b2 = 0
else:
    data_blue2 = np.load('data/'+datafile_blue2)
    b2 = np.sum(np.sum(data_blue2,axis=3)[WL_start_blue:WL_stop_blue+1,:,:],axis=0)
    
    




if Normalization == 'NORMeachCHANNEL':
    r = r/np.max(r)
    g = g/np.max(g)
    b = b/np.max(b)
    r2 = r2/np.max(r2)
    g2 = g2/np.max(g2)
    b2 = b2/np.max(b2)
if Normalization == 'NORMeachIMAGE':
    maxs = []
    for idx in r,g,b:
        mymax = np.max(idx)
        maxs.append(mymax)
    r = r/np.max(maxs)
    g = g/np.max(maxs)
    b = b/np.max(maxs)
    maxs2 = []
    for idx2 in r2,g2,b2:
        mymax2 = np.max(idx2)
        maxs2.append(mymax2)
    r2 = r2/np.max(maxs2)
    g2 = g2/np.max(maxs2)
    b2 = b2/np.max(maxs2)
if Normalization == 'NORMsingle':
        maxs = []
        for idx in r,g,b,r2,g2,b2:
            mymax = np.max(idx)
            maxs.append(mymax)
        r = r/np.max(maxs)
        g = g/np.max(maxs)
        b = b/np.max(maxs)
        r2 = r2/np.max(maxs)
        g2 = g2/np.max(maxs)
        b2 = b2/np.max(maxs)
    
# merge RGB colors
rgbArray = np.zeros((512,512,3), 'uint8')
rgbArray[..., 0] = r*256
rgbArray[..., 1] = g*256
rgbArray[..., 2] = b*256
# merge RGB colors
rgbArray2 = np.zeros((512,512,3), 'uint8')
rgbArray2[..., 0] = r2*256
rgbArray2[..., 1] = g2*256
rgbArray2[..., 2] = b2*256

img  = Image.fromarray(rgbArray)
img2 = Image.fromarray(rgbArray2)

plt.imshow(rgbArray)
img.save('composite_images/Region1_Red_'+Rlabel+'_Green_'+Glabel+'_Blue_'+Blabel+'_'+Normalization+'.png')
img2.save('composite_images/Region2_Red_'+Rlabel+'_Green_'+Glabel+'_Blue_'+Blabel+'_'+Normalization+'.png')

print('Files Saved')