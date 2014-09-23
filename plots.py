import numpy as np
import matplotlib.pyplot as plt
import math
import sys, os
from pylab import *
from main import *
from cluster import *

def get_color(i):
  if i == 0:
    return 'black'
  elif i == 1:
    return 'blue'
  elif i == 2:
    return 'green'
  elif i == 3:
    return 'red'
  elif i == 4:
    return 'cyan'
  elif i == 5:
    return 'magenta'
  elif i == 6:
    return 'brown'
  return 'black'

def plt_pix_hits(pix_x, pix_y, run_ID):
  plt.figure()
  h, xedges, yedges = np.histogram2d(pix_x, pix_y, bins = 60, range=[[0,350], [0,300]])
  extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
  plt.imshow(h, extent = extent, interpolation = 'nearest')
  plt.colorbar()
  plt.gca().invert_yaxis()
  plt.xlabel("pixel x")
  plt.ylabel("pixel y")
  plt.title("Number of Pixel Hits %s"%run_ID)

def plt_pix_vals(pix_val, run_ID, i):
  if i == 0:
    plt.figure()
  nval, bins, patches = plt.hist(pix_val, bins=40, color=get_color(i), edgecolor=get_color(i), normed=1, label='%s'%run_ID, histtype='step')
  plt.semilogy()
  plt.legend(loc='upper right')
  plt.xlabel("Pixel Value")
  plt.ylabel("Fraction of Events")
  plt.title("Pixel Values")
  #plt.gca().set_yscale("log")

def plt_pix_hitsVtime(evt_time, run_ID, i):
  if i == 0:
    plt.figure()
  t = times(evt_time)
  pix = pix_per_frame(evt_time)
  plt.plot(t, pix, label='%s'%run_ID)
  plt.semilogy()
  plt.legend(loc='upper right')
  plt.xlabel("Time")
  plt.ylabel("Number of Hit Pixels")
  plt.title("Number of Pixel Hits vs. Time")

def plt_pix_num(evt_time, run_ID, i):
  if i == 0:
    plt.figure()
  pix = pix_per_frame(evt_time)
  plt.semilogy()
  n, bins, patches = plt.hist(pix, normed=1, bins=30, color=get_color(i), edgecolor=get_color(i), label='%s'%run_ID, histtype='step')
  plt.legend(loc='upper right')
  plt.xlabel("Pixels/frame")
  plt.ylabel("Fraction of Events")
  plt.title("Number of Pixels per frame")

def plt_clu_num(totclucnt, run_ID, i):
  if i == 0:
    plt.figure()
  n, bins, patches = plt.hist(totclucnt, normed=1, bins=8, color=get_color(i), edgecolor=get_color(i), label='%s'%run_ID, histtype='step', range=[0,4])
  #plt.semilogy()
  plt.legend(loc='upper right')
  plt.xlabel("Clusters/frame")
  plt.ylabel("Number of Events")
  plt.title("Number of Clusters per Frame")

def plt_clu_len(totclulen, run_ID, i):
  if i == 0:
    plt.figure()
  n, bins, patches = plt.hist(totclulen, bins=45, normed=1, color=get_color(i), edgecolor=get_color(i), histtype='step',label='%s'%run_ID)
  plt.legend(loc='upper right')
  plt.xlabel("Cluster Length")
  plt.ylabel("Fraction of Events")
  plt.title("Cluster Lengths")
