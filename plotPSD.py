#!/bin/env python

import obspy.core as obspy
import obspy.core.utcdatetime as date
import obspy.signal.freqattributes as ffts
#import obspy.io.xseed
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import csd
import matplotlib.mlab as mlab
from obspy.signal.filter import lowpass
from obspy.signal.filter import highpass
from obspy.signal import xcorr
from obspy.signal.calibration import spectral_helper
import obspy

def rms(x):
   return np.sqrt(np.mean(np.power(x,2)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#out_stream1 = obspy.read('/home/kschramm/java/asl_sensor_suite/data/MAJO_data/HF_MAJO_10_EHZ.512.cut.seed')
#out_stream1 = obspy.read('/home/kschramm/python/waveformUtils/WN_EYMN_EHZ.512.cut.seed')
#out_stream2 = obspy.read('/home/kschramm/python/waveformUtils/TG_EYMN_EHZ.512.cut.seed')
#out_stream2 = obspy.read('/tr1/tel*/XX_TPNV/2017/*242/00_EHZ.512.seed')
out_stream1 = obspy.read('/TEST_ARCHIVE/XX_TST6/2016/2016_196/00_BH0.512.seed')
out_trace1 = out_stream1[0]
#out_trace2 = out_stream2[0]
#print(out_trace1.stats['npts'], out_trace2.stats['npts'])
nyq = out_trace1.stats['sampling_rate'] / 2
smpr=out_trace1.stats['sampling_rate']
#cal_stream1 = obspy.read('/home/kschramm/java/asl_sensor_suite/data/MAJO_data/HF_MAJO_CB_BC1.512.cut.seed')
#cal_stream1 = obspy.read('/home/kschramm/python/waveformUtils/WN_EYMN_BC1.512.cut.seed')
#cal_stream2 = obspy.read('/home/kschramm/python/waveformUtils/TG_EYMN_BC1.512.cut.seed')
#cal_stream1 = obspy.read('/msd/IU_MAJO/2017/213/CB_BC1.512.seed')
#cal_stream2 = obspy.read('/tr1/tel*/XX_TPNV/2017/*242/CB_BC0.512.seed')
#cal_stream = obspy.read('/msd/XX_GSN1/2017/236/CB_BC0.512.seed')
cal_stream1 = obspy.read('/TEST_ARCHIVE/XX_TST6/2016/2016_196/00_BH0.512.seed')
cal_trace1 = cal_stream1[0]
#cal_trace2 = cal_stream2[0]

#calculate the cross-correlations
x = out_stream1[0]
y = cal_stream1[0]
index,value,fct = xcorr(x,y,100,full_xcorr=True)
print('xcorr of cal input')
print(index)
print(value)
x = out_stream1[0]
y = cal_stream1[0]
index,value,fct = xcorr(x,y,100,full_xcorr=True)
print('xcorr of cal output')
print(index)
print(value)

#start = date.UTCDateTime(year=2017, julday=213, hour=18, minute=20)
#end = date.UTCDateTime(  year=2017, julday=213, hour=18, minute=35)
#start = date.UTCDateTime(year=2017, julday=242, hour=13, minute=38)
#end = date.UTCDateTime(  year=2017, julday=242, hour=13, minute=53)
#start = date.UTCDateTime(year=2017, julday=236, hour=16, minute=35)
#end = date.UTCDateTime(  year=2017, julday=236, hour=16, minute=45)

##out_trace1.trim(starttime=start, endtime=end)
##cal_trace1.trim(starttime=start, endtime=end)
#out_trace2.trim(starttime=start, endtime=end)
#cal_trace2.trim(starttime=start, endtime=end)
#
#changetr1=cal_trace1.copy()
#changetr1.data=cal_trace2.data
#cal_trace1=changetr1

#cal_stream1.spectrogram(log=True, title="Cal Input"+ cal_stream1[0].stats['station'])
#out_stream1.spectrogram(log=True, title="Cal Output"+out_stream1[0].stats['station'])
#cal_stream2.spectrogram(log=True, title="Cal Input"+ cal_stream2[0].stats['station'])
#out_stream2.spectrogram(log=True, title="Cal Output"+out_stream2[0].stats['station'])

# what happens if we filter:
print('demean the data')
cal_trace1.detrend('demean')
out_trace1.detrend('demean')
#cal_trace2.detrend('demean')
#out_trace2.detrend('demean')
#cal_trace.filter('lowpass',freq=10.,corners=4,zerophase=True)
#out_trace.filter('lowpass',freq=10.,corners=4,zerophase=True)

out = out_trace1.data
cal = cal_trace1.data
print(out_trace1.stats['npts'])
station = cal_trace1.stats['station']
print(out.size, cal.size)


# read in output from test suite code
freqTS=[]
rawPSD=[]
corPSD=[]
file='PSD_OF_TST6.00_BH0.512.seed.txt'
with open(file,'r') as f:
   #data=f.readline()
   mydat=f.read()
   lines=mydat.split('\n')
   for ln in lines:
       lv=ln.split(',')
# break up data into arrays
       freqTS.append(lv[0])
       # raw is off in amplitude...
       rawPSD.append(lv[1])
       corPSD.append(lv[2])

#pad = 1
#while pad < out.size:
#    pad *= 2
#pad=np.ceil(np.log2(out.size))
#nfft=pad/4
#print(pad, nfft,overlap)
#print(nfft/overlap)
#numer, freqs1 = mlab.csd(out, cal, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap, scale_by_freq=False)

nsegments=4.
pad=np.power(2,int(np.ceil(np.log2(out.size/nsegments))))
nfft=int(pad)
overlap=int(3*nfft//4)
scalg = 'density'
freqs1,numer = csd(out, cal, fs=smpr, nfft=nfft, nperseg=pad, return_onesided=True, noverlap=overlap,scaling=scalg)
scalg1 = 'spectrum'
freqs1,numer1 = csd(out, cal, fs=smpr, nfft=nfft, nperseg=pad, return_onesided=True, noverlap=overlap,scaling=scalg)
#numer, freqs1 = mlab.psd(out, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap, scale_by_freq=True)
#denom, freqs2 = mlab.psd(cal, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap, scale_by_freq=True)

smoothness = rms(np.diff(np.abs(numer)))
print(smoothness)

#freqs = freqs1 * nyq
plt.loglog( freqs1, np.abs(numer),label='Python cpsd, scaling='+scalg)
plt.loglog( freqs1, np.abs(numer1),label='Python cpsd, scaling='+scalg1)
plt.loglog( freqTS, rawPSD, label='Test suite psd')
plt.legend()
plt.title('cross psd')
plt.show()

#residual = np.abs(numer-rawPSD)
dBs = 20*np.log10(numer/rawPSD)
plt.plot(freqTS, dBs)
plt.show()


#x2=spectral_helper(out, cal)
#print(x2)
#calc smoothinjg
##plt.semilogx( freqs, 10. * np.log10( np.absolute(resp) ) )
#plt.title('nsegments: '+str(nsegments)+", smoothness: "+str(smoothness)+"at station "+station)
#plt.grid()
#plt.show()
#resp = numer/denom
# acceleration
#resp *= 2*np.pi*freqs*1j

#plt.subplot(2,1,1)
#plt.title('numerator = cross-psd')
#plt.loglog( freqs, numer)
#plt.subplot(2,1,2)
