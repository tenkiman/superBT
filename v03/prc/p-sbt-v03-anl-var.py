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
            'mmddopt':          ['m:',None,'a',' mmdd opt'],
            'doLs':             ['l:',None,'a',' only list a var'],
            'dobt':             ['b',0,1,'do bt or NN only'],
            'doDev':            ['d',0,1,'do Dev 9X only'],
            'doNon':            ['n',0,1,'do NonDev 9X only'],
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
if(verb): print CL.estr

MF.sTimer('ALL')

# -- make sbt object
#

MF.sTimer('sbt')
sbt=superBT(version,verb=verb)
MF.dTimer('sbt')

# -- make xaxis (dtg) n=0,maxTimes=100
#
rc=sbt.makeSbtVarTaxis()

# -- internal processing verb
#
overb=0

dofilt9x=0
if(doDev or doNon):
    dobt=0
    dofilt9x=1
    
stmids=None
if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+sbt.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=overb)

    sbtVarAll={}
    
    nNN=0
    sbt.stmopt=stmopt

    ovars=['bvmax','bspd','br34m',
           'mvmax',
           'shrspd',
           'tpw','rh700',
           'oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3',
           'epre3','eprr3',
           'ssta']

    #ovars=['mvmax','bvmax','stmspd']
    #ovars=['bvmax','br34m']
    ovars=['oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3',
           'epre3','eprr3',
           ]

    ovars=['bvmax','bspd','br34m',
           'mvmax',
           ]
    ovars=[
           'shrspd',
           'tpw','rh700',
           'ssta']

    ovars=['bvmax','bspd','br34m',
           'mvmax','btccode',
           'shrspd',
           'tpw','rh700',
           'roci1','roci0',
           'oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3','epre3','eprr3',
           'oprc5','oprg5','opri5',
           'eprc5','eprg5','epri5','epre5','eprr5',
           'ssta']

    #ovars=['opri3','epre3','eprr3']
    

    # -- get the sBt for the stmids
    #
    sbtvarNN={}
    sbtvarDev={}
    sbtvarNonDev={}
     
    overb=verb
    for stmid in stmids:
        (sbtType,sbtVar)=sbt.getSbtVar(stmid,doDtgKey=1,verb=overb)
        #print 'sss',stmid,sbtType
        if(sbtType == 'NONdev'):
            sbtvarNonDev[stmid]=sbtVar
        elif(sbtType == 'DEV'):
            sbtvarDev[stmid]=sbtVar
        else:
            sbtvarNN[stmid]=sbtVar
            nNN=nNN+1
    
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
        
        
    # -- ls only
    
    if(doLs != None):
        ovars=doLs.split(',')
        #rc=sbt.lsGaVarAllDict(sbtvarDev,ovars,sMdesc)
        #rc=sbt.makeGaStnVar(sbtvarNN, ovars, sMdesc,verb=verb)
        rc=sbt.makeGaStnVar(sbtvarDev, ovars, sMdesc,verb=verb)
        MF.dTimer('ALL')
        sys.exit()
        
    
    tovars=[]
    for ovar in ovars:
        tovars.append("%s"%(ovar))
        
    ovars=tovars

    # -- make the grads .dat .ctl
    #
    rc=sbt.makeGaVarAllDict(sbtvarAll,ovars,verb=overb)
    print sbt.gactlPath

MF.dTimer('ALL')



sys.exit()


