#!/bin/env python

from obspy.core.utcdatetime import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import csd
import matplotlib.mlab as mlab
import obspy

'''
   script for plotting up output from sensor test suite and comparing 
   the results to those produce in python in order to verify that the
   code is working as expected.

   Kimberly Schramm, ASL/KBRWyle
'''

def rms(x):
   return np.sqrt(np.mean(np.power(x,2)))

def readAline(data):
   outputData=(np.fromstring(data,sep=','))
   return outputData

def readAcomplexline(data):
   data.rstrip(']')
   data.lstrip('[')
   c_strs = data.split(',')
   tmpData=map(lambda x:x.replace(" ",""),c_strs)
   outputData=[]
   for value in tmpData:
      outputData.append(complex(value))
   outputArray=np.array(outputData)   
   
   return outputArray

def toComplex(field):
   return complex(field.replace(' ',''))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# create a plot flag
plotFlag=False

# read in some data
#out_stream1 = obspy.read('/TEST_ARCHIVE/XX_TST6/2016/2016_196/00_BH0.512.seed')
#out_stream1 = obspy.read('/TEST_ARCHIVE/XX_TST5/2016/2016_196/00_BH0.512.seed')
out_stream1 = obspy.read('XX_KAS.00_BHZ.seed')
full_trace = out_stream1[0]
out_trace1=full_trace.copy()

#stime=UTCDateTime('2016-07-14T00:59:59.994501Z')
##stime=UTCDateTime('2016-07-14T01:00:00.0250Z')
#etime = UTCDateTime('2016-07-14T02:29:59.994500Z')
#etime = UTCDateTime('2016-07-14T02:29:59.969500Z')
stime=UTCDateTime('1970-01-01T00:00:00.000000Z')
# etime for trimming needs to be window length
etime = UTCDateTime('1970-01-01T01:29:59.72500Z')

out_trace1.trim(starttime=stime,endtime=etime)
trimmedSeed=out_trace1.copy()
print(trimmedSeed.stats)
trimmedSeed.trim(starttime=stime,endtime=etime)
nyq = out_trace1.stats['sampling_rate'] / 2


# read in output from test suite code
rawData=[]
detrendData=[]
demeanData=[]
taperedData=[]
fftData=[]
PSDData=[]
numHeaderLines=7
resid=[]
#file='JAVAresults/XX_TST5_00_BH0-psdSteps_1.txt'
file='JAVAresults/XX_KAS_00_BHZ-psdSteps_13.txt'
#file='JAVAresults/tmp1.txt'
with open(file,'r') as f:
   mydat = f.read()
   mydat = mydat.replace("[","")
   mydat = mydat.replace("]","")
   lines = mydat.split('\n')
   print(len(lines))
   for i in range(numHeaderLines):
      header = lines[i]
      print(header)
# line numbers are off by one from vi because start at zero in python
   rawData=readAline(lines[8])
   detrendData=readAline(lines[10])
   demeanData=readAline(lines[12])
   taperedData=readAline(lines[14])
   fftData=readAcomplexline(lines[16])
   PSDData=readAline(lines[18])
