#!/bin/env python

from obspy import UTCDateTime
from obspy.core import *
from obspy import read
import glob
import numpy as np
import matplotlib.pyplot as plt
#from obspy.signal.spectral_estimation import psd
from matplotlib.mlab import psd
from scipy.signal import welch

stime=UTCDateTime('2017-213T23:35:00.0Z')
etime=UTCDateTime('2017-214T07:35:00.0Z')

#define input and output calibration data
calOutput=Stream()
fileName=('../waveformUtils/LF_MAJO_00_BHZ.512.cut.seed')
calOutput=read(fileName)

calInput=Stream()
fileName=('../waveformUtils/LF_MAJO__BC0.512.cut.seed')
calInput=read(fileName)
statsIn = calInput[0].stats

#create tapers same length as window
winlen=statsIn['npts']
print(winlen)
denom=winlen-1.
scale= 1
numtapers=12
tapers=np.array(np.empty([numtapers,winlen]))
taperSignalIn=np.array(np.empty([numtapers,winlen]))
taperSignalOut=np.array(np.empty([numtapers,winlen]))
taperVal=np.array(np.empty(winlen))
print(tapers)
print('starting loop')
for j in np.arange(0,numtapers):
   for i in np.arange(0,winlen):
#      print(i,j)
#      print(np.pi*i*(j+1)/denom)
      tapers[j,i] = scale* np.sin(np.pi*i*(j+1)/denom)
   print(np.trapz(np.abs(tapers[j])))
   taperSignalIn[j]=calInput[0].data*tapers[j]
   taperSignalOut[j]=calOutput[0].data*tapers[j]
#   plt.plot(taperSignalIn[j])
#   plt.show()

#now to take the PSD
#psdIn=np.array(np.empty([numtapers,winlen]))
psdIn=np.array(np.empty([numtapers,2**21]))
psdOut=np.array(np.empty([numtapers,2**21]))
freqs=np.array(np.empty([2**21]))
for j in np.arange(0,numtapers):
   print(j)
   #print(psd(np.array(taperSignalIn[j]),NFFT=2**20,Fs=statsIn['sampling_rate']))
   print(taperSignalIn[j].size)
   psdIn[j,:],freqs=psd(np.array(taperSignalIn[j]),NFFT=2**21,pad_to=2**21,Fs=statsIn['sampling_rate'])
   plt.semilogx(freqs,psdIn[j])
  

