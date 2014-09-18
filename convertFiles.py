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
