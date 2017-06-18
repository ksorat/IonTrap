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
IDs = ["p","Hep","Hepp","O6"]
Labs = ["H+","He+","He++","O6"]
doDelI = False #Subtract background (t=0)
doI = True

x0 = -1.0
y0 = 6.0

Nk = 250
iScl = 1.0/(4.0*np.pi)
figQ = 300
Sig = -1
TINY = 1.0e-2

imeth = 'linear'

NumS = len(IDs)
NumS = 1
for ns in range(NumS):
	
	fIn = os.path.expanduser('~') + "/Work/IonTrap/Data/KCyl/KCyl_" + IDs[ns] + ".h5"
	
	#Interpolate from simulation
	R,P,K,Tkc,I = kc.getCyl(fIn)
	if (Sig>0):
		I = kc.SmoothI(I,sig=Sig)
	Ii = kc.GetInterp(R,P,K,Tkc,I,imeth=imeth)
	kMin = K.min()
	kMax = K.max()
	
	#Have interpolant, now construct SC data
	Ksc = np.logspace(np.log10(kMin),np.log10(kMax),Nk)
	#Ksc = np.linspace(kMin,kMax,Nk)
	r0 = np.sqrt(x0**2.0+y0**2.0)
	p0 = np.arctan2(y0,x0)
	Nt = Tkc.shape[0]
	
	Isc = np.zeros((Nt,Nk))
	Isc0 = np.zeros((Nt,Nk))
	dK = np.zeros((Nt,Nk))
	dkScl = np.ones(Nk)
	iPts = np.zeros((Nk,4))
	
	for i in range(Nt):
		iPts[:,0] = r0
		iPts[:,1] = p0
		iPts[:,2] = Ksc
		iPts[:,3] = Tkc[i]
		Isc[i,:] = Ii(iPts)
	Isc = iScl*Isc
	
	Ik0 = Isc[0,:]
	Ind = Ik0<TINY
	dK0 = Ik0
	dK0[Ind] = 1.0
	dkScl[Ind] = 0.0

	for i in range(Nt):
		Isc0[i,:] = Isc[i,:] - Ik0
		dK[i,:] = dkScl*Isc[i,:]/dK0	

	#Now make figures
	vMin = 1.0e+0
	vMax = 1.0e+5

	cMap = "jet"
	vNorm = LogNorm(vmin=vMin,vmax=vMax)
	Tkc = Tkc-Tkc.min()

	#Ax = plt.gca()
	#Ax.set_axis_bgcolor('black')
	#Ax.patch.set_facecolor('black')
	if (doDelI):
		plt.pcolormesh(Tkc,Ksc,Isc0.T,norm=vNorm,cmap=cMap)
		plt.yscale('log')
		plt.ylim([50,1.0e+3])
		plt.colorbar()
		fOut = "dI_"+IDs[ns]+".png"
		print("Writing figure %s"%(fOut))
		plt.savefig(fOut,dpi=figQ)
		plt.close('all')
	if (doI):
		plt.close('all')
		plt.rc_context({'axes.edgecolor':'cyan', 'xtick.color':'cyan', 'ytick.color':'cyan', 'figure.facecolor':'cyan'})

		fig = plt.figure(0)

		fig.patch.set_facecolor('black')

		plt.pcolormesh(Tkc,Ksc,Isc.T,norm=vNorm,cmap=cMap)
		Ax = plt.gca()
		Ax.set_axis_bgcolor('black')
		plt.xlabel("Time [s]",fontsize="large")
		plt.ylabel("Energy [keV]",fontsize="large")
		plt.title("Intensity, %s"%(Labs[ns]),fontsize="large")
		plt.yscale('log')
		plt.ylim([50,1.0e+3])
		plt.xlim([Ksc.min(),Ksc.max()])
		cb = plt.colorbar()
		cb.set_label("Intensity\ns-1 cm-2 keV-1 ster-1",fontsize='large',color='cyan')
		Ax.xaxis.label.set_color('cyan')
		Ax.yaxis.label.set_color('cyan')

		#V = [1.2,2,5,10,20,50,100]
		#V = [1.5,2,4,5,6,7,8,9,10]
		#print(V)
		#CS = plt.contour(Tkc,Ksc,dK.T,V,colors='w')
		#plt.clabel(CS,inline=1,fontsize=10)
		
		fOut = "I_"+IDs[ns]+".png"
		print("Writing figure %s"%(fOut))
		plt.savefig(fOut,dpi=figQ,facecolor='black')
		plt.close('all')
