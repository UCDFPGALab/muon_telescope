from __future__ import print_function
from optparse import OptionParser
import time, sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import math
import os

from convertFiles import parseFileNames, textToArray


if __name__ == "__main__":
       
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
