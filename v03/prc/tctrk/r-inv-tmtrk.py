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
            'doInvPath':        ['P',0,1,'do inv path default is NOT'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

invpath=getInvPath4Dtgopt(dtgopt,invdir='./inv')

MF.sTimer('III-TMTRK-%s'%(dtgopt))
if(doInvPath):
    cmd="time s-sbt-tmtrkN.py %s -i > %s"%(dtgopt,invpath)
else:
    cmd="time s-sbt-tmtrkN.py %s -i"%(dtgopt)
    
mf.runcmd(cmd,ropt)
MF.dTimer('III-TMTRK-%s'%(dtgopt))

sys.exit()


