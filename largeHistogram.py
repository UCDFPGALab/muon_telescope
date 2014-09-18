from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

from convertFiles import parseFileNames, textToArray

#####################
## GIANT HISTOGRAM ##
#####################

def findAllDeltas(phoneTimes, arduinoTimes):

    print("calculating all differences...")
    
    deltaTimes = []

    # finds every combination of differences between all timestamps
    for i in xrange(len(phoneTimes)):              
   
        for z in xrange(len(arduinoTimes)):
            # subtract the times
            difference = phoneTimes[i] - arduinoTimes[z]
                                                
            # append all differences to deltaTimes
            deltaTimes.append(difference)
        
    # print ("finished findAllDeltas")
    return deltaTimes

def drawGiantHistogram(deltaTimes, numberOfBins, leftRange, rightRange, saveDirectory):
     
    print("generating histogram...")

    plt.figure(figsize=(16,6.5))
    plt.hist(deltaTimes, bins=numberOfBins, range=[leftRange,rightRange])
    
    # control spacing of x axis
    plt.locator_params(nbins=32,axis='x')
    
    plt.title("All Differences in Phone vs. Scintillator Timestamps")
    plt.xlabel(r'$\Delta$' "time in ms")
    plt.ylabel("Number of Hits")
    plt.xticks(rotation='vertical')
    
    # tweak spacing
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.21)
   
    # specify file naming and save location
    fileName = str(leftRange)+"to"+str(rightRange)+"_"+str(numberOfBins)+"bins"+".png"
    saveLocation = saveDirectory+"/giantHistograms/"+fileName

    # make save directory if it doesn't exist
    if not os.path.exists(saveDirectory+"giantHistograms/"):
        os.makedirs(saveDirectory+"giantHistograms/")

    # save the image
    plt.savefig(saveLocation, bbox_inches='tight')
    
    print("saved figure at", (saveLocation))

    plt.show()

if __name__ == "__main__":
    
    print("going to make a giant histogram of all timestamp difference combinations!")

    # parameters
    numberOfBins = 300
    leftRange = -2000
    rightRange = 2000
    #rightRange = leftRange+increment
        
    # parse names of files
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
 
    # convert data in files to arrays
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)
    dTimes = findAllDeltas(phoneTimes, arduinoTimes)
   
    # scan finely over wide area, produce a ton of graphs
    #interval = 8000
    #for i in xrange(int((-2*leftRange)/increment)):
    #    drawGiantHistogram(dTimes, numberOfBins, leftRange, rightRange, saveDirectory)
    #    leftRange += increment
    #    rightRange += increment
    
    # find EVERY combo of timestamp differences and plot a histogram
    drawGiantHistogram(dTimes, numberOfBins, leftRange, rightRange, saveDirectory)
