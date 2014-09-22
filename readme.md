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
