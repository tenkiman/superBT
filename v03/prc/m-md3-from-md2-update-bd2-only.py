#!/usr/bin/env pythonw

from tcbase import TcData

from sBT import *

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'oPath':          ['o:',None,'a','write output to oPath'],
            'doBdeck2':       ['2',1,0,'this version does bdeck by default'],
            }

        self.purpose='''
make mdeck3'''
        
        self.examples='''
%s -S 30w.19'''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- storms
#
if(stmopt != None):

    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt=None,yearOpt=None)
    # -- since update force doBdeck2=1
    #
    doBdeck2=1
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=0,doMd3Only=1)
    
    tcD=TcData(stmopt=stmopt,doBdeck2=doBdeck2,verb=verb)
    stmids=tcD.makeStmListMdeck(stmopt,dobt=dobt,cnvSubbasin=0,verb=verb)
    
    for stmid in stmids:
          
        print 'dddoooiiinnnggg stmid: ',stmid
        if(not(IsNN(stmid))):
            print 'WWW -- can only do NN ... press ...'
            continue
        
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        
        dobt=0
        dds=tcD.getDSsFullStm(stmid, dobt=dobt, doprint=0, set9xfirst=0, dowarn=0)
        scard=tcD.lsDSsStmSummary(dds,stmid,doprint=0)
        print 'sss',scard

        sname=dds.sname
        sname=sname.replace(' ','_')
        
        try:
            stmid9x=dds.stmid9x.upper()
        except:
            stmid9x=None
            
        try:
            stmidNN=dds.stmidNN.upper()
        except:
            stmidNN=None
            
        try:
            stm1id=dds.stm1id
        except:
            stm1id=None
            
        tname=stmid.replace('.','-').upper()
        osname=sname.upper()
        tname="%s-%s-"%(tname,osname)

        basin=md3.getBasin4b1id(b1id)
        tdir="%s/%s/%s"%(sbtSrcDir,year,basin)
        
        # -- look for existing tdir
        #
        b3id="%s%s"%(snum,b1id.upper())
        bd1mask="%s/%s*"%(tdir,b3id)
        bd1s=glob.glob(bd1mask)

        if(len(bd1s) == 1):
            tdir=bd1s[0]
        else:
            print 'EEE -- too many tdirs for bd2 update...'
            sys.exit()
    
        oPathBT="%s/%s-sum-BT2.txt"%(tdir,b3id)
        
        ocards=[]
        trk=dds.trk
        dtgs=dds.dtgs
        ktrk=trk.keys()
        ktrk.sort()

        for kt in ktrk:
            ocard=parseDssTrk(kt,trk[kt])
            if(verb): print ocard
            ocards.append(ocard)

        MF.WriteList2Path(ocards,oPathBT,verb=verb)
        
        # -- now do the qc that makes all md3
        #
        cmd="m-md3-qc-ALL.py -S %s -2"%(stmid)
        mf.runcmd(cmd,ropt)
        
        
