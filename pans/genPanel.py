#Generates panel figure from eq-VTIs and H5p file
import numpy as np
import os
import glob
import lfmViz as lfmv
import lfmPostproc as lfmpp
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Wedge

def getFld(vtiDir,t,dt=10.0,eqStub="eqSlc"):
	tSlc = np.int(t/dt)
	vtiFile = vtiDir + "/" + eqStub + ".%04d.vti"%(tSlc)

	dBz = lfmv.getVTI_SlcSclr(vtiFile).T
	ori,dx,ex = lfmv.getVTI_Eq(vtiFile)
	xi = ori[0] + np.arange(ex[0],ex[1]+1)*dx[0]
	yi = ori[1] + np.arange(ex[2],ex[3]+1)*dx[1]

	return xi,yi,dBz

def getPs(h5pFile,t,dt=10.0,doSort=True):
	tSlc = np.int(t/dt)
	t,xeq = lfmpp.getH5pT(h5pFile,"xeq",tSlc)
	t,yeq = lfmpp.getH5pT(h5pFile,"yeq",tSlc)
	t,kev = lfmpp.getH5pT(h5pFile,"kev",tSlc)

	t,mp = lfmpp.getH5pT(h5pFile,"mp",tSlc)
	t,tl = lfmpp.getH5pT(h5pFile,"tl",tSlc)
	t,atm = lfmpp.getH5pT(h5pFile,"atm",tSlc)

	In = (atm+tl+mp) < 0.5
	xeq = xeq[In]
	yeq = yeq[In]
	kev = kev[In]
	if (doSort):
		Ind = np.argsort(kev)
		xeq = xeq[Ind]
		yeq = yeq[Ind]
		kev = kev[Ind]
	return xeq,yeq,kev

Ts = [50,100,250,500,750,1000,1250]
x0 = -1.0
y0 = 6.0
dR = 1.0

Spcs = ["H+","He+","He++","O6"]
h5pStubs = ["p","Hep","Hepp","O6"]


titS = "Injection"
dt = 10.0


figSize = (18,14)
figQ = 300 #DPI
figName = "fpPanel.png"

#Plot bounds fields/particles (nT/keV), plot details
fldBds = [-35,35]
fldCMap = "RdGy_r"
fldOpac = 0.5
fldDomX = [-15,13]
fldDomY = [-20,20]

pBds = [10,400]
pCMap = "cool"
pLab = "Energy [keV]"
pSize = 2; pMark = 'o'; pLW = 0.2

#Locations
RootDir = os.path.expanduser('~') + "/Work/IonTrap/Data"
vtiDir = RootDir + "/" + "eqSlc"

#Do figures
lfmv.initLatex()
fig = plt.figure(figsize=figSize,tight_layout=True)
#fig = plt.figure()

Ns = len(Spcs)
Nt = len(Ts)
HRs = 4*np.ones(Ns+2)
HRs[-1] = 0.1
HRs[0] = 0.25

gs = gridspec.GridSpec(Ns+2,Nt,height_ratios=list(HRs))

for t in range(Nt):
	xi,yi,dBz = getFld(vtiDir,Ts[t],dt)
	for s in range(Ns):
		gStr = RootDir + "/" + h5pStubs[s] + "/*.h5part"
		h5ps = glob.glob(gStr)
		h5pf = h5ps[0]

		Ax = fig.add_subplot(gs[s+1,t])
		if (t == 0):
			plt.ylabel(Spcs[s],fontsize="large")
		elif (t == Nt-1):
			plt.ylabel("GSM-Y [Re]")
			Ax.yaxis.tick_right()
			Ax.yaxis.set_label_position("right")
		else:
			plt.setp(Ax.get_yticklabels(),visible=False)


		if (s < Ns-1):
			plt.setp(Ax.get_xticklabels(),visible=False)
		else:
			plt.xlabel('GSM-X [Re]')
		if (s == 0):
			plt.title("T = %d [s]"%Ts[t])

		fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap,shading='gouraud',alpha=fldOpac)
		#fldPlt = Ax.pcolormesh(xi,yi,dBz,vmin=fldBds[0],vmax=fldBds[1],cmap=fldCMap)
		lfmv.addEarth2D()

		#Now do particles
		xs,ys,zs = getPs(h5pf,Ts[t],dt)
		pPlt = Ax.scatter(xs,ys,s=pSize,marker=pMark,c=zs,vmin=pBds[0],vmax=pBds[1],cmap=pCMap,linewidth=pLW)
		plt.axis('scaled')
		plt.xlim(fldDomX); plt.ylim(fldDomY)

		#Add spacecraft marker
		cSC = plt.Circle((x0, y0), dR, ec='springgreen',fill=False,linewidth=0.75)
		Ax.add_artist(cSC)

AxCbar = plt.subplot(gs[-1,:])
plt.colorbar(pPlt, cax=AxCbar,orientation='horizontal',label=pLab)
plt.suptitle(titS,fontsize="large")
		
#gs.tight_layout(fig)
plt.savefig(figName,dpi=figQ)

