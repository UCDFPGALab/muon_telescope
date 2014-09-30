# runInfo.py

prints information about the run in the following format:

```
SCINT RUN STARTED: 2014-08-29 11:55 AM
SCINT RUN ENDED: 2014-08-31 02:43 PM
TOTAL TIME: 2.1 days
TOTAL EVENTS: 49064 
PHONE RUN STARTED: 2014-08-29 11:56 AM
PHONE RUN ENDED: 2014-08-31 02:43 PM
TOTAL TIME: 2.1 days
TOTAL EVENTS: 535 
SCINT/PHONE EVENT RATIO: 91.0 
```

# Taking data

### Taking scintillator data with arduino

  1) Check to see if the arduino is seeing hits (the device location may differ):
`$ python arduinoLogTime.py /dev/ttyACM0 -o "Output file name"` You should get a "starting!" 

  2) Run `$ nohup python arduinoLogTime.py /dev/ttyACM0 -o "Output file name" &` which pipes the output to a text file in the background. This code must be running for the entire run. `nohup` keeps the program running even if the shell is closed for whatever reason, unlike the ampersand alone.

### Taking phone data

  1) Run `$ sudo su brandon` and ~~steal his wife, kids, and fortune~~ run `$ /storage/crayfis/dataMerge.sh` to update the local storage from the crayfis server. Then `exit` back to youraccount.

  2) Look in /storage/crayfis/txtData/year.month/day/ for the uploaded data packets. The format is yourPhoneID_yourRunID_timeOfUpload.txt. Copy the runID you want.

  3) Copy /storage/crayfis/runID/yourRunID/yourRunID.combined to the run folder with the arduino.txt

  4) Run `$ python brandon_code/main.py runDir/yourRunID.combined` and check that it outputs a stream of timestamps. Then run `$ python brandon_code/main.py runDir/yourRunID.combined >> runDir/phone.txt` to write them to a text file.

# Data analysis

### histogram.py

Finds the closest scintillator timestamp to each phone timestamp, and creates a list of the differences. Makes a histogram showing the spread of the deltas.

### largeHistogram.py

Same as above, but includes not only the smallest delta ts but all of them.

### sumOffsets.py

Takes the delta ts from whatever mode you are working in, then sums them together. This is recalculated for different timestamp offsets. Produces a plot of sums over offsets.

Works in three modes:  
  1. Sums the smallest delta ts  
  2. Sums all delta ts  
  3. Sums the smallest delta ts, but only if they are under the tolerance specified  

### countOffsets.py

First calculates the smallest delta t for each phone timestamp, then tallies up how many of them are under the desired tolerance. This is calculated for timestamp offsets. Produces a plot of counts over offsets.

### correlation.py

Working on it...

### LED.sh

This takes in the (runID).combined file and outputs a sorted list of timestamps for LED hits. The syntax for the command is:
`$bash LED.sh -x 25 -y 25 -t 20 < runID.combined > LED.txt`
Here -x and -y set the coordinates for which pixels are identified as LED pixels and -t sets how many of these pixels must be lit up at once to qualify as an LED hit. All parameters are required, and it is likely to fail spectacularly if you enter a non-integer, so avoid that if possible.

### nonLED.sh

This takes in the (runID).combined file and outputs a similar file (in the same format) with pixels outside the range of interest removed. The syntax for the command is:
`$bash nonLED.sh -x 100 -y 100 < runID.combined > nonLED.combined`
This has the effect of greatly decreasing the file size of the file that must be analyzed by min3.py.

### min3.py

Used like main.py to input data from nonLED.sh.
