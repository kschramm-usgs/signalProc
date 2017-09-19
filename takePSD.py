#!/bin/env python

from matplotlib.mlab import psd,detrend_linear
import matplotlib.pyplot as plt
from obspy import read, Stream,UTCDateTime
import numpy as np
from scipy.signal import welch

stime=UTCDateTime('2017-213T23:35:00.0Z')
etime=UTCDateTime('2017-214T07:35:00.0Z')

#define input and output calibration data
calOutput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_10_EHZ.512.cut.seed')
calOutput=read(fileName)

calInput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_CB_BC1.512.cut.seed')
calInput=read(fileName)
statsIn = calInput[0].stats

#detrend
calInput.detrend()
calOutput.detrend()

#apply cosine taper


#calOutPSD,frqs = psd(calOutput,Fs=200,NFFT=2**18,sides='onesided',scale_by_freq=True)
calPSD,frqs = psd(calOutput,calInput,Fs=200,NFFT=2**18,sides='onesided',scale_by_freq=True)
plt.plot(frqs,calOutPSD)
plt.show()
