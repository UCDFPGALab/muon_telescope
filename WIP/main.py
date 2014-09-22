import numpy as np
import matplotlib.pyplot as plt
import math
import sys, os
from pylab import *
from cluster import * 
from plots import *

#********************#
#Begin side functions#
#********************#

led_run = 0 # Set this to anything besides zero, and the program will output only the timestamps of LED pixels

def times(time):
  times = []
  curtime = time[0]
  cnt = 0
  for i in range(0, len(time)):
    if curtime == time[i]:
      continue
    times.append(curtime)
    curtime = time[i]
  #Returns an array of time for each frame
  #1 entry corresponds to one frame
  return times

def pix_per_frame(time):
  pix_cnt = []
  curtime = time[0]
  cnt = 0
  for i in range(0, len(time)):
    if curtime == time[i]:
      cnt+=1
      continue
    pix_cnt.append(cnt)
    curtime = time[i]
    cnt = 1
  #Returns an array of counts of pixels per frame
  #1 entry corresponds to one frame
  return pix_cnt

def sort_arrs_by_time(pID,x,y,pval,pavg3,pavg5,pm,eID,etime,elon,elat,epAvg,epStd,eorx,eory,eorz,xID,xtime,xL1,xL2,xdrp):
  #initialize curtime to the first time value
  curtime = etime[0]
  pIDarr  = [];	xarr 	= [];	yarr 	= []
  valarr  = [];	avg3arr = [];	avg5arr = []
  pmarr   = [];	eIDarr  = [];	etimearr= []
  elonarr = [];	elatarr = [];	epAvgarr= []
  epStdarr= [];	eorxarr = [];	eoryarr = []
  eorzarr = [];	xIDarr  = [];	xtimearr= []
  xL1arr  = [];	xL2arr	= [];	xdrparr = []
  tpIDarr  = [];	txarr 	 = [];	tyarr 	 = []
  tvalarr  = [];	tavg3arr = [];	tavg5arr = []
  tpmarr   = [];	teIDarr  = [];	tetimearr= []
  telonarr = [];	telatarr = [];	tepAvgarr= []
  tepStdarr= [];	teorxarr = [];	teoryarr = []
  teorzarr = [];	txIDarr  = [];	txtimearr= []
  txL1arr  = [];	txL2arr	 = [];	txdrparr = []
  for i in range(0, len(etime)):
    #if curtime is equal to the time we are looking
    #at, then append to temp array and continue doing 
    #so until times no longer match
    if curtime == etime[i]:
      tpIDarr.append(pID[i])
      txarr.append(x[i])
      tyarr.append(y[i])
      tvalarr.append(pval[i])
      tavg3arr.append(pavg3[i])
      tavg5arr.append(pavg5[i])
      tpmarr.append(pm[i])
      teIDarr.append(eID[i])
      tetimearr.append(etime[i])
      telonarr.append(elon[i])
      telatarr.append(elat[i])
      tepAvgarr.append(epAvg[i])
      tepStdarr.append(epStd[i])
      teorxarr.append(eorx[i])
      teoryarr.append(eory[i])
      teorzarr.append(eorz[i])
      txIDarr.append(xID[i])
      txtimearr.append(xtime[i])
      txL1arr.append(xL1[i])
      txL2arr.append(xL2[i])
      txdrparr.append(xdrp[i])
      continue
    #once times no longer match, reset curtime
    curtime = etime[i]
    #append temporary array of image
    pIDarr.append(tpIDarr)
    xarr.append(txarr)
    yarr.append(tyarr)
    valarr.append(tvalarr)
    avg3arr.append(tavg3arr)
    avg5arr.append(tavg5arr)
    pmarr.append(tpmarr)
    eIDarr.append(teIDarr)
    etimearr.append(tetimearr)
    elonarr.append(telonarr)
    elatarr.append(telatarr)
    epAvgarr.append(tepAvgarr)
    epStdarr.append(tepStdarr)
    eorxarr.append(teorxarr)
    eoryarr.append(teoryarr)
    eorzarr.append(teorzarr)
    xIDarr.append(txIDarr)
    xtimearr.append(txtimearr)
    xL1arr.append(txL1arr)
    xL2arr.append(txL2arr)
    xdrparr.append(txdrparr)
    #flush out temp arrays
    tpIDarr  = [];	txarr 	 = [];	tyarr 	 = []
    tvalarr  = [];	tavg3arr = [];	tavg5arr = []
    tpmarr   = [];	teIDarr  = [];	tetimearr= []
    telonarr = [];	telatarr = [];	tepAvgarr= []
    teorzarr = [];	txIDarr  = [];	txtimearr= []
    txL1arr  = [];	txL2arr	 = [];	txdrparr = []
    #append most recent values to not skip them
    tpIDarr.append(pID[i])
    txarr.append(x[i])
    tyarr.append(y[i])
    tvalarr.append(pval[i])
    tavg3arr.append(pavg3[i])
    tavg5arr.append(pavg5[i])
    tpmarr.append(pm[i])
    teIDarr.append(eID[i])
    tetimearr.append(etime[i])
    telonarr.append(elon[i])
    telatarr.append(elat[i])
    tepAvgarr.append(epAvg[i])
    tepStdarr.append(epStd[i])
    teorxarr.append(eorx[i])
    teoryarr.append(eory[i])
    teorzarr.append(eorz[i])
    txIDarr.append(xID[i])
    txtimearr.append(xtime[i])
    txL1arr.append(xL1[i])
    txL2arr.append(xL2[i])
    txdrparr.append(xdrp[i])
  #Returns each array now sorted by their timestamp
  return(pIDarr,xarr,yarr,valarr,avg3arr,avg5arr,pmarr,eIDarr,etimearr,elonarr,elatarr,epAvgarr,epStdarr,eorxarr,eoryarr,eorzarr,xIDarr,xtimearr,xL1arr,xL2arr,xdrparr)

