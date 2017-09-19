import matplotlib.pyplot as plt
import numpy as np

def readAline(data):
   outputData=(np.fromstring(data,sep=','))
   return outputData

def readAcomplexline(data):
   #data.rstrip(']')
   #data.lstrip('[')
   c_strs = data.split(',')
   tmpData=map(lambda x:x.replace(" ",""),c_strs)
   outputData=[]
   for value in tmpData:
      print(value)
      outputData.append(complex(value))
      
   outputArray=np.array(outputData)   
   
   return outputArray

def toComplex(field):
   return complex(field.replace(' ',''))

timeseries=[]
detrend=[]
demean=[]
taper=[]
fft=[]
psd=[]
#fileName = 'JAVAresults/test_Complex.txt'
fileName = 'JAVAresults/XX_KAS_BH_00-psdSteps_1.txt'
with open(fileName,'r') as f:
   mydat = f.read()
   mydat = mydat.replace("[","")
   mydat = mydat.replace("]","")
   lines = mydat.split('\n')
   timeseries=readAline(lines[8])
   detrend=readAline(lines[9])
   demean=readAline(lines[11])
   taper=readAline(lines[13])

   print('here')
   #fft=readAcomplexline(fileName)
   fft=readAcomplexline(lines[16])
   print('here2')

   plt.semilogx(10*np.log10(abs(fft)))
   plt.show()

   psd=readAline(lines[17])
   print('here4')
