from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

from convertFiles import parseFileNames, textToArray

##########
## SUMS ##
##########

def findSyncWithSums(phoneTimes, arduinoTimes, leftRange, rightRange, offsetIncrement, tolerance, normalization):

    # initial offset in milliseconds
    sums = []
    offsetValues = []
    numberOfPoints = int(math.fabs(((rightRange - leftRange)/offsetIncrement))) + 1
    
    # the first offset to be plotted is the starting x value. it is later incremented
    offset = leftRange
    
    # indicator of how many points have been calculated
    pointNumber = 0
    
    print ("going to plot", numberOfPoints, "points.")
    
    for i in xrange(numberOfPoints):
   
        deltaTimes = cutDeltasForSums(phoneTimes, arduinoTimes, offset, tolerance)
        
        currentSum = np.sum(np.absolute(deltaTimes))
        
        # normalizes the sums to the number of components in sum
        if (len(deltaTimes) != 0) and (normalization == True):
            currentSum = (currentSum / len(deltaTimes))
        
        # y axis for drawSums
        sums.append(currentSum)
        
        # x axis for drawSums
        offsetValues.append(offset)
        
        # increment the offset before looping again
        pointNumber += 1
        print (pointNumber, "/", numberOfPoints, "    SUM: ", int(currentSum), "    OFFSET: ", offset, " ms")
        offset += offsetIncrement
 
    print ("finished findCorrectSync")
    return offsetValues, sums, numberOfPoints

def cutDeltasForSums(phoneTimes, arduinoTimes, offset, tolerance):
    
    deltaTimes = []

    for i in xrange(len(phoneTimes)):
    
        if tolerance == "smallest":
            # index of the smallest difference between index i of phone timestamps and ALL of arduino timestamps
            index = np.argmin(np.abs(phoneTimes[i] + offset - arduinoTimes))
            # plugs index in to find actual value of that smallest difference
            smallestMatch = (phoneTimes[i] + offset - arduinoTimes[index])
            deltaTimes.append(smallestMatch)
        
        elif tolerance == "all":
            baseDifferences = (phoneTimes[i] - arduinoTimes)
            # include every difference
            deltaTimes = np.append(deltaTimes, (baseDifferences + offset))
       
        # run if tolerance is a number
        elif isinstance(tolerance, int) == True:
            baseDifference = (phoneTimes[i] + offset - arduinoTimes)
            # only include differences below the tolerance value
            valuesLessThanTolerance = baseDifference[baseDifference <= tolerance]
            valuesLessThanTolerance = valuesLessThanTolerance[valuesLessThanTolerance >= -tolerance]
            deltaTimes = np.append(deltaTimes, valuesLessThanTolerance)
        
        # less efficient method
        # run if tolerance is a number
        #elif isinstance(tolerance, int) == True:
        #    for z in xrange(len(arduinoTimes)):
        #        currentDelta = (phoneTimes[i] + offset - arduinoTimes[z])
        #        if (math.fabs(currentDelta) <= tolerance):
        #            # only include differences below the tolerance value
        #            deltaTimes.append(phoneTimes[i] + offset - arduinoTimes[z])

    return deltaTimes

def drawSums(offsetValues, sums, numberOfPoints, offsetIncrement, saveDirectory, tolerance, normalization):

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
    y = sums
    labels = offsetValues
    
    # tweak sizing
    # more points = wider graph
    if numberOfPoints > 1000:
        figureSize = (25,6)
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
    plotTitle = str(r'$\Sigma$'+"|"+r'$\Delta$'+"t| over time offset")
    
    # naming with value cut, range, offset increment, etc
    fileName = str(str(offsetValues[0])+"To"+str(offsetValues[len(offsetValues) - 1])+"OffsetIncrement"+str(offsetIncrement)+".png")
    
    # label with thresholding info only if they are enabled
    if tolerance == "smallest":
        plotTitle = plotTitle+" (smallest |"+r'$\Delta$'+"t| kept)" 
        fileName = "smallest_"+fileName
    elif tolerance == "all":
        plotTitle = plotTitle+" (all |"+r'$\Delta$'+"t| kept)" 
        fileName = "all_"+fileName
    elif isinstance(tolerance, int) == True:
        plotTitle = plotTitle+" (values > "+str(tolerance)+"ms dropped)"
        fileName = "tolerance<"+str(tolerance)+"ms_"+fileName
        if normalization == True:
            plotTitle = plotTitle+" (normalized by number of elements)" 
            fileName = "normalized_"+fileName
    
    # plot and axis labelling
    plt.title(plotTitle)
    plt.xlabel("Scintillator Time Shift in ms")
    plt.ylabel(r'$\Sigma$'+"|"+r'$\Delta$'+"t |")
    plt.xticks(rotation='vertical')
    
    # pad margins so that markers don't get clipped by the axes
    plt.margins(0.05)
    
    # tweak spacing
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.23)

    # make save directory if it doesn't exist
    if not os.path.exists(saveDirectory+"sums/"):
        os.makedirs(saveDirectory+"sums/")
    
    # save the graph
    saveLocation = saveDirectory+"sums/"+fileName
    plt.savefig(saveLocation, bbox_inches='tight')
    print("saved graph at "+saveLocation)

    # show the graph
    plt.show()

if __name__ == "__main__":
    
    print("going to make a graph of sums across offsets...")

    # parameters
    leftRange =      -1000
    rightRange =      1000
    offsetIncrement = 20
    # "smallest", "all", and integers are accepted
    tolerance = 150
    normalization = True
        
    # uncomment if you want to produce lots of graphs
    #for i in xrange(100): 

    if (tolerance == "all") or (tolerance == "smallest"):
        normalization = False
    startTime = time.time()
    
    # parse names of files
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    
    # convert data in files to arrays
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)

    # find the chosen set of deltaTimes (based on parameters) and sum them up
    offsetValues, sums, numberOfPoints = findSyncWithSums(phoneTimes, arduinoTimes, leftRange, rightRange, offsetIncrement, tolerance, normalization)
        
    # print total time
    endTime = time.time()
    timeItTook = endTime - startTime
    print ("finished in", round((timeItTook/60),2), "minutes")
    
    # plot the sums over millisecond offset
    drawSums(offsetValues, sums, numberOfPoints, offsetIncrement, saveDirectory, tolerance, normalization)
    
    # also uncomment for lots of graphs
    #   tolerance += 10

