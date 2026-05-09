#!/usr/bin/env python

#from tcbase import *
#from WxMAP2 import *
#w2=W2()

from sBTtctrkS import TmTrkSimple
from sBT import *

def getEra5Grb(era5bdir,dtg,model='era5'):
    
    year=dtg[0:4]
    
    if(model == 'era5'):
        
        grbpath="%s/%s/%s/%s-w2flds-%s-ua.grb2"%(era5bdir,year,dtg,model,dtg)
        ctlpath="%s/%s/%s/%s-w2flds-%s-ua.ctl"%(era5bdir,year,dtg,model,dtg)
        sizgrb=MF.getPathSiz(grbpath)
        sizctl=MF.getPathSiz(ctlpath)

        grbpath2="%s/%s/%s/%s-w2flds-%s-sfc.grb"%(era5bdir,year,dtg,model,dtg)
        ctlpath2="%s/%s/%s/%s-w2flds-%s-sfc.ctl"%(era5bdir,year,dtg,model,dtg)
        sizgrb2=MF.getPathSiz(grbpath2)
        sizctl2=MF.getPathSiz(ctlpath2)
        
    elif(model == 'ecop'):
        
        
        grbmask="%s/%s/%s/*w2flds*%s*.grb2"%(era5bdir,year,dtg,dtg)
        grbs=glob.glob(grbmask)
        ngrbs=len(grbs)
        if(ngrbs > 0):
            grbpath=grbs[0]

        ctlpath="%s/%s/%s/%s-w2flds-%s.ctl"%(era5bdir,year,dtg,model,dtg)
        sizgrb=MF.getPathSiz(grbpath)
        sizctl=MF.getPathSiz(ctlpath)
        
        grbpath2=grbpath
        ctlpath2=ctlpath
        sizgrb2=sizgrb
        sizctl2=sizctl
        
    
    return(ctlpath,sizgrb,ctlpath2,sizgrb2)

def rsyncEra2Local(dtg,model='era5',doRsync=1):
        
    MF.sTimer('Local-TCtrk-rsync-%s' % (dtg))

    # -- for era5 use pull previous 00/12 run if 06/18
    #
    eradtg = dtg
    if(is0618Z(dtg)):
        eradtg = mf.dtginc(dtg, -6)
        
    year=eradtg[0:4]
    if(model == 'era5'):
        sdirE = '/raid01/dat/nwp2/w2flds/dat/%s/%s/%s' % (model,year, eradtg)
    elif(model == 'ecop'):
        sdirE = '/raid02/dat/nwp2/w2flds/dat/%s/%s/%s' % (model,year, eradtg)
            
        
    tdirE = "%s/nwp2/w2flds/dat/%s/%s/%s" % (sbtDatDirL, model, year, eradtg)
    era5bdir= "%s/nwp2/w2flds/dat/%s" % (sbtDatDirL,model)
    rc = MF.ChkDir(tdirE, 'mk')
    if(doRsync):
        ropt=''
    else:
        ropt='norun'
        
    cmdE = "rsync -alv %s/ %s/" % (sdirE, tdirE)
    mf.runcmd(cmdE, ropt)

    MF.dTimer('Local-TCtrk-rsync-%s' % (dtg))
    return(tdirE,era5bdir)

def specCaseTauOffset(dtg,tauOffset):
    
    """special case of no 022900 for 1952 1956
"""

    ayear=dtg[0:4]	
    mmdd=dtg[4:8]

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
        dtg=mf.dtginc(dtg,-tauOffset)
        print 'SSS--special case: for dtg: ',dtg,' tauOffset: ',tauOffset
            
    return(ayear,tauOffset)

def getMdtgMtaus(dtg,taus,tauOffset):

    """20260507 -- make a dictionary between model taus and tracker taus
"""
    
    mdtg=dtg
    if(tauOffset > 0):
        mdtg=mf.dtginc(dtg,-tauOffset)

    tauOff=mf.dtgdiff(mdtg,dtg)
    mtauOff=int(tauOff)
    mtaus={}
    
    if(taus == None):
        print 'OOOPPPSSS -- no data form dtg: ',dtg,'sayounara baby'
        sys.exit()
        
    for tau in taus:
        mtau=tau+mtauOff
        if(mtau in taus):
            mtaus[tau]=mtau
        else:
            mtaus[tau]=tau
        
    if(verb):
        mm=mtaus.values()
        mm.sort()
        print 'mmtaukeys',mm
        print 'tttaaauuu',taus
        
    if(tauOffset > 6):
        print 'EEooppss tauOffset: ',tauOffset,' for dtg: ',dtg,' too big???'
        sys.exit()
    
    return(mdtg,mtaus)

