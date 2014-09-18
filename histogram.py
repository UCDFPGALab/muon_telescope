from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

from convertFiles import parseFileNames, textToArray

#############################
## SINGLE OFFSET HISTOGRAM ##
#############################

def smallestDelta(phoneTimes, arduinoTimes, offset):
    
    deltaTimes = []

    for i in xrange(len(phoneTimes)):
    
        # index of the smallest difference between index i of phone timestamps and ALL of arduino timestamps
        index = np.argmin(np.abs(phoneTimes[i] + offset - arduinoTimes))
        # plugs index in to find actual value of that smallest difference
        smallestMatch = (phoneTimes[i] + offset - arduinoTimes[index])
        deltaTimes.append(smallestMatch)
        
    return deltaTimes

def drawHistogram(deltaTimes, offset, numberOfBins, leftRange, rightRange, saveDirectory):
      
    plt.figure(figsize=(16,6))
    plt.hist(deltaTimes, bins=numberOfBins, range=[leftRange,rightRange])
    plt.title("Smallest Differences in Phone vs. Scintillator Timestamps with "+str(offset)+"ms Timestamp Shift")
    plt.xlabel(r'$\Delta$' "time in ms")
    plt.ylabel("Number of Hits")

    # create save directory if it does not exist
    if not os.path.exists(saveDirectory+"histograms/"):
        os.makedirs(saveDirectory+"histograms/")

    # specify file naming
    fileName = str(offset)+"msOffset_"+str(leftRange)+"to"+str(rightRange)+".png"
    saveLocation = saveDirectory+"histograms/"+fileName

    # save the graph
    plt.savefig(saveLocation, bbox_inches='tight')
    print("saved graph at "+saveLocation)
    
    # show the graph in a popup
    plt.show()


if __name__ == "__main__":
    
    # parameters
    offset = -129000 
    numberOfBins = 200
    leftRange = -15000
    rightRange = 15000
        
    print("going to make a histogram of smallest timestamp differences at offset"+str(offset)+"ms...")

    # parse names of files
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    
    # convert data in files to arrays
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)
    
    # find the closest timestamp to each phone timestamp (at whatever offset you want)
    dTimes = smallestDelta(phoneTimes, arduinoTimes, offset)

    # plot a histogram of the delta times
    drawHistogram(dTimes, offset, numberOfBins, leftRange, rightRange, saveDirectory)
