#!/usr/bin/env python

from sBT import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }

        self.options={
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'model':            ['m:','ecop','a','model '],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
redo atcf-form for era5"""

        self.examples='''
%s -Y 1945.1950'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(mf.find(yearOpt,'-')):
    tt=yearOpt.split('-')
    byear=int(tt[0])
    eyear=int(tt[1])
elif(mf.find(yearOpt,'.')):
    tt=yearOpt.split('.')
    byear=int(tt[0])
    eyear=int(tt[1])
else:
    byear=int(yearOpt)
    eyear=int(yearOpt)
    
years=mf.yyyyrange(byear,eyear)
for year in years:
    yearm1=mf.yyyyinc(year,-1)
    yearp1=mf.yyyyinc(year,1)
    bdtg="%s122000"%(yearm1)
    edtg="%s010100"%(yearp1)
    cmd="m-ln-fXXX-wmo-veri-flds.py %s.%s.12 -m %s"%(bdtg,edtg,model)
    mf.runcmd(cmd,ropt)
    
