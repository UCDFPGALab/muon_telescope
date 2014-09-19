import numpy as np
import matplotlib.pyplot as plt 
import math
import sys, os

########## Begin helper functions ##########
def times(t_min, t_max, N_hits, random):
  if ~random:
    times = np.linspace(t_min, t_max, N_hits);
  if random:
    times = sorted(np.random.uniform(t_min, t_max, N_hits));
  return times

def offset_gaus(times, mu, sigma):
  for i in range(0, len(times)):
    times[i] += np.random.normal(mu, sigma, 1)
  return times

def offset_unif(times, offset):
  return [x+offset for x in times]
########## End helper functions ############



# Generate uniformly distributed background samples
P_b = times(0, 1E3, 100, False)
S_b = times(0, 1E3, 100*100, False)

# Generate signal hits offset uniformly
#P_s = times(0, 1E3, 10, False)
#S_s = offset_unif(times(0, 1E3, 10*100, False), 10)

#Generate signal hits offset by Gaussian random number
P_s = times(0, 1E3, 10, False)
S_s = offset_gaus(times(0, 1E3, 10*100, False), 100, 10)

# Add the signal and background
P = sorted(np.concatenate([P_b, P_s]))
S = sorted(np.concatenate([S_b, S_s]))

# Compute the time differences between each phone hit and all scint hits
DT_b = []
for i in range(0, len(P_b)):
  for j in range(0, len(S_b)):
    DT_b.append(P_b[i]-S_b[j])
DT_s = []
for i in range(0, len(P_s)):
  for j in range(0, len(S_s)):
    DT_s.append(P_s[i]-S_s[j])
DT = []
for i in range(0, len(P)):
  for j in range(0, len(S)):
    DT.append(P[i]-S[j])


# Plot a histogram of the background time differences
plt.figure()
n, bins, patches = plt.hist(DT_b, 60, normed=0)
plt.xlabel("Background t_Phone - t_Scintillator [s]")
plt.ylabel("Fraction of Events")

# Plot a histogram of the signal time differences
plt.figure()
n, bins, patches = plt.hist(DT_s, 60, normed=0)
plt.xlabel("Signal t_Phone - t_Scintillator [s]")
plt.ylabel("Fraction of Events")

# Plot a histogram of the total time differences
plt.figure()
n, bins, patches = plt.hist(DT, 60, normed=0)
plt.xlabel("t_Phone - t_Scintillator [s]")
plt.ylabel("Fraction of Events")
plt.show()

