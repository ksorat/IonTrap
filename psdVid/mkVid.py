import sys
import os
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv

Quiet = True

Base = os.path.expanduser('~') + "/Work/IonTrap/Data/"
fPSD = Base + "KCyl/KCyl_p.xmf"
fEq  = Base + "eqSlc/eqSlc.*.vti database"
cMapI = "viridis"
cMapF = "RdGy"

kSlc = 200
titS = "%d keV Intensity"%(kSlc)
Ibds = [1.0,1.0e+5]
iMin = 5000.0

fbds = [-35,35]
Nc = 11

#Legends
plXs = [0.03]
plYs = [0.9,0.4]
plTits = ["Intensity\ns-1 cm-2 keV-1","Residual Bz [nT]"]


if (Quiet):
	LaunchNowin()
else:
	Launch()

#Do some defaults
pyv.lfmExprs()

#Open databases
OpenDatabase(fPSD)
OpenDatabase(fEq)

md0 = GetMetaData(fPSD)
dt = md0.times[1] - md0.times[0]
T0 = md0.times[0]# - md0.times[0] #Reset to zero

#Create correlation
CreateDatabaseCorrelation("ifCor",[fPSD,fEq],0)




#Create intensity pcolor
pyv.lfmPCol(fPSD,"f",cMap=cMapI,vBds=Ibds,Log=True)
AddOperator("Slice")
sOp = GetOperatorOptions(0)
sOp.originType = 1
sOp.originIntercept = np.log10(kSlc)
SetOperatorOptions(sOp)
pyv.addThreshold("f",iMin,1.0e+8,opNum=1)

#Create field contours
#plotContour(db, var, cmap=None, multicolors=None, color=(255,255,255,255), Legend=True, lineWidth=1, lineStyle='solid', values=None, Nlevels=5, vBds=None, Log=False):
pyv.plotContour(fEq,"dBz",cmap=cMapF,vBds=fbds,Nlevels=Nc,lineWidth=0)
cOp = GetPlotOptions()
print(cOp)

#Set background and such
pyv.setAtts()
anAt = AnnotationAttributes()
anAt.backgroundColor = (0,0,0,0)
anAt.foregroundColor = (0, 204, 255, 255)
#anAt.axes2D.xAxis.grid = 1
#anAt.axes2D.yAxis.grid = 1

anAt.userInfoFlag = 0
anAt.databaseInfoFlag = 0
anAt.timeInfoFlag = 0
anAt.axes2D.xAxis.title.userTitle = 1
anAt.axes2D.yAxis.title.userTitle = 1
anAt.axes2D.xAxis.title.title = "X [Re]"
anAt.axes2D.yAxis.title.title = "Y [Re]"
SetAnnotationAttributes(anAt)

tit = pyv.genTit( titS=titS,Pos=(0.45,0.955),height=0.02)
pyv.cleanLegends(plXs,plYs,plTits)

#Let's see what we got
DrawPlots()

#Do time loop
pyv.doTimeLoop(T0=T0,dt=dt,Save=True,tLabPos=(0.3,0.05),Trim=True)

outVid = Stubs[n] + ".mp4"
pyv.makeVid(Clean=True,outVid=outVid,tScl=1)

DeleteAllPlots()
CloseDatabase(dbs[0])
CloseDatabase(dbs[1])




