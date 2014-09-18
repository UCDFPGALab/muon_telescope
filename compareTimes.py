from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

##############################################
## PUTS TEXT FILES FROM OPTIONS INTO ARRAYS ##
##############################################

def testFunc(): # Just to play around with the code without changing anything important.
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)
    print(phoneDupes)
    print(phoneTimes)

def parseFileNames():

    print("parsing filenames...")
    
    # parse the command line options
    parser = OptionParser()
    parser.add_option("-p", "--phone", action="store", type="string", dest="phonef", help="location of file containing phone timestamps", metavar="FILE")
    parser.add_option("-a", "--arduino", action="store", type="string", dest="arduinof", help="location of file containing arduino timestamps", metavar="FILE")
    parser.add_option("-d", "--directory", action="store", type="string", dest="savedir", help="directory in which to save graphs", metavar="DIR")

    # store the command line options as variables
    (options, args) = parser.parse_args()
    phoneFile = options.phonef
    arduinoFile = options.arduinof
    saveDirectory = options.savedir

    return phoneFile, arduinoFile, saveDirectory

def textToArray(phoneFile, arduinoFile): # New return variable added- counts duplicate timestamps

    print("converting text files to arrays...")

    # numpy arrays will print in their entirety with no ellipses, use when debugging if convenient
    #np.set_printoptions(threshold=np.nan)

    # stick each line from the text file in an array, stripping newlines
    file = open(phoneFile)
    phoneTimes = [line.strip('\n') for line in file.readlines()]
    file.close()
    file = open(arduinoFile)
    arduinoTimes = [line.strip('\n') for line in file.readlines()]
    file.close()
    
    # remove first value from arduino array, contains the text "starting!"
    arduinoTimes = np.delete(arduinoTimes, 0)
    
    # remove last value from arduino array
    # do this because the script can cut off mid-number when the run ends
    arduinoTimes = np.delete(arduinoTimes, (len(arduinoTimes) - 1))
    
    # convert strings to ints 
    x = np.array(phoneTimes)
    phoneTimes = x.astype(np.int)
    y = np.array(arduinoTimes)
    arduinoTimes = y.astype(np.int)
    
    # make sure timestamps are sorted unique with no duplicates
    phoneTimes = np.sort(phoneTimes)
    phoneLength = len(phoneTimes)
    phoneTimes, phoneDupes = np.unique(phoneTimes, return_index=True)
    arduinoTimes = np.unique(arduinoTimes)
    
    # Determines the number of duplicates of each timestamp and stores them in an array
    for i in range(0,len(phoneDupes)-1): 
        phoneDupes[i] = phoneDupes[i+1]-phoneDupes[i]
    phoneDupes[-1] = phoneLength - phoneDupes[-1]

    # maximum difference that the start and end times are allowed to differ
    maxDifference = 1000 # 1 second
   
    # truncate beginning of runs to match each other
    startDiscrepency = phoneTimes[0] - arduinoTimes[0]
    location = " nowhere"
    while True:
        # see how far apart the beginning of each run is
        startDifference = phoneTimes[0] - arduinoTimes[0]
        # cut whichever one is longer so they match
        if startDifference <- maxDifference:
            phoneTimes = np.delete(phoneTimes, 0)
            location = " phone data"
        elif startDifference > maxDifference:
            arduinoTimes = np.delete(arduinoTimes, 0)
            location = " arduino data"
        elif (math.fabs(startDifference)) <= maxDifference:
            print("    cut "+str(int(math.fabs((startDiscrepency - startDifference)/60000)))+" excess minutes from beginning of"+location+"!")
            break
    
    # truncate end of runs to match each other
    endDiscrepency = phoneTimes[-1] - arduinoTimes[-1]
    location = " nowhere"
    while True:
        # see how far apart the end of each run is
        endDifference = phoneTimes[-1] - arduinoTimes[-1]
        # cut whichever one is longer so they match
        if endDifference > maxDifference:
            phoneTimes = np.delete(phoneTimes, -1)
            location = " phone data"
        elif endDifference < -maxDifference:
            arduinoTimes = np.delete(arduinoTimes, -1)
            location = " arduino data"
        elif (math.fabs(endDifference)) <= maxDifference:
            print("    cut "+str(int(math.fabs((endDiscrepency - endDifference)/60000)))+" excess minutes from end of"+location+"!")
            break

    return phoneTimes, arduinoTimes, phoneDupes

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

##############################
## CHASE'S CORRELATION CODE ##
##############################

