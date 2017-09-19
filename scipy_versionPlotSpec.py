#!/bin/env

#from obspy.imaging.spectrogram import spectrogram
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from obspy import Stream, read
import numpy as np

fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.75, 0.7, 0.2]) #[left bottom width height]
ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.60], sharex=ax1)
ax3 = fig.add_axes([0.83, 0.1, 0.03, 0.6])

#make time vector
calOutput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_10_EHZ.512.cut.seed')
calOutput=read(fileName)

calInput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_CB_BC1.512.cut.seed')
calInput=read(fileName)
t = np.arange(calOutput[0].stats.npts) / calOutput[0].stats.sampling_rate

#plot waveform (top subfigure)    
ax1.plot(t, calOutput[0].data, 'k')

#plot spectrogram (bottom subfigure)
calOutput = calOutput[0]
f,t,Sxx = spectrogram(calOutput.data,200)
ax2.pcolormesh(t, f, Sxx)
mappable = ax2.images[0]
plt.colorbar(mappable=mappable, cax=ax3)
plt.show()
