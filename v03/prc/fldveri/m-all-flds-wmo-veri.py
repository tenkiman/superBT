#!/usr/bin/env python

from sBT import *

def getInvEcop():
    idir='/raid02/dat-doc'
    ipaths=glob.glob('%s/ecm?*txt'%(idir))

    invEcop={}
    for ipath in ipaths:
        cards=open(ipath).readlines()
    
        for card in cards:
            tt=card.split()
            model=tt[0].strip()
            dtg=tt[1].strip()
            if(len(dtg) == 10):
                MF.appendDictList(invEcop, dtg, model)
                
    idtgs=invEcop.keys()
    idtgs.sort()
    return(idtgs,invEcop)

def selectEcop(iEcop):
    
    if(len(iEcop) == 1):
        oEcop=iEcop[0]
    elif(len(iEcop) == 2):
        ie0=iEcop[0]
        ie1=iEcop[1]
        if(ie1 == 'ecm5' or ie1 == 'ecm6'):
            oEcop=ie1
        else:
            oEcop=ie0
    elif(len(iEcop) == 3):
        print '333333333333',iEcop
        sys.exit()
    else:
        oEcop='...'
        
    return(oEcop)


class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }

        self.options={
            'runwmo':           ['X',0,1,'run the wmo-veri fields'],
            'doWmoCtlOnly':     ['T',0,1,'only do the .ctl '],
            'override':         ['O',0,1,'override'],
            'WGBoverride':      ['o',0,1,'wgrib2 list override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'diag':             ['D',0,1,'turn on diag'],
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

(idtgs,invEcop)=getInvEcop()

dtgs=mf.dtg_dtgopt_prc(dtgopt)

oopt=''
if(override): oopt='-O'

dopt=''
if(diag): dopt='-D'

topt=''
if(doWmoCtlOnly):
    topt='-T'
    dopt=oopt=''
    WGBoverride=0
    diag=2
    
if(diag == 2): MF.sTimer('ALL-%s'%(dtgopt))
    
for dtg in dtgs:
    if(dtg in idtgs):
        iEcop=invEcop[dtg]
        oEcop=selectEcop(iEcop)
        #print 'YYY for ',dtg,iEcop,oEcop
        wgopt=''
        if(WGBoverride and (oEcop != 'era5' and oEcop != 'ecm5')):
            wgopt='-o'
        if(runwmo):
            if(diag == 1): MF.sTimer('wmo-%s-%s'%(dtg,oEcop))
            cmd='m-flds-wmo-veri.py %s -m %s %s %s %s %s'%(dtg,oEcop,oopt,dopt,topt,wgopt)
            if(diag == 1): mf.runcmd(cmd,ropt)
            else:     mf.runcmd(cmd,'quiet')
            if(diag == 1): MF.dTimer('wmo-%s-%s'%(dtg,oEcop))
            
            
    else:
        print 'NNN for ',dtg,'...'
        
if(diag == 2): MF.dTimer('ALL-%s'%(dtgopt))
    
sys.exit()    
