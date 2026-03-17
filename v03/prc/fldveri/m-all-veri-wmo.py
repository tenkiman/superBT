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
            'dtgopt':           ['d:',None,'a','dtgopt for setting paths of md3'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
do era5 veri-wmo for an entire year"""

        self.examples='''
%s -Y 2001'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(yearOpt != None):
    
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

oopt=''
if(override):
    oopt='-O'
     
gotdtg=0
if(dtgopt != None):
    years=[dtgopt[0:4]]
    gotdtg=1

MF.sTimer('ALL-VERI')
for year in years:

    logpath='./inv/veri-wmo-inv-%s.txt'%(year)

    if(not(gotdtg)): 
        dtgopt="%s010100.%s123112.12"%(year,year)
    MF.sTimer('ALL-eff-%s'%(year))
    cmd='m-fld-veri-wmo.py %s %s | tee %s'%(dtgopt,oopt,logpath)
    mf.runcmd(cmd,ropt)
    MF.dTimer('ALL-eff-%s'%(year))
    

MF.dTimer('ALL-VERI')
