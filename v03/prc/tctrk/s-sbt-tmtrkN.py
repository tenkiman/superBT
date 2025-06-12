#!/usr/bin/env python

#from tcbase import *
#from WxMAP2 import *
#w2=W2()

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

def rsyncEra2Local(dtg):
        
    MF.sTimer('Local-TCtrk-rsync-%s' % (dtg))

    # -- for era5 use pull previous 00/12 run if 06/18
    #
    eradtg = dtg
    if(is0618Z(dtg)):
        eradtg = mf.dtginc(dtg, -6)
        
    year=eradtg[0:4]
    if(sbtHost != 'mike5'):
        sdirE2  = 'fiorino@mike5:/raid01/dat/nwp2/w2flds/dat/era5/%s/%s' % (year, eradtg)
        sdirE = '/mnt/mike5-mnt/USB3RAID5-01/dat/nwp2/w2flds/dat/era5/%s/%s'%(year,eradtg)
    else:
        sdirE = '/raid01/dat/nwp2/w2flds/dat/era5/%s/%s' % (year, eradtg)
        
    tdirE = "%s/nwp2/w2flds/dat/era5/%s/%s" % (sbtDatDirL, year, eradtg)
    era5bdir= "%s/nwp2/w2flds/dat/era5" % (sbtDatDirL)
    rc = MF.ChkDir(tdirE, 'mk')
    
    cmdE = "rsync -alv %s/ %s/" % (sdirE, tdirE)
    mf.runcmd(cmdE, ropt)

    MF.dTimer('Local-TCtrk-rsync-%s' % (dtg))
    return(tdirE,era5bdir)



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
            'doClean':          ['K',1,0,'1 do NOT clean'],            
            'doBail':           ['B',0,1,'1 bail if no era5 fields'],            
            'doInv':            ['i',0,1,'do Inventory'],            
            'doCpTctrk':        ['P',0,1,'make the tctrk.atcf|sink.dtg.txt from adeck_stm -> adeck_dtg'],            
            'doLocal':          ['C',0,1,'''run on local filesystem in /sbt/local'''],
            
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

prcdir=sbtPrcDirTctrk
MF.ChangeDir(prcdir,verb=verb)

# -- lllllllllllllllllllllllllllllllllllll -- set local dirs
#
if(doLocal):
    tsbdbdir = tsbdbdirL
    tmtrkbdir= tmtrkbdirL
    abdirDtg=abdirDtgL
    abdirStm=abdirStmL
    
#    
# -- lllllllllllllllllllllllllllllllllllll -- set local dirs

if(not(doInv)):
    MF.ChkDir(tmtrkbdir,'mk')
    MF.ChkDir(abdirStm,'mk')
    MF.ChkDir(abdirDtg,'mk')

if(verb):
    print 'pppDDD',prcdir
    print 'tttBBB',tmtrkbdir
    print 'aaaSSS',abdirStm
    print 'aaaDDD',abdirDtg
    
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
yearOpt=None
doBT=0
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
if(doBdeck2): doBT=1

# -- doBT set in md3.getCvsYearPaths vice at initiation
#
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

for dtg in dtgs:

    tdtg=dtg
    if(IsBadEra5Dtg(tdtg) == 0):
        print 'EEE---BBB era5 dtg...press...'
        continue

    ayear=dtg[0:4]
    mmdd=dtg[4:8]
    
    (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg,maxtau=maxtau,verb=verb,doSfc=0,doBail=doBail)

    # -- special case of no 022900 for 1952 1956
    #
    if((ayear == '1952' or ayear == '1956') and mmdd == '0229'):
        hh=dtg[-2:]
        if(hh == '00'):
            tauOffset=24
        elif(hh == '06'):
            tauOffset=30
        elif(hh == '12'):
            tauOffset=36
        elif(hh == '18'):
            tauOffset=42
            
        print 'SSS--special case: for dtg: ',dtg,' tauOffset: ',tauOffset
    # -- model dtg whe tauOffset=6
    #
    if(tauOffset != None):
        mdtg=mf.dtginc(dtg,-tauOffset)
    else:
        mdtg=dtg

    if(tauOffset > 0):
        (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,mdtg,maxtau=maxtau,verb=verb,doSfc=0,doBail=doBail)

    # -- get era5 fields and tmtrkN output to local -- llllllllllllllllllllllllllllllllllllllllllll
    # -- IIFF there are storms
    #
    if(doLocal): 
        (tdirE,era5bdir) = rsyncEra2Local(dtg)

    rc=getEra5Grb(era5bdir,mdtg,model='era5')
    (ctlpath2,sizgrb,ctlpath2a,sizgrb2a)=rc
    
    if(sizgrb <= 0):
        if(not(doInv)): print 'WWW-unable to find data in: ',ctlpath
        continue

    MF.sTimer("sbt-tmtrkN-%s"%(dtg))

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
                   prcdir=prcdir,
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
                   doBdeck2=doBdeck2,
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
        # -- should I do this here? -- yes, for case when not override, but redoing...
        # -- NNOO!! if not override
        #TT.getStatPaths(dolsonly=1)
        #TT.doCP()
        MF.dTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))


    if(doLocal):
        cmd = "rm %s/*" % (tdirE)
        mf.runcmd(cmd, ropt)
    
    MF.dTimer("sbt-tmtrkN-%s"%(dtg))
