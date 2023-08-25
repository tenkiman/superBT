#!/usr/bin/env python

from sBT import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
#            1:['yearOpt',  'years to run'],
#            2:['basinOpt',  'basins'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is noru'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'doTcdiag':         ['D',0,1,' try re running s-sbt-tcdiat.py -O'],
        }

        self.purpose="""
run p-pr.py by cycling through stmids...because it call grads each time..."""

        self.examples='''
%s -S w.17'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

md3=Mdeck3()

if(stmopt != None):
    stmopts=getStmopts(stmopt)
    tstmids=[]
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt)
else:
    print 'EEE- must set stmopt'
    sys.exit()

noMd3={}
divg999={}
lsdiagsAll={}

for tstmid in tstmids:

    (rc,mcard)=md3.getMd3StmMeta(tstmid)

    tyear=rc[0]
    stm3id=rc[1]
    lmask="%s/%s/*/%s*/*lsdiag*"%(sbtSrcDir,tyear,stm3id)
    lpaths=glob.glob("%s"%(lmask))
    
    if(len(lpaths) == 1):
        lpath=lpaths[0]
    else:
        print 'WWW--no lsdiag-md3-*-MRG.txt'
        lpath=None

    if(lpath != None):
        
        # -- get track
        #
        if(IsNN(tstmid)):
            (rc,m3trk)=md3.getMd3track(tstmid,dobt=1)
        else:
            (rc,m3trk)=md3.getMd3track(tstmid)
        
        lcards=open(lpath).readlines()
        lsdiagsAll[tstmid]=lcards
        
        for lcard in lcards:
            #print lcard[0:-1]
            tt=lcard.split()
            dtg=tt[1].strip()
            divg200=tt[5].strip()
            divg200=float(divg200)
            try:
                trk=m3trk[dtg][0:4]
            except:
                trk=None
            
            if(trk == None):
                if(verb): print 'no md3 for tstmid: ',tstmid,' dtg: ',dtg
                appendDictList(noMd3,tstmid,dtg)
                continue

            if(divg200 < -888.):
                if(verb): print '999',tstmid,dtg,'divg200: %5.0f %s %s'%(divg200,str(trk),lcard[0:144])
                appendDictList(divg999,tstmid,dtg)
                
# -- noMD3 problems        
#
tstmids=noMd3.keys()
tstmids.sort()
for tstmid in tstmids:
    # -- redo 
    #
    cmd="p-lsdiag.py -S %s -O"%(tstmid)
    mf.runcmd(cmd)
    continue

    
# -- noMD3 problems        
#
tropt='norun'
if(doTcdiag): tropt=''
tstmids=divg999.keys()
tstmids.sort()
for tstmid in tstmids:
    print 'redo tcdiag for stmid: ',tstmid
    rdtgs=divg999[tstmid]
    for rdtg in rdtgs:
        cmd="tcdiag/s-sbt-tcdiag.py %s -O"%(rdtg)
        mf.runcmd(cmd,tropt)
        
    cmd="p-lsdiag.py -S %s -O"%(tstmid)
    mf.runcmd(cmd,tropt)
    
    

    

sys.exit()
