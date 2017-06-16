#Generate XMLs for PSD calculation


import xml.etree.ElementTree as et
import xml.dom.minidom

import numpy as np
import os


BaseP = "~/Work/IonTrap/Data/"
IDs = ["p","Hep","Hepp"]
#IDs = ["p"]

#Uniform parameters
T0 = 3235.85
Tf = 4500.0
dt = 10.0

Rin = 2
Rout = 20
Nth = 8
Nr = 18
Np = 96
Nk = 50
kMin = 1.0
kMax = 1250.0
Na = 10

NumPSD = len(IDs)

#Create masks
MaskP = []
for i in range(NumPSD):
	mStr = IDs[i] + "/*.h5part"
	MaskP.append(mStr)


NumPop = len(MaskP)

for i in range(NumPSD):

	#Create XML
	iDeck = et.Element('Params')

	#Particle/population details
	pInfo = et.SubElement(iDeck,"particles")
	pInfo.set("species","")
	pInfo.set("equatorial","T")

	#Only one population per
	pID = "population"+str(1)
	popInfo = et.SubElement(pInfo,pID)
	popInfo.set("files",BaseP+MaskP[i])
	popInfo.set("weighting","ionMax")

	#Timing data
	tInfo = et.SubElement(iDeck,"timing")
	tInfo.set("weighting",str(T0))
	cStr = "%s:%s:%s"%(str(T0),str(dt),str(Tf))
	tInfo.set("calculation",cStr)

	#Options
	oInfo = et.SubElement(iDeck,"options")
	oInfo.set("relativistic","T")
	oInfo.set("doFlux","T")
	oInfo.set("background","T")
	oInfo.set("f0","ionMax")
	
	#Phasespace
	psInfo = et.SubElement(iDeck,"phasespace")
	psR = et.SubElement(psInfo,"r")
	psR.set("N",str(Nr))
	psR.set("min",str(Rin))
	psR.set("max",str(Rout))
	psT = et.SubElement(psInfo,"theta")
	psT.set("N","1")
	psP = et.SubElement(psInfo,"phi")
	psP.set("N",str(Np))
	psK = et.SubElement(psInfo,"k")
	psK.set("N",str(Nk))
	psK.set("min",str(kMin))
	psK.set("max",str(kMax))
	psK.set("log","T")
	psA = et.SubElement(psInfo,"alpha")
	psA.set("N",str(Na))
	psS = et.SubElement(psInfo,"psi")
	psS.set("N","1")

	#Output
	ioInfo = et.SubElement(iDeck,"output")
	ioInfo.set("base",IDs[i])
	ioInfo.set("fullevery","0")
	slc = et.SubElement(ioInfo,"slice3D1")
	slc.set("dim1","r")
	slc.set("dim2","phi")
	slc.set("dim3","k")
	slcT = et.SubElement(slc,"theta")
	slcT.set("ignore","T")

	#Write out
	fOut = IDs[i]+".xml"
	#Finished creating XML tree, now write
	xmlStr = xml.dom.minidom.parseString(et.tostring(iDeck)).toprettyxml(indent="    ")
	with open(fOut,"w") as f:
		f.write(xmlStr)


#Generate runner
RunF = "RunPSD.sh"
with open(RunF,"w") as fID:
	fID.write("#!/bin/bash")
	fID.write("\n\n")
	fID.write("export OMP_NUM_THREADS=%d\n"%Nth)
	for i in range(NumPSD):
		IDi = IDs[i]
		ComS = "psd.x %s.xml\n"%IDi
		fID.write(ComS)
		ComS = "mv %s_r_phi_k_Slice3D#1.h5 KCyl_%s.h5\n"%(IDi,IDi)
		fID.write(ComS)
