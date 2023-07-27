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
def lsQcSpd(ocdev,lcdev):
    
    ocardsDev=ocdev.values()
    ocardsDev.sort()
    
    for ocard in ocardsDev:
        if(verb): print
        print ocard
        tt=ocard.split()
        stmid=tt[0]
        stmspd=tt[1]
        stmspd=float(stmspd)
        stmidNN=tt[4]

        if(verb):
            print 'DEV long ls for: ',stmid
            for card in lcdev[stmid]:
                print card
        
    return

def getSrcSumTxt(stmid,verb=0):
    
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    basin=sbtB1id2Basin[b1id]
    stmid3=stm1id.split('.')[0].upper()
    tdir="%s/%s/%s"%(sbtSrcDir,year,basin)
    mmask="%s/%s*/*-sum.txt"%(tdir,stmid3)
    mmaskBT="%s/%s*/*-sum-BT.txt"%(tdir,stmid3)
    mmaskMBT="%s/%s*/*-sum-MBT.txt"%(tdir,stmid3)
    mpaths=glob.glob(mmask)
    mpathBTs=glob.glob(mmaskBT)
    mpathMBTs=glob.glob(mmaskMBT)
    
    if(len(mpaths) == 1): mpath=mpaths[0]
    else: mpath=None

    if(len(mpathMBTs) == 1): 
        mpathBT=mpathMBTs[0]
        print 'III -- using bd2 for mpathBT: ',mpathBT
    elif(len(mpathBTs) == 1): 
        mpathBT=mpathBTs[0]
    else: 
        mpathBT=None
    
    if(verb):
        print mpath
        print mpathBT
    
    return(mpath,mpathBT)
    

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
            'bspdmax':          ['M:',30.0,'f',' stmid target'],
            'doX':              ['X',0,1,'run md2a -X'],
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
        
    # -- ls only
    
    (ocdev,lcdev)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarDev,stmidNNDev,bspdmax=bspdmax)
    (ocnon,lcnon)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarNonDev,stmidNNDev,bspdmax=bspdmax)
    (ocNN,lcNN)=sbt.chkSpdDirGaVarAllDict(sbtvarType,sbtvarNN,stmidNNDev,bspdmax=bspdmax)
    
    rc=lsQcSpd(ocdev,lcdev)
    rc=lsQcSpd(ocnon,lcnon)
    rc=lsQcSpd(ocNN,lcNN)

    MF.dTimer('ALL')



sys.exit()


