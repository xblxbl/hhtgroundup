import math
import numpy
import scipy.signal.signaltools as sigtool
from cmath import phase
from numpy import unwrap
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

"""
______________________________________________________________________
______________________________________________________________________
"""

### chirp signal 

f = open('chirp.txt', 'w')
g= open('ht.txt','w')

l1=[]
l2=[]
l3=[]
l4=[]
for i in xrange(10000):
	v = i/10000.0
#	print v
	if v < 0.25:
		k=0.4*(math.sin(2*3.14*90*v))
		l1.append(k)
	elif 0.25 <= v < 0.5:
		k=0.8*(math.sin(2*3.14*90*v))
		l2.append(k)
	elif 0.5 <= v < 0.75:
		k=0.6*(math.sin(2*3.14*300*v))
		l3.append(k)
	elif 0.75 <= v < 1.0:
		k=0.9*(math.sin(2*3.14*300*v))
		l4.append(k)

#	l=math.sin(v)
#	f.write((str(v))+" "+(str(k))+" "+(str(l) + "\n"))

comb= l1+l2+l3+l4
k=[]
for i in range(len(comb)):
	i1=i/10000.
	k.append(i1)
	f.write(str(i1)+" "+(str(comb[i])+"\n"))

hsignal = sigtool.hilbert(comb)

amp = [abs(hsignal[i])for i in range(len(hsignal))]
ph  = [phase(hsignal[i])for i in range(len(hsignal))]

tm=[]
mxt=[]
mnt=[]

for i in range(1,len(ph)):
	if ph[i-1] > ph[i]:
		tm.append(i-1)
		mxt.append(ph[i-1])
		mnt.append(ph[i])

dat=open("dat.txt","w")
slp=[]

for i in range(len(tm)):
	slp.append((mxt[i]-mnt[i-1])/(tm[i]-tm[i-1]))
for i in range(len(slp)): 
	dat.write(str(slp[i])+"\n") 
uph = unwrap(ph)
freq = [(((uph[i]-uph[i-1])/(k[i]-k[i-1]))/(2*3.14)) for i in range(1,len(k))]
freq.append(0)


for i in range(len(comb)):
	g.write((str(k[i])+" "+str(ph[i])+" "+str(uph[i])+" "+str(amp[i])+" "+((str((freq[i])/(2*3.14)))+"\n")))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#plot
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plt.figure(1)

plt.subplot(321)
plt.plot(k, comb,color='r',lw=0.5)
plt.title("chirp_signal")
plt.grid(True)

plt.subplot(322, polar=True)
plt.plot(uph,amp, color='r', linewidth=0.5)
#plt.set_rmax(2.0)
plt.title("phase_space")
plt.grid(True)


plt.subplot(323)
plt.plot(k, ph,color='r',lw=0.5)
plt.title("phase")
plt.grid(True)

plt.subplot(324)
plt.plot(k, uph,color='r',lw=0.5)
plt.title("ur phase")
plt.grid(True)

plt.subplot(325)
plt.plot(k, amp,color='r',lw=0.5)
plt.title("amp")
plt.grid(True)

plt.subplot(326)
plt.plot(k, freq,color='r',lw=0.5)
plt.title("freq")
plt.grid(True)

plt.show()

