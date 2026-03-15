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
            'yearOpt':          ['Y:',None,'a','yearOpt for start of 30-y average'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
make 30-year annual daily mean for WMO NWP veri
runs m-daily-climo.gs yyyy"""

        self.examples='''
%s -Y 1991 # make 365-d mean 1992 - 366 mean (leap year)'''

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

MF.sTimer('ALL-ALL')
for year in years:
    
    MF.sTimer('daily-CLM-%s'%(year))
    cmd='''grads -lbc "m-daily-climo.gs %s"'''%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('daily-CLM-%s'%(year))
    

MF.dTimer('ALL-ALL')
