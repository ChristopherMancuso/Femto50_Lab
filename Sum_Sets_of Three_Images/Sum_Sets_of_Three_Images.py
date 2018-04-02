import numpy as np

'''

This program assumes you do three grating positions and for each grating position there are three separate files to be summed together.
Must be careful of the naming. If over 100 scans need to order like Scan001, Scan010 and Scan100 for python to read files in the correct order.
The files to be summed over need to be placed in the data folder and the final summed images will be in the summed_images folder. The files are sorted using sorted function before being read.

'''
print('This program has started')

FileNames =  sorted(glob.glob('data/*.npy'))


# the max range is how many sets, it is way more than needed so the program probably will end in an error but it is OK
for idx in range(0,100):
    Sums1 = np.load(FileNames[9*idx+0]) + np.load(FileNames[9*idx+3]) + np.load(FileNames[9*idx+6])
    Sums2 = np.load(FileNames[9*idx+1]) + np.load(FileNames[9*idx+4]) + np.load(FileNames[9*idx+7])
    Sums3 = np.load(FileNames[9*idx+2]) + np.load(FileNames[9*idx+5]) + np.load(FileNames[9*idx+8])
    
    np.save('summed_images/Summed_'+FileNames[9*idx+0],Sums1)
    np.save('summed_images/Summed_'+FileNames[9*idx+1],Sums2)
    np.save('summed_images/Summed_'+FileNames[9*idx+2],Sums3)
    
    del Sums1
    del Sums2
    del Sums3
    
    
