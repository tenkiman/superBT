#!/usr/bin/env python

from sBTtcdiag import *  # imports sBT
#from sbt import  *
#from M2 import setModel2

class MyCmdLine(CmdLine):

    # -- set up here to put in an object
    #

    btau06=0
    etau06=48
    dtau06=6

    btau12=etau06+12
    etau12=168
    dtau12=12
    ndaybackDefault=25

    ttaus=range(btau06,etau06+1,dtau06)+range(btau12,etau12+1,dtau12)

    gaopt='-g 1024x768'

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            #2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'doga':1,
            'dowebserver':1,
            'modelopt':'era5'
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'TDoverride':       ['o:',None,'a','TDoverride invokes tests in lsDiagProc(): test-trkplot | test-htmlonly | test-plot-html'],
            'SSToverride':      ['z',0,1,'override just making oisst -- for old cases when grid changed'],
            'redoLsdiag':       ['R',0,1,'override just running the '],
            'doRealTime':       ['r',1,0,'default is to do real time'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'iVunlink':         ['v',0,1,'unlink invHash pypdb'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doTcFlds':         ['F',0,1,'''doTcFlds -- make f77 input files for lsdiags.x only'''],
            'doTcFc':           ['f',0,1,'''increase taus for forecasting purposes...'''],
            'runInCron':        ['C',0,1,'''being run in crontab'''],
            'doCycle':          ['c',0,1,'cycle by dtgs'],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'doLgemOnly':       ['G',0,1,'doLgemOnly'],
            'doxv':             ['X',0,1,'1 - xv the plot'],
            'doplot':           ['P',1,0,'0 - do NOT make diag plots in lsdiag (now same as jtdiag-plot)'],
            'aidSource':        ['T:',None,'a','aid.source to pull adeck from the adeck_source_year_pypdb'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'getpYp':           ['Y',0,1,'1 - get from pyp'],
            'doclean':          ['k',0,1,'clean off files < dtgopt'],
            'docleanDpaths':    ['K',1,0,'do NOT clean off dpaths for current dtg -- default is to clean'],
            'dohtmlvars':       ['H',0,1,'do html for individual models'],
            'dothin':           ['t',0,1,'dothin -- reduce # of taus .dat files to reduce storage'],
            'lsInv':            ['i',0,1,'ls the inventory'],
            'doInv':            ['I',0,1,'do html for individual models'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'dolsDiag':         ['L',0,1,'do ls the diag file...'],
            'ndayback':         ['n:',self.ndaybackDefault,'i','ndays back to do inventory from current dtg...'],
            'invtag':           ['g:',None,'a','tag to put on inventory file'],
            'zoomfact':         ['Z:',None,'a','zoomfact'],
            'dtype':            ['d:','w2flds','a','default source of fields'],
            'doall':            ['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M:','tmtrkN','a','default tmtrk for trkSource'],
            'TRKoverride':      ['e',0,1,'set override=1 when running tracker to get track using -r option...'],
            'bypassRunChk':     ['y',1,0,'do NOT chkRunning ...'],
            'bmoverride':       ['B',1,0,'do NOT regen the basemaps'],
            'putAdeckOnly':     ['a',0,1,'just write out the adeck...'],
            'selectNN':         ['9',1,0,'default is 1 -- use NN, if 0 use 9X (more operational)'],
            'dobt':             ['b:',0,'i','use BT or working BT 2'],
            'nminWait':         ['W:',30,'i','set number of minutes to wait on other runs'],
            'doEra5sst':        ['5',0,1,'use ERA5 00z daily SST'],
            'doEcm5sst':        ['6',1,0,'make use ECM5 3-d ave SST the default -- oisst broken 20221201'],
            'useFldOutput':     ['U',0,1,'use fldoutput for plotting -- set to 1 for ERA5'],
            'doRoci':           ['p',1,0,'do NOT do roci/poci'],
            

        }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
%s cur-6 gfs2 -l -o test-plot-html  # ls and html & track plot
%s cur12-12 ecm5 -l -o test-trkplot # ls track plot only
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

#MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb):
    print CL.estr
    print CL.opts

prcdir=sbtPrcDirTcdiag
MF.ChangeDir(prcdir,verb=1)
prcdirIships=prcdir

(dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)
# -- get md3
#
yearOpt=None
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
doBT=0
if(doBdeck2): doBT=1
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

cTest=(len(dtgs) == 1 and len(modelsDiag[dtgs[0]]) == 1)

if(doCycle and not(cTest)):
    MF.sTimer('ALL-cycle-%s'%(dtgopt))
    for dtg in dtgs:
        
        models=modelsDiag[dtg]
        for model in models:
            
            overopt=''
            #if(override): overopt='-O'
            cmd="%s %s %s %s -y"%(pyfile,dtg,model,overopt)
            #print cmd
            for o,a in CL.opts:
                if(o != '-c'):
                    cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)    

    MF.dTimer('ALL-cycle-%s'%(dtgopt))
    sys.exit()
    
    
if(dolsDiag): dols=1
if(dols or dolsDiag): 
    bypassRunChk=1    
    doRoci=0

if(not(doCycle) and not(bypassRunChk)):
    rc=MF.chkRunning(pyfile, strictChkIfRunning=1, verb=0, killjob=0, 
                     timesleep=10, nminWait=nminWait)

    if(rc > 1 and not(dols) and not(bypassRunChk)):
        print 'AAA allready running...'
        sys.exit()


xgrads=setXgrads(useStandard=1)


# -- do inventory if cur in dtgopt
#
doInvAtEnd=0
if((mf.find(dtgopt,'cur') or mf.find(dtgopt,'ops') or runInCron) and not(dols) ): doInvAtEnd=1


# -- grads processing object
#

gaP=GaProc(Quiet=quiet,Bin=xgrads)

useLsdiagDat=0
if(redoLsdiag): useLsdiagDat=1



# -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm dtg loop
#

didIt=0

for dtg in dtgs:

    MF.sTimer(tag='SBT-LSDIAG-%s'%(dtg))
    # -- 20230314 -- will miss storms with missing dtgs...
    #    see inv/dtgmiss/m-B-2007-22.txt 
    #    need to add interpolated dtgs into 'all-md3-2007-2022-MRG.csv'
    #
    dstmids=md3.getMd3Stmids4dtg(dtg,convertXstm=1)
    
    # -- only track in stmopt
    #
    if(stmopt != None):
        m3stmids=md3.getMd3Stmids(stmopt)
        # -- use trk to find the stmids by dtg
        #
        nstmids=[]
        for m3stmid in m3stmids:
            (rc,m3trk)=md3.getMd3track(m3stmid)
            if(dtg in m3trk.keys()):
                nstmids.append(m3stmid)
        dstmids=nstmids
        if(len(nstmids) == 0):
            print 'EEE could find stmids for stmopt:',stmopt,' dtg: ',dtg,'sayounara...'
            sys.exit()


    models=modelsDiag[dtg]
    year=dtg[0:4]
    tbdir=TcTcanalDatDir
    tbdirInv="%s/%s/INV"%(tbdir,year)
    MF.ChkDir(tbdirInv,'mk')
    
    # -- inventory object
    #
    dbname='invTcdiag.%s'%(dtg)
    
    iV=InvHash(dbname=dbname,
               tbdir=tbdirInv,
               override=override,
               lsInv=lsInv,
               unlink=iVunlink)

    if(lsInv):
        iV.lsInv(models,dtg)
        if(dtg == dtgs[-1]):
            sys.exit()

    # -- check how old this run -- if 'tooold' force regen
    #
    HH=dtg[8:10] 

    itaus=CL.ttaus

    # -- defaults non era5
    #
    doSfc=0
    doTrkPlot=1
    
    atcfname=None
    if(modelopt == 'era5'): 
        doRealTime=0
        trkSource='tmtrkN'
        trkSource='tmtrkN-sbt'
        #docleanDpaths=1
        doSfc=1
        doTrkPlot=1
        itaus=[0,6,12,18,24]
        if(doTcFc):
            itaus=[0,6,12,18,24,36,48,60,72]
        useFldOutput=1
        atcfname='tera5'
        
    
    for model in models:

        iyear=int(dtg[0:4])
        if(model == 'era5' and iyear <= endEra5Year):
            doEra5sst=1

        print 'DDDDDDDDDDDDD doing dtg: ',dtg,' model: %-10s'%(model),' trkSource: ',trkSource,'dstmids: ',dstmids
        if(ropt == 'norun'): continue

        if(not(dols)):

            if(verb): MF.sTimer('setModel2: %s dtg: %s'%(model,dtg))
            m=setModel2(model)
            fm=m.DataPath(dtg,dtype=dtype,diag=1)
            fd=fm.GetDataStatus(dtg)

            if(HH == '00' or HH == '12'):
                minTau=modelMinTau0012[model]
            else:
                minTau=modelMinTau0618[model]

            if(verb): MF.dTimer('setModel2: %s dtg: %s'%(model,dtg))

            # -- check if mintau available
            #
            if(fd.dslatestCompleteTau < minTau and not(dothin)):
                print 'WWW(fd.dslatestCompleteTau): ',fd.dslatestCompleteTau,' is < minTau: ',minTau,' model: ',model,' continue...'
                #continue

        dobail=0
        if(ropt == 'norun'): dobail=0
        MF.sTimer('tcdiag')
        tG=TcDiagS(dtg,model,
                  ttaus=itaus,
                  gaopt=CL.gaopt,
                  domandonly=domandonly,
                  doStndOnly=doStndOnly,
                  doDiagOnly=doDiagOnly,
                  dols=dols,
                  tbdir=tsbdbdir,
                  dowebserver=dowebserver,
                  trkSource=trkSource,
                  selectNN=selectNN,
                  dstmids=dstmids,
                  atcfname=atcfname,
                  dobt=dobt,
                  dobail=dobail,doshort=dothin,
                  adeckSdir=adeckSdir,
                  useLsdiagDat=useLsdiagDat,
                  xgrads=xgrads,
                  tD=None,
                  md3=md3,
                  doSfc=doSfc,
                  doRoci=doRoci,
                  sbtProdDir=sbtProdDir,
                  doga=0,verb=verb)


        # -- 20230607 -- clean all files if override -- to overcome problem of redos with storms in all hemis
        #
        if(override):
            tG.cleanLsdiagAll()
            

        if(tG.ctlStatus == 0):
            print 'WWW--w2.tc.lsdiag--tG.ctlStatus=0 '
            sys.exit()
        
        # -- check if done
        #
        chkOquiet=0
        (rc,todoStmids)=tG.chKOutput(iV,dstmids,aidSource=aidSource,quiet=chkOquiet)
        
        if(dols):
            print 'dols only rc: ',rc
            print '  todoStmids: ',todoStmids
            continue

        if(rc == -2):
            print 'WWW(chKOutput) 22222 rc: ',rc,'need to do the following: ',todoStmids
        elif( (rc == 0) and not(override) and not(SSToverride) and not(redoLsdiag) and TDoverride == None and not(dols) ):
            print 'WWW(chKOutput) 00000 rc: ',rc,' override: ',override,' SSToverride: ',SSToverride,'TDoveride: ',TDoverride,'redoLsdiag: ',redoLsdiag,'dols: ',\
                  dols,'docleanPaths: ',docleanDpaths,' continue...'
            continue        
        
        tG.grads21Cmd=xgrads
        tG.md3=md3
        tG.prcdir=prcdir
        MF.dTimer('tcdiag')

        # -- get storms and make sure ctlpath there...
        #
        ctlpath=tG.ctlpath

        if(ropt == 'norun'):  continue

        # -- check if a data tau 0
        #
        if(not(0 in tG.targetTaus)):
            print 'EEE no data tau0...continue...',ctlpath
            #continue
            sys.exit()

        # -- input fields
        #
        MF.sTimer('tcfldsdiag:%s:%s'%(dtg,model))

        # -- set taus based on available data, not ttaus
        #
        doregrid=1

        if(model == 'era5' and doSfc):
            # -- 20200405 -- for better vmax/rmax calc -- now works in TcFldsDiag
            #
            dlatRegrid=0.25
            dlonRegrid=0.25

        else:
            # -- 20200406 -- use coarser grid...less i/o...and use tracker vmax vice tcdiag vmax in plots
            #
            dlatRegrid=0.50
            dlonRegrid=0.50


        mfT=TcFldsDiag(dtg,model,ctlpath,
                       ctlpath2=tG.ctlpath2,
                       taus=tG.targetTaus,
                       tauoffset=tG.tauOffset,
                       dstmids=dstmids,
                       tbdir=tG.tbdir,
                       dlat=dlatRegrid,
                       dlon=dlonRegrid,
                       doregrid=doregrid,
                       Quiet=quiet,
                       dols=dols,
                       doSfc=tG.doSfc,
                       verb=verb,
                       )
        MF.dTimer('tcfldsdiag:%s:%s'%(dtg,model))

        if(mfT.status == 0):
            print 'mfT.status = 0'
            continue
        
        if(not(mfT.sstDone and mfT.meteoDone) or override or SSToverride):

            MF.sTimer('fldinput:%s:%s'%(dtg,model))
            # -- start grads; decoreate the tG object (TcDiag()); open fld ctlpath
            mfT.makeFldInputGA(gaP)
            
            # -- SST
            #
            overrideSST=0
            if(override or SSToverride): overrideSST=1
            
            if(doEra5sst):
                mfT.makeEra5sst(override=overrideSST)
            elif(doEcm5sst):
                mfT.makeEcm5sst(override=overrideSST)
            else:
                mfT.makeOisst(override=overrideSST)
            
            # -- meteo
            #
            mfT.makeFldInput(override=override,
                             verb=verb,doconst0=0,dogetValidTaus=0)
            # -- get the data status
            #
            mfT.getDpaths(verb=verb,useAvailTaus=1)
            
            # -- reinit ga
            #
            mfT.reinitGA(gaP)
            MF.dTimer('fldinput:%s:%s'%(dtg,model))
            



        # -- setup .ga using field output file
        #
        if(doplot):
            # -- use the fld output ctl to plot...if set at command line
            # -- use full res ctl to plot
            #
            tG.useFldOutput=useFldOutput
            if(tG.useFldOutput):
                tG.ctlpath=mfT.ctlpathFldOutput

            # -- get the sst ctl...
            #tG.oisstCtlpath=tG.ctlpath.replace(model,'oisst')

            # -- from jtdiag-plot ... use sstcpath from...
            #
            tG.oisstCtlpath=mfT.sstcpath
            
            # -- make new ga,ge using new tG.ctlpath
            tG.initGA(tG.gaopt)


        # -- if we got this far, we're going to do something...
        #
        didIt=didIt+1

        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # -- cycle by stmids
        #
        for stmid in dstmids:

            # -- get tctracker and make tc meta file -- this sets the aid and source for setDiagPath
            #
            
            #if(tG.setTCtracker(stmid,aidSource,quiet=0) == 0):
            if(tG.setTCtracker(stmid,aidSource,quiet=0,verb=verb) == 0):
                #didIt=doInvAtEnd=0 #-- don't really need to kill inventory
                print 'III(%s) cycling by storms for dtg: %s model: %s no tracker continue to next stmid...'%(pyfile,dtg,model)
                continue

            rc=tG.makeTCmeta(tdir=mfT.tdir,taus=mfT.meteoTausDone)

            # -- set diagfile output path
            #
            (rc,dtime,dpath)=tG.setDiagPath(stmid,tdir=mfT.tdir)

            # -- run fortran
            #
            MF.sTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))
            rcLsDiag=runLsDiag(mfT,tG)
            MF.dTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))

            if(rcLsDiag == 0):
                print 'EEE -- problem in either sst or meteo file'
                sys.exit()

            # -- 20230324 -- don't run of lgem...for ERA5
            # -- run iships.x fortran app (ships/lgem)
            #
            #MF.sTimer('iships.x:%s:%s:%s'%(dtg,model,stmid))
            #runLgem(dpath,tG,dtg,model,stmid,
                    #prcdir=prcdir,
                    #prcdirIships=prcdirIships,
                    #verb=1)
            #MF.dTimer('iships.x:%s:%s:%s'%(dtg,model,stmid))

            # -- parse output ; this sets tG.taus
            #
            tG.parseDiag(stmid,dobail=0,verb=verb)

            # -- make plots; set the ctlpath to lsdiag binary
            #
            if(doplot):

                # -- condition for overrideing precip plot which makes the roci
                #
                
                overridePlot=0
                if(redoLsdiag or override): overridePlot=1
                
                MF.sTimer('plots')
                plat1=plat2=plon1=plon2=None
                print 'sssss',stmid.lower()
                if(stmid.lower() == '13l.1975'):
                    plat1=5.0
                    plat2=45.0
                    plon1=255.0
                    plon2=320.0

                for tau in tG.taus:
                    
                    rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau,
                                             lat1=plat1,lat2=plat2,lon1=plon1,lon2=plon2)
                    if(rc < 0):
                        print 'ETETET -- too far poleward, bail...stop doing PLOTS'
                        continue
                        
                    if(bmoverride): tG.pltBasemap(bmoverride=1)
                    
                    MF.sTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                    tG.pltShear(override=override)
                    tG.pltDiv200(override=override)
                    tG.pltPrw(override=override)
                    tG.pltVmax(override=override)
                    tG.pltSst(override=override)
                    # -- always override precip plot to get roci/poci
                    tG.pltPrecip(override=overridePlot)
                    tG.pltVort850(override=override)
                    MF.dTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                         

                # -- parse diag to get urls for plots
                #
                tG.parseDiag(stmid,dobail=0)

                MF.dTimer('plots')


            # -- do track plot -- this resets the open files
            #
            if(doTrkPlot):
                MF.sTimer('tGtrk:%s:%s:%s'%(dtg,model,stmid))
                TRKplotoverride=0
                if(redoLsdiag or doplot): TRKplotoverride=1
                tGtrk=TcTrkPlot(tG,md3,stmid,zoomfact,doveribt=0,override=TRKplotoverride,verb=verb,Bin=xgrads)
                MF.dTimer('tGtrk:%s:%s:%s'%(dtg,model,stmid))

            # -- do html if NOT ERA5
            #
            if(model != 'era5'):
                tGh=TcDiagHtml(tG,tGtrk)
                tGh.doHtml()
                # -- old w2.tc.flddiag.py tGh.doPyp()

                tGhs=TcDiagHtmlVars(tG,verb=verb,keepmodels=keepmodels)
                tGhs.doHtml()
                
            # -- put adecks and diagfiles
            #
            tG.putAdeckCards(stmid,verb=verb)



        # -- 20221110 -- do all rocis here vice TcDiag()
        #
        MF.sTimer('pickle-rocis')
        
        kk=tG.AllRocis.keys()
        kk.sort()
        for k in kk:
            print 'rrr',k,tG.AllRocis[k]

        rociPypPath="%s/roci.%s.%s.pyp"%(tG.tdir,tG.model,tG.dtg)
        rociPS=open(rociPypPath,'w')
        pyp=tG.AllRocis
        pickle.dump(pyp,rociPS)
        rociPS.close()
        MF.dTimer('pickle-rocis')

        # -- load inventory
        #
        (rc,todoStmids)=tG.chKOutput(iV,dstmids,aidSource=aidSource,quiet=1)

        # -- blow away ga2 here...
        #
        if(hasattr(tG,'ga2')): tG.ga2('quit')

        # -- make a sfc data set with uas/vas/psl/pr/prc
        #
        tG.makePrPrcSfcData()

        # -- clean dpaths
        #
        if(docleanDpaths):
            MF.sTimer('tcfldscleandpaths:%s:%s'%(dtg,model))
            mfT.cleanDpaths(ropt=ropt)
            MF.dTimer('tcfldscleandpaths:%s:%s'%(dtg,model))

            

    # -- run lats4d -- 20230314  -- disable during catchup
    #
    #roptLats='norun'
    #cmd='p-lats4d.py %s'%(dtg)
    #mf.runcmd(cmd,roptLats)

    MF.dTimer(tag='SBT-LSDIAG-%s'%(dtg))
            
# -- rsync over from web-config/tcdiag/YYYY to $W2_HFIP...
#
if(ropt != 'norun' and model != 'era5'):
    rc=rsync2data()

# -- do inventory for tcdiag.php
#
if(((didIt > 0 and doInvAtEnd) or doInv) and not(dols) and dowebserver ):
    MF.sTimer(tag='tGinventory')
    tGi=TcdiagInv(tG,ndayback=ndayback,verb=verb)
    MF.dTimer(tag='tGinventory')
    MF.sTimer('rsync-tcdiag')
    rc=rsync2Wxmap2('tcdiag')
    MF.dTimer('rsync-tcdiag')
    

