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
            'lsVars':           ['L',0,1,' just list norun is norun'],
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

# -- get meta data
#
lsverb=0
if(lsVars): lsverb=1

sMdesc=lsSbtVars(verb=lsverb)
mD3desc=lsMd3Vars(verb=lsverb)
mD3sum=lsMd3SumVars(verb=lsverb)

if(lsVars):  sys.exit()


MF.sTimer('ALL')

# -- make sbt object
#
version=sbtVersion
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
           'tpw','rh70',
           'roci1','roci0',
           'oc3','og3','oi3',
           'ec3','eg3','ei3','e3','re3',
           'oc5','og5','oi5',
           'ec5','eg5','ei5','e5','re5',
           'ssta']

    #ovars=['opri3','epre3','eprr3']
    

    # -- get the sBt for the stmids
    #
    sbtvarNN={}
    sbtvarDev={}
    sbtvarNonDev={}
    sbtvarAll={}
     
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
        
        sbtvarAll[stmid]=sbtVar
    
    # -- ls only
    
    if(doLs != None):
        ovars=doLs.split(',')
        sbtls=sbtvarAll
        if(dobt):
            sbtls=sbtvarNN
        elif(doDev):
            sbtls=sbtvarDev
        elif(doNon):
            sbtls=sbtvarNonDev
            
        rc=sbt.lsGaVarAllDict(sbtls,ovars,sMdesc)
        #rc=sbt.makeGaStnVar(sbtvarNN, ovars, sMdesc,verb=verb)
        #rc=sbt.makeGaStnVar(sbtvarAll, ovars, sMdesc,verb=verb)
        MF.dTimer('ALL')
        sys.exit()

    
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


