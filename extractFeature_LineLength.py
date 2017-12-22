#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pranavburugula
"""

import os
import numpy as np
import pandas as pd
import re
import sys
import pyedflib
from multiprocessing import Pool




epochLength = 1000 # In milliseconds
slidingWindowLength = 10 # In number of epochs

def calculateLineLength(filename):
    if (re.search('\.edf', filename) != None):
        f = pyedflib.EdfReader(sys.argv[1])
        numChannels = f.signals_in_file
        print ("number of signals in file = ", numChannels)
        signal_labels = f.getSignalLabels()
        print ("signal labels = ", signal_labels)

        numSamples = f.getNSamples()[0]
        sampleFrequency = f.getSampleFrequency(0)
        # fields['fs'] contains the frequency
        numSamplesPerEpoch = int(sampleFrequency * 1000 / epochLength)
        sigbufs = np.zeros((numChannels, numSamples))
        for i in np.arange(numChannels):
            sigbufs[i, :] = f.readSignal(i)
        sigbufs = sigbufs.transpose()
        allChannelsDF = pd.DataFrame(data = sigbufs[:,:], columns = signal_labels)
        llDf = pd.DataFrame(columns = signal_labels)
        print (allChannelsDF.shape)
#        for i in range(20):
#            allChannelsDF = allChannelsDF.add(other = sig[i, :])
        print (allChannelsDF.head())
        
        for i in range(1000):
            if (i > numSamplesPerEpoch):
                row = allChannelsDF.iloc[i-1] - allChannelsDF.iloc[i]
                for j in range(2, numSamplesPerEpoch):
                    row = row + (allChannelsDF.iloc[i-j] - allChannelsDF.iloc[i-j+1])
#                llDf = llDf.append(allChannelsDF.iloc[i] - allChannelsDF.iloc[i+1], 
#                                   ignore_index=True)
                llDf = llDf.append(row, ignore_index=True)
                
        print ("Printing Line Length Data frame")
        print (llDf.head())
    return


#p = Pool()
#p.map(calculateLineLength, [filesList[0]])
#print (filesList[0])
#calculateLineLength(filesList[0])
    
print (sys.argv[1])
calculateLineLength(sys.argv[1])
