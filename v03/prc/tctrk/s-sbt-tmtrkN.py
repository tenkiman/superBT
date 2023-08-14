#!/usr/bin/env python

from tcbase import *
from WxMAP2 import *
w2=W2()

from sBTtctrkS import TmTrkSimple
from sBT import *

def getEra5Grb(era5bdir,dtg,model='era5'):
    
    year=dtg[0:4]
    grbpath="%s/%s/%s/%s-w2flds-%s-ua.grb2"%(era5bdir,year,dtg,model,dtg)
    ctlpath="%s/%s/%s/%s-w2flds-%s-ua.ctl"%(era5bdir,year,dtg,model,dtg)
    sizgrb=MF.getPathSiz(grbpath)
    sizctl=MF.getPathSiz(ctlpath)

    grbpath2="%s/%s/%s/%s-w2flds-%s-sfc.grb"%(era5bdir,year,dtg,model,dtg)
    ctlpath2="%s/%s/%s/%s-w2flds-%s-sfc.ctl"%(era5bdir,year,dtg,model,dtg)
    sizgrb2=MF.getPathSiz(grbpath2)
    sizctl2=MF.getPathSiz(ctlpath2)
    
    return(ctlpath,sizgrb,ctlpath2,sizgrb2)



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
            'stmopt':           ['S:',None,'a','stmopt'],
            'doTrackerOnly':    ['T',0,1,'run trackeronly'],
            'doClean':          ['C',1,0,'1 do NOT clean'],            
            'doInv':            ['i',0,1,'do Inventory'],            
            'doCpTctrk':        ['P',0,1,'make the tctrk.atcf|sink.dtg.txt from adeck_stm -> adeck_dtg'],            
        }

        self.purpose="""
run TmTrkSimple for the fim7 subseasonal"""

        self.examples='''
%s 2002 '''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

# -----------------------------------  default setting of max taus
#
maxtau=168
mintauTC=132

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(not(doInv)):
    MF.ChkDir(tmtrkbdir,'mk')
    MF.ChkDir(abdirStm,'mk')
    MF.ChkDir(abdirDtg,'mk')

    
ptable=None

dtgs=mf.dtg_dtgopt_prc(dtgopt)

model='era5'
atcfname='tera5'

regridTracker=0.50
regridGen=0.5

maxtau=168

#dtau=6
#max6h=120
#max12h=240
##max12h=maxtau

#dattaus=range(0,max6h+1,6)+range(max6h+12,max12h+1,12)

# -- get md3
#
md3=Mdeck3()

for dtg in dtgs:

    ayear=dtg[0:4]
    
    (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg,maxtau=maxtau,doSfc=0)
    
    # -- model dtg whe tauOffset=6
    #
    mdtg=mf.dtginc(dtg,-tauOffset)
    rc=getEra5Grb(era5bdir,mdtg,model='era5')
    (ctlpath2,sizgrb,ctlpath2a,sizgrb2a)=rc
    #print 'qqqq',sizgrb,ctlpath2
    
    if(sizgrb <= 0):
        print 'WWW-unable to find data in: ',ctlpath
        continue


    MF.sTimer("all-%s"%(dtg))

    tdirAdeck='%s/%s/%s'%(abdirDtg,ayear,dtg)
    tdir='%s/%s/%s'%(tmtrkbdir,ayear,dtg)

    if(not(doInv)):
        MF.ChkDir(tdirAdeck,'mk')
        MF.ChkDir(tdir,'mk')

    if(verb): MF.sTimer('tmtrkN-base-%s-%s'%(model,dtg))
    TT=TmTrkSimple(dtg,
                   mdtg,
                   model,
                   atcfname,
                   tdir,
                   ctlpath,
                   taus,
                   md3=md3,
                   tcD=None,
                   tdirAdeck=tdirAdeck,
                   tbdirAdeckStm=abdirStm,
                   ptable=ptable,
                   doClean=doClean,
                   doTrackerOnly=doTrackerOnly,
                   stmopt=stmopt,
                   regridTracker=regridTracker,
                   regridGen=regridGen,
                   override=override,
                   verb=verb,
                   doInv=doInv,
                   )
    if(verb): MF.dTimer('tmtrkN-base-%s-%s'%(model,dtg))
    
    if(doInv):
        MF.sTimer('tmtrkN-inv-%s-%s'%(model,dtg))
        TT.getStatPaths(dolsonly=1)
        TT.doLS()
        MF.dTimer('tmtrkN-inv-%s-%s'%(model,dtg))
        
    elif(doCpTctrk):
            MF.sTimer('tmtrkN-inv-%s-%s'%(model,dtg))
            TT.getStatPaths(dolsonly=1)
            TT.doCP()
            MF.dTimer('tmtrkN-inv-%s-%s'%(model,dtg))
    else:
        
        TT.getStatPaths()
        MF.sTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))
        TT.doTrk(ropt=ropt)
        MF.dTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))
    
        MF.dTimer("all-%s"%(dtg))
