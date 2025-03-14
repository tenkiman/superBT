#!/usr/bin/env python

from sBTtcdiag import * 

from WxMAP2 import *
w2=W2()

def runLats4Era5(ectlpath,ropt='',doClean=1,verb=0):
    
    (epath,efile)=os.path.split(ectlpath)
    (base,ext)=os.path.splitext(ectlpath)
    region=base.split('.')[-1]

    if(verb):
        print 'bbb',base
        print 'eee',epath,efile
        print 'rrr',region

    MF.sTimer("lats-%s-%s"%(dtg,efile))
    
    latscmd="lats4d.sh -i %s -format grads_grib -precision 9 -o %s"%(ectlpath,base)
    mf.runcmd(latscmd,ropt)
         
    if(doClean):
        cmd="rm %s*.dat"%(base)
        mf.runcmd(cmd,ropt)

    MF.dTimer("lats-%s-%s"%(dtg,efile))
            

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
        }


        self.options={
            'doClean':          ['K',1,0,'do NOT clean .dat and .grb files'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doLocal':          ['C',0,1,'use local files vice mike8:/raid01'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
run lats4d.sh on era5 tcdiag .dat files in grads_grib mode convert to .grb"""

        self.examples='''
%s 1953090700'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

if(doLocal):
    TcTcanalDatDir = TcTcanalDatDirL

MF.sTimer("ALL-lats")
for dtg in dtgs:
        
    year=dtg[0:4]
    eraDir='%s/%s/%s/era5'%(TcTcanalDatDir, year,dtg)
    
    emask="%s/era5.%s.*.ctl"%(eraDir,dtg)
    efiles=glob.glob(emask)
    n1e=len(efiles)

    omask="%s/oisst.%s.*.ctl"%(eraDir,dtg)
    ofiles=glob.glob(omask)
    n1o=len(ofiles)

    smask="%s/sfc-era5.%s.*.ctl"%(eraDir,dtg)
    sfiles=glob.glob(smask)
    n1s=len(sfiles)
    
    if(n1e == 1):
        ectlpath=efiles[0]
        rc=runLats4Era5(ectlpath,doClean=doClean,ropt=ropt,verb=verb)
            
    if(n1o == 1):
        octlpath=ofiles[0]
        rc=runLats4Era5(octlpath,doClean=doClean,ropt=ropt,verb=verb)

    if(n1s == 1):
        sctlpath=sfiles[0]
        rc=runLats4Era5(sctlpath,doClean=doClean,ropt=ropt,verb=verb)
        
    if(n1e == 0 or n1o == 0 or n1s == 0):
        print 'no tcanal files .dat for dtg: ',dtg
        continue
    
MF.dTimer("ALL-lats")