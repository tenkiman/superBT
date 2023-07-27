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
    
def addQCspd2sum(sumPath,spdCards,verb=0):

    qcSpd={}
    for card in spdCards:
        ndtg=6
        if(find(card,'NONdev')): ndtg=5
        tt=card.split()
        spd=tt[1].strip()
        dtg=tt[ndtg].strip()
        if(verb): print 'sss',dtg,spd
        qcSpd[dtg]=int(spd)
        
    # -- read the cards
    #
    icards=open(sumPath).readlines()
    
    # -- convert to hash
    #
    iDict=cards2dict(icards)
    
    # -- add qc speed
    #
    qcards=[]
    
    dtgs=iDict.keys()
    dtgs.sort()
    
    for dtg in dtgs:
        try:
            qs=qcSpd[dtg]
        except:
            qs=-999

        qcard="%4i %s"%(qs,iDict[dtg])
        qcard=qcard[0:-10]
        qcards.append(qcard)
        
    return(icards,qcards)

def cards2dict(icards):
    
    oDict={}
    for icard in icards:
        tt=icard.split(',')
        dtg=tt[0].strip()
        oDict[dtg]=icard
        
    return(oDict)

def qcSpd(ocdev,lcdev,bspdmax,doMeld=0,doX=0,verb=0):    

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

        (sumPath,mpathBT)=getSrcSumTxt(stmid)
        
        if(sumPath != None):
            
            qcSumPath=sumPath.replace('.txt','.txt-QC%i'%(int(bspdmax)))
            savSumPath=sumPath.replace('.txt','.txt-SAV')
            rc=getStmids4SumPath(sumPath)
            (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
            stm1id=ostm1id.lower()
            stm9xid=ostm9xid.lower()
            if(stmDev == 'nonDev'): 
                stm1id=ostm9xid.lower()
                stm9xid=ostm9xid.lower()
            elif(stmDev == 'DEV'):
                stm1id=ostm9xid.lower()
                stm9xid=ostm1id.lower()

            spdCards=lcdev[stmid]
            (icards,qcards)=addQCspd2sum(sumPath,spdCards,verb=verb)
            
            rc=WriteList(qcards,qcSumPath,verb=verb)
            if(verb):
                print 'long ls for: ',stmid
                for card in lcdev[stmid]:
                    print card
                
            dom3=0
            md3=MD3trk(icards,stm1id,stm9xid,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
            dtgs=md3.dtgs
            btrk=md3.trk
            basin=md3.basin
            
            # -- make the plot
            MF.sTimer('trkplot')
            tP=TcBtTrkPlot(stm1id,btrk,dobt=0,
                           Window=0,Bin=xgrads,
                           zoomfact=zoomfact,override=override,
                           background=background,dopbasin=0,
                           dtgopt=dtgopt,pltdir=sdir)
        
            tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg)
            MF.dTimer('trkplot')
            if(doX): tP.xvPlot(zfact=0.75)
            
            if(doMeld):
                cmd="meld %s %s"%(sumPath,qcSumPath)
                runcmd(cmd)
                
            
        else:
            print 'EEEEE---whoa---no -SUM.txt for stmid: ',stmid,'WTF?'
            sys.exit()
            
         
        if(verb):
            print 'long ls for: ',stmid
            for card in lcdev[stmid]:
                print card
                
    return
        

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

xgrads='grads'
xgrads=setXgrads(useX11=0,useStandard=0)
zoomfact=None
background='black'
dtgopt=None
ddtg=6
dtg0012=0

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

    sys.exit()


    MF.dTimer('ALL')



sys.exit()