HOUR = 3600000
DAY = 86400000

    # Generate a simulated discrete timestream for the phone and scintillator data.
    #
    # Arguments:
    #   interval    -- the amount of time to sample (milliseconds)
    #   resolution  -- the sampling resolution (milliseconds)
    #   rate_phone  -- the rate of (real) muon hits in the phone (mHz)
    #   rate_scint  -- the rate of (real and/or noise) hits on the scintillator (mHz)
    #   phone_noise -- the noise factor for the phone. E.g. phone_nose=2 means add extra
    #                 noise to the phone timestream at twice the "real" hit rate.
    #
    # Returns:
    #   (ph_data, sc_data, shift)
    #   ph_data -- the phone timestream data
    #   sc_data -- the scintillator timestream data
    #   shift   -- the offset shift (in bins) of the true correlated hit events


def gen_events(interval, resolution, rate_phone, rate_scint, phone_noise=5):

    # number of bins to sample
    nbins = int(interval/resolution)
    print("  using nbins =",nbins)

    # number of bins to shift to get the target delta_t
    n_shift = np.random.randint(1,100)

    # expected number of hits per sampling interval (bin)
    expect_ph = rate_phone * resolution
    expect_sc = rate_scint * resolution

    # generate simulated timestream of "real" hits for the phone
    data_ph = np.random.poisson(expect_ph, size=nbins)
    # and generate data for the scintillator timestream
    data_sc = np.random.poisson(expect_sc, size=nbins)

    # shift the "real" phone hits and copy them into the scintillator
    # timestream (they are the correlated events)
    data_sc += np.hstack([np.zeros(n_shift), data_ph[:-n_shift]])

    # now add noise to the phone data
    data_ph += np.random.poisson(expect_ph*phone_noise, size=nbins)

    # finally, return the two timestreams, and the true shift
    return data_ph, data_sc, n_shift


    # Turn a list of timestamps into a discrete timestream
    #
    # Arguments:
    #   timestamps -- a list of the event timestamps (in milliseconds)
    #   resolution -- the timing resolution (milliseconds)
    #
    # Returns:
    #   a list of numbers corresponding to the number of events in
    #   each timestep


def make_timestream(timestamps, resolution):
    start = np.min(timestamps)
    stop = np.max(timestamps)

    print("    STOP - START:", (stop-start)) 

    nbins = int((stop-start) / (resolution))
    
    print("    START:", start)
    print("    STOP:", stop)
    print("    RESOLUTION:", resolution)
    print("    BINS:",nbins)
    timestream, _ = np.histogram(timestamps, bins=nbins)
    return timestream


    # Truncate a portion of the phone timestream on each end, then compute the correlation
    # function to look for the maximal correlation as a function fo time shift.
    # Note that the longer the sample timestreams and the wider the scanning window, the
    # more computationally expensive this becomes.
    #
    # Arguments:
    #   data_phone -- the phone data timestream
    #   data_scint -- the scintillator data timestream
    #   resolution -- the sampling resolution of the timestreams
    #   width      -- the width of the window over which to scan the time shift (seconds)
    #   plot       -- plot the correlation function

def find_shift(saveDirectory, data_phone, data_scint, resolution, width=None, plot=False):

    if width==None:
        width = resolution*200

    print("    PHONE DATA LENGTH:", len(data_phone))
    print("    SCINT DATA LENGTH:", len(data_scint))
    
    # figure out how many bins we have to shift in order to scan the
    # requested window
    shift_width = int(width/resolution)/2
    #shift_width = int(100)
    print("    SHIFT WIDTH:", shift_width)

    # calculate the correlation function
    corr = np.correlate(data_phone[shift_width:-shift_width], data_scint)
 
    print("CORR ARRAY:", corr)
    print("LENGTH OF CORR ARRAY:", len(corr))

    # calculate the times for each correlation point
    times = (shift_width - np.arange(corr.size)) * resolution

    if plot:
        # make save directory if it doesn't exist
        if not os.path.exists(saveDirectory+"correlation/"):
            os.makedirs(saveDirectory+"correlation/")


        plt.figure(figsize=(16,6))
        plt.plot(times, corr)
        plt.savefig(str(saveDirectory)+"correlation/correlation_resolution"+str(resolution)+"ms_width"+str(width)+".png")
        plt.show()

    # get the time shift corresponding to the maximal correlation
    dt = times[np.argmax(corr)]

    return corr, dt

#######################################################
## RUN *ONE* OF THE BELOW FUNCTIONS IN MAIN FUNCTION ##
#######################################################

