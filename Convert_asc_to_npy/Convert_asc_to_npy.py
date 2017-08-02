import numpy as np
import glob

'''
For this program to work the file names have to include the x and y dimenisons in pixels. The three standard ones we use are included, but other can be added.
The asc files need to be in a folder called data and a folder named processed_files needs to be made to save the results.

'''

print('This program has started')
print

FileNames = glob.glob('data/*.asc')



for FileName in FileNames:
    FileName_crop = FileName.split('data/')[-1]
    print('Loading File ' + FileName_crop)
    print
    if '512x512' in FileName:
        NumPMTs   = 16
        NumTimeCh = 4
        NumPixX   = 512
        NumPixY   = 512
        ElementsinImage = NumPixX * NumPixY
    if '256x16' in FileName:
        NumPMTs   = 16
        NumTimeCh = 256
        NumPixX   = 256
        NumPixY   = 16
        ElementsinImage = NumPixX * NumPixY
    if '16x256' in FileName:
        NumPMTs   = 16
        NumTimeCh = 256
        NumPixX   = 16
        NumPixY   = 256
        ElementsinImage = NumPixX * NumPixY


    
    data = np.genfromtxt(FileName,skip_header=10,skip_footer=1)
    print('Length of the data is')
    print(np.shape(data)[0])
    print

    LengthofPMTData = int(np.shape(data)[0]/NumPMTs)

    DiffPMTs = np.zeros((LengthofPMTData,NumPMTs))
    for idx in range(0,NumPMTs):
        DiffPMTs[:,idx] = data[(idx*LengthofPMTData):(idx*LengthofPMTData)+(LengthofPMTData)]

    FullImages = []
    for idx in range(0,NumPMTs):
        ImageArray = []
        for idx2 in range(0,int(NumTimeCh)):
            All_Elements_for_a_time = np.zeros((ElementsinImage))
            for idx3 in range(0,int(ElementsinImage)):
                All_Elements_for_a_time[idx3] = DiffPMTs[(idx3*NumTimeCh)+idx2 ,idx]
            Reshape_to_image = np.reshape(All_Elements_for_a_time,(NumPixX,NumPixY))
            if idx2 == 0:
                ImageArray = Reshape_to_image
            if idx2 > 0:
                ImageArray = np.dstack((ImageArray,Reshape_to_image))
        FullImages.append(ImageArray)

    FullImages = np.array(FullImages)
    print('Shape of saved .npy file is')
    print(np.shape(FullImages))
    print

    np.save('processed_files/FullImages_'+FileName_crop+'_.npy',FullImages)

