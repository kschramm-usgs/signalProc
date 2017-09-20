#!/bin/env python

from obspy.core.utcdatetime import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import obspy

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

# create a plot flag
plotFlag=True

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
file='JAVAresults/XX_KAS_00_BHZ-psdSteps_1.txt'
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
   rawData=readAline(lines[8])
   detrendData=readAline(lines[9])
   demeanData=readAline(lines[11])
   taperedData=readAline(lines[13])
   fftData=readAcomplexline(lines[16])
   PSDData=readAline(lines[17])
# look at the raw data
   print(len(rawData))
   print(len(trimmedSeed))
   #for i in range(len(rawData)):
   #    resid.append(rawData[i] - trimmedSeed[i])
   if(plotFlag):
   #    plt.subplot(2,1,1)
       plt.plot(trimmedSeed,'r',label='raw from seed plotted in python')
       plt.plot(rawData,'k',label='raw from test suite')
       #plt.xlim(0,100)
       plt.legend()
   #    plt.subplot(2,1,2)
   #    plt.plot(resid,'b',label='residual')
   #    plt.title('Residual')
   #    plt.ylim(-.0005, 0.0005)
       plt.show()
# now look at the detrended data
   resid[:]=[]
   trimmedSeed.detrend('linear')
   for i in range(trimmedSeed.stats['npts']):
       resid.append(detrendData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(2,1,1)
       plt.plot(detrendData,'k',label='detrend from test suite')
       plt.plot(trimmedSeed,'r',label='detrend (linear) in python')
       plt.title('detrended data')
       plt.legend()
       plt.subplot(2,1,2)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.show()
# now look at the demeaned data
   resid[:]=[]
   trimmedSeed.detrend('constant')
   for i in range(trimmedSeed.stats['npts']):
       resid.append(demeanData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(2,1,1)
       plt.plot(demeanData,'k',label='demean from test suite')
       plt.plot(trimmedSeed,'r',label= 'demean (detrend constant) in python')
       plt.title('demeaned Data')
       plt.legend()
       plt.subplot(2,1,2)
       plt.plot(resid,'b',label='residual')
       plt.title('Residual')
       plt.show()
# now look at the tapered data
   resid[:]=[]
   print(taperedData[-1])
   trimmedSeed.taper(0.05,type='cosine')
   for i in range(trimmedSeed.stats['npts']):
       resid.append(demeanData[i] - trimmedSeed[i])
   if(plotFlag):
       plt.subplot(2,1,1)
       plt.plot(taperedData,'k',label='taper from test suite')
       plt.plot(trimmedSeed,'r',label= 'tapered in python')
       plt.title('tapered Data')
       plt.legend()
       plt.subplot(2,1,2)
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
   pad=np.power(2,int(np.ceil(np.log2(trimmedSeed.stats['npts']))))
   print(pad)
   fftSeed = np.fft.fft(trimmedSeed,n=pad)
   fftSeedFreq=np.fft.fftfreq(pad)
   print(min(fftSeed))
   if(plotFlag):
       plt.semilogx(10*np.log10(fftData),'k',label='fft from test suite')
       plt.semilogx(10*np.log10(fftSeed),'r',label= 'fft in python')
       plt.legend()
       plt.title('by index')
       plt.show()
# now look at the PSD data
   PSDSeed = (fftSeed*np.conj(fftSeed))
   if(plotFlag):
       plt.loglog(PSDData,'k',label='PSD from test suite')
       plt.loglog(PSDSeed,'r',label= 'PSD in python')
       plt.title('PSD of FFT')
       plt.legend()
       plt.show()
# then we need to add the PSDSeed results for each of the files up and average them



#nsegments=4.
#pad=np.power(2,int(np.ceil(np.log2(out.size/nsegments))))
##nfft=pad/4
#nfft=int(pad)
#overlap=int(3*nfft//4)
#print(pad, nfft,overlap)