def printRunInfo():
       
    # no parameters for this function
    
    # parse names of files
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    
    # convert data in files to arrays
    phoneTimes, arduinoTimes, phoneDupes = textToArray(phoneFile, arduinoFile)
        
    # ARDUINO RUN TIME

    # find difference between start and end time, convert form millis to days
    runTimeArduino = ((float(arduinoTimes[len(arduinoTimes) - 1]) - float(arduinoTimes[0]))/(1000*60*60*24))
    # convert from millis epoch to seconds epoch, then to readable format 
    runStartArduino = int(arduinoTimes[0])/1000
    readableRunStartArduino = time.strftime('%Y-%m-%d %I:%M %p', time.localtime(runStartArduino))
    runEndArduino = int(arduinoTimes[len(arduinoTimes)-1])/1000
    readableRunEndArduino = time.strftime('%Y-%m-%d %I:%M %p', time.localtime(runEndArduino))

    # PHONE RUN TIME

    # find difference between start and end time, convert form millis to days
    runTimePhone = ((float(phoneTimes[len(phoneTimes) - 1]) - float(phoneTimes[0]))/(1000*60*60*24))
    # convert from millis epoch to seconds epoch, then to readable format 
    runStartPhone = int(phoneTimes[0])/1000
    readableRunStartPhone = time.strftime('%Y-%m-%d %I:%M %p', time.localtime(runStartPhone))
    runEndPhone = int(phoneTimes[len(phoneTimes)-1])/1000
    readableRunEndPhone = time.strftime('%Y-%m-%d %I:%M %p', time.localtime(runEndPhone))
        
    print("\nSCINT RUN STARTED:", readableRunStartArduino)
    print("SCINT RUN ENDED:", readableRunEndArduino)
    print("TOTAL TIME:", round(runTimeArduino, 1), "days")
    print("TOTAL EVENTS:", len(arduinoTimes), "\n")

    print("PHONE RUN STARTED:", readableRunStartPhone)
    print("PHONE RUN ENDED:", readableRunEndPhone)
    print("TOTAL TIME:", round(runTimePhone, 1), "days")
    print("TOTAL EVENTS:", len(phoneTimes), "\n")

    print("SCINT/PHONE EVENT RATIO:", round((len(arduinoTimes)/len(phoneTimes)), 2), "\n")

def runOffsetHistogram():
    
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

def runSums():
    
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

def runGiantHistogram():
    
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

def runCountDeltas():
    
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

def runCorrelation():

    # your guess is as good as mine as to what this does. Refer to corr.py to look at the unadulterated code

    #interval   = 1.*DAY # millisec
    resolution = 100.   # millisec

    #phone_rate = 0.0012 # mHz
    #scint_rate = 30.    # mHz
    
    #print("generating events...")
    #p, s, truth = gen_events(interval, resolution, phone_rate, scint_rate)
    
    print("getting list of times from text files...")
    phoneFile, arduinoFile, saveDirectory = parseFileNames()
    p, s, ignoreMe = textToArray(phoneFile, arduinoFile)

    print("converting phone timestamps to timestream...")
    p = make_timestream(p, resolution)

    print("converting scintillator timestamps to timestream...")
    s = make_timestream(s, resolution)

    #gen_dt = truth*resolution
 
    print("correlating...")
    corr, dt = find_shift(saveDirectory, p, s, resolution, width=100000, plot=True)
 
    #print("true dt =", (resolution*truth))
    print("recovered dt =", dt)
    print("significance = %g" % ( (corr.max() - corr.mean())/corr.std() ))
     
    #if gen_dt == dt:
    #    print("SUCCESS!")
    #else:
    #    print("FAIL")
  
###################
## MAIN FUNCTION ##
###################

if __name__ == "__main__":
        
    # prints start and end times, total hits, total run time for phone and scintillator.
    #printRunInfo()
    
    # input an offset, will graph histogram of delta t.
    #runOffsetHistogram()

    # finds the sum of all delta t's between phone and scintillator over the given interval. It can cut out any percentage of worst matched time it graphs the sums over the offset amount.
    #runSums()
    
    # piles up every phone time subtracted by every arduino time. The background looks like a triangle, the signal is a smaller triangle centered at the correct offset.
    #runGiantHistogram()

    # looks for an offset that maximizes exact timestamp matches only.
    #runCountDeltas()
    
    # run the timestamps through Chase's correlation code
    runCorrelation()

    #testFunc()