def sort_arrs_by_thresh(xarr, yarr, valarr, thresh):
  lowx = []
  lowy = []
  lowval = []
  highx = []
  highy = []
  highval = []
  high = False
  for i in range(0, len(valarr)):
    for j in range(0, len(valarr[i])):
      #Check if any pixel in frame is above thresh
      if valarr[i][j] >= thresh:
        high = True
      else:
        high = False
    #Fill accordingly
    if high:
      highx.append(xarr[i])
      highy.append(yarr[i])
      highval.append(valarr[i])
    else:
      lowx.append(xarr[i])
      lowy.append(yarr[i])
      lowval.append(valarr[i])
  return (lowx, lowy, lowval, highx, highy, highval)

def count_hits(xarr, yarr, valarr, thresharr):
  cnt = []
  count = 0
  for i in range(0, len(xarr)):
    for j in range(0, len(xarr[i])):
      for k in range(0, len(xarr[i][j])):
	#Record as a hit if greater than the threshold val
        if valarr[i][j][k] >= thresharr[i][j][k]:
          count+=1
    cnt.append(count)
    count = 0
  #Returns an array of counts for each event
  return cnt

def process_clusters(pIDarr,xarr,yarr,valarr,avg3arr,avg5arr,pmarr,eIDarr,etimearr,elonarr,elatarr,epAvgarr,epStdarr,eorxarr,eoryarr,eorzarr,xIDarr,xtimearr,xL1arr,xL2arr,xdrparr):
  totclarr = []
  for i in range(0, len(xarr)):
    #Get huge indexed clustered array for whole run
    totclarr.append(cluster(xarr[i], yarr[i]))
  pIDclu    = [];  pxclu    = [];  pyclu    = []
  pvalclu   = [];  pavg3clu = [];  pavg5clu = []
  pmclu     = [];  eIDclu   = [];  etimeclu = []
  elonclu   = [];  elatclu  = [];  epavgclu = []
  epstdclu  = [];  eorxclu  = [];  eoryclu  = []
  eorzclu   = [];  xIDclu   = [];  xtimeclu = []
  xL1clu    = [];  xL2clu   = [];  xdrpclu  = []
  totclucnt = []
  for i in range(0, len(totclarr)):
    #Sort out the x, y, and vals by their respective clusters now
    tpID, tpx, tpy, tpval, tpavg3, tpavg5, tpm, teID, tetime, telon, telat, tepAvg, tepStd, teorx, teory, teorz, txID, txtime, txL1, txL2, txdrp = cluster_merge(pIDarr[i],xarr[i],yarr[i],valarr[i],avg3arr[i],avg5arr[i],pmarr[i],eIDarr[i],etimearr[i],elonarr[i],elatarr[i],epAvgarr[i],epStdarr[i],eorxarr[i],eoryarr[i],eorzarr[i],xIDarr[i],xtimearr[i],xL1arr[i],xL2arr[i],xdrparr[i],totclarr[i])
    #Used for histogram
    xval = []
    yval = []
    for n in range(0, len(xarr[i])):
      for m in range(0, int(valarr[i][n])):
        xval.append(xarr[i][n])
        yval.append(yarr[i][n])  
    #If desired, can output individual event image
    #Need to manually input num and set range
    '''
    num = 712
    if i == num:
      #Create an image for each cluster in the frame
      for f in xrange(len(tmpx)):
        #Create a zoomed in image for each individual cluster
        hval, xedges, yedges = np.histogram2d(xval, yval, bins = 40, range=[[tmpx[f][0]-19,tmpx[f][0]+20],[tmpy[f][0]-19,tmpy[f][0]+20]])
        extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
        plt.figure()
        plt.imshow(hval, extent = extent, interpolation = 'nearest')
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.xlabel("pixel x")
        plt.ylabel("pixel y")
        plt.title('Pixel Value (Cluster: %s)'%(f+1))
      hval, xedges, yedges = np.histogram2d(xval, yval, bins = 350, range=[[0,350],[0,350]])
      extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
      plt.figure()
      plt.imshow(hval, extent = extent, interpolation = 'nearest')
      plt.gca().invert_yaxis()
      plt.colorbar()
      plt.xlabel("pixel x")
      plt.ylabel("pixel y")
      plt.title('Pixel Value (Frame: %s)'%(i))
      #plt.show()
    #'''
    #Make full run cluster x, y, val, and count arrays 
    #for each event
    pIDclu.append(tpID)
    pxclu.append(tpx)
    pyclu.append(tpy)
    pvalclu.append(tpval)
    pavg3clu.append(tpavg3)
    pavg5clu.append(tpavg5)
    pmclu.append(tpm)
    eIDclu.append(teID)
    etimeclu.append(tetime)
    elonclu.append(telon)
    elatclu.append(telat)
    epavgclu.append(tepAvg)
    epstdclu.append(tepStd)
    eorxclu.append(teorx)
    eoryclu.append(teory)
    eorzclu.append(teorz)
    xIDclu.append(txID)
    xtimeclu.append(txtime)
    xL1clu.append(txL1)
    xL2clu.append(txL2)
    xdrpclu.append(txdrp)
    totclucnt.append(len(tpx))
  #get all of the clusters lengths for each individual frame
  #and throw into an array of arrays
  totclulen = []
  #Find the cluster lengths for each cluster in run
  for i in xrange(len(pxclu)):
    length = cluster_length(pxclu[i], pyclu[i])
    for j in xrange(len(length)):
      totclulen.append(length[j])
  return pIDclu,pxclu,pyclu,pvalclu,pavg3clu,pavg5clu,pmclu,eIDclu,etimeclu,elonclu,elatclu,epavgclu,epstdclu,eorxclu,eoryclu,eorzclu,xIDclu,xtimeclu,xL1clu,xL2clu,xdrpclu,totclucnt,totclulen

