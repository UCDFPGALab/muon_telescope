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

# histogram.py

Finds the closest scintillator timestamp to each phone timestamp, and creates a list of the differences. Makes a histogram showing the spread of the deltas.

# largeHistogram.py

Same as above, but includes not only the smallest delta ts but all of them.

# sumOffsets.py

Takes the delta ts from whatever mode you are working in, then sums them together. This is recalculated for different timestamp offsets. Produces a plot of sums over offsets.

Works in three modes:  
  1. Sums the smallest delta ts  
  2. Sums all delta ts  
  3. Sums the smallest delta ts, but only if they are under the tolerance specified  

# countOffsets.py

First calculates the smallest delta t for each phone timestamp, then tallies up how many of them are under the desired tolerance. This is calculated for timestamp offsets. Produces a plot of counts over offsets.

# correlation.py

Working on it...
