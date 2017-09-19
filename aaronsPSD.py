import obspy.core as obspy
import obspy.core.utcdatetime as date
import obspy.signal.freqattributes as ffts
import obspy.io.xseed
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

out_stream = obspy.read('/TEST_ARCHIVE/XX_TST6/2016/2016_196/00_BH0.512.seed')
print out_stream
out_trace = out_stream[0]
nyq = out_trace.stats['sampling_rate'] / 2
cal_stream = obspy.read('/TEST_ARCHIVE/XX_TST6/2016/2016_196/00_BH0.512.seed')
print cal_stream
cal_trace = cal_stream[0]

start = date.UTCDateTime(year=2017, julday=213, hour=18, minute=20)
end = date.UTCDateTime(year=2017, julday=213, hour=18, minute=35)

out_trace.trim(starttime=start, endtime=end)
cal_trace.trim(starttime=start, endtime=end)

out = out_trace.data
cal = cal_trace.data

print(out_trace.stats['npts'])
station = cal_trace.stats['station']
print(station)
print(out.size, cal.size)

pad = 1
#while pad < out.size:
#        pad *= 2
#
#using this instead of Aaron's method which throws an error.
nsegments=4.
pad=np.power(2,int(np.ceil(np.log2(out.size/nsegments))))
nfft=int(pad)
overlap=int(3*nfft//4)


numer, freqs1 = mlab.csd(out, cal, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap)
denom, freqs2 = mlab.psd(cal, sides='onesided', pad_to=pad, NFFT=nfft, noverlap=overlap)
# aaron's
#denom, freqs2 = mlab.psd(cal, sides='onesided', pad_to=pad, NFFT=pad/4, noverlap=3*pad/16)

freqs = freqs1 * nyq
resp = numer/denom
resp *= 2*np.pi*freqs*1j

plt.semilogx( freqs, 10. * np.log10( np.absolute(resp) ) )
plt.show()

