"""
2nd attempt general model class

"""

#from WxMAP2 import *
#w2=W2()
from sBT import *

from GRIB import Grib1
from GRIB import Grib2

from grads import GrADSError

class Model(MFbase):


    def DoGribmap(self,gmpverb=0):

        if(self.gribtype == 'grb1'): xgribmap='gribmap'
        if(self.gribtype == 'grb2'): xgribmap='gribmap'
        xgopt='-i'
        if(gmpverb):
            xgopt='-v -i'
                
        cmd="%s %s %s"%(xgribmap,xgopt,self.ctlpath)
        mf.runcmd(cmd)



class EnsModel(Model,Grib1,Grib2):

    
    def __init__(self,
                 model,
                 dtgs,
                 dtau=12,
                 ddtg=12,
                 maxtau=240,
                 justinit=0,
                 overrideLN=0,
                 overrideGM=0,
                 ropt='',
                 verb=0,
                 undef=-999.,
                 postfix=None,
                 do12hr=1,
                 tdirbase=None,
                 doLnOnly=0,
                 ):


        self.model=model
        self.dtgs=dtgs
        self.bdtg=dtgs[0]
        self.edtg=dtgs[-1]
        self.maxtau=maxtau
        self.dtau=int(dtau)
        self.ddtg=int(ddtg)
        self.undef=undef
        self.tdirbase=tdirbase
        self.postfix=postfix
        
        # -- calc dtgs using ddtg
        #
        (is0012,remainder)=MF.isSynopticHour(self.dtgs[0],12)
        if(self.ddtg == 12 and not(is0012) and do12hr):
            self.bdtg=mf.dtginc(self.dtgs[0],-6)
            self.edtg=mf.dtginc(self.dtgs[-1],+6)
            
        self.dtgs=mf.dtgrange(self.bdtg,self.edtg,self.ddtg)

        for dtg in dtgs:
            rc=getW2fldsRtfimCtlpath(self.model,dtg,maxtau=self.maxtau,verb=verb)
            if(rc[0] == 0):
                print 'III(EnsModel) no ctl for dtg: ',dtg
                gotdtg=0
            elif(rc[0] == 1):
                print "found ctl for dtg: ",dtg
                #self.bdtg=dtg
                gotdtg=1
                break
                
        if(gotdtg == 1):
            sdir=tdir=taus=ctlpath=gribver=gribtype=datpaths=None
            ctlpath=rc[1]
            taus=rc[2]
            gribtype=rc[3]
            gribver=rc[4]
            datpaths=rc[5]
            (dir,file)=os.path.split(ctlpath)
            sdir=os.path.normpath("%s/.."%(dir))
            tdir="%s/ensFC"%(sdir)
            MF.ChkDir(tdir,'mk')
        else:
            print 'EEE: EnsModel.__init__ rc from getW2fldsRtfimCtlpath != 1'
            print rc
            sys.exit()
            return

        self.sdir=sdir

        if(tdirbase == None):
            self.tdirbase=tdir
        
        self.tdirPYPDB  ='%s/PYPDB'%(self.tdirbase)
        self.tdirSTATS  ='%s/STATS'%(self.tdirbase)
        self.tdirFIELDS ='%s/FIELDS'%(self.tdirbase)
        self.tdirPLTS   ='%s/PLTS'%(self.tdirbase)

        if(hasattr(self,'tdirbase')):
            self.tdir="%s/%s"%(self.tdirbase,self.model)
            MF.ChkDir(self.tdir,'mk')
            
        # -- bug in doing gfs2 donomads=1 on wxmap2 -- 168 missing -- corrected on 2014061200
        #
        #if(not(168 in taus)): taus.append(168)
        taus.sort()
        
        self.taus=taus
        self.ctlpath=ctlpath
        self.gribver=gribver
        self.gribtype=gribtype
        self.tdatbase=os.path.splitext(ctlpath)[0]
        self.tdatbase=os.path.splitext(self.tdatbase)[0]
        self.tbase=os.path.split(self.tdatbase)[1]
        
        # -- new setting of .ctl file based on size to make search in veri-wmo easier
        #
        ndtgs=len(self.dtgs)

        if(justinit):
            newbdtg1=self.bdtg[0:4]
            newbdtg2=self.bdtg[0:6]
            newbdtg3=self.bdtg
            newbdtg4="%s-%s"%(self.bdtg,self.edtg)
            
            bctl1=self.tbase.replace(self.bdtg,newbdtg1)
            ctl1="%s/%s.%s.ctl"%(self.tdir,bctl1,self.gribtype)
            bctl2=self.tbase.replace(self.bdtg,newbdtg2)
            ctl2="%s/%s.%s.ctl"%(self.tdir,bctl2,self.gribtype)
            bctl3=self.tbase.replace(self.bdtg,newbdtg3)
            ctl3="%s/%s.%s.ctl"%(self.tdir,bctl3,self.gribtype)
            fctl=None
            if(MF.getPathSiz(ctl1) > 0):
                fctl=ctl1
                bctl=bctl1
            elif(MF.getPathSiz(ctl2) > 0):
                fctl=ctl2
                bctl=bctl2
            elif(MF.getPathSiz(ctl3) > 0):
                fctl=ctl3
                bctl=bctl3
            else:
                print 'EEE-could not find ctl for veri-wmo.py...press...'
                sys.exit()
                
            self.octlpath=fctl
            self.ogmppath="%s/%s.%s.gmp"%(self.tdir,bctl,self.gribtype)
            
            self.ensFcCtlpath=self.octlpath
            self.ensFcGmppath=self.ogmppath
            
            return
    
        else:
            
            if(ndtgs >= 365):
                newbdtg=self.bdtg[0:4]
            elif(ndtgs >= 28):
                newbdtg=self.bdtg[0:6]
            else:
                newbdtg="%s-%s"%(self.bdtg,self.edtg)
        
        # -- hardwire to year
        #
        newbdtg=self.bdtg[0:4]
        self.tbaseCtl=self.tbase.replace(self.bdtg,newbdtg)
        
        if(postfix != None):
            self.tbaseCtl="%s-%s"%(self.tbase,postfix)
        self.datpaths=datpaths
            
        self.octlpath="%s/%s.%s.ctl"%(self.tdir,self.tbaseCtl,self.gribtype)
        self.ogmppath="%s/%s.%s.gmp"%(self.tdir,self.tbaseCtl,self.gribtype)

        self.ensFcCtlpath=self.octlpath
        self.ensFcGmppath=self.ogmppath

        if(justinit): return

        if(rc):
            self.ctlpath=rc[1]
            self.taus=rc[2]
            self.gribtype=rc[3]
            self.gribver=rc[4]

        else:
            return

        # -- 20260311 -- don't need to do for era5-wmo
        #
        print 'self.model ',self.model
        
        self.doLnFc(override=overrideLN,ropt='',verb=verb)
        if(doLnOnly): return
            

        self.EnsFcCtl(ddtg=self.ddtg,override=overrideGM,verb=verb)


    def doLnFc(self,override=0,ropt='',verb=0):
        """ cycle through dtgs to make ln -s
        """
        if(self.model == 'era5w'):
            ldtgs=[self.bdtg]
        else:
            ldtgs=self.dtgs

        for dtg in ldtgs:
            self.LnFc(dtg,self.dtau,override,ropt,verb)



    def cnvDatpaths2dict(self,datpaths):
        odatpaths={}
        
        for dpath in datpaths:
            (ddir,dfile)=os.path.split(dpath)
            (bfile,bext)=os.path.splitext(dfile)
            tau=int(bfile[-3:])
            odatpaths[tau]=dpath
            
        return(odatpaths)
        
        
    def LnFc(self,dtg,dtau=12,override=0,ropt='',verb=0):
        """
        make sybmolic links to do ensembles by forecast (FC)
        """

        rc=getW2fldsRtfimCtlpath(self.model,dtg,maxtau=self.maxtau,verb=verb)
        if(rc[0]):
            ctlpath=rc[1]
            taus=rc[2]
            gribtype=rc[3]
            gribver=rc[4]
            datpaths=rc[5]
            tauOffset=rc[6]
        else:
            print 'WWW: EnsModel.__init__ rc from getW2fldsRtfimCtlpath != 1 in LnFc() for dtg: ',dtg,'...press'
            print rc
            return
        
        
        datpaths=self.cnvDatpaths2dict(datpaths)
        if(self.model == 'era5w'):
            datpaths=datpaths[0]
        
        nln=0
        
        if(not(hasattr(self,'tdir'))): 
            'print EEEEE self.tdir not set...'
            self.ls()
            sys.exit()
        
        alltaus=0
        if(len(datpaths) == 1):
            alltaus=1
            
        
        tdatbase=os.path.splitext(ctlpath)[0]
        tdatbase=os.path.splitext(tdatbase)[0]
        tbase=os.path.split(tdatbase)[1]        

        #self.taus=[0,12]
        
        for n in range(0,len(self.taus)):
            
            tau=self.taus[n]
            ftau="f%03d"%(tau)
            vdtg=mf.dtginc(dtg,tau)
            
            if(tau%dtau == 0):

                if(self.model == 'era5w'):
                    ldir=self.tdir
                    spath='/raid05/era5-wmo/%s'%(ftau)
                    MF.ChangeDir(ldir)
                    lpath=ftau
                    try:
                        cmd="ln -s %s %s"%(spath,lpath)
                        mf.runcmd(cmd,ropt)
                    except:
                        None
                
                else:

                    if(alltaus):
                        spath=datpaths[0]
                    else:
                        try:
                            spath=datpaths[tau]
                        except:
                            if(verb == 0): print ' no datpaths form tau: ',tau,' bdtg: ',dtg
                            continue
                    
                    
                        ldir="%s/%s"%(self.tdir,ftau)
                        mf.ChkDir(ldir,'mk')
                        lpath="%s/%s.%s.%s"%(ldir,tbase,ftau,gribtype)
                        
                    if(not(os.path.exists(lpath)) or override):
                        cmd="ln -s -f %s %s"%(spath,lpath)
                        mf.runcmd(cmd,ropt)
                        nln=nln+1
                    else:
                        if(verb): print '  did:  ln -s ',spath,lpath
                    continue


        self.nln=nln
        self.dtauLnFc=dtau




    def EnsFcCtl(self,
                 ddtg=12,
                 override=0,chkonly=0,ropt='',verb=0):
        """
        make .ctl for model runs as an ensemble of forecasts f000, f012, ... ,fLLL
        """

        maxtau=self.maxtau
        ddtg=self.ddtg
        if(self.sdir == None):
            print 'EEE nada for dtg: ',self.dtg,' model: ',self.model
            sys.exit()
            
        fcdtgs=self.dtgs
        
        # -- time increment in .ctl
        dtime=self.dtauLnFc 
        if(self.dtauLnFc != self.ddtg): dtime=self.ddtg        
        #print 'ddd',dtime,len(fcdtgs),self.maxtau
        #sys.exit()
        
        # -- add the max
        ntd=len(fcdtgs)
        nt=ntd + (self.maxtau/dtime) 

        if(verb): print 'lllllllllllllllll ',nt,self.bdtg,self.edtg,ddtg

        # -- just get paths...
        #

        if(os.path.exists(self.ensFcCtlpath) and os.path.exists(self.ensFcGmppath) and override == 0 and self.nln == 0):
            if(verb): print 'm2.EnsFcCtl ctl and gmp already there...',self.ensFcCtlpath,self.ensFcGmppath
            return

        tctlpath=self.ctlpath

        self.tctlpath=tctlpath


        #
        # make the fc taus that will be the ensemble dimentions
        #
        fctaus=[]
        fcgtimes={}
        for fctau in self.taus:
            if(fctau%self.dtauLnFc == 0):
                fcvdtg=mf.dtginc(self.bdtg,fctau)
                fcgtime=mf.dtg2gtime(fcvdtg)
                fctaus.append(fctau)
                fcgtimes[fctau]=fcgtime

        #
        # make the 5-d .ctl
        #
        cards=open(tctlpath).readlines()

        (dir,file)=os.path.split(tctlpath)
        (base,ext)=os.path.splitext(file)

        ntaus=len(fctaus)
        
        edefcard="edef %d names "%(ntaus)
        for fctau in fctaus:
            edefcard="%s f%03d"%(edefcard,fctau)

        octl=''
        for n in range(0,len(cards)):
            card=cards[n]
            if(mf.find(card,'dset')):
                #tt=self.tbase.split('-')
                #fmask='%iy4%im2%id2%ih2'
                #dset=self.tbase.replace(self.bdtg,fmask)
                #card="dset ^%%e/%s.f%%f3.%s"%(dset,self.gribtype)
                #card="dset ^%e/%y4/%y4%m2%d2%h2/era5-w2flds-%y4%m2%d2%h2-ua.grb2"
                card="dset ^%e/%y4/era5-w2flds-%y4%m2%d2%h2-ua.grb2"
                octl=card
            elif(mf.find(card,'index')):
                if(self.postfix != None):
                    gmpfile="%s-%s.%s.gmp"%(self.tbase,self.postfix,self.gribtype)
                else:
                    gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
                    
                (gmpdir,gmpfile)=os.path.split(self.ogmppath)
                gmppath=self.ogmppath
                gmpcard="index ^%s"%(gmpfile)
                octl="""%s
%s"""%(octl,gmpcard)
                
            elif(mf.find(card,'tdef')):
                gtime=mf.dtg2gtime(self.bdtg)
                # -- if dtauLnFc != ddtg, use ddtg

                tdefcard="tdef %d linear %s %dhr"%(nt,gtime,dtime)
                octl="""%s
%s
%s"""%(octl,tdefcard,edefcard)
                
            else:
                octl="""%s
%s"""%(octl,card.strip())
                
        nedef=len(fctaus)
        
        edefcard="edef %d"%(nedef)
        octl="""%s
%s"""%(octl,edefcard)

        for fctau in fctaus:
            nte=ntd-(fctau/dtime)
            fcgtime=fcgtimes[fctau]
            ofctau="f%03d %d %s"%(fctau,nte,fcgtime)
            edefcard="%s"%(ofctau)
            octl="""%s
%s"""%(octl,edefcard)

        edefcard='endedef'
        octl="""%s
%s
"""%(octl,edefcard)

        MF.WriteCtl(octl,self.octlpath,verb=1)

        #
        # force use of gribmap2 since we're using the ensemble dimension
        #
        dogribmap=1
        if(dogribmap):
            self.ctlpath=self.octlpath
            self.gribtype='grb2'
            self.DoGribmap(gmpverb=verb)
        return