# look at the raw data
   for i in range(len(rawData)):
       resid.append(rawData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(3,1,1)
       plt.plot(rawData,'k',label='raw from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label='raw from seed plotted in python')
       plt.xlim(0,100)
       plt.title('First 100 samples')
       plt.legend()
       plt.subplot(3,1,2)
       plt.plot(rawData,'k',label='raw from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label='raw from seed plotted in python')
       plt.xlim((len(trimmedSeed)-100),len(trimmedSeed))
       plt.title('Last 100 samples')
       plt.legend()
       plt.subplot(3,1,3)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.ylim(-.0005, 0.0005)
       plt.show()
# now look at the detrended data
   resid[:]=[]
   trimmedSeed.detrend('linear')
   print(len(detrendData))
   print(len(trimmedSeed))
   for i in range(trimmedSeed.stats['npts']):
       resid.append(detrendData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(3,1,1)
       plt.plot(detrendData,'k',label='detrend from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label='detrend (linear) in python')
       plt.title('detrended data, first 100 samples')
       plt.xlim(0,100)
       plt.legend()
       plt.subplot(3,1,2)
       plt.plot(detrendData,'k',label='detrend from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label='detrend (linear) in python')
       plt.title('detrended data, last 100 samples')
       plt.xlim((len(trimmedSeed)-100),len(trimmedSeed))
       plt.legend()
       plt.subplot(3,1,3)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.show()
# now look at the demeaned data
   resid[:]=[]
   trimmedSeed.detrend('constant')
   for i in range(trimmedSeed.stats['npts']):
       resid.append(demeanData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(3,1,1)
       plt.plot(demeanData,'k',label='demean from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label= 'demean (detrend constant) in python')
       plt.title('demeaned Data, first 100 samples')
       plt.xlim(0,100)
       plt.legend()
       plt.subplot(3,1,2)
       plt.plot(demeanData,'k',label='demean from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label= 'demean (detrend constant) in python')
       plt.title('demeaned Data, last 100 samples')
       plt.xlim((len(trimmedSeed)-100),len(trimmedSeed))
       plt.legend()
       plt.subplot(3,1,3)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.show()
# now look at the tapered data
   resid[:]=[]
   print(taperedData[-1])
   trimmedSeed.taper(0.1,type='cosine')
   for i in range(trimmedSeed.stats['npts']):
       resid.append(demeanData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(3,1,1)
       plt.plot(taperedData,'k',label='taper from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label= 'tapered in python')
       plt.title('tapered Data')
       plt.xlim(0,2000)
       plt.legend()
       plt.subplot(3,1,2)
       plt.plot(taperedData,'k',label='taper from test suite'
               ,linewidth=3.0)
       plt.plot(trimmedSeed,'r',label= 'tapered in python')
       plt.title('tapered Data')
       plt.xlim((len(trimmedSeed)-2000),len(trimmedSeed))
       plt.legend()
       plt.subplot(3,1,3)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.show()
# now look at the fft data
   print(fftData[0])
   print(fftData[-1])
# reset plot flag
   plotFlag=True
# calculate frequencies
   sampRate = 40.
   ivl = 1/sampRate
   deltaFreq = 1.52587890625E-4
   TSFreq = np.arange(0,len(fftData))*deltaFreq
   print(len(fftData))
# take fft of seed data read into python   
   pad=np.power(2,int(np.ceil(np.log2(trimmedSeed.stats['npts']))))
   print(pad)
   fftSeed = np.fft.fft(trimmedSeed,n=pad)
   fftSeedFreq=np.fft.fftfreq(pad,d=ivl)
   realSQ=np.real(fftData)**2.
   imagSQ=np.imag(fftData)**2.
   fftMag=np.sqrt(realSQ+imagSQ)
   pblm=len([tmp for tmp in fftData if tmp < 0])
   print('problem:'+ str(fftData[pblm]))
   print(min(fftSeed))
   if(plotFlag):
       plt.loglog(TSFreq,np.abs(fftData),'k',label='fft from test suite'
               ,linewidth=3.0)
       #plt.loglog(TSFreq,(fftMag),'k',label='fft from test suite'
       #        ,linewidth=3.0)
       plt.loglog(fftSeedFreq,np.abs(fftSeed),'r',label= 'fft in python')
       plt.legend()
       plt.grid(True,which='both',ls=':')
       plt.title('by frequency')
       plt.show()
# now look at the PSD data
   PSDSeed = (fftSeed*np.conj(fftSeed))
   nsegments=4.
   pad=np.power(2,int(np.ceil(np.log2(fftSeed.size/nsegments))))
   nfft=int(pad)
   overlap=int(3*nfft//4)
   scalg = 'density'
   #numer, freqs2 = mlab.psd(fftSeed, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap, scale_by_freq=True)
   if(plotFlag):
       plt.loglog(PSDData,'k',label='PSD from test suite'
               ,linewidth=3.0)
       plt.loglog(PSDSeed,'r',label= 'PSD in python')
       #plt.loglog(numer,'r',label= 'PSD in python')
       plt.title('PSD of FFT')
       plt.legend()
       plt.grid(True,which='both',ls=':')
       plt.show()
# then we need to add the PSDSeed results for each of the files up and average them



#nsegments=4.
#pad=np.power(2,int(np.ceil(np.log2(out.size/nsegments))))
##nfft=pad/4
#nfft=int(pad)
#overlap=int(3*nfft//4)
#print(pad, nfft,overlap)


