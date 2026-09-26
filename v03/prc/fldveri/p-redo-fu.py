#!/usr/bin/env python

from sBT import *
from ad2vm import yearOptPrc

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['year',    'year to process FU-'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'WGBoverride':      ['o',0,1,'wgrib2 list override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'diag':             ['D',0,1,'turn on diag'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
filter era5 fields for wmo verification"""

        self.examples='''
%s 1953090700'''



argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

try:
    fucards=open("./inv/fu/fu-%s.txt"%(year)).readlines()
except:
    fucards=[]

if(len(fucards) == 0):
    print 'NO FU for year: ',year
    sys.exit()

fudtgs=[]
for fucard in fucards:
    dtg=fucard[-11:-1]
    fudtgs.append(dtg)

fudtgs.sort()

pycmd='m-all-wmo-veri-flds.py'


oopt=''
if(override): oopt='-O'
     
wgopt=''
if(WGBoverride): wgopt='-o'
    


MF.sTimer('ALL-FU-%s'%(year))
for fudtg in fudtgs:
    
    MF.sTimer('FU-%s'%(fudtg))
    fus=glob.glob("/raid05/ecop-wmo/%s/%s/*FU*"%(year,fudtg))
    if(len(fus) == 0):
        print 'III - FU not there...press...'
        continue

    fupath=fus[0]
    
    cmd="%s %s %s %s -X"%(pycmd,fudtg,oopt,wgopt)
    mf.runcmd(cmd,ropt)
    
    cmd="%s %s -X"%(pycmd,fudtg)
    mf.runcmd(cmd,ropt)    
    
    cmd="rm  %s"%(fupath)
    mf.runcmd(cmd,ropt)
    MF.dTimer('FU-%s'%(fudtg))

cmd=""

MF.dTimer('ALL-FU-%s'%(year))
