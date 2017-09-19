#!/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from obspy.mseed.util import shift_time_of_file
from obspy import Stream, Trace, UTCDateTime

dt = np.pi / 100.
fs = 1. / dt
print('sampling frequency = '+str(fs))
nsamp=(280.*60.*60.)*dt
t = np.arange(0, nsamp-1, dt)
y = 10. * np.sin(2 * np.pi * 4 * t) + 5. * np.sin(2 * np.pi * 4.25 * t)
#y = y + np.random.randn(*t.shape)

nfft=np.int(np.power(2,np.ceil(np.log2(len(y)))))

fig=plt.figure()
plt.subplot(411)
plt.psd(y,NFFT=nfft, pad_to=nfft, Fs=fs)
plt.title("Whole signal")

nfft=np.int(np.power(2,np.ceil(np.log2(len(y)/8.))))

# Pad to is the number of data points to pad the segment to
# You want to pad each segment with 0's not the whole data set
plt.subplot(412)
plt.psd(y,NFFT=nfft, pad_to=nfft, Fs=fs)
plt.title("4 Blocks no overlap")

plt.subplot(413)
plt.psd(y,NFFT=nfft, pad_to=nfft, Fs=fs,noverlap=nfft//2)
plt.title("4 blocks 50% overlap")

plt.subplot(414)
plt.psd(y,NFFT=nfft, pad_to=nfft, Fs=fs,noverlap=nfft//2,detrend='mean')
plt.title("demean")
plt.show()


tr=Trace()
tr.stats.station='KAS'
tr.stats.network='XX'
tr.stats.channel='00'
tr.stats.location='BHZ'
tr.data=y
tr.stats.sampling_rate=40.
tr.starttime=UTCDateTime('2017-09-19T00:00:00')
print(tr.stats['starttime'])
print(tr.stats['endtime'])
st=Stream()
st+=tr
st.write('XX_KAS.00_BHZ.seed', format='MSEED')
#shift_time_of_file(fileIn, fileOut, 10000)
#