def rsyncTrk2Sbt(dtg,ropt=''):
    
    MF.sTimer('R2S-%s'%(dtg))
    year=dtg[0:4]
    rsyncOpt='-alv'
    cmd='rsync %s %s/%s/ %s/%s/'%(rsyncOpt,tmtrkbdirL,year,tmtrkbdirS,year)
    mf.runcmd(cmd,ropt)
    cmd='rsync %s %s/%s/ %s/%s/'%(rsyncOpt,abdirDtgL,year,abdirDtgS,year)
    mf.runcmd(cmd,ropt)
    cmd='rsync %s %s/%s/ %s/%s/'%(rsyncOpt,abdirStmL,year,abdirStmS,year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('R2S-%s'%(dtg))
    
    return(1)

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
            'modelOpt':         ['m:','era5','a','set model for era5 or ecop'],
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
tsbdbdirS  = tsbdbdir
tmtrkbdirS = tmtrkbdir
abdirDtgS  = abdirDtg
abdirStmS  = abdirStm

if(doLocal):
    tsbdbdir  = tsbdbdirL
    tmtrkbdir = tmtrkbdirL
    abdirDtg  = abdirDtgL
    abdirStm  = abdirStmL
    
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

if(modelOpt == 'era5'):
    model='era5'
    atcfname='tera5'
elif(modelOpt == 'ecop'):
    model='ecop'
    atcfname='tecop'
    
# -- set tracker properties
#
regridTracker=0.50
regridGen=0.5
maxtau=168

# -- get md3
#
yearOpt=None
doBT=0
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
if(doBdeck2): doBT=1

# -- doBT set in md3.getCvsYearPaths vice at initiation
#
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

# -- cycle dtgs
#

for dtg in dtgs:

    tdtg=dtg
    if(IsBadEra5Dtg(tdtg) == 0):
        print 'EEE---BBB era5 dtg...press...'
        continue

    # -- 20260507 -- details handled in getCtlpathTaus() 
    #    and dtg of valid .ctl found here!!  Ditto for mdtg and mtaus
    #
    (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg,maxtau=maxtau,verb=verb,
                                                    doSfc=0,doBail=doBail)

    (ayear,tauOffset)=specCaseTauOffset(dtg,tauOffset)
    (mdtg,mtaus)=getMdtgMtaus(dtg,taus,tauOffset)


    # -- set target dirs
    #
    tdirAdeck='%s/%s/%s'%(abdirDtg,ayear,dtg)
    tdir='%s/%s/%s'%(tmtrkbdir,ayear,dtg)
    
    tdirAdeckS='%s/%s/%s'%(abdirDtgS,ayear,dtg)
    tdirS='%s/%s/%s'%(tmtrkbdirS,ayear,dtg)

    if(not(doInv)):
        MF.ChkDir(tdirAdeck,'mk')
        MF.ChkDir(tdir,'mk')

    # -- make the tracker obj using sBT directories
    #
    if(verb): MF.sTimer('tmtrkN-base-%s-%s'%(model,dtg))
    TT=TmTrkSimple(dtg,
                   mdtg,
                   model,
                   atcfname,
                   tdirS,
                   ctlpath,
                   mtaus,
                   taus,
                   md3=md3,
                   prcdir=prcdir,
                   tcD=None,
                   tdirAdeck=tdirAdeckS,
                   tbdirAdeckStm=abdirStmS,
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

    # -- get tracker status...determine if to run...
    #
    TT.doLocal=0
    TT.getStatPaths()
    doItSbt=TT.setStatus(quiet=1)
    
    if(doLocal):
        TT.tdir=tdir
        TT.tdirAdeck=tdirAdeck
        TT.tbdirAdeckStm=abdirStm
        TT.doLocal=doLocal

        TT.getStatPaths()
        doIt=TT.setStatus(quiet=1)
    
    trkRopt='norun'
    if( (doItSbt and ropt =='') or override):
        trkRopt=''

    if(trkRopt != ''):
        print 'DONE:doIt: ',doItSbt,'ropt: ',ropt,'override: ',override
        sys.exit()

    # -- get era5 fields and tmtrkN output to local -- llllllllllllllllllllllllllllllllllllllllllll
    # -- IIFF there are storms
    #
    if(doLocal): 
        (tdirE,era5bdir) = rsyncEra2Local(dtg,model=model,doRsync=doIt)

    rc=getEra5Grb(era5bdir,mdtg,model=model)
    (ctlpath2,sizgrb,ctlpath2a,sizgrb2a)=rc
    
    if(sizgrb <= 0):
        if(not(doInv)): print 'WWW-unable to find data in: ',ctlpath
        continue

    MF.sTimer("sbt-tmtrkN-%s"%(dtg))
    
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
            
    # -- DO the tttrrrkkk 
    else:
        TT.getStatPaths()
        MF.sTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))
        TT.doTrk(ropt=trkRopt)
        # -- should I do this here? -- yes, for case when not override, but redoing...
        # -- NNOO!! if not override
        #TT.getStatPaths(dolsonly=1)
        #TT.doCP()
        MF.dTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))


    if(doLocal and trkRopt == ''):
        cmd = "rm %s/*" % (tdirE)
        mf.runcmd(cmd, trkRopt)
        rc=rsyncTrk2Sbt(dtg, trkRopt)
    
    MF.dTimer("sbt-tmtrkN-%s"%(dtg))
