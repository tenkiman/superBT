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

def xvPlot(pltpath,ropt='',xsize=1000,xb='-10',yb='+10',zfact=1.0):
    ysize=(xsize*3)/4
    cmd="xv  -geometry %ix%i%s%s %s &"%(xsize*zfact,ysize*zfact,xb,yb,pltpath)
    MF.runcmd(cmd,ropt)

def doCorrAll(stmid,sumPath,doX=1):
    
    # -- read the cards
    #
    icards=open(sumPath).readlines()

    xgrads='grads'
    xgrads=setXgrads(useX11=0,useStandard=0)
    zoomfact=None
    background='black'
    dtgopt=None
    ddtg=6
    dtg0012=0

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


    dom3=0
    md3=MD3trk(icards,stm1id,stm9xid,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    dtgs=md3.dtgs
    trk=md3.trk
    basin=md3.basin

    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)

    ktrk=trk.keys()
    ktrk.sort()
    ocards=[]
    
    opathTmp='/tmp/tt.md3'
    
    for kt in ktrk:
        ocard=parseDssTrkMD3(kt,trk[kt],stm1id,stm9xid,basin,rcsum=rcsum,sname=sname)
        ocard=ocard.replace(' ','')
        if(verb): print 'ooo---iii',ocard,len(ocard.split(','))
        ocards.append(ocard)

    rc=MF.WriteList2Path(ocards, opathTmp,verb=verb)
    (m3trk,m3info)=getMd3trackSpath(opathTmp,verb=verb)
    m3trki=setMd3track(m3trk,stm1id,verb=verb)
    btrk=m3trki
    dtgs=m3trki.keys()
    dtgs.sort()
    
    for dtg in dtgs:
        print 'm3btrk ',dtg,btrk[dtg]
        
    # -- make the plot
    #
    override=1
    MF.sTimer('trkplot')
    tP=TcBtTrkPlot(stm1id,btrk,dobt=0,
                   Window=0,Bin=xgrads,
                   zoomfact=zoomfact,override=override,
                   background=background,dopbasin=0,
                   dtgopt=dtgopt,pltdir=sdir,
                   xsize=1000,
                   plttag='corr')

    tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg)
    MF.dTimer('trkplot')
    if(doX): tP.xvPlot(xb='+10',yb='+10',zfact=1.0)

    

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
            'redoQC':           ['R',0,1,'rerunQC'],
            'doSingleOnly':     ['I',0,1,'just do singletons'],
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

md3=Mdeck3(doBT=0,doSumOnly=1)

MF.sTimer('ALL')

# -- make sbt object
#
#MF.sTimer('sbt')
#sbt=superBT(version)
#md3=Mdeck3(doBT=0,doSumOnly=1)
#MF.dTimer('sbt')

qcStms={}

invmask="../qcinv/qcspd-%i-*.txt"%(int(bspdmax))

invs=glob.glob(invmask)

qcards=[]

for inv in invs:
    qcards=qcards+MF.ReadFile2List(inv)

for qcard in qcards:
    tt=qcard.split()
    stmid=tt[0].strip()
    qcStms[stmid]=qcard
    
qcstmids=qcStms.keys()
qcstmids.sort()

nqcAll=len(qcstmids)

if(verb):
    for qc in qcstmids:
        print qc

diffCmd="emacs -nw -q -l ~/.emacs.nw "
diffCmd='meld'

if(stmopt != None):
    
    qctime=dtg('dtg_mn')
    oqcpath="../qcact/qc-%2i-%s-%s.txt"%(int(bspdmax),qctime,stmopt)
    oqccards=[]
    
    istmopt=stmopt
    stmids2qc=[]
    stmids2Try=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids2Try=stmids2Try+md3.getMd3Stmids(stmopt)
        
    for stmid in stmids2Try:
        if(stmid in qcstmids):
            stmids2qc.append(stmid)
                
    nqcStm=len(stmids2qc)
    print "N All qcstmids: %4i for bspdmax: %i"%(nqcAll,bspdmax)
    print "N 2do         : %4i for stmopt: %s"%(nqcStm,istmopt)
    
    for stmid in stmids2qc:
        
        (sumPath,sumPathBT)=getSrcSumTxt(stmid,verb=verb)
        if(sumPath != None):
            savSumPath=sumPath.replace('.txt','.txt-SAV')
        else:
            print 'NO sumPath for stmid: ',stmid,'press...'
            continue
        
        if(ropt == 'norun'):
            print 'QC stmid: ',stmid
            continue

        # -- ALWAYS save original
        #
        if(not(ChkPath(savSumPath))):
            cmd="cp %s %s"%(sumPath,savSumPath)
            runcmd(cmd)
            
        # -- if need to redo...
        #
        if(redoQC):
            cmd="cp %s %s"%(savSumPath,sumPath)
            runcmd(cmd)
            
            
        (sdir,sfile)=os.path.split(sumPath)
        pngfile=glob.glob("%s/*png"%(sdir))[0]
        qcSumPath=glob.glob("%s/*QC%2i"%(sdir,bspdmax))[0]
        qccard=qcStms[stmid][0:-1]
        (sdir,sfile)=os.path.split(sumPath)

        isSingle=(find(qccard,'sngleton'))
        
        
        print '222qqq: ',isSingle,qccard

        if(doSingleOnly):
            if(isSingle):
                rc=raw_input("this is a singleton...want rm -r? y|n :  ")
                if(rc.lower() == 'y'):
                    cmd="rm -r %s/"%(sdir)
                    runcmd(cmd)
                    oqccard="%s YYY %-40s %s"%(stmid,'rm -r singleton',qccard)
                else:
                    oqccard="%s NNN %-40s %s"%(stmid,'NO to rm -r ',qccard)
                    
                oqccards.append(oqccard)

            else:
                continue
                    
                
        else:
        
            roptD=''
            cmd="%s %s %s &"%(diffCmd,sumPath,qcSumPath)
            runcmd(cmd,roptD)
    
            rc=xvPlot(pngfile)
    
            doCorr=0
            if(isSingle):
                rc=raw_input("this is a singleton...want rm -r? y|n :  ")
                if(rc.lower() == 'y'):
                    cmd="rm -r -i %s/"%(sdir)
                    runcmd(cmd)
                    oqccard="%s YYY %-40s %s"%(stmid,'rm -r singleton',qccard)
                else:
                    oqccard="%s NNN %-40s %s"%(stmid,'NO to rm -r ',qccard)
            else:
                rc=raw_input("do you want to edit? y|n :  ")
                qccard=qcStms[stmid][0:-1]
                if(rc.lower() == 'y'):
                    comment=raw_input("comment:  ")
                    oqccard="%s YYY %-40s %s"%(stmid,comment,qccard)
                    doCorr=1
                else:
                    oqccard="%s NNN %-40s %s"%(stmid,'no change',qccard)
                
            oqccards.append(oqccard)
    
            if(doCorr):
                rc=doCorrAll(stmid,sumPath)
            
    rc=WriteList(oqccards,oqcpath,verb=1)
        
        
    sys.exit()


sys.exit()


