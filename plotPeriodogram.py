#!/bin/env

from obspy.imaging.spectrogram import spectrogram
import matplotlib.pyplot as plt
from obspy import Stream, read
import numpy as np


#make time vector
calOutput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_10_EHZ.512.cut.seed')
calOutput=read(fileName)

calInput=Stream()
fileName=('../../java/asl_sensor_suite/data/MAJO_data/HF_MAJO_CB_BC1.512.cut.seed')
calInput=read(fileName)
t = np.arange(calOutput[0].stats.npts) / calOutput[0].stats.sampling_rate


#plot spectrogram (bottom subfigure)
calOutput[0].spectrogram(show=True)
plt.show()
