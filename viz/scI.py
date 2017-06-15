#Show spacecraft intensity for ion injection

import kCyl as kc
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import lfmViz as lfmv
import numpy


lfmv.ppInit()

BaseP = "~/Work/IonTrap/Data/KCyl/"
IDs = ["p","Hep","Hepp"]
i = 0

#x0 = -1.0
#y0 = 6.0

x0 = 0.0
y0 = 7.0

Nk = 100
iScl = 1.0/(4.0*np.pi)
fOut = "Ifig.png"
figQ = 300

Sig = -1
imeth = 'linear'

fIn = os.path.expanduser('~') + "/Work/IonTrap/Data/KCyl/KCyl_" + IDs[i] + ".h5"

#Interpolate from simulation
R,P,K,Tkc,I = kc.getCyl(fIn)
if (Sig>0):
	I = kc.SmoothI(I,sig=Sig)
Ii = kc.GetInterp(R,P,K,Tkc,I,imeth=imeth)
kMin = K.min()
kMax = K.max()

#Have interpolant, now construct SC data
Ksc = np.logspace(np.log10(kMin),np.log10(kMax),Nk)
r0 = np.sqrt(x0**2.0+y0**2.0)
p0 = np.arctan2(y0,x0)
Nt = Tkc.shape[0]

Isc = np.zeros((Nt,Nk))
iPts = np.zeros((Nk,4))

for i in range(Nt):
	iPts[:,0] = r0
	iPts[:,1] = p0
	iPts[:,2] = Ksc
	iPts[:,3] = Tkc[i]
	Isc[i,:] = Ii(iPts)

#Now make figure
vMin = 1.0
vMax = 1.0e+6
cMap = "jet"
vNorm = LogNorm(vmin=vMin,vmax=vMax)

plt.pcolormesh(Tkc,Ksc,iScl*Isc.T,norm=vNorm,cmap=cMap)
plt.yscale('log')
plt.ylim([50,1.0e+3])
plt.colorbar()

plt.savefig(fOut,dpi=figQ)