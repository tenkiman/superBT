#!/usr/bin/env python

from sbt import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
#            1:['yearOpt',  'years to run'],
#            2:['basinOpt',  'basins'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is noru'],
            'stmopt':           ['S:',None,'a',' stmid target'],
        }

        self.purpose="""
run p-pr.py by cycling through stmids...because it call grads each time..."""

        self.examples='''
%s -S w.17'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

md3=Mdeck3()

if(stmopt != None):
    stmopts=getStmopts(stmopt)
    tstmids=[]
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt)
else:
    print 'EEE- must set stmopt'
    sys.exit()


oOpt=''
if(override): oOpt='-O'
MF.sTimer('ALL-LSDIAG-%s'%(stmopt))

for tstmid in tstmids:

    MF.sTimer('LSDIAG-%s'%(tstmid))
    cmd="p-lsdiag.py -S %s %s"%(tstmid,oOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('LSDIAG-%s'%(tstmid))

MF.dTimer('ALL-LSDIAG-%s'%(stmopt))
    
sys.exit()
