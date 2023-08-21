#!/usr/bin/env python

from sBT import *

def getPrCtls(dtg):
        
    # -- prTCmean opens the control file...only do once for obs
    #year=dtgs[0][0:4]
    # -- 20230609 -- no ... for storms crossing the year boundary
    #
    year=dtg[0:4]
    iyear=int(year)
    
    # -- CCCCCCCCCCCCCCCCCCCCmorph
    #
    if(iyear <= 2019):
        tbdirProd=PrCmorphV10Products
        cprpath06="%s/prc_a06h-%s.ctl"%(tbdirProd,year)
        cprpath12="%s/prc_a12h-%s.ctl"%(tbdirProd,year)
    else:
        tbdirProd=PrCmorphVX0Products
        cprpath06="%s/prc_a06h-%s.ctl"%(tbdirProd,year)
        cprpath12="%s/prc_a12h-%s.ctl"%(tbdirProd,year)
    
    # -- GGGGGGGGGGGGGGGGGGGsmap
    #
    tbdirProd=PrGsmapV6GProducts
    gprpath06="%s/prg_a06h-%s.ctl"%(tbdirProd,year)
    gprpath12=None
    
    # -- IIIIIIIIIIIIIIIIIImerg
    #
    tbdirProd=PrImergV06Products
    iprpath06="%s/pri_a06h-%s.ctl"%(tbdirProd,year)
    iprpath12=None
    
    cprpath06siz=MF.getPathSiz(cprpath06)
    gprpath06siz=MF.getPathSiz(gprpath06)
    iprpath06siz=MF.getPathSiz(iprpath06)
    
    if(verb):
        print 'ctP06 using: ',cprpath06,' siz: ',cprpath06siz
        print 'gtP06 using: ',gprpath06,' siz: ',gprpath06siz
        print 'itP06 using: ',iprpath06,' siz: ',iprpath06siz
    
    if(cprpath06siz < 0):
        print 'EEE problem getting the CMORPH prpath for tstmid: ',tstmid
        oPrpath="%s-NOCmorph"%(oPrpath)
        cmd='touch %s'%(oPrpath)
        mf.runcmd(cmd)
    
    if(gprpath06siz < 0):
        print 'EEE problem getting the GSMAP prpath for tstmid: ',tstmid
        oPrpath="%s-NOGsmap"%(oPrpath)
        cmd='touch %s'%(oPrpath)
        mf.runcmd(cmd)
        
    if(iprpath06siz < 0):
        print 'EEE problem getting the IMERG prpath for tstmid: ',tstmid
        oPrpath="%s-NOImerg"%(oPrpath)
        cmd='touch %s'%(oPrpath)
        mf.runcmd(cmd)
    
    # -- make p06 obj for the three pr data sets
    #
    ctP06=prTCMean(dtg,cprpath06,verb=verb)
    gtP06=prTCMean(dtg,gprpath06,verb=verb)
    itP06=prTCMean(dtg,iprpath06,verb=verb)
    
    return(ctP06,gtP06,itP06)
    
    
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

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
            'basinOpt':         ['B:',None,'a','basinOpt'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'doSingle':         ['s',0,1,'expect only one storm'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'dobt':             ['b',0,1,'dobt'],
            'model':            ['M:','era5','a',' model '],
            'tauopt':           ['t:',None,'a',' tauopt -- single tau '],
            'doHemis':          ['H',0,1,'1 - do hemispheres in direction of motion'],
            'startGenDtg':      ['g',0,1,'1 - do start the NN dtgs with gendtg'],
            'doInvOnly':        ['I',0,1,'inventory oPrfiles'],
        }

        self.purpose="""
calc R34 using tcprop"""

        self.examples='''
%s cur12 ukm2 tukm2'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

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

if(doInvOnly and stmopt == None):
    print 'EEE-invonly must set year and basin one at a time...sayounara...'
    sys.exit()
elif(doInvOnly):
    invCards=[]
    invPath="inv/pr/inv-pr-%s.txt"%(istmopt)

for tstmid in tstmids:
    
    ocards=[]
    (rc,mcard)=md3.getMd3StmMeta(tstmid)
    (yyyy,stm,livestatus,tctype,sname,ovmax,tclife,stmlife,latb,lonb,bdtg,edtg,
     latmn,latmx,lonmn,lonmx,
     stcd,oACE,
     nRI,nED,nRW,
     RIstatus,timeGen,stm9x,ogendtg)=rc
    
    
    ocards=[]
    
    tyear=rc[0]
    stm3id=rc[1]
    
    # -- get dtgs from track
    #
    if(IsNN(tstmid)):
        (rc,m3trk)=md3.getMd3track(tstmid,dobt=1)
    else:
        (rc,m3trk)=md3.getMd3track(tstmid)
        
    if(rc != 1):
        print 'EEE-md3 getMd3track for tstmid: ',tstmid
        sys.exit()
    
    dtgs=m3trk.keys()
    dtgs.sort()

    # -- get the dir
    #
    tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
    opaths=glob.glob("%s"%(tmask))
    
    # -- 20230412 -- handle case where one 9X is the one for two NN storms
    #    happens in the LANT/EPAC several times, 2016

    odirPrs=[]
    
    if(len(opaths) == 1):
        odirPrs.append(opaths[0])
    elif(len(opaths) == 2):
        odirPrs.append(opaths[0])
        odirPrs.append(opaths[1])
    else:
        print 'EEE no or more than 2 sbt/src output dirs for: ',tstmid,' tmask: ',tmask
        sys.exit()
        
    if(len(odirPrs) == 2):
        print 'III'
        print 'III -- multiple DEV from ONE 9X -- happens in LANT/EPAC...for tstmid: ',tstmid
        print 'III'
        
    for odirPr in odirPrs:
     
        if(IsNN(tstmid)):
            oPrpath="%s/%s-%s-md3-BT.txt"%(odirPr,oPrpre,stm3id)
        else:
            oPrpath="%s/%s-%s-md3.txt"%(odirPr,oPrpre,stm3id)
            
        oPrsiz=MF.getPathSiz(oPrpath, verb=0)
    
        # -- IIIIIIIIIIIIIIIIIIIIIINNNNNNNNNNNNNNNNNNNNVVVVVVVVVVVVVVVVVVV
        #
        if(doInvOnly):
            invcard=getPrStatus(tstmid,oPrsiz)
            invCards.append(invcard)
            continue
        
        if(oPrsiz > 0 and not(override)):
            print 'oPrpath: ',oPrpath,'already done...press...not override...'
            continue
         
        # -- DDDDDDDDDDDDDDDDOOOOOOOOOOOOOOOOOOOOOOIIIIIIIIIIIIIIIIITTTTTTTTTTTT
        #
        doIt=1
        if(oPrsiz > 0):
            print 'WWW -- oPrsiz: %4d oPrpath: %-80s '%(oPrsiz,oPrpath),' already done...'
            doIt=0
            if(override): doIt=1
            
            
        if(not(doIt) and not(override)):
            print 'WWW -- override = 0 -- press....'
            continue
        
        endEra5Dtg='2023040100'
        
        byear=int(dtgs[ 0][0:4])
        eyear=int(dtgs[-1][0:4])
        cyear=byear
        didOpen=0
        
        for dtg in dtgs:

            # -- 20230608 -- logic to handle opening prs only once / year
            #
            cyear=int(dtg[0:4])

            if(cyear == byear and didOpen == 0):
                (ctP06,gtP06,itP06)=getPrCtls(dtg)
                didOpen=1
                print 'BBBBBBBBBBBB open prs for: ',dtg
                
            if(cyear == eyear and didOpen == 1 and byear != eyear):
                (ctP06,gtP06,itP06)=getPrCtls(dtg)
                print 'EEEEEEEEEEEE open prs for: ',dtg
                didOpen=0
             
                
            dEnd=mf.dtgdiff(dtg,endEra5Dtg)
            if(dEnd <= 0.0):
                print 'no ERA5 fields for: ',dtg,' press...'
                continue

            year=dtg[0:4]
            
            eraPath=None
            eraDir="%s/%s/%s/%s"%(tsbdbdir,year,dtg,model)    
            
            # -- use grib2 .ctl2 file
            emask="%s/sfc-era5.*%s*.ctl"%(eraDir,dtg)
            efiles=glob.glob(emask)
            if(len(efiles) == 1):
                eraPath=efiles[0]
            else:
                print 'EEE problem getting TWO eraPaths for dtg: ',dtg,' emask: ',emask,'...PRESS...'
                #continue
            
            if(verb): print '  ERA5:',eraPath
    
            etrk=getEraTrk(eraDir,tstmid,model,dtg,verb=verb)
    
            tPEra=None
    
            if(len(etrk) != 0):
                tPEra=prTCMean(dtg,eraPath,verb=verb)
                tPEraC=prTCMean(dtg,eraPath,prvar='prc',verb=verb)
                    
            # -- need to go directly too era5 sfc.ctl vice the tcanal .grb2 files
            #    to get the conv precip
            #tPEra=prTCMean(dtg,eraPath,'prc',verb=verb)
    
            for tau in taus:
                
                pdtg=mf.dtginc(dtg,tau)
                vdtg=dtg
                
                etau=tau-6
                
                # -- get BT for the tau
                # bdir undef handled in getTClatlonNew
                #
                (blat,blon,bdir)=getTClatlonNew(vdtg,0,m3trk,verb=verb)
                
                # -- get era5 track for tau
                #
                try:
                    rc=etrk[etau]
                    gotEra=1
                except:
                    print 'WWW - no etrack for tau: ',tau
                    gotEra=0
                    elat=undef
                
                
                if(gotEra):
                    
                    elat=rc[0]
                    elon=rc[1]
                    edir=rc[2]
                    # -- undefined
                    if(edir > 360.0 or edir == undef): edir=270.0
                
                    if(elat == undef):
                        print 'WWW -- no mdeck for: ',tstmid,' tau:',tau,' set to undef'
                        pelat=-99
                        pelon=-99
                        pedir=99
                    else:
                        pelat=elat
                        pelon=elon
                        pedir=edir
                    
                else:
                    pelat=-99
                    pelon=-99
                    pedir=99
                    
                
                dtgdat=(tstmid,vdtg,tau)
                
                pblat=blat
                pblon=blon
                pbdir=bdir
                
                if(blat == undef):
                    pblat=-99
                    pblon=-99
                    pbdir=99
                
                    
                tcdat=(pblat,pblon,pbdir,pelat,pelon,pedir)
                
                ctpr6em=gtpr6em=itpr6em={}
    
                if(elat != undef):
                    ctP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        ctP06.setTcprop(elat,elon,rad,edir,verb=verb)
                    ctpr6em=ctP06.prM
                
                    gtP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        gtP06.setTcprop(elat,elon,rad,edir,verb=verb)
                    gtpr6em=gtP06.prM
    
                    itP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        itP06.setTcprop(elat,elon,rad,edir,verb=verb)
                    itpr6em=itP06.prM
                else:
                    ctpr6em={}
                    gtpr6em={}
                    itpr6em={}
                    for r in radkms:
                        rad=radInfPrNM[r]
                        ctpr6em[rad]=undef
                        gtpr6em[rad]=undef               
                        itpr6em[rad]=undef               
                    
                
                ctpr6bm=gtpr6bm=itpr6bm={}
                
                if(blat != undef):
                    # -- cmorph
                    #
                    ctP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        ctP06.setTcprop(blat,blon,rad,bdir,verb=verb)
                    ctpr6bm=ctP06.prM
                    
                    # -- gsmap
                    #
                    gtP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        gtP06.setTcprop(blat,blon,rad,bdir,verb=verb)
                    gtpr6bm=gtP06.prM
    
                    # -- imerg
                    #
                    itP06.setGrads(vdtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        itP06.setTcprop(blat,blon,rad,bdir,verb=verb)
                        
                    itpr6bm=itP06.prM
                    
                else:
                    tpr6bm={}
                    gtpr6bm={}
                    itpr6bm={}
                    for r in radkms:
                        rad=radInfPrNM[r]
                        tpr6bm[rad]=undef
                        gtpr6bm[rad]=undef               
                
                
                if(doHemis):
                    print 'nnnn not implemented...sayounara'
                    sys.exit()
                    rm=tP06.prMH
                    kk=rm.keys()
                    kk.sort()
                    for k in kk:
                        print 'ppp 06 k',k,'pr',rm[k]
    
                if(tPEra != None and (elat != undef)):
                    tPEra.setGrads(dtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        tPEra.setTcprop(elat,elon,rad,edir,verb=verb)
                    
                    eprm=tPEra.prM
    
                    tPEraC.setGrads(dtg,tau)
                    for radkm in radkms:
                        rad=radInfPrNM[radkm]
                        tPEraC.setTcprop(elat,elon,rad,edir,verb=verb)
                    
                    eprm=tPEra.prM
                    eprmc=tPEraC.prM
                    kk=eprmc.keys()
                    
                    for k in kk:
                        epc=float(eprmc[k])
                        ept=float(eprm[k])
                        if(ept == 0.):
                            eprmc[k]=undef
                        else:
                            ratioC2T=(epc/ept)*100.0
                            eprmc[k]=ratioC2T
                
                    if(doHemis):
                        rm=tPEra.prMH
                        kk=rm.keys()
                        kk.sort()
                        for k in kk:
                            print 'eee 06 k',k,'pr',rm[k]
                            
                else:
                    print 'WWW - no era5 pr...set to undef'
                    eprm={}
                    ratioC2T={}
                    for r in radkms:
                        rad=radInfPrNM[r]
                        eprm[rad]=undef
                        ratioC2T[rad]=undef
                        
                    
                fcard=makePrCard(dtgdat,tcdat,ctpr6bm,ctpr6em,gtpr6bm,gtpr6em,itpr6bm,itpr6em,eprm,eprmc)
                ocards.append(fcard)
    
        MF.WriteList2Path(ocards, oPrpath, verb=1 )

if(doInvOnly):
    MF.WriteList2Path(invCards, invPath,verb=verb)
    
