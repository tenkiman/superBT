#!/usr/bin/env python

from sBT import *

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
            'verbose':          ['v',0,1,'verbose=1 is REALLY verbose'],
            'doit':             ['X',0,1,'do it anyway...'],
            'ropt':             ['N','','norun',' norun is norun'],
            'yearopt':          ['Y:',None,'a','yearopt YYYY or BYYYY.EYYYY'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'rerunAdTd':        ['R',0,1,' run tcdiag and/or tracker for missing dtgs'],
            'doLog':            ['L',1,0,'do NOT do logfile to raid02/log'],
            'doLocal':          ['C',1,0,'''do NOT do local - default is to run locally'''],
            
            
        }

        self.purpose="""
make atcf-form of trackers in adeck-stm"""

        self.examples='''
%s -S l.07  # dtgopt ignored'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    if(len(byear) == 2 and len(eyear) == 2):
        years=range(int(byear),int(eyear)+1)
    else:
        years=mf.yyyyrange(byear, eyear)
    oyearOpt="%s-%s"%(str(byear),str(eyear))

elif(len(tt) == 1):

    years=[yearopt]
    oyearOpt=yearopt

else:
    print 'EEE -- invalid yearopt: ',yearopt

b1ids=['h','w','e','l','c','i']
MF.sTimer('AALLLL-AD-TD-%s'%(oyearOpt))

rerunopt=''
if(rerunAdTd): rerunopt='-R'
roptSbt=''
if(ropt == 'norun'): 
    roptSbt='-N'
    ropt=''
if(doit): ropt=''

for year in years:
    syear=str(year)
    MF.sTimer('AD-TD-%s'%(syear))
    for b1id in b1ids:
        MF.sTimer('B1ID-AD-TD-%s-%s'%(b1id,syear))
        sopt="%s.%s"%(b1id,syear)
        cmd='i-sbt-tctrk-tcdiag.py -S %s %s %s'%(sopt,rerunopt,roptSbt)
        mf.runcmd(cmd,ropt)
        MF.dTimer('B1ID-AD-TD-%s-%s'%(b1id,syear))
    MF.dTimer('AD-TD-%s'%(syear))
MF.dTimer('AALLLL-AD-TD-%s'%(oyearOpt))
    
sys.exit()


dtgopt=yearOpt=None





istmopt=stmopt
stmopts=getStmopts(stmopt)

lopt='-L'
if(doLog): lopt=''

copt=''
if(doLocal): copt='-C'
    

tcdStat={}
adStat={}
aStmids=[]
MF.sTimer('aDtD-ALL-%s'%(istmopt))
for stmopt in stmopts:
    
    MF.sTimer('aDtD-stmopt-%s'%(stmopt))
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    aStmids=aStmids+tstmids
    
    tyears=[]
    for tstmid in tstmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
        tyears.append(year)
        rc=getAdeckTcdiag4Stmid(tstmid,verb=verb,verbose=verbose)
        
    MF.dTimer('aDtD-stmopt-%s'%(stmopt))
    
MF.sTimer('anl-adtd-%s'%(istmopt))
(redoAd,redoTd)=anlAdTdStat(aStmids,verb=verb)
MF.dTimer('anl-adtd-%s'%(istmopt))

if(len(redoAd) > 0):
    print 'AAADDD redo:',redoAd
else:
    print 'AAADDD -- trackers ALLGOOD   for istmopt: ',istmopt
    
if(len(redoTd) > 0):
    
    redoTd=mf.uniq(redoTd)
    print 'TTTDDD redo Nruns:',len(redoTd)
    if(rerunAdTd):
        MF.ChangeDir('tcdiag')
        MF.sTimer('redoTD-All')
        for dtg in redoTd:
            
            # -- check for bad dtgs
            #
            tdtg=dtg
            if(IsBadEra5Dtg(tdtg) == 0):
                print 'EEE---BBB era5 dtg...press...'
                continue
            
            MF.sTimer('redoTD-All')
            cmd="r-all-tcdiag.py %s %s %s"%(dtg,lopt,copt)
            mf.runcmd(cmd,ropt)
            MF.sTimer('redoTD-All')
        MF.sTimer('redoTD-All')
        # -- now sync over...
        if(doLocal):
            tyears=mf.uniq(tyears)
            for tyear in tyears:
                cmd='r-rsync-tcdiag-local-output.py -R dat -Y %s -X'%(tyear)
                mf.runcmd(cmd,ropt)
                cmd='r-rsync-tcdiag-local-output.py -R prod -Y %s -X'%(tyear)
                mf.runcmd(cmd,ropt)
        MF.ChangeDir('../')
    
else:
    print 'TTTDDD -- diag files ALLGOOD for istmopt: ',istmopt


MF.dTimer('aDtD-ALL-%s'%(istmopt))
        
sys.exit()


