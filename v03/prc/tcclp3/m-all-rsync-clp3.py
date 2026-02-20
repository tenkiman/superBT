#!/usr/bin/env python

from ad2vm import *

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

sbdir='/sbt/superBT-V04/dat-v03/atcf-form'
tbdir='/w21/dat/tc/adeck/atcf-form'
model='clp3'
rsyncOpt='-alv'

years=yearOptPrc(yearOpt)

MF.sTimer('ALL-rsync-clp3')
for year in years:
    MF.sTimer('rsync-clp3-%s'%(year))
    cmd="rsync %s %s/%s/%s/ %s/%s/%s/"%(rsyncOpt,sbdir,year,model,tbdir,year,model)
    mf.runcmd(cmd,ropt)
    MF.dTimer('rsync-clp3-%s'%(year))
MF.dTimer('ALL-rsync-clp3')
