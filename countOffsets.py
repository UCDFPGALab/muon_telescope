from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

from convertFiles import parseFileNames, textToArray

#######################################
## COUNT NUMBER OF TIMESTAMP MATCHES ##
#######################################

def countDeltas(phoneTimes, arduinoTimes, leftRange, rightRange, offsetIncrement, tolerance):
    
    # initial offset in milliseconds
    numberOfPoints = int(math.fabs(((rightRange - leftRange)/offsetIncrement))) + 1
    
    # the first offset to be plotted is the starting x value. it is later incremented
    offset = leftRange
    
    # indicator of how many points have been calculated
    pointNumber = 0

    counts = []
    offsetValues = []
    
    print ("going to scan", numberOfPoints, "points.")

    for i in xrange(numberOfPoints):
        
        # get list of timestamp differences
        deltaTimes = []    
        deltaTimes = cutDeltasForCounts(phoneTimes, arduinoTimes, offset, tolerance)

        # y axis for graph
        counts.append(len(deltaTimes))
        # x axis for graph
        offsetValues.append(offset)

        print ((pointNumber+1), "/", numberOfPoints, "  COUNT:", str(len(deltaTimes)), "  OFFSET:", offset, "ms  ")
        
        # increment the offset before looping again
        pointNumber += 1
        offset += offsetIncrement


    print("found matches! accidentally set building on fire")

    return offsetValues, counts, numberOfPoints

def cutDeltasForCounts(phoneTimes, arduinoTimes, offset, tolerance):
    
    deltaTimes = []

    for i in xrange(len(phoneTimes)): 
        # create a sorted array of one phone time - all arduino phone times
        deltaList = np.sort((np.abs(phoneTimes[i] + offset - arduinoTimes)))
        
        # append the smallest delta, but only if below the tolerance value
        if (deltaList[0] <= tolerance):
            # only include differences below the tolerance value
            deltaTimes.append(deltaList[0])
        
    return deltaTimes

def drawCounts(offsetValues, counts, numberOfPoints, saveDirectory, offsetIncrement, tolerance):

    # more points --> smaller dots on graph
    if numberOfPoints <= 100:
        markerSize = 4
    else:
        if numberOfPoints <= 300:
            markerSize = 3
        else:
            if numberOfPoints <= 1000:
                markerSize = 2
            else:
                if numberOfPoints > 1000:
                    markerSize = 1

    x = offsetValues
    y = counts
    labels = offsetValues
    
    # tweak sizing: more points --> wider graph
    if numberOfPoints > 1000:
        figureSize = (28,6)
    elif 1000 >= numberOfPoints > 100:
        figureSize = (16,6)
    elif numberOfPoints <= 100:
        figureSize = (8,6)
    plt.figure(figsize=(figureSize))
    
    # set size of the points with markersize
    plt.plot(x, y, 'ro', markersize=markerSize)
    
    # control spacing of x axis
    plt.locator_params(nbins=32,axis='x')
    
    # plot labels
    plotTitle = str("Count of |"+r'$\Delta$'+"t| values under threshold "+str(tolerance)+"ms over time offset")
    plt.title(plotTitle)
    plt.xlabel("Phone timestamp shift in ms")
    plt.ylabel("Count of |"+r'$\Delta$'+"t | < "+str(tolerance)+"ms")
    plt.xticks(rotation='vertical')
    
    # pad margins so that markers don't get clipped by the axes
    plt.margins(0.05)
    
    # tweak spacing
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.23)

    # file naming shenanigans
    fileName = str("tolerance"+str(tolerance)+"ms"+str(offsetValues[0])+"To"+str(offsetValues[len(offsetValues) - 1])+"OffsetIncrement"+str(offsetIncrement)+".png")
    saveLocation = saveDirectory+"counts/"+fileName
   
    # make save directory if it doesn't exist
    if not os.path.exists(saveDirectory+"counts/"):
        os.makedirs(saveDirectory+"counts/")

    # save the graph
    plt.savefig(saveLocation, bbox_inches='tight')
    print("saving plot to", saveLocation)
    
    # show the graph
    plt.show()

if __name__ == "__main__":
    
    # parameters
    leftRange = -300000
    rightRange = 300000
    offsetIncrement = 3000
    # give a maximum ms value to include
    tolerance = 1000
    
    # uncomment for making lots of graphs
    #for i in xrange(100):

    startTime = time.time()
    
    # parse names of files
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    
    # convert data in files to arrays
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)
        
    # find how many of the phone timestamps have an arduino timestamp within the tolerance range
    offsetValues, counts, numberOfPoints = countDeltas(phoneTimes, arduinoTimes, leftRange, rightRange, offsetIncrement, tolerance)
    
    # plot each number above over the offset in milliseconds
    drawCounts(offsetValues, counts, numberOfPoints, saveDirectory, offsetIncrement, tolerance)

    # print total time
    endTime = time.time()
    timeItTook = endTime - startTime
    print ("finished in", round((timeItTook/60),2), "minutes")
    
    # uncomment for mass graphing
    #   tolerance += 10
