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
            'doit':             ['X',0,1,'run with default pmodmin'],
            'podmin':           ['P:',98.5,'f',' set the minimum pod for find unders...'],
            'doRedo':           ['R',0,1,'run m-redo-clp3-under.py'],
        }

        self.purpose="""
redo clp3 for stmops with under 100%% PoD"""

        self.examples='''
%s -S w.2009'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
tpath='/tmp/clp3.txt'
cmd='clp3-under.sh > %s'%(tpath)
mf.runcmd(cmd)

cards=open(tpath).readlines()
pminbasins={}

for card in cards:
    if(mf.find(card,'Nfc')):
        tt=card.split()
        basin=tt[0]
        tau=tt[1]
        pod=float(tt[2])
        opod="%4.1f %2s"%(pod,tau)
        if(pod < podmin):
            MF.appendDictList(pminbasins,basin,opod)


pp=pminbasins.keys()
pp.sort()

for p in pp:
    print 'pmin ',p,pminbasins[p]
    if(doRedo):
        roptRedo='-N'
        if(doit):
            roptRedo=''
            ropt=''
        cmd='m-redo-clp3-under.py -S %s %s'%(p,roptRedo)
        mf.runcmd(cmd,ropt)
