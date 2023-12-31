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
            'ropt':             ['N','','norun',' norun is norun'],
            'dtgopt':           ['d:',None,'a','dtgopt'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'doTrackerOnly':    ['T',0,1,'do NOT run trackeronly'],
        }

        self.purpose="""
run s-sbt-tctrk.py by dtgs or stmopt"""

        self.examples='''
%s -S l.07
%s -d cur12-24'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

m3=Mdeck3()

if(dtgopt != None): MF.sTimer('AAA-TCTRK-%s'%(dtgopt))
if(stmopt != None): MF.sTimer('AAA-TCTRK-%s'%(stmopt))

if(dtgopt != None and stmopt == None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
elif(stmopt != None and dtgopt == None):
    syear=None
    dtgs=m3.getMd3StmDtgs4Stmopt(stmopt,syear=syear)
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
    if(dtg[8:10] == '00'): topt=''
    cmd="s-sbt-tmtrkN.py %s %s %s"%(dtg,topt,oopt)
    mf.runcmd(cmd,ropt)
    
if(dtgopt != None): MF.dTimer('AAA-TCTRK-%s'%(dtgopt))
if(stmopt != None): MF.dTimer('AAA-TCTRK-%s'%(stmopt))

sys.exit()


