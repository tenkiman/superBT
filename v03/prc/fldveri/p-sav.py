#!/usr/bin/env python

from sBT import *
from ad2vm import yearOptPrc

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['yearOpt',    'year opt process to process SAV-'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
find 'SAV' dtgs by year"""

        self.examples='''
%s 2012'''



argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

years=yearOptPrc(yearOpt)

MF.sTimer('ALL-SAV')
for year in years:
    MF.sTimer('SAV-%s'%(year))
    cmd="ls -la /raid05/ecop-wmo/%s/%s??????/*SAV*   > ./inv/SAV/SAV-%s.txt"%(year,year,year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('SAV-%s'%(year))
MF.dTimer('ALL-SAV')