class WmoStats(MFbase):

    
    wmoversion='0.1 -- comp to ncep vsdb'

    def __init__(self,area,vdtg,var,lev,tau,wmo,
                 bdtg=None,
                 modelAn=None,
                 modelFc=None,
                 doAnom=1,
                 doFwrite=0,
                 verb=0
                 ):

        self.ggdx=wmo.ggdx
        self.ggmethod=wmo.method
        self.ggshfilt=wmo.ggshfilt
        self.ggshfiltNwaves=wmo.ggshfiltNwaves

        self.curdtg=mf.dtg('dtg.phm')
        self.wmoversion=self.wmoversion
        self.tdirbase=tdirbase

        self.verb=verb
        self.modelAn=modelAn
        self.modelFc=modelFc
        
        self.area=area
        self.vdtg=vdtg
        self.bdtg=bdtg
        
        self.var=var
        self.lev=lev
        self.tau=tau
        self.doAnom=doAnom


        self.sumCoslat     = None
        self.sumMeanErr    = None
        self.sumAbsMeanErr = None
        self.sumAn         = None
        self.sumFc         = None
        self.sumAnCl       = None
        self.sumFcCl       = None
        self.sum2An        = None
        self.sum2Fc        = None
        self.sum2AnFc      = None
        self.sum2AnCl      = None
        self.sum2FcCl      = None
        self.sum2AnFcCl    = None
        self.meanAn        = None
        self.meanFc        = None
        self.meanAnCl      = None
        self.meanFcCl      = None
        self.sum2An        = None
        self.sum2Fc        = None
        self.sum2AnCl      = None
        self.sum2FcCl      = None
        self.MeanErr       = None
        self.MeanAbsErr    = None
        self.corrAnFc      = None
        self.corrAnFcCl    = None
        self.sigAn         = None
        self.sigFc         = None
        self.sigAnCl       = None
        self.sigFcCl       = None
        self.rmseT         = None
        self.rmseE         = None
        self.rmseP         = None

        self.doFwrite=doFwrite
        
        if(self.doFwrite):
            obdtg=mf.dtginc(self.vdtg, -self.tau)
            odatbase="%s_%s.%s.%s.%s.%s.f%03d"%(self.modelFc,self.modelAn,self.var,self.lev,self.area,obdtg,self.tau)
            odatdir="%s/%s"%(tdirFIELDS,obdtg)
            MF.ChkDir(odatdir,'mk')
            
            self.odatpath="%s/%s.dat"%(odatdir,odatbase)
            self.octlpath="%s/%s.ctl"%(odatdir,odatbase)


    def makeVectorStats(self,ssu,ssv):

        #ssu.ls()
        #ssv.ls()

        Ninv=ssu.sumCoslat

        sig2a=(ssu.sum2An + ssv.sum2An)/Ninv
        sig2f=(ssu.sum2Fc + ssv.sum2Fc)/Ninv

        sig2aCl=(ssu.sum2AnCl + ssv.sum2AnCl)/Ninv
        sig2fCl=(ssu.sum2FcCl + ssv.sum2FcCl)/Ninv

        siga=sqrt(sig2a)
        sigf=sqrt(sig2f)

        sig2aCL=(ssu.sum2AnCl + ssv.sum2AnCl)/Ninv
        sig2fCL=(ssu.sum2FcCl + ssv.sum2FcCl)/Ninv

        sigaCl=sqrt(sig2aCl)
        sigfCl=sqrt(sig2fCl)

        # -- wmo corr
        #
        corr=( (ssu.sum2AnFc + ssv.sum2AnFc)/Ninv ) / (siga*sigf)
        corrCl=( (ssu.sum2AnFcCl + ssv.sum2AnFcCl)/Ninv ) / (sigaCl*sigfCl)

        mseP= sig2f+sig2a - 2.0*sigf*siga*corr
        mseE= (ssu.meanFc - ssu.meanAn)*(ssu.meanFc - ssu.meanAn) +  (ssv.meanFc - ssv.meanAn)*(ssv.meanFc - ssv.meanAn) 

        mseT=mseP+mseE

        if(mseT < 0.001): mseT=0.0
        if(mseE < 0.001): mseE=0.0
        if(mseP < 0.001): mseP=0.0
        
        self.rmseTUV=sqrt(mseT)
        self.rmseEUV=sqrt(mseE)
        self.rmsePUV=sqrt(mseP)
        self.corrUV=corr
        self.corrClUV=corrCl

        if(self.verb):
            print
            print 'VVVV  area: %8s'%(ssu.area),' vdtg: ',ssu.vdtg,' tau: ',ssu.tau
            print 'VVuu UsigA: %8.4g   UsigF: %8.4g '%(ssu.sigAn,ssu.sigFc)
            print 'VVvv VsigA: %8.4g   VsigF: %8.4g '%(ssv.sigAn,ssv.sigFc)
            print 'VVVV  siga: %8.4g    sigf: %8.4g '%(siga,sigf)
            print 'VVVV  corr: %8.4g  corrCL: %8.4g'%(corr,corrCl)
            print 'VVVV rmseT: %8.4g   rmseP: %8.4g  rmseE: %8.4g'%(self.rmseTUV,self.rmsePUV,self.rmseEUV)
            print

        
        #self.hashvalue=[siga,sigf,corr,sigaCl,sigfCl,corrCl,self.rmse,self.bias]
        #self.hashvaluedesc=['sigmaAn','sigmaFc','vectorCorr','sigmaAnCl','sigmaFcCl','vectorCorrCl','rmse','bias']

        

    def makeStats(self,ga,wmo):
        """
         strictly by the wmo red book, ii.7-36 - ii.7-38
         and grads using scorr
         
         attachment II.7 - Table F -- include points on boundaries
         
        """
        from math import sqrt
        
        wmo.getAreaLatLon(self.area)

        # -- sums
        #
        
        sumFunc=ga.get.asumg
        
        self.sumCoslat     = sumFunc('coslat',wmo)
        
        self.sumMeanErr    = sumFunc('vd*coslat',wmo)

        self.sumAbsMeanErr = sumFunc('abs(vd*coslat)',wmo)

        self.sumAn         = sumFunc('va*coslat',wmo)
        self.sumFc         = sumFunc('vf*coslat',wmo)
        
        self.sumAnCl       = sumFunc('vaa*coslat',wmo)
        self.sumFcCl       = sumFunc('vfa*coslat',wmo)
                
        self.meanAn        = self.sumAn/self.sumCoslat
        self.meanFc        = self.sumFc/self.sumCoslat
        
        self.meanAnCl      = self.sumAnCl/self.sumCoslat
        self.meanFcCl      = self.sumFcCl/self.sumCoslat

        self.sum2An        = sumFunc('(((va  - %g)*(va  - %g))*coslat)'%(self.meanAn,self.meanAn),wmo)
        self.sum2Fc        = sumFunc('(((vf  - %g)*(vf  - %g))*coslat)'%(self.meanAn,self.meanAn),wmo)
        self.sum2AnFc      = sumFunc('(((va  - %g)*(vf  - %g))*coslat)'%(self.meanAn,self.meanAn),wmo)
        
        self.sum2AnCl      = sumFunc('(((vaa - %g)*(vaa - %g))*coslat)'%(self.meanAnCl,self.meanAnCl),wmo)
        self.sum2FcCl      = sumFunc('(((vfa - %g)*(vfa - %g))*coslat)'%(self.meanFcCl,self.meanFcCl),wmo)
        self.sum2AnFcCl    = sumFunc('(((vaa - %g)*(vfa - %g))*coslat)'%(self.meanAnCl,self.meanFcCl),wmo)

        # -- errors
        #
        self.MeanErr       = self.sumMeanErr/self.sumCoslat
        self.MeanAbsErr    = self.sumAbsMeanErr/self.sumCoslat
        
        self.corrAnFc      = self.sum2AnFc   / (sqrt(self.sum2An)  * sqrt(self.sum2Fc))
        self.corrAnFcCl    = self.sum2AnFcCl / (sqrt(self.sum2AnCl)* sqrt(self.sum2FcCl))
        
        # -- std dev
        #
        self.sigAn         = sqrt(self.sum2An/self.sumCoslat)
        self.sigFc         = sqrt(self.sum2Fc/self.sumCoslat)

        self.sigAnCl       = sqrt(self.sum2AnCl/self.sumCoslat)
        self.sigFcCl       = sqrt(self.sum2FcCl/self.sumCoslat)

        # -- vsdb breakdown of mse into P (pattern) and E (mean)
        #
        sig2a              = self.sum2An/self.sumCoslat
        sig2f              = self.sum2Fc/self.sumCoslat

        mseP               = sig2f+sig2a - 2.0*self.sigAn*self.sigFc*self.corrAnFc
        mseE               = (self.meanFc - self.meanAn)*(self.meanFc - self.meanAn)
        mseT               = mseP + mseE

        if(mseT < 0.001): mseT=0.0
        if(mseE < 0.001): mseE=0.0
        if(mseP < 0.001): mseP=0.0
        
        self.rmseT=sqrt(mseT)
        self.rmseE=sqrt(mseE)
        self.rmseP=sqrt(mseP)

        #- output hashes...
        #
        #self.hashkey=(self.modelFc,self.vdtg,self.area,self.var,self.tau,self.lev)
        #self.hashvalue=[self.acAnFc,self.rmse,self.meane,self.corrAnFc,self.sigmaAn,self.sigmaFc,self.sigmaCl]
        #self.hashvaluedesc=['acAnFc','rmse','meane','corrAnFc','sigmaAn','sigmaFc','sigmaCl']

    def makeAnfld(self,ga,ovar,ivar,tau,wmo,doshfilt=0):
        
        if(self.bdtg == None):
            ivar=self.makeIvar(ivar,tau,ga.nfAn)
        else:
            ivar=self.makeIvarRunAn(ivar,self.bdtg,tau,ga.nfAn)

        #ga('undefine %s'%(ovar))

        ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
        ga.dvar.regrid(ovar,ivar,wmo.reargs)
            
        if(ga.get.stat(ovar).nvalid == 0):
            print 'EEEaaaaaaaaaaaaa no fields found Anfld...',ga.vdtg,'var: ',ivar,' tau: ',tau,' press...'
            return(0)
        else:
            if(doshfilt):
                ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
                ga.dvar.shfilt(ovar,self.makeIvar(ivar,tau,1))
                ga.dvar.regrid(ovar,ovar,wmo.reargs)
            return(1)
        
    def makeFcfld(self,ga,ovar,ivar,tau,wmo,doshfilt=0):

        if(self.bdtg == None):
            ivar=self.makeIvar(ivar,tau,ga.nfFc)
        else:
            ivar=self.makeIvarRun(ivar,self.bdtg,tau,ga.nfFc)
            
        #ga('undefine %s'%(ovar))
        
        ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
        ga.dvar.regrid(ovar,ivar,wmo.reargs)

        if(ga.get.stat(ovar).nvalid == 0):
            print 'EEEfffffffffff no fields found Fcfld...',ga.vdtg,'var: ',ivar,' tau: ',tau,' press...'
            return(0)   
        else:   
            if(doshfilt):   
                ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
                ga.dvar.shfilt(ovar,self.makeIvar(ivar,tau,1))
                ga.dvar.regrid(ovar,ovar,wmo.reargs)
            return(1)
            #except GrADSError:
            #print 'GrADSError---EEEfffffffffff no fields found Fcfld...',ga.vdtg,'var: ',ivar,' tau: ',tau,' press...'
            #return(0)
        
    def getClgaC(self,ga,ivar):
        
        if(ivar == 'ua' or ivar == 'va' or ivar == 'uva' or ivar == 'wa'):
            gaC=ga.nfcUV
        elif(ivar == 'zg' or ivar == 'ta' or ivar == 'hur'):
            gaC=ga.nfcMS
        else:
            print 'EEE invalid ivar: ',ivar,'in getClgaC'
            sys.exit()
        
        return(gaC)
        
    def makeCl(self,ga,ovar,ivar,wmo):
    
        byear=ga.Climo.byear
        cvdtg="%s%s"%(str(byear),ga.vdtg[4:])
        
        # -- because 00/12 only use 0012
        #
        cvdtg=mf.dtgShift0012(cvdtg)
        gtime=mf.dtg2gtime(cvdtg)
    
        gaC=self.getClgaC(ga,ivar)
        
        levCl=self.lev
        if(self.lev == 200 and ga.Climo.ctype == 'cmean'): levCl=250
        
        expr="%s.%d(time=%s,lev=%d)"%(ivar,gaC,gtime,levCl)
        
        if(ivar == 'zg' and ga.Climo.ctype == 'era-dailyclim'):
            expr="zgg.%d(time=%s,lev=%d)"%(gaC,gtime,levCl)
            expr="(%s/%f)"%(expr,ga.Climo.gravity)
            
        elif(ivar == 'hur'):
            if(ga.Climo.ctype == 'era-dailyclim'):
                if(self.lev == 700):
                    expr="hur7.%d(time=%s,lev=%d)"%(gaC,gtime,levCl)
                elif(self.lev == 850):
                    expr="hur8.%d(time=%s,lev=%d)"%(gaC,gtime,levCl)
                else:
                    print 'EEE makeCl - hur available only at 700/850 mb in ecmwf daily climo'
                    sys.exit()
            else:
                print 'EEE makeCL -- hur not available in NCEP climo...'
                sys.exit()
                
        elif(ivar == 'wa'):
            expr="mag((ua.%d(time=%s,lev=%d)),((va.%d(time=%s,lev=%d))"%(gaC,gtime,levCl,gaC,gtime,levCl)

        ga.dvar.regrid(ovar,expr,wmo.reargs)
        if(ga.get.stat(ovar).nvalid == 0):
            print 'EEE no verifiying analysis...'
            return(0)
        else:
            return(1)

    def fwriteOvars(self,ovars,ga,wmo,odatfile=None,octlfile='fields.ctl'):
            
        ga('set lon %f %f'%(wmo.gglon1,wmo.gglon2-wmo.ggdx))
        
        if(odatfile != None):
            ga('set fwrite %s'%(odatfile))
            self.fwriteOpen=1
        
        ctlvars="""vars %d"""%(len(ovars))

        wmo.setCtlhead(odatfile)
        for ovar in ovars:
            ctlvars="""%s
%s 0 0 %s"""%(ctlvars,ovar,ovar)
            ga.dvar.writef77(ovar)
            #print 'pdpppppppppppppppppppppppppppppp',ovar
            #ga('d %s'%(ovar))
            
            ctl="""%s
%s
endvars"""%(wmo.ctlhead,ctlvars)
            
            if(octlfile != None): octlpath=octlfile
            MF.WriteString2Path(ctl,octlpath)
            
        ga('disable fwrite')
            
        print 'octlpath: ',octlpath
        
        return(octlpath)


        
    def makeFields(self,ga,wmo,vdtg,var,lev,tau,override=1):
        
        """ makes defined variables:
        
        vc = var climo
        va = var analysis (an)
        vf = var forecast (fc)
        vaa = va-vc = anom an from climo
        vfa = vf-vc = anom fc from climo
        vd  = vf-va = fc - an 
        coslat = cosine weights from makeCoslatWhgt()
        
        20140618
        override = 0 looked like a good idea to avoid redefines, but probably not worth the complexity
        
"""
        if(not(hasattr(ga,'didFields'))):  ga.didFields={}

        try:
            doneAlready=(ga.didFields[var,vdtg,lev,tau]==1)
        except:
            doneAlready=0
            
        if(doneAlready and not(override)):
            print 'AAAAllready done -- var: ',var,' vdtg: ',vdtg,' lev: ',lev,' tau: ',tau
            return(1)
        
        ovars=['vc','va','vf','vaa','vfa','vd']
        #ovars=['va','vf']
        #ovars=['va']
 
        # -- set dim env
        #
        
        ga.vdtg=vdtg
        ga.set.dtg(vdtg)
        ga.set.lev(lev)
        ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
    
        # -- make Climo, verifying ANalysis and FC forecast fields
        #
        rcc=self.makeCl(ga,'vc',var,wmo)
        rca=self.makeAnfld(ga,'va',var,0,wmo)
        rcf=self.makeFcfld(ga,'vf',var,tau,wmo)
        
        # -- if OK make departures
        #
        if(rcc and rca and rcf):
            ga.dvar.var('vaa','va-vc')
            ga.dvar.var('vfa','vf-vc')
            ga.dvar.var('vd','vf-va')

            # -- fwrite out temp vars
            #
            if(self.doFwrite):  octlpath=self.fwriteOvars(ovars,ga,wmo,self.odatpath,self.octlpath)
            ga.didFields[var,vdtg,lev,tau]=1

            return(1)
        else:
            
            ga.didFields[var,vdtg,lev,tau]=0
            return(0)
        
    
    #def makeFieldsUV(self,ga,wmo,vdtg,var,lev,tau,override=1):
        
        #""" makes defined variables:
        
        #vc = var climo
        #va = var analysis (an)
        #vf = var forecast (fc)
        #vaa = va-vc = anom an from climo
        #vfa = vf-vc = anom fc from climo
        #vd  = vf-va = fc - an 
        #coslat = cosine weights from makeCoslatWhgt()

        #20140618
        #override = 0 looked like a good idea to avoid redefines, but probably not worth the complexity
        
        #"""

        #if(not(hasattr(ga,'didFields'))):  ga.didFields={}

        #try:
            #doneAlready=(ga.didFields[var,vdtg,lev,tau]==1)
        #except:
            #doneAlready=0
            
        #if(doneAlready and not(override)):
            #print 'AAAAllready done -- var: ',var,' vdtg: ',vdtg,' lev: ',lev,' tau: ',tau
            #return(1)

        #ovars=['wvc','wvf','wva','uvc','uva','uvf','uvaa','uvfa','uvd','vvc','vva','vvf','vvaa','vvfa','vvd']
    
        #ga.vdtg=vdtg
        #ga.set.dtg(vdtg)
        #ga.set.lev(lev)
    
        #ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
        
        #rcc=self.makeCl(ga,'uvc','ua',wmo)
        #rca=self.makeAnfld(ga,'uva','ua',0,wmo)
        #rcf=self.makeFcfld(ga,'uvf','ua',tau,wmo)
    
        #if(rcc and rca and rcf):
            #ga.dvar.var('uvaa','uva-uvc')
            #ga.dvar.var('uvfa','uvf-uvc')
            #ga.dvar.var('uvd','uvf-uva')
        #else:
            #print 'qqqqqqqqqqqqqqqqqqqqqq failed to u in makeFieldsUV'
            #return(0)
    
        #rcc=self.makeCl(ga,'vvc','va',wmo)
        #rca=self.makeAnfld(ga,'vva','va',0,wmo)
        #rcf=self.makeFcfld(ga,'vvf','va',tau,wmo)
    
        #if(rcc and rca and rcf):
            #ga.dvar.var('vvaa','vva-vvc')
            #ga.dvar.var('vvfa','vvf-vvc')
            #ga.dvar.var('vvd','vvf-vva')
            ## -- fwrite out temp vars
            ##
            #####if(self.doFwrite):  octlpath=self.fwriteOvars(ovars,ga,wmo,self.odatpath,self.octlpath)
            #ga.didFields[var,vdtg,lev,tau]=1
            #return(1)
        #else:
            #ga.didFields[var,vdtg,lev,tau]=0
            #return(0)

        #rcc=self.makeCl(ga,'wvc','wa',wmo)
        #rca=self.makeAnfld(ga,'wva','wa',0,wmo)
        #rcf=self.makeFcfld(ga,'wvf','wa',tau,wmo)
        
        #if(rcc and rca and rcf):
            #ga.dvar.var('wvaa','wva-wvc')
            #ga.dvar.var('wvfa','wvf-wvc')
            #ga.dvar.var('wvd','wvf-wva')
            ## -- fwrite out temp vars
            ##
            #if(self.doFwrite):  octlpath=self.fwriteOvars(ovars,ga,wmo,self.odatpath,self.octlpath)
            #ga.didFields[var,vdtg,lev,tau]=1
            #return(1)
        #else:
            #ga.didFields[var,vdtg,lev,tau]=0
            #return(0)
        
    
    
    def makeIvar(self,ivar,tau,fh=1):
        
        expr="%s.%d(lev=%d,ens=f%03d)"%(ivar,fh,self.lev,tau)

        # -- wind speed
        if(ivar == 'wa'):
            expru="ua.%d(lev=%d,ens=f%03d)"%(fh,self.lev,tau)
            exprv="va.%d(lev=%d,ens=f%03d)"%(fh,self.lev,tau)
            expr="mag(%s,%s)"%(expru,exprv)
        
        return(expr)
            
    
    def makeIvarRun(self,ivar,bdtg,tau,fh=1):
        """use ga.set.dtg to set the time...in makeFields"""
        vdtg=mf.dtginc(bdtg,tau)
        gtime=mf.dtg2gtime(vdtg)
        #expr="%s.%d(time=%s,lev=%d)"%(ivar,fh,gtime,self.lev)
        expr="%s.%d(lev=%d)"%(ivar,fh,self.lev)
        
        # -- wind speed
        if(ivar == 'wa'):
            #expru="ua.%d(time=%s,lev=%d)"%(fh,gtime,self.lev)
            #exprv="va.%d(time=%s,lev=%d)"%(fh,gtime,self.lev)
            expru="ua.%d(lev=%d)"%(fh,self.lev)
            exprv="va.%d(lev=%d)"%(fh,self.lev)
            expr="mag(%s,%s)"%(expru,exprv)
            
        return(expr)
            
    def makeIvarRunAn(self,ivar,bdtg,tau,fh=1):
        
        vdtg=mf.dtginc(bdtg,tau)
        gtime=mf.dtg2gtime(vdtg)
        expr="%s.%d(lev=%d,ens=f%03d)"%(ivar,fh,self.lev,tau)
        
        # -- wind speed
        if(ivar == 'wa'):
            #expru="ua.%d(time=%s,lev=%d,ens=f%03d)"%(fh,gtime,self.lev,tau)
            #exprv="va.%d(time=%s,lev=%d,ens=f%03d)"%(fh,gtime,self.lev,tau)
            expru="ua.%d(lev=%d,ens=f%03d)"%(fh,self.lev,tau)
            exprv="va.%d(lev=%d,ens=f%03d)"%(fh,self.lev,tau)
            expr="mag(%s,%s)"%(expru,exprv)
            
        return(expr)
            
                

    

