#!/usr/bin/env python

import numpy as np
import pylab as pl

HOUR = 3600
DAY = 86400

'''
Generate a simulated discrete timestream for the phone and scintillator data.

Arguments:
  interval    -- the amount of time to sample (seconds)
  resolution  -- the sampling resolution (seconds)
  rate_phone  -- the rate of (real) muon hits in the phone (Hz)
  rate_scint  -- the rate of (real and/or noise) hits on the scintillator (Hz)
  phone_noise -- the noise factor for the phone. E.g. phone_nose=2 means add extra
                 noise to the phone timestream at twice the "real" hit rate.

Returns:
  (ph_data, sc_data, shift)
  ph_data -- the phone timestream data
  sc_data -- the scintillator timestream data
  shift   -- the offset shift (in bins) of the true correlated hit events
'''

def gen_events(interval, resolution, rate_phone, rate_scint, phone_noise=5):
  # number of bins to sample
  nbins = int(interval/resolution)
  print "  using nbins =",nbins

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

'''
Truncate a portion of the phone timestream on each end, then compute the correlation
function to look for the maximal correlation as a function fo time shift.
Note that the longer the sample timestreams and the wider the scanning window, the
more computationally expensive this becomes.

Arguments:
  data_phone -- the phone data timestream
  data_scint -- the scintillator data timestream
  resolution -- the sampling resolution of the timestreams
  width      -- the width of the window over which to scan the time shift (seconds)
  plot       -- plot the correlation function
'''
def find_shift(data_phone, data_scint, resolution, width=None, plot=False):
  if width==None:
    width = resolution*200

  # figure out how many bins we have to shift in order to scan the
  # requested window
  shift_width = int(width/resolution)/2

  # calculate the correlation function
  corr = np.correlate(data_phone[shift_width:-shift_width], data_scint)

  # calculate the times for each correlation point
  times = (shift_width - np.arange(corr.size)) * resolution

  if plot:
    pl.clf()
    pl.plot(times, corr)

  # get the time shift corresponding to the maximal correlation
  dt = times[np.argmax(corr)]

  return corr, dt

'''
Turn a list of timestamps into a discrete timestream

Arguments:
  timestamps -- a list of the event timestamps (in seconds)
  resolution -- the timing resoultion (seconds)

Returns:
  a list of numbers corresponding to the number of events in
  each timestep
'''
def make_timestream(timestamps, resolution):
  start = np.min(timestamps)
  stop = np.max(timestamps)

  nbins = int((stop-start) / resolution)
  print nbins
  timestream, _ = np.histogram(timestamps, bins=nbins)
  return timestream

if __name__ == "__main__":
  pl.ion()

  interval   = 1.*DAY # sec
  resolution = 0.01   # sec
  phone_rate = 0.0012 # Hz
  scint_rate = 30.    # Hz

  print "generating events..."
  p, s, truth = gen_events(interval, resolution, phone_rate, scint_rate)
  gen_dt = truth*resolution

  print "correlating..."
  corr, dt = find_shift(p, s, resolution, plot=True)

  print "true dt =", (resolution*truth)
  print "recovered dt =", dt
  print "signifcance = %g" % ( (corr.max() - corr.mean())/corr.std() )

  if gen_dt == dt:
    print "SUCCESS!"
  else:
    print "FAIL"

  raw_input("press enter")
