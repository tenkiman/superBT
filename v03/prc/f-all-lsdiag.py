#!/usr/bin/env python

from sBT import *

def testTctrk(mdtg,stmsAct,override=0,verb=0):
    cmd="tctrk/s-sbt-tmtrkN.py %s -i"%(mdtg)
    lcards=MF.runcmdLog(cmd, ropt='', quiet=1, printCmd='runcmdLog')
    
    stmsDone=[]
    rc=0
    for lcard in lcards:
        if(verb): print 'ttt',lcard
        if(mf.find(lcard,'vmax')):
            tt=lcard.split()
            stmid=tt[0].lower()
            nl=int(tt[5])  # number of lines in tracker file
            if(nl == -999 or nl >= 1):
                stmsDone.append(stmid)
                
    for lcard in lcards:
        if(mf.find(lcard,'tracking alldone')): 
            rc=1
    
    trkStatus=(len(stmsDone) == len(stmsAct))
    if(not(trkStatus)):
        rc=-1
        print 'TCtrk stms: ',str(stmsDone)
        print 'TCOBS stms: ',str(stmsAct)

    return(rc,trkStatus)
    
def testTcdiag(mdtg,override=0,verb=0):
    
    topt='-l'
    cmd="tcdiag/s-sbt-tcdiag.py %s %s"%(mdtg,topt)
    lcards=MF.runcmdLog(cmd, ropt='', quiet=1, printCmd='runcmdLog')

    stmsDoneTD=[]
    rc=None
    for lcard in lcards:
        if(verb): print 'ddd',lcard
        if(mf.find(lcard,'TCTC')):
            tt=lcard.split()
            stmid=tt[13]
            stmsDoneTD.append(stmid)
            
    for lcard in lcards:

        if(mf.find(lcard,'been run yet')):
            rc=-1

        elif(mf.find(lcard,'try running')):
            rc=-2
        
        elif(mf.find(lcard,'dols only')):
            tt=lcard.split()
            rc=int(tt[-1])
        
        
    trkStatusTD=(len(stmsDoneTD) == len(stmsAct))
    if(not(trkStatusTD)):
        print 'tcDGN stms: ',str(stmsDoneTD)
        print 'TCOBS stms: ',str(stmsAct)
 

    return(rc,trkStatusTD)
    
def runTcdiag(mdtg,override=0,ropt=''):
    topt=''
    if(override): topt='-O'
    cmd="tcdiag/s-sbt-tcdiag.py %s %s"%(mdtg,topt)
    mf.runcmd(cmd,ropt)


def runTctrk(mdtg,cpOnly=0,override=0,topt=None,ropt=''):
    if(topt != None):
        topt=topt
    elif(override): 
        topt='-O'
    elif(cpOnly): 
        topt='-P'
    else:
        topt=''
        
    if(mdtg[8:10] != '00'): topt="%s -T"%(topt)
    cmd="tctrk/s-sbt-tmtrkN.py %s %s"%(mdtg,topt)
    mf.runcmd(cmd,ropt)
    #lcards=MF.runcmdLog(cmd, ropt='', quiet=1, printCmd='runcmdLog')
    
    
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doIt':             ['X',0,1,' execute tctrk/tcdiag if necessary'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'maskOpt':          ['M:',None,'a','mask to pull specific inventory'],
            'stmopt':           ['S:',None,'a','stmopt'],
        }

        self.purpose="""
run s-sbt-tctrk.py by dtgs or stmopt"""

        self.examples='''
%s -S l.07
%s -d cur12-24'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

m3=Mdeck3()

if(yearOpt != None):
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=mf.yyyyrange(byear, eyear)

    elif(len(tt) == 1):
        years=[yearOpt]
    else:
        print 'EEE -- invalid yearopt: ',yearOpt
else:
    print 'EEE - must set yearOpt in %s'%(CL.pyfile)



for year in years:
    
    # -- read log file
    #
    MF.sTimer('FFF-%s'%(year))
    mask='all'
    if(maskOpt != None):
        mask=maskOpt
    lmask="inv/lsdiag/*%s*%s*"%(mask,year[2:4])
    logfiles=glob.glob(lmask)
    if(len(logfiles) > 1):
        print 'WWW... have more than one logfiles in lmask: ',lmask
        print 'III... using the first...'
        
    logfile=logfiles[0]
    cards=open(logfile).readlines()
    
    mstms={}
    mdtgs=[]
    for card in cards:
        tt=card.split()
        stmid=tt[2]
        dtg=tt[4]
        mdtgs.append(dtg)
        rc=appendDictList(mstms, dtg, stmid)
        
    mdtgs=mf.uniq(mdtgs)
    
    for mdtg in mdtgs:
        
        # -- first check tctrk
        #
        stmsAct=m3.getMd3Stmids4dtg(mdtg,dobt=0,verb=verb,warn=0)

        (rct,trkStatus)=testTctrk(mdtg,stmsAct,verb=verb)
        (rcd,trkStatusTD)=testTcdiag(mdtg,stmsAct,verb=verb)

        runTrk=(rct == 2 and not(trkStatus))
        runDgn=(rcd == -1 or rcd == -2 or not(trkStatusTD))

        print '111st pass -- dtg: ',mdtg,' rct: ',rct,' rcd: ',rcd,\
              ' trkStatus: ',trkStatus,' trkStatusTD: ',trkStatusTD,\
              ' runTrk: ',runTrk,' runDgn: ',runDgn

        if(runTrk):
            print 'III--TTT -- need to run the tracker in override mode for dtg: ',mdtg

        if(ropt == 'norun'): continue
            

        if(runTrk and doIt):
            
            MF.sTimer('FFF-tctrk-%s'%(mdtg))
            rc=runTctrk(mdtg,override=1)
            (rct,trkStatus)=testTctrk(mdtg,stmsAct,verb=0)
            rc=runTctrk(mdtg,cpOnly=1)
            MF.dTimer('FFF-tctrk-%s'%(mdtg))

            runTrk=(rct == 2 and not(trkStatus))
            print '222nd pass TTT -- dtg: ',mdtg,' rct: ',rct,' rcd: ',rcd,\
                  ' trkStatus: ',trkStatus,' trkStatusTD: ',trkStatusTD,\
                  ' runTrk: ',runTrk,' runDgn: ',runDgn
            
            if(runTrk):
                print 'EEE problem running tracker for dtg:',mdtg
                sys.exit()

        if(runDgn):
            print 'III-DDD -- tracker good but need to run tcdiag for dtg: ',mdtg

        if(runDgn and doIt):
            MF.sTimer('FFF-lsdiag-%s'%(mdtg))
            rc=runTcdiag(mdtg)
            (rcd,trkStatusTD)=testTcdiag(mdtg,verb=0)
            MF.dTimer('FFF-lsdiag-%s'%(mdtg))

            print '222nd pass DDD -- dtg: ',mdtg,' rct: ',rct,' rcd: ',rcd,\
                  ' trkStatus: ',trkStatus,' trkStatusTD: ',trkStatusTD,\
                  ' runTrk: ',runTrk,' runDgn: ',runDgn
            

            runDgn=(rcd == -1 or rcd == -2 or not(trkStatusTD))
            if(runDgn):
                print 'EEE problem running tracker for dtg:',mdtg
                sys.exit()
            
                
            
            
            
    MF.dTimer('FFF-%s'%(year))
    




    