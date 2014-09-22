# takes Arduino serial output, prints it and sticks it in a file

# write to file and monitor simultaneously
# put time in variable
# append the variable to a file, then print it
# add command line argument for filename

from optparse import OptionParser
import serial, sys, time
from datetime import datetime

ser = serial.Serial(port=sys.argv[1], baudrate=115200)


parser = OptionParser()
parser.add_option("-c", "--count", action="store_true", dest="countFlag")
parser.add_option("-t", "--timer", action="store", type="float", default="0", dest="runTimeLength")
parser.add_option("-o", "--output", action="store", dest="outputname", default="youforgottonamethis.txt")

# false by default, the parser will set them to true if flags are used
counterOn = False
timerOn = False
runTimeLength = 0.0 

# stores the command line options as variables
(options, args) = parser.parse_args()
counterOn = options.countFlag
runTimeLength = options.runTimeLength
outputname = options.outputname
if runTimeLength!=0:
    timerOn = True 

# start the timer if the flag is on
if timerOn == True:
    timerStart = time.time()

# start counting 
count = 0

# there's junk at the beginning of serial output, so timestamps are
# only used when "started" is output by arduino and this is set True
started = False

while ser.isOpen():
        
    # breaks the loop when the timer is up
    if timerOn==True:
        curTime = time.time()
        if((curTime - timerStart) >= runTimeLength):
            break

    # script won't move on unless a line is read
    val = ser.readline()

    # start the timer when the "start" signal is given by arduino
    if val.rstrip() == "starting":
        startTime = int(round(time.time() * 1000))
        started = True
        print("started!") 
        fil = open(outputname,"a")
        fil.write("started!")
        fil.write("\n")
        fil.close()
            
    # arduino prints out millis since started, which is tacked onto the start time
    if (started == True) and (val.rstrip() != "starting"):
        eventTime = startTime + int(val)
        fil = open(outputname,"a")
        fil.write(str(eventTime))
        fil.write("\n")
        fil.close()

        # increment the timer
        count = count + 1

        if (counterOn==True):
            print "Count: ", count

print "ran for", round((curTime - timerStart), 1), "seconds"
