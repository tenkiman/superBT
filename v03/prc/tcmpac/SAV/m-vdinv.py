#!/usr/bin/env python

from WxMAP2 import *
from sBT import *

from ad2vm import *    

def makeStmOptByBasin(year):
    basins=['i','h','w','c','e','l']
    stmopt=''
    for b in basins:
        if(stmopt == ''):
            stmopt="%s.%s"%(b,year)
        else:
            stmopt="%s,%s.%s"%(stmopt,b,year)
    return(stmopt)


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
            'pfilt':            ['f:',None,'a',"""filter: 'z0012' | 'z0618'..."""],
            'useTaids':         ['t',0,1,"""use taids vice vaids -- do alias in vd2deck v ad2deck -- Only need to do once"""],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            
        }

        self.purpose="""
make era5 ad2  and inventory in both .txt and .pyp"""

        self.examples='''
%s -Y 1969.1970'''
    

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

years=yearOptPrc(yearOpt)
vdcmd='p-vdinv.py'

ovopt=''
if(override):  ovopt='-O'


filtOpt=''
if(pfilt != None): 
    filtOpt='-f %s'%(pfilt)
    
utaidsOpt=''
if(useTaids):
    utaidsOpt='-t'
    

MF.sTimer('Mk-Vd-All-%s'%(yearOpt))
for year in years:

    vdtimerOpt='%s'%(year)
    if(pfilt != None): vdtimerOpt="%s-%s"%(year,pfilt)
        
    MF.sTimer('vdinv-%s'%(vdtimerOpt))
    cmd="%s -S all.%s %s %s %s"%(vdcmd,year,filtOpt,utaidsOpt,ovopt)
    mf.runcmd(cmd,ropt)
    cmd="%s -S all.%s -p pod %s %s %s"%(vdcmd,year,filtOpt,utaidsOpt,ovopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vdinv-%s'%(vdtimerOpt))
        
    
MF.dTimer('Mk-Vd-All-%s'%(yearOpt))