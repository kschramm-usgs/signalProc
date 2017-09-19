#!/bin/env python
import numpy as np
import matplotlib.pyplot as plt
winlen =2000.
denom=winlen-1.
scale= np.sqrt(2./denom)
print(scale)
scale= 1
numtapers=12
taper=np.array(np.empty([numtapers,winlen]))
taperVal=np.array(np.empty(winlen))
print(taper)
#taper[0][0]=3.14159
print('starting loop')
for j in np.arange(0,numtapers):
   for i in np.arange(0,winlen):
#      print(i,j)
#      print(np.pi*i*(j+1)/denom)
      taper[j,i] = scale* np.sin(np.pi*i*(j+1)/denom)
   print(np.trapz(np.abs(taper[j])))
   plt.plot(taper[j])
plt.title('Sine Tapers - no scaling')
plt.show()