def get_run_length(xbTime):
  cur = xbTime[0]
  tot = xbTime[0]
  for i in xrange(len(xbTime)):
    if xbTime[i] != cur:
      cur=xbTime[i]
      tot+=xbTime[i]
  return tot

def get_rid_of_hot_pixels(pID,x,y,pval,pavg3,pavg5,pm,eID,etime,elon,elat,epAvg,epStd,eorx,eory,eorz,xID,xtime,xL1,xL2,xdrp,LED=0):
  #Get number of frames
  count=0
  for i in xrange(len(x)):
    if x[i] == 1:
      count+=1
  
  #Say that if a pixel is hit 10x of the avg
  #pix hit, it is a hot pixel
  maxx = int(max(x))
  maxy = int(max(y))
  #Create a 2D array to store how many time each pix was hit
  frame = [[0 for j in xrange(maxy)] for i in xrange(maxx)]
  #Now loop through x and y and count # each pix is hit
  for i in xrange(len(x)):
    frame[int(x[i])-1][int(y[i])-1]+=1
  
  hit_tot = 0
  #Find average number of pixel hits
  for i in xrange(maxx):
    for j in xrange(maxy):
      hit_tot+=frame[i-1][j-1]
  avg_hit = float(hit_tot)/float(maxx*maxy)
  
  #If it's a bad data set with low avg return unaltered arrays
  if avg_hit <= .10:
    return pID,x,y,pval,pavg3,pavg5,pm,eID,etime,elon,elat,epAvg,epStd,eorx,eory,eorz,xID,xtime,xL1,xL2,xdrp

  ind_to_rem = []
  #Loop through and get indecies for hot pix
  for i in xrange(len(x)):
    if LED == 0:
        if float(frame[int(x[i])-1][int(y[i])-1]) >= float(10*avg_hit):
            ind_to_rem.append(i)
    else:
        if float(frame[int(x[i])-1][int(y[i])-1]) < float(10*avg_hit):
            ind_to_rem.append(i)

  #remove hot pixels
  pID 	= np.delete(pID, ind_to_rem)
  x 	= np.delete(x, ind_to_rem)
  y 	= np.delete(y, ind_to_rem)
  pval 	= np.delete(pval, ind_to_rem)
  pavg3 = np.delete(pavg3, ind_to_rem)
  pavg5	= np.delete(pavg5, ind_to_rem)
  pm 	= np.delete(pm, ind_to_rem)
  eID 	= np.delete(eID, ind_to_rem)
  etime = np.delete(etime, ind_to_rem)
  elon 	= np.delete(elon, ind_to_rem)
  elat 	= np.delete(elat, ind_to_rem)
  epAvg	= np.delete(epAvg, ind_to_rem)
  epStd = np.delete(epStd, ind_to_rem)
  eorx	= np.delete(eorx, ind_to_rem)
  eory	= np.delete(eory, ind_to_rem)
  eorz	= np.delete(eorz, ind_to_rem)
  xID	= np.delete(xID, ind_to_rem)
  xtime	= np.delete(xtime, ind_to_rem)
  xL1	= np.delete(xL1, ind_to_rem)
  xL2	= np.delete(xL2, ind_to_rem)
  xdrp	= np.delete(xdrp, ind_to_rem)

  return pID,x,y,pval,pavg3,pavg5,pm,eID,etime,elon,elat,epAvg,epStd,eorx,eory,eorz,xID,xtime,xL1,xL2,xdrp


