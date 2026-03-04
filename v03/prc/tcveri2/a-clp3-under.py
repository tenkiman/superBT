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
            'targetTau':        ['t:',None,'i',' set the target taus'],
            'doRedo':           ['R',0,1,'run m-redo-clp3-under.py'],
            'byStm':            ['Y',0,1,'redo m-redo-clp3-under.py to dectect problem stmid'],
            
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
        tau=int(tt[1])
        pod=float(tt[2])
        if(pod < podmin):
            opod="%4.1f %2s"%(pod,tau)
            if(targetTau != None and tau == targetTau):
                opod="%4.1f %2s"%(pod,tau)
                MF.appendDictList(pminbasins,basin,opod)
            #else:
            #    MF.appendDictList(pminbasins,basin,opod)

pStmoptsOk=[
#'l.1961',
#'l.1964',
#'l.2004',
#'l.2006',
]
pp=pminbasins.keys()
pp.sort()

podmin=podmin

opodmin=str(podmin)
MF.sTimer('AALLLL-clp3-under-%s'%(opodmin))

tauopt=''
if(targetTau != None):
    tauopt='-t %d'%(targetTau)

for p in pp:
   
    if(p in pStmoptsOk):
        print 'p: ',p,'okay'
        continue
    else:
        print 'pmin ',p,pminbasins[p],'tau: ',tauopt
    
    if(doRedo):
        
        MF.sTimer('clp3-under-%s'%(pminbasins[p]))
        if(byStm):

            roptRedo='-N'
            if(doit):
                roptRedo=''
                ropt=''
            cmd='m-redo-clp3-under.py -S %s -Y %s -P %3.1f %s'%(p,roptRedo,podmin,tauopt)
            
        else:

            roptRedo='-N'
            if(doit):
                roptRedo=''
                ropt=''
            cmd='m-redo-clp3-under.py -S %s %s -P %3.1f %s'%(p,roptRedo,podmin,tauopt)
        mf.runcmd(cmd,ropt)
        MF.dTimer('clp3-under-%s'%(pminbasins[p]))
        
MF.dTimer('AALLLL-clp3-under-%s'%(opodmin))
        