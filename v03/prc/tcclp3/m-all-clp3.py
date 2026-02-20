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

years=yearOptPrc(yearOpt)

ropt='norun'
ropt=''
MF.sTimer('ALL-clp3')
for year in years:
    MF.sTimer('clp3-%s'%(year))
    cmd="p-clp3.py -S all.%s"%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('clp3-%s'%(year))
MF.dTimer('ALL-clp3')