def get_run_ID(fn):
  f0 = os.path.basename(fn)
  return f0.split('.')[0].split('_')

#*************#
#Main Function#
#*************#
if __name__== "__main__":
  #Create an array to hold each input file so we can unpack each
  #one individually... Hopefully I find a better way to do this
  hyl = []
  fmb = []
  for i in xrange(len(sys.argv)):
    if i==0:
      continue
    #initialize all the arrays
    fmb = []
    #Skip first row since it is just text
    pix_ID, pix_x, pix_y, pix_val, pix_avg3, pix_avg5, pix_m, evt_ID, evt_time, evt_lon, evt_lat, evt_pixAvg, evt_pixStd, evt_or_x, evt_or_y, evt_or_z, xb_ID, xb_time, xb_L1thr, xb_L2thr, xb_drpFms = np.loadtxt(sys.argv[i], skiprows=1, unpack=True)
    fmb.append(pix_ID)    
    fmb.append(pix_x)    
    fmb.append(pix_y)
    fmb.append(pix_val)
    fmb.append(pix_avg3)
    fmb.append(pix_avg5)
    fmb.append(pix_m)
    fmb.append(evt_ID)
    fmb.append(evt_time)
    fmb.append(evt_lon)
    fmb.append(evt_lat)
    fmb.append(evt_pixAvg)
    fmb.append(evt_pixStd)
    fmb.append(evt_or_x)
    fmb.append(evt_or_y)
    fmb.append(evt_or_z)
    fmb.append(xb_ID)
    fmb.append(xb_time)
    fmb.append(xb_L1thr)
    fmb.append(xb_L2thr)
    fmb.append(xb_drpFms)
    hyl.append(fmb)

  #***********************************************************#
  #Note on how to handle the data     :                       #
  #hyl is a collection of each file inputted                  #
  #Each element in hyl corresponsd to a different file        #
  #Each element in hyl is an array of the unpacked txt data   #
  #So it's a 3D array in total...                             #
  #To access the 4th pix_x from the first txt file it would be#
  #hyl[0][1][3] since pix_x is the 2nd array element in fmb   #
  #***********************************************************#
  #pix_ID 	= 0  #pix_x	= 1  #pix_y	= 2
  #pix_val	= 3  #pix_avg3	= 4  #pix_avg5	= 5
  #pix_m	= 6  #evt_ID	= 7  #evt_time	= 8
  #evt_lon	= 9  #evt_lat	= 10 #evt_pixAvg= 11
  #evt_pixStd	= 12 #evt_or_x	= 13 #evt_or_y  = 14
  #evt_or_z	= 15 #xb_ID	= 16 #xb_time	= 17
  #xb_L1thr	= 18 #xb_L2thr	= 19 #xb_drpFms = 20

  #Get rid of hot pixels and respective data
  for i in xrange(len(hyl)):
    hyl[i][0],hyl[i][1],hyl[i][2],hyl[i][3],hyl[i][4],hyl[i][5],hyl[i][6],hyl[i][7],hyl[i][8],hyl[i][9],hyl[i][10],hyl[i][11],hyl[i][12],hyl[i][13],hyl[i][14],hyl[i][15],hyl[i][16],hyl[i][17],hyl[i][18],hyl[i][19],hyl[i][20] = get_rid_of_hot_pixels(hyl[i][0],hyl[i][1],hyl[i][2],hyl[i][3],hyl[i][4],hyl[i][5],hyl[i][6],hyl[i][7],hyl[i][8],hyl[i][9],hyl[i][10],hyl[i][11],hyl[i][12],hyl[i][13],hyl[i][14],hyl[i][15],hyl[i][16],hyl[i][17],hyl[i][18],hyl[i][19],hyl[i][20],led_run)
  
  hylem = []
  for i in xrange(len(hyl)):
    fmb = []
    #reorganize into array of arrays by time stamp
    pID, px, py, pval, pavg3, pavg5, pma, eID, et, elon, elat, epavg, epstd, eorx, eory, eorz, xID, xt, xL1, xL2, xdrp = sort_arrs_by_time(hyl[i][0],hyl[i][1],hyl[i][2],hyl[i][3],hyl[i][4],hyl[i][5],hyl[i][6],hyl[i][7],hyl[i][8],hyl[i][9],hyl[i][10],hyl[i][11],hyl[i][12],hyl[i][13],hyl[i][14],hyl[i][15],hyl[i][16],hyl[i][17],hyl[i][18],hyl[i][19],hyl[i][20])
    #loop through arrs and classify as above or below hit thresh
    #SHOULD ALWAYS BE ABOVE THRESHOLD SINCE WE ONLY UPLOAD FRAMES WITH 
    #A PIXEL ABOVE THRESHOLD
    #lowx, lowy, lowval, highx, highy, highval = sort_arrs_by_thresh(px, py, pval, 3)
    #Create clustered arrays
    cpID, cpx, cpy, cpval, cpavg3, cpavg5, cpma, ceID, cet, celon, celat, cepavg, cepstd, ceorx, ceory, ceorz, cxID, cxt, cxL1, cxL2, cxdrp, ccounts, clengths = process_clusters(pID, px, py, pval, pavg3, pavg5, pma, eID, et, elon, elat, epavg, epstd, eorx, eory, eorz, xID, xt, xL1, xL2, xdrp)
    fmb.append(cpID)		#clu_pix_ID		= 0
    fmb.append(cpx)		#clu_pix_x		= 1
    fmb.append(cpy)		#clu_pix_y		= 2
    fmb.append(cpval)		#clu_pix_val		= 3
    fmb.append(cpavg3)		#clu_pix_avg3		= 4
    fmb.append(cpavg5)		#clu_pix_avg5		= 5
    fmb.append(cpma)		#clu_pix_ma		= 6
    fmb.append(ceID)		#clu_evt_ID		= 7
    fmb.append(cet)		#clu_evt_time		= 8
    fmb.append(celon)		#clu_evt_lon		= 9
    fmb.append(celat)		#clu_evt_lat		= 10
    fmb.append(cepavg)		#clu_evt_pix_avg	= 11
    fmb.append(cepstd)		#clu_evt_pix_std	= 12
    fmb.append(ceorx)		#clu_evt_orient_x	= 13
    fmb.append(ceory)		#clu_evt_orient_y	= 14
    fmb.append(ceorz)		#clu_evt_orient_z	= 15
    fmb.append(cxID)		#clu_xb_ID		= 16
    fmb.append(cxt)		#clu_xb_time		= 17
    fmb.append(cxL1)		#clu_xb_L1_thresh	= 18
    fmb.append(cxL2)		#clu_xb_L2_thresh	= 19
    fmb.append(cxdrp)		#clu_xb_drp_frames	= 20
    fmb.append(ccounts)		#clu_counts		= 21
    fmb.append(clengths)	#clu_lengths 		= 22
    #hylem holds all clustered stuff
    hylem.append(fmb)
    #Ex. hylem[0][1][2][3][4] accesses:
    #the 5th element in the 4th cluster in the 3rd frame
    #in the cpx of the 1st file 
    #Ex. hylem[2][4][16][1][7] accesses:
    #the 8th element in the 2nd cluster in the 17th frame
    #in the cpavg3 of the 3rd file

  #Print the length of each run
  #for i in xrange(len(hyl)):
  #  print('Total run time for %s is: %s'%(get_run_ID(sys.argv[i+1]),get_run_length(hyl[i][17])))
  #Plot everything you want
  #for i in xrange(len(hyl)):
  #  plt_pix_hits(hyl[i][1],hyl[i][2],get_run_ID(sys.argv[i+1]))
  #for i in xrange(len(hyl)):
  #  plt_pix_hitsVtime(hyl[i][8],get_run_ID(sys.argv[i+1]),i)
  #for i in xrange(len(hyl)):
  #  plt_pix_vals(hyl[i][3],get_run_ID(sys.argv[i+1]),i)
  #for i in xrange(len(hyl)):
  #  plt_pix_num(hyl[i][8],get_run_ID(sys.argv[i+1]),i)
  #for i in xrange(len(hylem)):
  #  plt_clu_num(hylem[i][21],get_run_ID(sys.argv[i+1]),i)
  #for i in xrange(len(hylem)):
  #  plt_clu_len(hylem[i][22],get_run_ID(sys.argv[i+1]),i)
  #plt.show()

  for i in xrange(len(et)):
    print "\n".join('{0:.0f}'.format(z) for z in et[i])

