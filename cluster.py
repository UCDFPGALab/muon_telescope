import numpy as np
import matplotlib.pyplot as plt
import math

def dist(x1, x2, y1, y2):
  return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

###This function uses the x and y arrays
###to create a cluster array that has the indexes
###separated into the different clusters
###according to their x and y positions.
###Ex: [[0,3],[1,2]] as the cluarr output
###would be x[0] and x[3] are in a cluster together
###and x[1] and x[2] are in another cluster
def cluster(x, y):
  #initialize clarr with the first index already in
  clarr = [[]]

  #make sure any pixels were detected
  if len(x) >= 1:
    clarr[0].append(0)
  else: return clarr

  #variables to help cluster
  alrInArray = False
  putInCluster = False

  #loop through every combination of x and y
  for i in range(0, len(x)):
    for j in range(0, len(x)):
      #skip if comparing with itself
      if i == j:
        continue
      #check to see if in same cluster or not
      if dist(x[i], x[j], y[i], y[j]) > 30:
        alrInArray = False
	#IF NOT IN SAME CLUSTER
  	#check to see if j index is already in cluster array
	for k in range(0, len(clarr)):
	  for l in range(0, len(clarr[k])):
	    #if j index is in clarr mark it as already in
	    if j == clarr[k][l]:
	      alrInArray = True
	#if j was not found in clarr then put it in right cluster
        if alrInArray == False:
	  #variable to make sure don't double put in index
	  putInCluster == False
          for m in range(0, len(clarr)):
	    for n in range(0, len(clarr[m])):
	      #if within distance with an index in a cluster put it into 
	      # that cluster
	      if (putInCluster == False) and (dist(x[j], x[clarr[m][n]], y[j], y[clarr[m][n]]) <= 30):
	        clarr[m].append(j)
		#mark as put in cluster
		putInCluster = True
	  #if j was not put into any cluster since it was too far away
	  # from all current clusters put into new cluster
	  if putInCluster == False:
	    clarr.append([j])
      #this means i and j are in the same cluster
      else:
        alrInArray = False
        #check to see which cluster i is in
	for k in range(0, len(clarr)):
	  for l in range(0, len(clarr[k])):
	    #if i is in that cluster append j to it
	    if i == clarr[k][l]:
	      #check to make sure j is not already in cluster
	      for m in range(0, len(clarr[k])):
	        if j == clarr[k][m]:
		  #if it is in already mark it as such
	          alrInArray = True
		  continue
              #if not in array already, then append it
	      if(alrInArray == False):
	        clarr[k].append(j)
	        
  return clarr

###This function takes in the indexed cluarr and uses
###it to sort the arrays into clusters
def cluster_merge(pID,px,py,pval,pavg3,pavg5,pm,eID,etime,elon,elat,epavg,epstd,eorx,eory,eorz,xID,xtime,xL1,xL2,xdrp,clu):
  pIDclu   = [];	xclu 	= [];	yclu 	 = []
  valclu   = [];	avg3clu = [];	avg5clu  = []
  pmclu    = [];	eIDclu	= [];	etimeclu = []
  elonclu  = []; 	elatclu = [];	epavgclu = []
  epstdclu = [];	eorxclu = [];	eoryclu  = []
  eorzclu  = [];	xIDclu	= [];	xtimeclu = []
  xL1clu   = [];	xL2clu	= [];	xdrpclu	 = []
  for i in range(0, len(clu)):
    pIDclu.append([])
    xclu.append([])
    yclu.append([])
    valclu.append([])
    avg3clu.append([])
    avg5clu.append([])
    pmclu.append([])
    eIDclu.append([])
    etimeclu.append([])
    elonclu.append([])
    elatclu.append([])
    epavgclu.append([])
    epstdclu.append([])
    eorxclu.append([])
    eoryclu.append([])
    eorzclu.append([])
    xIDclu.append([])
    xtimeclu.append([])
    xL1clu.append([])
    xL2clu.append([])
    xdrpclu.append([])
    for j in range(0, len(clu[i])):
      pIDclu[i].append(pID[clu[i][j]])
      xclu[i].append(px[clu[i][j]])
      yclu[i].append(py[clu[i][j]])
      valclu[i].append(pval[clu[i][j]])
      avg3clu[i].append(pavg3[clu[i][j]])
      avg5clu[i].append(pavg5[clu[i][j]])
      pmclu[i].append(pm[clu[i][j]])
      eIDclu[i].append(eID[clu[i][j]])
      etimeclu[i].append(etime[clu[i][j]])
      elonclu[i].append(elon[clu[i][j]])
      elatclu[i].append(elat[clu[i][j]])
      epavgclu[i].append(epavg[clu[i][j]])
      epstdclu[i].append(epstd[clu[i][j]])
      eorxclu[i].append(eorx[clu[i][j]])
      eoryclu[i].append(eory[clu[i][j]])
      eorzclu[i].append(eorz[clu[i][j]])
      xIDclu[i].append(xID[clu[i][j]])
      xtimeclu[i].append(xtime[clu[i][j]])
      xL1clu[i].append(xL1[clu[i][j]])
      xL2clu[i].append(xL2[clu[i][j]])
      xdrpclu[i].append(xdrp[clu[i][j]])
  return pIDclu,xclu,yclu,valclu,avg3clu,avg5clu,pmclu,eIDclu,etimeclu,elonclu,elatclu,epavgclu,epstdclu,eorxclu,eoryclu,eorzclu,xIDclu,xtimeclu,xL1clu,xL2clu,xdrpclu

###This function takes in the clustered x and y arrays
###and loops over them to find the length of each cluster
###Output is an array of int lengths
def cluster_length(xc, yc):
  clulength = []
  #select cluster
  for i in range(0, len(xc)):
    #initialize with dummy length 0
    clulength.append(0)
    #need to loop through every combination within cluster
    for j in range(0, len(xc[i])):
      for k in range(0, len(xc[i])):
        distance = dist(xc[i][j], xc[i][k], yc[i][j], yc[i][k]) 
	if distance > clulength[i]:
	  clulength[i] = distance
  return clulength

#input should be all the clustered arrays taken from cluster_merge
def cluster_lines():
  #if cluster has less than 3 pixels, probably a dud... Ignore
  
  #Loop though cluster and find highest val pixel
    #Use as the starting point for creating lines
    #If the pixel is separated by a space from the seed pixel,
    #create a line between seed_pix and cur_pix

    #Need some way to determine if lines are adjacent though because those are probably
    #not to be considered individual lines

  #Return a line count for each cluster because that will probably
  #be the thing that determines energy of the incoming particle

  return 
