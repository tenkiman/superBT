#!/usr/bin/env python

from sBT import *

# -- get dict with sBt vars and descriptions
#
sMdesc=lsSbtVars()

#print sbtvars
#sys.exit()

#import pandas as pd
#import numpy as np

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#


class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.defaults={
            #'version':'v01',
            }

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'bspdmax':          ['m:',30.0,'f',' stmid target'],
            'doX':              ['X',0,1,'xv trkplot'],
            'doMeld':           ['M',0,1,'meld -sum.txt and-sum.txt-QC'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s -S 01w.07 -l epre3
%s -S w.07-09 -m 0701.0901 -d # get Dev 9X for july/aug '''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)

MF.sTimer('ALL')

# -- make sbt object
#
MF.sTimer('sbt')
sbt=superBT(version)
md3=Mdeck3(doBT=0,doSumOnly=1)
MF.dTimer('sbt')

# -- internal processing verb
#
overb=0
dofilt9x=0
dobt=0
    
stmids=None
ocardsAll=[]


if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+sbt.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=overb)

    ovars=['blat','blon','bvmax','btccode']

    # -- get the sBt for the stmids
    #
    sbtvarNN={}
    sbtvarDev={}
    stmidNNDev={}
    sbtvarNonDev={}
    sbtvarType={}
     
    overb=verb
    for stmid in stmids:

        (sbtType,sbtVar)=sbt.getSbtVar(stmid,doDtgKey=1,verb=overb)
        sbtvarType[stmid]=sbtType
        if(sbtType == 'NONdev'):
            sbtvarNonDev[stmid]=sbtVar
        elif(sbtType == 'DEV'):
            ss=md3.stmMetaMd3[stmid]
            rc=getStmParams(stmid)
            stmidNN="%s.%s"%(ss[-4],rc[2])
            sbtvarDev[stmid]=sbtVar
            stmidNNDev[stmid]=stmidNN
        else:
            sbtvarNN[stmid]=sbtVar
    
    nonStmids=sbtvarNonDev.keys()
    nonStmids.sort()
        
    devStmids=sbtvarDev.keys()
    devStmids.sort()
    
    NNStmids=sbtvarNN.keys()
    NNStmids.sort()
        
    nDev=len(devStmids)
    nNon=len(nonStmids)
    nNN=len(NNStmids)
    
    # -- stats
    #
    if(nNon != 0 and nNN != 0 and nDev != 0):
        rDev=nDev*1.0/float(nNon+nDev)
        rDev=rDev*100.0
        rDevN=nNN*1.0/float(nNon+nNN)
        rDevN=rDevN*100.0
        pMissN=rDevN-rDev
        print 'NNN for stmopt: ',stmopt,'nNN: ',nNN,'nDev',nDev,'nNon',nNon
        print 'DDD rFormDev: %3.0f%%  NNM rFormN: %3.0f%%  nMiss: %4.1f%%'%(rDev,rDevN,pMissN)
        print 'SSS bspdmax: %4.0f'%(bspdmax)
        
    # -- get storms with 6-h speed > bspdmax (30 kt default)
    #
    (ocdev,lcdev)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarDev,stmidNNDev,bspdmax=bspdmax)
    (ocnon,lcnon)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarNonDev,stmidNNDev,bspdmax=bspdmax)
    (ocNN,lcNN)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarNN,stmidNNDev,bspdmax=bspdmax)

    rc=qcSpd(ocdev,lcdev,bspdmax,doMeld=doMeld,doX=doX,verb=verb)
    rc=qcSpd(ocnon,lcnon,bspdmax,doMeld=doMeld,doX=doX,verb=verb)
    rc=qcSpd(ocNN,lcNN,bspdmax,doMeld=doMeld,doX=doX,verb=verb)

    MF.dTimer('ALL')



sys.exit()


