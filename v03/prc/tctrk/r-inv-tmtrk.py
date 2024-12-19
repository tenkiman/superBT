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
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'yearOpt':          ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'doInvPath':        ['P',0,1,'do inv path default is NOT'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s -Y 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

def makeTmtrkNInv(dtgopt,doInvPath,ropt,override=0):
    
    invpath=getInvPath4Dtgopt(dtgopt,invdir='./inv',override=override)
    if(doInvPath):
        MF.sTimer("inv: %s"%(dtgopt))
        
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        for dtg in dtgs:
            cmd="s-sbt-tmtrkN.py %s -i >> %s"%(dtg,invpath)
            mf.runcmd(cmd,ropt)
            
        MF.dTimer("inv: %s"%(dtgopt))
    else:
        cmd="time s-sbt-tmtrkN.py %s -i"%(dtgopt)
        mf.runcmd(cmd,ropt)
    
    return

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

years=[]
if(yearOpt == None and dtgopt == None):
    print 'you have to set either yearOpt or dtgOpt...press...'
    
elif(yearOpt != None and dtgopt == None):
    
    doInvPath=1
    tt=yearOpt.split('.')

    if(len(tt) == 1):
        years=tt
    elif(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=yyyyrange(byear, eyear)        
    else:
        print 'eee invalid yearOpt: ',yearOpt,' try again...'
        sys.exit()
    
elif(yearOpt == None and dtgopt != None):
    print 'doing just dtgopt: ',dtgopt,'setting doInvPath = 0'
    doInvPath=0

else:
    print """ooopppsss can't set BOTH yearOpt and dtgopt...ja sayounara..."""
    sys.exit()
    
MF.sTimer('III-TMTRK-%s'%(dtgopt))

if(len(years) == 0):
    
    MF.sTimer('III-TMTRK-%s'%(dtgopt))
    rc=makeTmtrkNInv(dtgopt,doInvPath,ropt)
    MF.dTimer('III-TMTRK-%s'%(dtgopt))
    
else:
    
    for year in years:
        iyear=str(year)
        dtgopt="%s01.%s12.6"%(iyear,iyear)
        MF.sTimer('III-TMTRK-%s-YYY'%(iyear))
        rc=makeTmtrkNInv(dtgopt,doInvPath,ropt,override=override)
        MF.dTimer('III-TMTRK-%s-YYY'%(iyear))

sys.exit()


