import sys
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv

ebscl = pyv.EBscl
MagM = -0.311*1.0e+5 #Mag moment, Gauss->nT
G2nT = 10**5.0 #Convert Gauss to nT
eb2nT = G2nT/ebscl
fData = "lorez.vti"
doQuiet = False

DefineScalarExpression("RadAll","polar_radius(mesh)")
DefineScalarExpression("Radius","if( ge(RadAll, 2.1), RadAll, 2.1)") #Respect cutout
DefineScalarExpression("rm5","Radius^(-5.0)")

#Residual field
DefineScalarExpression("dBx","(%e)*B[0]"%(eb2nT))
DefineScalarExpression("dBy","(%e)*B[1]"%(eb2nT))
DefineScalarExpression("dBz","(%e)*B[2]"%(eb2nT))

#Grid
DefineScalarExpression("xRe","coord(mesh)[0]")
DefineScalarExpression("yRe","coord(mesh)[1]")
DefineScalarExpression("zRe","coord(mesh)[2]")

DefineScalarExpression("eBx","3*xRe*zRe*(%e)*rm5"%(MagM))
DefineScalarExpression("eBy","3*yRe*zRe*(%e)*rm5"%(MagM))
DefineScalarExpression("eBz","(3.0*zRe*zRe - Radius*Radius)*(%e)*rm5"%(MagM))

#Total field components and vector
DefineScalarExpression("Bx","eBx+dBx")
DefineScalarExpression("By","eBy+dBy")
DefineScalarExpression("Bz","eBz+dBz")

#Launch viewer
if (doQuiet):
	LaunchNowin()
else:
	Launch()

#Open database
OpenDatabase(fData)
md0 = GetMetaData(fData)


