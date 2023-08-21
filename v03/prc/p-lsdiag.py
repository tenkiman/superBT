#!/usr/bin/env python


#from sBTtcdiag import *  # imports tcbase
#from sbt import *

from sBT import *

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
            #1:['dtgopt',  'run dtgs'],
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
            'dtgopt':           ['d:',None,'a','dtgopt'],
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
purpose -- lsdiag input to superBT '''
        
        self.examples='''
%s -S w.17
%s -S e,c.17-19'''


def makeOcard(dtg,tau,stmid,ostmd,ocusd,ocusNames,osndd,
              poci,roci,pocip1,rocip1,
              verb=0):
    
    if(verb): print 'ddd',dtg,tau,poci,roci,pocip1,rocip1
    vdtg=mf.dtginc(dtg,tau)
    hcard="lsdiag: %s %s "%(vdtg,stmid)
    
    stmcard="STM:"
    stmcard="S:"
    
    kk=ostmd.keys()
    kk.sort()
    for k in kk:
        if(verb): print 'stm: ',k,ostmd[k]
        if(mf.find(k,'sst')):
            if(ostmd[k] == undef):
                oval=-999.
                stmcard=stmcard+" %s: %4.0f"%(k,oval)
            else:
                if(abs(ostmd[k]) > 500.0):
                    oval=undef
                    stmcard=stmcard+" %s: %4.0f"%(k,oval)
                else:
                    oval=ostmd[k]*0.1
                    stmcard=stmcard+" %s: %4.1f"%(k,oval)
        elif(mf.find(k,'land')):
            stmcard=stmcard+" %s: %5.0f"%(k,ostmd[k])
        elif(mf.find(k,'max_wind')):
            stmcard=stmcard+" %s: %4.0f"%(k,ostmd[k])
        elif(mf.find(k,'shr_m')):
            stmcard=stmcard+" %s: %3.0f"%(k,ostmd[k])
        elif(mf.find(k,'vort') or mf.find(k,'dvr')):
            stmcard=stmcard+" %s: %5.0f"%(k,ostmd[k])
        elif(mf.find(k,'tpw')):
            stmcard=stmcard+" %s: %-5.0f"%(k,ostmd[k])
        else:
            stmcard=stmcard+" %s: %-4.0f"%(k,ostmd[k])
            
    
    kk=ocusd.keys()
    
    if(verb):
        for k in kk:
            print 'cus: ',ocusNames[k],ocusd[k]
    
    ckks=[5,16,11,12,13]
    cuscard="CUS:"
    cuscard="C:"
    for k in ckks:
        nvar=ocusNames[k]
        var=ocusd[k]
        if(k == 5): 
            if(var == undef):
                var=-999.
                cuscard=cuscard+" %s: %-4.0f "%(nvar,var)
            else:
                var=var*0.1
                cuscard=cuscard+" %s: %4.1f "%(nvar,var)
        elif(k == 16): 
            var=var*1.
            cuscard=cuscard+" %s: %4.0f "%(nvar,var)
        elif(k == 11): 
            var=var*1.
            cuscard=cuscard+" %s: %3.0f "%(nvar,var)
        elif(k == 12 or k == 13): 
            var=var*1.
            cuscard=cuscard+" %s: %4.0f "%(nvar,var)
        else:
            cuscard=cuscard+" %s: %3.0f "%(nvar,var)
            
    
    sndcard="SND: "
    sndcard=" D:"
    kk=osndd.keys()
    for k in kk:
        if(verb): print 'snd: ',k,osndd[k]
        sndcard=sndcard+" %s %-5.0f"%(k,osndd[k])
        
    prcard='Poci_roci: %4.0f_%-3.0f  Poci_roci_p1: %4.0f_%-3.0f'%(poci,roci,pocip1,rocip1)

    if(verb):
        print stmcard
        print cuscard
        print sndcard
        print prcard
        
    
    ocard=hcard+stmcard+cuscard+sndcard+prcard
    #ocard=ocard.replace('    ',' ')
    #ocard=ocard.replace('   ',' ')
    return(ocard)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb):
    print CL.estr
    print CL.opts

prcdir='%s/prc/tcdiag'%(curdir)
prcdirIships=prcdir

md3=Mdeck3()

if(stmopt != None):
    istmopt=stmopt
    stmopts=getStmopts(stmopt)
    tstmids=[]
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt)
else:
    print 'EEE- must set stmopt'
    sys.exit()

# -- topside settings
#

model='era5'
dols=1
doRealTime=0
trkSource='tmtrkN-sbt'
docleanDpaths=0
doSfc=1
doTrkPlot=0
itaus=[0,6,12,18,24]
useFldOutput=1
atcfname='tera5'


#MF.ChangeDir(prcdir)
    
if(dolsDiag): dols=1
if(dols or dolsDiag): bypassRunChk=1    

useLsdiagDat=0
if(redoLsdiag): useLsdiagDat=1

didIt=0
mcards=[]

missPath="%s/inv/lsdiag/inv-missing-lsdiag-%s.txt"%(curdir,istmopt)

for tstmid in tstmids:

    (rc,mcard)=md3.getMd3StmMeta(tstmid)
    (yyyy,stm,livestatus,tctype,sname,ovmax,tclife,stmlife,latb,lonb,bdtg,edtg,
     latmn,latmx,lonmn,lonmx,
     stcd,oACE,
     nRI,nED,nRW,
     RIstatus,timeGen,stm9x,ogendtg)=rc
    
    ocards=[]
    
    tyear=rc[0]
    stm3id=rc[1]
    tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
    opaths=glob.glob("%s"%(tmask))

    # -- 20230412 -- handle case where one 9X is the one for two NN storms
    #    happens in the LANT/EPAC several times, 2016

    odirLss=[]
    
    if(len(opaths) == 1):
        odirLss.append(opaths[0])
    elif(len(opaths) == 2):
        odirLss.append(opaths[0])
        odirLss.append(opaths[1])
    else:
        print 'EEE no or more than 2 sbt/src output dirs for: ',tstmid,' tmask: ',tmask
        sys.exit()
        
    if(len(odirLss) == 2):
        print 'III'
        print 'III -- multiple DEV from ONE 9X -- happens in LANT/EPAC...for tstmid: ',tstmid
        print 'III'
        
    for odirLs in odirLss:
        
        if(IsNN(tstmid)):
            (rc,m3trk)=md3.getMd3track(tstmid,dobt=1)
        else:
            (rc,m3trk)=md3.getMd3track(tstmid)
            
        if(rc != 1):
            print 'EEE-md3 getMd3track for tstmid: ',tstmid
            sys.exit()
        
        dtgs=m3trk.keys()
        dtgs.sort()
        
        oLspath="%s/lsdiag-md3-%s-MRG.txt"%(odirLs,stm3id)
        
        osiz=MF.getPathSiz(oLspath)
        if(osiz > 0 and not(override)):
            print 'oLspath: ',oLspath,'already done...press...not override...'
            continue
        
        for dtg in dtgs:
    
            tyear=dtg[0:4]
            tdir="%s/%s/%s/%s"%(tsbdbdir,tyear,dtg,model)    
        
            # -- don't need anymore since we run every hour
            #
            #if(w2.is0618Z(dtg)): continue
        
            iyear=int(dtg[0:4])
            if(model == 'era5' and iyear <= 2021):
                doEra5sst=1
        
            #print 'DDDDDDDDDDDDD doing  stmid:',tstmid,'dtg: ',dtg,' model: %-10s'%(model)
            if(ropt == 'norun'): continue
        
            dobail=0
            if(ropt == 'norun'): dobail=0
            MF.sTimer('tcdiag')
    
    
                
            tdmask="%s/tcdiag.*%s*"%(tdir,tstmid.lower())
            tdfiles=glob.glob(tdmask)
    
            #print 'tdfiles: ',len(tdfiles),tdfiles
            if(len(tdfiles) == 0):
                mcard='MMMissing: stm: %s  dtg: %s '%(tstmid,dtg)
                mcards.append(mcard)
                continue
            
            lsdiagpath=None
            if(len(tdfiles) == 1):
                lsdiagpath=tdfiles[0]
            elif(len(tdfiles) == 2):
                # -- select the 'tmtrkN' if 2 files
                #
                lsdiagpath=tdfiles[-1]
                b1=b2=0
                t1=t2=0
                if(mf.find(tdfiles[0],'best')):b1=1
                if(mf.find(tdfiles[1],'best')):b2=1
                if(mf.find(tdfiles[0],'tmt')):t1=1
                if(mf.find(tdfiles[1],'tmt')):t2=1
                if(b1 and t2): lsdiagpath=tdfiles[1]
                if(b2 and t1): lsdiagpath=tdfiles[0]
                print 'HHHMMMMMMM - two tdfiles? ',tdfiles,'using: ',lsdiagpath
                
            #tG=TcDiagS(dtg,model,
                      #ttaus=itaus,
                      #gaopt=CL.gaopt,
                      #domandonly=domandonly,
                      #doStndOnly=doStndOnly,
                      #doDiagOnly=doDiagOnly,
                      #dols=dols,
                      #tbdir=tsbdbdir,
                      #dowebserver=dowebserver,
                      #trkSource=trkSource,
                      #selectNN=selectNN,
                      #dstmids=tstmids,
                      #atcfname=atcfname,
                      #dobt=dobt,
                      #dobail=dobail,doshort=dothin,
                      #adeckSdir=adeckSdir,
                      #useLsdiagDat=useLsdiagDat,
                      #tD=None,
                      #md3=md3,
                      #doSfc=doSfc,
                      #doRoci=doRoci,
                      #prodDir=prodDir,
                      #doga=0,verb=verb)
    
    
            #if(ropt == 'norun'):  continue
    
    
            #tdirBase="%s/%s/%s"%(tsbdbdir,tyear,dtg)
            #tdir="%s/%s"%(tdirBase,model)
    
            ## -- set diagfile output path
            ##
            #(rc,dtime,dpath)=tG.setDiagPath(tstmid,tdir=tdir)
            #rc=tG.parseDiag(tstmid,lsdiagpath=lsdiagpath,dobail=0)
    
            tG=LsDiagFile(dtg,lsdiagpath,verb=verb)
            # -- parse diag to get urls for plots
            #
            rc=tG.parseDiag(tstmid)
            
            if(rc == 0):
                print 'WWW -- no lsdiag file for ',tstmid9,' at dtg: ',dtg,' press...'
                continue
    
            # -- sounding
            #
            okeys=[('r',850),('r',700),('r',500),('u',850),('u',700),('u',500),('v',850),('v',700),('v',500)]
            osndd0={}
            osndd6={}
            sndd0={}
            sndd6={}
            sndn=tG.sndLabels
            kk=sndn.keys()
            #for k in kk:
            #    print 'ccc',k,sndn[k]
                
            sndd=tG.sndDataVar
            kk=sndd.keys()
            lstaus=[]
            for k in kk:
                lstaus.append(k[0])
                
            lstaus=mf.uniq(lstaus)
    
            for k in kk:
                #print 'k: ',k[0],k[1],k[2],'snddata: ',sndd[k]
                if(k[0] == 0):
                    sndx=(k[1],k[2])
                    sndd0[sndx]=sndd[k]
                
                if(k[0] == 6):
                    sndx=(k[1],k[2])
                    sndd6[sndx]=sndd[k]
    
            kk=sndd0.keys()
            #kk.sort()
            for k in kk:
                #print 'sss',k,sndd0[k]
                
                if(k in okeys):
                    #varn=sndn[k]
                    vark="%s_%d"%(k[0].upper(),k[1])
                    osndd0[vark]=sndd0[k]
                    #print 'k0: ',vark,'sndd0: ',sndd0[k]
    
    
            kk=sndd6.keys()
            #kk.sort()
            for k in kk:
                if(k in okeys):
                    vark="%s_%d"%(k[0].upper(),k[1])
                    osndd6[vark]=sndd6[k]
                    #print 'k6: ',vark,'sndd6: ',sndd6[k]
                    
    
            # -- custom
            #
            #ccc 1 ADECK  VMAX (KT)
            #ccc 2 DIAG   VMAX (KT)
            #ccc 3 precip
            #ccc 4 DIAG   PMIN (MB)
            #ccc 5 sstanom
            #ccc 6 precip-actual
            #ccc 7 PR  ASYM/TOT (%)
            #ccc 8 TOTSHR MAG  (KT)
            #ccc 9 SHR/TOTSHR   (%)
            #ccc 10 SHR ASYM/TOT (%)
            #ccc 11 CPS  B(AROCLINC)
            #ccc 12 CPS   VTHERM(LO)
            #ccc 13 CPS   VTHERM(HI)
            #ccc 14 POCI        (MB)
            #ccc 15 ROCI        (KM)
            #ccc 16 R34mean     (KM)
            #ccc 17 R50mean     (KM)
            #ccc 18 R64mean     (KM)
    
            okeys=[5,8,9,10,11,12,13,16]
            ocusNames={5:'ssta',
                       8:'totshr',
                       9:'shr_tot',
                       10:'shr_asym',
                       11:'cps_b',
                       12:'cps_lo',
                       13:'cps_hi',
                       16:'r34m',
                       }
            
            ocusd0={}
            ocusd6={}
            cusd0={}
            cusd6={}
    
            cusn=tG.customVarNameByIndex
            kk=cusn.keys()
    
            #for k in kk:
                #print 'ccc',k,cusn[k]
                
            cusd=tG.customData
            kk=cusd.keys()
            for k in kk:
                #print 'k: ',k[0],k[1],'cusdata: ',cusd[k]
                if(k[0] == 0):
                    sndx=k[1]
                    cusd0[sndx]=float(cusd[k])
                
                if(k[0] == 6):
                    sndx=k[1]
                    cusd6[sndx]=float(cusd[k])
    
            kk=cusd0.keys()
            for k in kk:
                if(k in okeys):
                    ocusd0[k]=cusd0[k]
                    #if(k == 5 and float(ocusd0[k]) == 999.9): 
                    if(k == 5 and abs(ocusd0[k]) > 100.):
                        ocusd0[k]=undef
                    if(k == 16):
                        (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
                         tcstate,warn,roci,poci,alf,depth,
                         eyedia,tdo,ostmid,ostmname,r34,r50)=m3trk[dtg]
                        #(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci)=m3trk[dtg]
                        if(r34m != 'NaN'): 
                            ocusd0[k]=r34m
                    else:
                        if(k == 16 and ocusd0[k] != 9999): ocusd0[k]=ocusd0[k]*km2nm
                        #print 'k0: ',k,cusn[k],'cusd0: ',cusd0[k]
            
            kk=cusd6.keys()
            for k in kk:
                if(k in okeys):
                    ocusd6[k]=cusd6[k]
                    # -- special case for ssta
                    #
                    if(k == 5 and abs(ocusd6[k]) > 100.):
                        ocusd6[k]=undef
    
                    if(k == 16):
                        
                        dtg6=mf.dtginc(dtg,6)
                        try:
                            (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
                             tcstate,warn,roci,poci,alf,depth,
                             eyedia,tdo,ostmid,ostmname,r34,r50)=m3trk[dtg6]
                        except:
                            r34m='NaN'
                            
                        if(r34m != 'NaN'): 
                            ocusd6[k]=r34m
                    else:
                        if(k == 16 and ocusd6[k] != 9999): ocusd6[k]=ocusd6[k]*km2nm
                    
                    #print 'k0: ',k,stmn[k],'stmd0: ',stmd0[k]
                    
            
            # -- storm section
            #
            #sss 1 latitude
            #sss 2 longitude
            #sss 3 max_wind
            #sss 4 rms
            #sss 5 min_slp
            #sss 6 shr_mag
            #sss 7 shr_dir
            #sss 8 stm_spd
            #sss 9 stm_hdg
            #sss 10 sst
            #sss 11 ohc
            #sss 12 tpw
            #sss 13 land
            #sss 14 850tang
            #sss 15 850vort
            #sss 16 200dvrg
    
            okeys=[3,6,7,8,9,10,12,13,15,16]
            ostmd0={}
            ostmd6={}
            stmd0={}
            stmd6={}
    
            stmn=tG.stmVarNameByIndex
            kk=stmn.keys()
            #for k in kk:
                #print 'sss',k,stmn[k]
            stmd=tG.stmData
            kk=stmd.keys()
            kk.sort()
            for k in kk:
                #print 'k: ',k[0],k[1],'stmdata: ',stmd[k]
                if(k[0] == 0):
                    sndx=k[1]
                    stmd0[sndx]=float(stmd[k])
                
                if(k[0] == 6):
                    sndx=k[1]
                    stmd6[sndx]=float(stmd[k])
                    
            kk=stmd0.keys()
            for k in kk:
                if(k in okeys):
                    varn=stmn[k]
                    valn=stmd0[k]
                    if(valn == 9999.): valn=undef
                    ostmd0[varn]=valn
                    #print 'k0: ',k,stmn[k],'stmd0: ',stmd0[k]
            
            kk=stmd6.keys()
            for k in kk:
                if(k in okeys):
                    varn=stmn[k]
                    valn=stmd6[k]
                    if(valn == 9999.): valn=undef
                    ostmd6[varn]=valn
                    #print 'k0: ',k,stmn[k],'stmd0: ',stmd0[k]
                    
    
            if(verb):
                kk=ostmd0.keys()
                for k in kk:
                    print 'STM: %10s'%(k),'var: ',ostmd0[k],ostmd6[k]
        
                kk=ocusd0.keys()
                kk.sort()
                for k in kk:
                    print 'CUS: %10s'%(ocusNames[k]),'var: ',ocusd0[k],ocusd6[k]
        
                kk=osndd0.keys()
                for k in kk:
                    print 'SND: %10s'%(k),'var: ',osndd0[k],osndd6[k]
            
            
            # -- roci/poci
            #
            
            rociPypPath="%s/roci.%s.%s.pyp"%(tG.tdir,tG.model,tG.dtg)
            rpath=rociPypPath
            sizrpath=MF.GetPathSiz(rpath)
    
            poci0=poci0p1=undef
            roci0=roci0p1=999.
            poci6=poci6p1=undef
            roci6=roci6p1=999.
    
            if(sizrpath > 0):
                
                rociPS=open(rpath,'r')
                try:
                    rocis=pickle.load(rociPS)
                except:
                    print 'EEE-bad roci pickle:',rpath
                    break
                    
                kk=rocis.keys()
                kk.sort()
                
                #for k in kk:
                #    if(k[0] == tstmid):
                #        print k,rocis[k]
    
                for k in kk:
                    tau=k[1]
                    if(k[0] == tstmid):
                        if(tau == 0 or tau == 6):
                            rr=rocis[k]
                            if(tau == 0):
                                poci0=poci0p1=undef
                                roci0=roci0p1=999.
                                if(len(rr) >= 2):
                                    (poci0p1,roci0p1)=rr[len(rr)-2]
                                    poci0p1=float(poci0p1)
                                    roci0p1=float(roci0p1)
                                    (poci0,roci0)=rr[len(rr)-1]
                                    poci0=float(poci0)
                                    roci0=float(roci0)
                                if(len(rr) == 1): 
                                    (poci0,roci0)=rr[0]
                                    poci0=float(poci0)
                                    roci0=float(roci0)
                                if(verb): print 'roci000: ',k,poci0,roci0,poci0p1,roci0p1
                                
                            elif(tau == 6):
                                poci6=poci6p1=undef
                                roci6=roci6p1=999.
                                if(len(rr) >= 2):
                                    (poci6p1,roci6p1)=rr[len(rr)-2]
                                    poci6p1=float(poci6p1)
                                    roci6p1=float(roci6p1)
                                    (poci6,roci6)=rr[len(rr)-1]
                                    poci6=float(poci6)
                                    roci6=float(roci6)
                                if(len(rr) == 1): 
                                    (poci6,roci6)=rr[0]
                                    poci6=float(poci6)
                                    roci6=float(roci6)
                                if(verb): print 'roci666: ',k,poci6,roci6,poci6p1,roci6p1
    
            # -- don't need anymore since we're running 0/6/12/18 Z
            #
            #if(not(6 in lstaus)):
                    
                #print 'WWWW no tau 6...set to tau 0... for dtg: ',dtg,' tstmid: ',tstmid
                #ostmd6=ostmd0
                #ocusd6=ocusd0
                #osndd6=osndd0
                #poci6=poci0
                #roci6=roci0
                #poci6p1=poci0p1
                #roci6p1=roci0p1
                
            # -- put tau0 if available (will always be since we'er using the best track
            #
            if(len(ostmd0) > 0):
                card0=makeOcard(dtg,0,tstmid,ostmd0,ocusd0,ocusNames,osndd0,poci0,roci0,poci0p1,roci0p1)
                ocards.append(card0)
                
            # -- only use tau6 if tau0 not available
            #
            elif(len(ostmd6) > 0):
                card6=makeOcard(dtg,6,tstmid,ostmd6,ocusd6,ocusNames,osndd6,poci6,roci6,poci6p1,roci6p1)
                ocards.append(card6)
    
        rc=MF.WriteList2Path(ocards, oLspath,verb=1)
        
if(len(mcards) > 0 or (override and len(mcards) > 0)):
    rc=MF.WriteList2Path(mcards, missPath,verb=1)
    
MF.ChangeDir(curdir)

MF.dTimer(tag='all')
