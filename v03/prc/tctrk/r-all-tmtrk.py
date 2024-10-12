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
            1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            #'dtgopt':           ['d:',None,'a','dtgopt'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'doBdeck2':         ['2',0,1,'using bdeck at command line vice in getYears4Opts'],
            'doTrackerOnly':    ['T',0,1,'do NOT run trackeronly'],
            
        }

        self.purpose="""
run s-sbt-tctrk.py by dtgs or stmopt"""

        self.examples='''
%s 2007 -S l.07  # dtgopt ignored
%s 197901.6'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
doBT=0
if(doBdeck2): doBT=1

md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

if(dtgopt != None): MF.sTimer('AAA-TCTRK-%s'%(dtgopt))
if(stmopt != None): MF.sTimer('AAA-TCTRK-%s'%(stmopt))

if(dtgopt != None and stmopt == None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
elif(stmopt != None and dtgopt == None):
    syear=None
    dtgs=md3.getMd3StmDtgs4Stmopt(stmopt,syear=syear)
else:
    print 'EEE--(%s) must set either dtgopt or stmopt alone...sayounara'%(CL.pyfile)
    sys.exit()

if(dtgopt != None): MF.dTimer('AAA-TCTRK-%s'%(dtgopt))
if(stmopt != None): MF.dTimer('AAA-TCTRK-%s'%(stmopt))

# -- do tcgen at 00Z onl
#
oopt=''
if(override): oopt='-O'

for dtg in dtgs:
    topt='-T'
    sopt=''
    #if(stmopt != None): sopt='-S %s'%(stmopt)
    if(dtg[8:10] == '00'): topt='' 
    cmd="s-sbt-tmtrkN.py %s %s %s %s"%(dtg,topt,sopt,oopt)
    mf.runcmd(cmd,ropt)
    
if(dtgopt != None): MF.dTimer('AAA-TCTRK-%s'%(dtgopt))
if(stmopt != None): MF.dTimer('AAA-TCTRK-%s'%(stmopt))

sys.exit()