class WmoAreaGrid(MFbase):


    ggdx=2.5
    ggdy=2.5
    globalgrid='pole'

    # -- new standard
    #
    ggdx=1.5
    ggdy=1.5

    # -- new standard has a pole point
    #globalgrid='nopole'
    # --use box averaging because wmo grid coarser than models circa 2000-2010 and is set in para 6.1 Table F 20120
    #
    method='ba'
    
    xlinear=1
    ylinear=1

    # global grid (gg) properties
    
    ggdlat=180.0
    ggdlon=360.0
    
    gglat1=-90.0
    gglat2=gglat1+ggdlat
    gglon1=0.0
    gglon2=gglon1+ggdlon

    areas={
        'nhem':[20,90,0,360],
        'shem':[-90,-20,0,360],
        'tropics':[-20,20,0,360],
        }

    ggshfilt=0
    ggshfiltNwaves=20
    
    def __init__(self,globalgrid=globalgrid,method=method):


        if(self.globalgrid == 'nopole'):
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)
            self.gglat11=self.gglat1+self.ggdy*0.5
            self.gglon11=self.gglon1+self.ggdx*0.5
        else:
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)+1
            self.gglat11=self.gglat1
            self.gglon11=self.gglon1

        rexopt='linear'
        reyopt='linear'

        self.method=method
        self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(self.ni,rexopt,self.gglon11,self.ggdx,self.nj,reyopt,self.gglat11,self.ggdy,self.method)
        
        # -- hange output dirs here
        #
        self.tdirSTATS=tdirSTATS
        self.tdirPYPDB=tdirPYPDB
        self.tdirFIELDS=tdirFIELDS
        self.tdirPLTS=tdirPLTS
        
        
        
    def setCtlhead(self,odatfile='grads.fwrite'):
        
        (dir,datfile)=os.path.split(odatfile)
        self.ctlhead="""dset ^%s
title wmo grid arrays used in stats
undef 1e20
xdef %d linear %f %f
ydef %d linear %f %f
zdef  1 levels 1013
tdef  1 linear 18z4jul1776 6hr"""%(datfile,
                                   self.ni,self.gglon1,self.ggdx,
                                   self.nj,self.gglat1,self.ggdy,
                                   )


    def getAreaLatLon(self,area='nhem'):
            
        self.lat1=self.areas[area][0]
        self.lat2=self.areas[area][1]
        self.lon1=self.areas[area][2]
        self.lon2=self.areas[area][3]


    def makeCoslatWght(self,ga,ovar,fh=1):
        from math import pi
        expr="(cos(lat.%d(t=1)*%g/%f))"%(fh,pi,self.ggdlat)
        ga.dvar.regrid(ovar,expr,self.reargs)
        return(1)
    
        
    def makeSinlatWght(self,ga,wmo,fh=1):
        from math import pi
        dyh=wmo.ggdx*0.5
        ggdlat=wmo.ggdlat
        fh=ga.nfAn
        exprhi="(sin((lat.%d(t=1)+%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
        exprlo="(sin((lat.%d(t=1)-%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
        ga.dvar.regrid('sinhi',exprhi,wmo.reargs)
        ga.dvar.regrid('sinlo',exprlo,wmo.reargs)
        ga.dvar.var('dsinlat','abs(sinhi-sinlo)*%g'%(wmo.ggdy))
        return(1)
    
    
    # -- setup areas veriables
    #
    def setAreaVars(self,vStd='wmo',model='gfs2',dtau=24,bdtg=None):
        
        areavars={}
        areaTaus=[]
        
        if(vStd == 'wmo'):
            areas=['nhem','shem','tropics']
    
            areavars['nhem']=[
                ['zg',850], ['zg',500], ['zg',250], ['zg',100],
                ['hur',850],['hur',700],
                ['ta',850], ['ta',500], ['ta',250], ['ta',100],
                ['uva',850],['uva',500],['uva',250],['uva',100],
            ]
    
            areavars['shem']=areavars['nhem']
    
            areavars['tropics']=[
                ['zg',500],
                ['ta',850],['ta',500],['ta',200],['ta',100],
                ['hur',850],['hur',700],
                ['uva',850],
                ['uva',500],
                ['uva',250],
                ['uva',200],
                ['uva',100],
            ]
            
        elif(vStd == 'hur'):
    
            areas=['nhem','tropics']
    
            areavars['nhem']=[
                ['hur',700],
            ]   
    
            areavars['shem']=areavars['nhem']
    
            areavars['tropics']=[
                ['hur',850],
                ['hur',700],
                ]
            areaTaus=[0,72]

        elif(vStd == 'zg500'):
    
            areas=['nhem']
    
            areavars['nhem']=[
                ['zg',500],
            ]   
    
            areavars['shem']=areavars['nhem']
    
            areavars['tropics']=[
                ['hur',850],
                ['hur',700],
                ]
            
            #areaTaus=[0,72]

        elif(vStd == 'wa'):
    
            areas=['nhem','tropics']
    
            areavars['nhem']=[
                ['uva',200],
            ]   
    
            areavars['shem']=areavars['nhem']
    
            areavars['tropics']=[
                ['uva',850],
                ['uva',200],
                ]
            areaTaus=[0,72]

        else:
            print 'EEE invalid vStd: ',vStd,' in setAreaVars...'
            sys.exit()
        

        if(len(areaTaus) == 0):
            
            (is0012,remainder)=MF.isSynopticHour(bdtg,12)
            
            etau=240
            
            if(model == 'gfs2'):
                etau=192
                
            elif(model == 'cmc2'):
                if(is0012 and remainder == 12):
                    etau=144
                elif(is0012):
                    etau=168
                else:
                    print 'EEEE setAreaVars: invalid dtg for cmc2: ',bdtg,' sayoonara...'
                    sys.exit()
                
            elif(model == 'navg'):
                if(is0012):
                    etau=180
                else:
                    etau=144
                
            elif(model == 'ukm2'):
                if(not(is0012)):
                    etau=60
                else:
                    etau=144
    
            elif(model == 'fim8'):
                if(is0012):
                    etau=240
                else:
                    print 'EEEE setAreaVars: invalid dtg for fim8: ',bdtg,' sayoonara...'
                    sys.exit()
                    
            elif(model == 'ecm2'):
                if(is0012):
                    etau=240
                else:
                    print 'EEEE setAreaVars: invalid dtg for ecm2: ',bdtg,' sayoonara...'
                    sys.exit()
                
            areaTaus=range(0,etau+1,dtau) 
        
            
        return(areas,areavars,areaTaus)

if (__name__ == "__main__"):

    modelopt='gfs2'
    dtgopt='2011050100.2011051900.12'
    dtgopt='2011041500.2011051900.12'
    dtgs=mf.dtg_dtgopt_prc(dtgopt)

    if(modelopt == 'all'):
        models=n2.allmodels
    else:
        models=modelopt.split(',')
    
    for model in models:
        m2=EnsModel(model,dtgs)
        m2.doLnFc(override=0,ropt='',verb=1)
        m2.EnsFcCtl()
        m2.ls()

    sys.exit()

