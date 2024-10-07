#!/usr/bin/env pythonw

from tcbase import *
from sBT import Mdeck3,sbtSrcDir

undef=-999.

class Trkdata(MFbase):

    def __init__(self,
                 rlat,
                 rlon,
                 vmax,
                 pmin=undef,
                 dir=undef,
                 spd=undef,
                 tccode='XX',
                 wncode='XX',
                 trkdir=undef,
                 trkspd=undef,
                 dirtype='X',
                 b1id='X',
                 tdo='XXX',
                 ntrk=0,
                 ndtgs=0,
                 r34m=undef,
                 r50m=undef,
                 r34=undef,
                 r50=undef,
                 alf=undef,
                 depth='X',
                 poci=undef,
                 roci=undef,
                 rmax=undef,
                 ):


        self.undef=undef
        self.rlat=rlat
        self.rlon=rlon
        self.vmax=vmax
        self.pmin=pmin
        self.dir=dir
        self.spd=spd
        self.tccode=tccode
        self.wncode=wncode
        self.trkdir=trkdir
        self.trkdir=trkspd
        self.dirtype=dirtype
        self.b1id=b1id
        self.tdo=tdo
        self.ntrk=ntrk
        self.ndtgs=ndtgs
        self.r34=r34
        self.r50=r50
        self.r34m=r34m
        self.r50m=r50m
        self.alf=alf
        self.depth=depth
        self.poci=poci
        self.roci=roci
        self.rmax=rmax


    def gettrk(self):

        trk=(self.rlat,self.rlon,self.vmax,self.pmin,
             self.dir,self.spd,
             self.tccode,self.wncode,
             self.trkdir,self.trkspd,self.dirtype,
             self.b1id,self.tdo,self.ntrk,self.ndtgs,
             self.r34m,self.r50m,self.alf,self.sname,
             self.r34,self.r50,self.depth,
             )

        return(trk)


    def getposit(self):

        posit=(self.rlat,self.rlon,self.vmax,self.pmin,
               self.dir,self.spd,self.tccode,
               )
        return(posit)




class MD3trk(MDdataset):

    undef=-999.
    
    def __init__(self,cards,stm1id,stm9xid,basin=None,sname=None,stmDev=None,dobt=0,doPutDSs=0):

        # -- input
        #
        self.cards=cards
        (self.itrk,self.idtgs)=self.getTrk4Cards()
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm1id)
         
        self.b1id=b1id
        self.snum=snum
        self.syear=year
        self.stm2id=stm2id
        self.ostm2id=stm2id
        self.stm1id=stm1id
        self.stm9xid=stm9xid
        self.basin=basin
        self.sname=sname
        self.stmDev=stmDev

        # -- output
        #
        self.trk={}
        
        # -- make trk and analyze
        #
        rc=self.makeTrkdata()
        rc=self.anlMDtrk()

    def getTrk4Cards(self,verb=0):
        
        undef=self.undef
        cards=self.cards
        itrk={}
        for card in cards:
            tt=card.split(',')
            dtg=tt[0].strip()
            ott=[]
            for t in tt[1:]:
                ott.append(t.strip())
            itrk[dtg]=ott
            
        idtgs=itrk.keys()
        idtgs.sort()
        
        if(verb):
            for idtg in idtgs:
                print 'iii',idtg,itrk[idtg]
            
        return(itrk,idtgs)
    
    def getTrkData4Itrk(self,dtg,ntrk,ndtgs,verb=0):
#     01W.2019', '', '11.2', '125.6', '20', '', '183', '9', '195', '8', '', '', '', '', '', '', '', '', '', '', 'NT', 'NW', 'c', 'c', '', '', '0.27', '', '', '', '', '---']   
        #     0   1      2        3     4    5     6    7      8    9   10  11  12  13  14  15  16  17  18  19   20    21    22   23  24  25     26   27  28  29  30    31
        trk=self.itrk[dtg]

        n=0
        stmid=trk[n] ; n=n+1                       # 0
        sname=trk[n] ; n=n+1                       # 1
        
        rlat=float(trk[n]) ; n=n+1                 # 2
        rlon=float(trk[n]) ; n=n+1                 # 3       
        
        if(trk[n] != 'NaN' and trk[n] != '' ): vmax=float(trk[n])       # 4
        else: vmax=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): pmin=float(trk[n])       # 5
        else: pmin=undef
        n=n+1
        
        if(trk[n] != 'NaN'and trk[n] != '' ): dir=float(trk[n])        # 6
        else: dir=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): spd=float(trk[n])        # 7
        else: spd=undef
        n=n+1
        
        if(trk[n] != 'NaN' and trk[n] != '' ): trkdir=float(trk[n])     # 8
        else: trkdir=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): trkspd=float(trk[n])     # 9
        else: trkspd=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34m=float(trk[n])     #10
        else: r34m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34ne=float(trk[n])     #11
        else: r34ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34se=float(trk[n])     #12
        else: r34se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34sw=float(trk[n])     #13
        else: r34sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34nw=float(trk[n])     #14
        else: r34nw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50m=float(trk[n])      #15
        else: r50m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50ne=float(trk[n])     #16
        else: r50ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50se=float(trk[n])     #17
        else: r50se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50sw=float(trk[n])     #18
        else: r50sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50nw=float(trk[n])     #19
        else: r50nw=undef
        n=n+1

        r34=[r34ne,r34se,r34sw,r34nw]
        r50=[r50ne,r50se,r50sw,r50nw]
        
        tccode=trk[n]     #20
        n=n+1

        wncode=trk[n]     #21
        n=n+1

        dirtype=trk[n]     #22
        n=n+1

        postype=trk[n]     #23
        n=n+1


        if(trk[n] != 'NaN' and trk[n] != '' ): roci=float(trk[n])   #24
        else: roci=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): poci=float(trk[n])   #25
        else: poci=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): alf=float(trk[n])   #26
        else: alf=undef
        n=n+1

        depth=trk[n]     #27
        n=n+1

        # -- bug in parseDssTrk
        #
        if(len(trk) > 30):
            unknown=trk[n]     #28
            n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): rmax=float(trk[n])   #29
        else: rmax=undef
        n=n+1

        tdo=trk[n]   #30
        if(tdo == 'NaN' or tdo == '---'): tdo='   '
        n=n+1

        if(verb):
            print self.b1id,rlat,rlon,vmax,pmin,dir,spd
            print tccode,wncode,self.b1id,tdo,ntrk,ndtgs
            print r34m,r34m,r50m,depth
            print r34,r50,poci,roci,rmax
            
        self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,\
                              tccode,wncode,b1id=self.b1id,tdo=tdo,ntrk=ntrk+1,ndtgs=ndtgs+1,
                              r34m=r34m,r50m=r50m,depth=depth,
                              r34=r34,r50=r50,poci=poci,roci=roci,
                              rmax=rmax)        
        
        self.trk[dtg].tdo=tdo
        self.trk[dtg].alf=alf
        self.trk[dtg].sname=sname
        self.trk[dtg].stmid=stmid
        self.trk[dtg].postype=postype
        self.trk[dtg].ostm2id=self.ostm2id
        
                
    def makeTrkdata(self,verb=0):
        
        ntrk=0
        ndtgs=0
        dtgs=self.idtgs
        for dtg in dtgs:
            if(verb): print 'ddd',dtg,len(self.itrk[dtg]),self.itrk[dtg]
            
            self.getTrkData4Itrk(dtg,ntrk,ndtgs)
            
            ntrk=ntrk+1
            ndtgs=ndtgs+1
            
            
        
        # -- get prev 12-h track dir/spd
        #
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=mf.dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        self.ndtgs=ndtgs
        self.dtgs=dtgs

        # -- set the bt dir/spd and dirtype
        #
        for dtg in dtgs:
            
            self.trk[dtg].dirtype=self.trk[dtg].postype
            (trkdir,trkspd)=dirspd[dtg]

            if( (self.trk[dtg].dir == None)):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    
        
        
    def anlMDtrk(self,stmD=None,verb=0):

        (ltln,latmn,latmx,lonmn,lonmx,latb,lonb)=self.getlatlon()
        
        (gendtg,gendtgs,genstdd,time2gen)=self.getgenesis()
        if(self.sname != None): sname=self.sname
        else:
            sname=self.getname()
            
        (vmax,ace,stcd)=self.getvmax()
        (nRI,nED,nRW,dRI,dED,dRW)=self.getRI()
        (tclife,stclife,stmlife)=self.gettclife()
        syear=self.stm1id.split('.')[1]

        rc=getStmParams(stm1id)
        
        # -- if a warning is put, set stmlife to tcgen -- for 9X with warnings in the adecks
        #
        if(time2gen > 0 and Is9X(self.stm1id)):
            stmlife=time2gen/24.0


        if(verb):
            print 'FFFFFFFFFF(stm1|2id0:  ',self.stm2id,self.stm1id
            print 'FFFFFFFFFF(tclife):    ',tclife
            print 'FFFFFFFFFF(stclife):   ',stclife
            print 'FFFFFFFFFF(stmlife):   ',stmlife

            print 'FFFFFFFFFF(ace):       ',ace
            print 'FFFFFFFFFF(stcd):      ',stcd

            print 'FFFFFFFFFF(latb):      ',latb
            print 'FFFFFFFFFF(lonb):      ',lonb
            
            print 'FFFFFFFFFF(latmn):     ',latmn
            print 'FFFFFFFFFF(latmx):     ',latmx
            print 'FFFFFFFFFF(lonmn):     ',lonmn
            print 'FFFFFFFFFF(lonmx):     ',lonmx

            print 'FFFFFFFFFF(gendtg):    ',gendtg
            print 'FFFFFFFFFF(gendtgs):   ',gendtgs
            print 'FFFFFFFFFF(genstdd):   ',genstdd
            print 'FFFFFFFFFF(time2gen):  ',time2gen
            print 'FFFFFFFFFF(sname):     ',sname
            print 'FFFFFFFFFF(vmax):      ',vmax

            print 'FFFFFFFF(nRI):         ',nRI
            print 'FFFFFFFF(nED):         ',nED
            print 'FFFFFFFF(nRW):         ',nRW

            print 'FFFFFFFF(dRI):         ',dRI
            print 'FFFFFFFF(dED):         ',dED
            print 'FFFFFFFF(dRW):         ',dRW


        # -- decorate stm Dataset
        #
        
        self.gendtg=gendtg
        self.gendtgs=gendtgs
        self.genstdd=genstdd
        self.time2gen=time2gen

        self.sname=sname
        self.vmax=vmax

        self.ace=ace
        self.stcd=stcd

        self.tclife=tclife
        self.stclife=stclife
        self.stmlife=stmlife

        self.latb=latb
        self.lonb=lonb
        
        self.latmn=latmn
        self.lonmn=lonmn
        
        self.latmx=latmx
        self.lonmx=lonmx
    
        self.nRI=nRI
        self.nED=nED
        self.nRW=nRW
        self.dRI=dRI
        self.dED=dED
        self.dRW=dRW
        
        
        # -- adjust 9X dtgs
        #
        if(self.gendtg != None):
            dtg9Xs=mf.dtgrange(self.dtgs[0],self.gendtg)
            if(len(dtg9Xs) > 0):
                for dtg9x in dtg9Xs[0:-1]:
                    if(dtg9x in self.dtgs):
                        self.trk[dtg9x].stmid=self.stm9xid

        
    def getRI(self,dvmaxRI=30,dvmaxED=50,dvmaxRD=-30):

        dRI=dED=-999
        dRW=999
        nRI=0
        nED=0
        nRW=0
        
        for dtg in self.dtgs:
            dtgm24=mf.dtginc(dtg,-24)
            if(dtgm24 in self.dtgs):
                ttm24=self.trk[dtgm24]
                tt=self.trk[dtg]
                vmaxm24=ttm24.vmax
                vmax=tt.vmax
                if(vmax != None):
                    dvmax=vmax-vmaxm24
                else:
                    continue
                if(dvmax >= dvmaxRI):
                    nRI=nRI+1
                    if(dvmax > dRI and dvmax < dvmaxED): dRI=dvmax
                
                if(dvmax >= dvmaxED):
                    nED=nED+1
                    if(dvmax > dED): dED=dvmax

                if(dvmax <= dvmaxRD):
                    nRW=nRW+1
                    if(dvmax < dRW): dRW=dvmax
                

                

        return(nRI,nED,nRW,dRI,dED,dRW)

    def getvmax(self,ddtg=6):
        """assume ddtg=6h"""
        vmax=-999
        ace=0.0
        stcd=0.0
        n=0
        ns=0
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            svmax=tt.vmax
            if(svmax > vmax and svmax != self.undef): vmax=tt.vmax

            tace=aceTC(svmax)
            if(tace > 0.0):
                ace=ace+tace*ddtg
                ns=ns+1

            stcd=stcd+scaledTC(svmax)
            n=n+1

        stcd=stcd*0.25

        if(ns > 0):
            ace=ace/(24.0*tymin*tymin)

        return(vmax,ace,stcd)




    def getname(self):

        sname='---------'
        snames=[]
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            #if(tt.sname[0:5] != 'NONAME' and tt.sname[0:5] != 'INVES' and tt.sname != ''):
            if(tt.sname[0:5] == 'INVES' or tt.sname == ''):
                continue
            else:
                snames.append(tt.sname)

        snames=mf.uniq(snames)
        return(sname)

        
    def getgenesis(self,dtgm=-18,dtgp=+12,vmaxTD=25.0,vmaxMin=10.0,verb=0):

        time2gen=-999.
        gendtg=gendtgWN=gendtgBT=None
        stdd=0.0
        
        gendtgs=[]
        genstd=None

        minvmax=1e20
        maxvmax=-1e20
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            if(tt.wncode.lower() == 'wn' and gendtgWN == None): gendtgWN=dtg

        # -- if gendtg = None; then no warnings!  use when became tc...
        #
        tcCodeWind=0
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            istc=IsTc(tt.tccode)
            if(tt.tccode == 'TW'):tcCodeWind=1
            if(istc >= 1 and gendtgBT == None): gendtgBT=dtg

        if(gendtgWN != None):
            if(tcCodeWind >= 0):  gendtg=gendtgWN
            else:                 gendtg=gendtgBT
            
        if(gendtg == None and gendtgBT != None): gendtg=gendtgBT
        
        if(gendtg != None):

            time2gen=mf.dtgdiff(self.dtgs[0],gendtg)
            
            bdtg=mf.dtginc(gendtg,dtgm)
            edtg=mf.dtginc(gendtg,dtgp)
            gendtgs=mf.dtgrange(bdtg,edtg)


            stddtime=0.0
            ngd=len(gendtgs)
            for n in range(1,ngd):
                dtgm1=gendtgs[n-1]
                dtg0=gendtgs[n]
                
                if(dtg0 in self.dtgs and dtgm1 in self.dtgs):

                    dtau=mf.dtgdiff(dtgm1,dtg0)
                    ttm1=self.trk[dtgm1]
                    tt0=self.trk[dtg0]
                    
                    vmaxm1=ttm1.vmax
                    vmaxm0=tt0.vmax
                    if(vmaxm1 < 0): vmaxm1=vmaxMin
                    if(vmaxm0 < 0): vmaxm0=vmaxMin

                    if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                    if(vmaxm1 < minvmax): minvmax=vmaxm1
                    if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                    if(vmaxm0 < minvmax): minvmax=vmaxm0
                    
                    stdd=stdd+(((vmaxm1+vmaxm0)*0.5)/vmaxTD)*dtau
                    stddtime=stddtime+dtau

                    if(verb): print 'ggggggggggg ',dtau,dtg0,dtgm1,vmaxm1,vmaxm0,stdd,stddtime

            if(stddtime > 0.0):

                stdd=stdd/24.0
                if(verb): print 'ggggggggggg final stdd: ',stdd


        genstdd=stdd

        if(verb):
            print 'ggggggg ',gendtg
            print 'ggggggg ',gendtgs
            print 'ggggggg ',genstdd
            print 'ggggggg ',time2gen

        return(gendtg,gendtgs,genstdd,time2gen)
    
    def getlatlon(self):

        latb=0.0
        lonb=0.0
        
        latmn=999
        latmx=-999
        lonmn=999
        lonmx=-999

        latlon={}
        n=0
            
        for dtg in self.dtgs:
            tt=self.trk[dtg]

            tlat=tt.rlat
            if(n==0):  tlonPri=tt.rlon
            tlon=tt.rlon
            
            # -- cross prime meridion
            if(tlon < primeMeridianChk and tlonPri > primeMeridianChk): tlon=tlon+360.0
            
            if(tlat > latmx): latmx=tlat
            if(tlon > lonmx): lonmx=tlon
            if(tlat < latmn): latmn=tlat
            if(tlon < lonmn): lonmn=tlon
            n=n+1
            latb=latb+tlat
            lonb=lonb+tlon
            latlon[dtg]=(tlat,tlon)
            tlonPri=tlon

        if(n>0):
            latb=latb/n
            lonb=lonb/n

        ndtgs=len(self.dtgs)
        for n in range(0,ndtgs):
            dtg=self.dtgs[n]
            tt=self.trk[dtg]
            
        return(latlon,latmn,latmx,lonmn,lonmx,latb,lonb)


    def gettclife(self):

        tclife=0
        stclife=0
        stmlife=0
        
        ndtgs=len(self.dtgs)

        if(ndtgs == 0):
            return(tclife,stclife,stmlife)
            
        for n in range(1,ndtgs):
            tt=self.trk[self.dtgs[n]]
            dtau=mf.dtgdiff(self.dtgs[n-1],self.dtgs[n])
            stmlife=stmlife+dtau
            if(IsTc(tt.tccode) == 1):
                tclife=tclife+dtau
            if(IsTc(tt.tccode) == 2):
                stclife=stclife+dtau
            
        tclife=tclife/24.0
        stclife=stclife/24.0
        stmlife=stmlife/24.0

        return(tclife,stclife,stmlife)
            

    def lsDSsDtgs(self,dtgs=None,dobt=0,dupchk=0,verb=0,selectNN=1,countsOnly=0,filtTCs=0,doprint=1):

        if(dtgs == None):
            dtgs=self.dtgs
        else:
            if(not(type(dtgs) is ListType)): dtgs=[dtgs]
            else: dtgs=dtgs
            
        itrk=None

        dobtLs=dobt
        if(filtTCs): dobtLs=1

        cards=[]
        ncards=0
        nstrms=0
        nstms=1
        stmid=self.stm1id
        sname=self.sname
        
        for dtg in dtgs:

            if(dtg in self.dtgs):
                
                gentrk=0
                if(dtg in self.gendtgs): gentrk=1
                trk=self.trk[dtg]
                card=printTrk(trk.stmid,dtg,trk.rlat,trk.rlon,trk.vmax,trk.pmin,
                              trk.dir,trk.spd,trk.dirtype,trk.tdo,
                              tccode=trk.tccode,wncode=trk.wncode,
                              r34m=trk.r34m,r50m=trk.r50m,alf=trk.alf,
                              ntrk=trk.ntrk,ndtgs=trk.ndtgs,
                              sname=sname,gentrk=gentrk,doprint=doprint)
                cards.append(card)
                ncards=ncards+1
                
        else:
            nstms=0
            nstmTCs=0
            
        if(countsOnly):
            if(filtTCs):
                print dtg,'N: ',nstmTCs
            else:
                print dtg,'N: ',nstms
                
        if(ncards == 0 and not(countsOnly)): 
            if(filtTCs): 
                print "%s-N"%(dtg),'   NNNNNNNNNNNNNN: filtTCs: ',filtTCs,' nstrms All: ',nstrms
            else:
                print "%s-N -- no storms for this dtg..."%(dtg)    

        return(cards)

    def lsDSsStmSummary(self,
                        doprint=1,warn=0):

        # -- season storm card
        #
        
        stmid=self.stm1id
        sname=self.sname

        if(hasattr(self,'ace')):

            curdtg=mf.dtg()
            curdtgm6=mf.dtginc(curdtg,-6)

            if(len(self.dtgs) == 0):
                if(warn): print 'DDDDDDDDDDDDDDDDDd nada dtgs for stmid: ',stmid
                return

            bdtg=self.dtgs[0]
            edtg=self.dtgs[-1]
            
            ostmid=stmid
                
                
            (snum,b1id,yyyy,b2id,stm2id,stm1id)=getStmParams(ostmid)

            stm=snum+b1id

            livestatus=' '
            tctype=TCType(self.vmax)
            edtgdiff=mf.dtgdiff(edtg,curdtg)
            if(edtg == curdtg or edtg == curdtgm6 or edtgdiff <= 0.0): livestatus='*'
            RIstatus=' NaN '
            timeGen=' NaN '
            if(self.nRI > 0): RIstatus='rrRI'
            if(self.nED > 0): RIstatus='rrED'
            if(self.nRW > 0):
                RIstatus='ddRW'
                if(self.nRI > 0): RIstatus='ddRI'
                if(self.nED > 0): RIstatus='ddED'

                
            stm9x=''
            ostmid9x=self.stm9xid
                
            pad=''
            if(len(stm9x) > 0): pad=' '
            if(self.stmDev == None):
                if(IsNN(ostmid)):
                    stmDev='NN'
                elif(IsNN(ostmid9x)):
                    stmDev='DEV'
                else:
                    stmDev='nonDEV'
            else:
                stmDev=self.stmDev
            
            if(IsNN(ostmid9x)):
                stm9x=stm9x+pad+"NN , %s"%(ostmid9x.split('.')[0])
            else:
                stm9x=stm9x+pad+"9X , %s"%(ostmid9x.split('.')[0])


            otimeGen='NaN'
            if(hasattr(self,'time2gen') and not(Is9X(stmid))):
                if(self.time2gen >= 0.0):
                    timeGen="tG:%3.0f"%(self.time2gen)
                    otimeGen="%3.0f"%(self.time2gen)
                    
            oACE=self.ace
            if(Is9X(stmid)): oACE=0.0


            ovmax="%3d"%(self.vmax)
            if(self.vmax == self.undef): ovmax='***'

            #if(mf.find(stmid,'CC')):
                #tctype='___'

                #ocard="%s %s%1s %3s %-10s :%s :%4.1f;%4.1f :%5.1f %5.1f :%s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%s"%\
                    #(yyyy,stm,livestatus,tctype,sname[0:9],ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
                     #self.latmn,self.latmx,self.lonmn,self.lonmx,
                     #stm9x)
            #else:

            try:
                n=int(stm[0:2])
                ogendtg="%s"%(self.gendtg)
            except:
                ogendtg='NaN'

            ocard="%s.%s ,  %3s , %s , %s , %s , %5.1f , %5.1f , %5.1f , %5.1f , \
%s , %s , %5.1f , %-5.1f , %5.1f , %-5.1f , %4.1f , %4.1f , \
%2d , %2d , %2d , %s , %s , %s , %s"%\
                                    (stm,yyyy,tctype,stmDev,sname,ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
                                     self.latmn,self.latmx,self.lonmn,self.lonmx,
                                     self.stcd,oACE,
                                     self.nRI,self.nED,self.nRW,
                                     RIstatus,stm9x,otimeGen,ogendtg)

                
            if(doprint): 
                print ocard
            return(ocard)


def parseDssTrk(dtg,dds,verb=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    osname='               , '
    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
 
    oroci='   '
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='    '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    ovmax='   '
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='    '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34 != None and r34 != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34='     ,     ,     ,     ,'
        or34m='    , '
    
    got50=0
    if(r50 != None and r50 != undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50='     ,     ,     ,     ,'
        or50m='     , '
        if(got34):
            or50m='    , '

    ormax='   , '
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='  , '
    if(depth != None and depth != undef):
        odepth='%s , '%(depth)
        
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    odtgstm="%s , %s , %s , "%(dtg,stmid,osname)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf='    '
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    return(ocard)
    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
    elif(Is9X(stmid)):
        stype='9X'
        stm9xid=stmid
        sname=ss[2]
        if(mf.find(sname,'NON')):
            stm1id='XXX.%s'%(ss[1])
        else:
            stm1id="%s.%s"%(ss[-1],ss[1])
        
    return(stype,stm1id,sname,stm9xid)         
    
# -- bug in parseDssTrk -- handle here since we can't redo making NNW-sum.txt
#
def parseDssTrkMD3(dtg,dds,stm1id,stm9xid,sname=None,verb=0,warn=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    # -- not here...sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
    else:
        osname="%-15s"%('NaN')
 
    oroci='NaN'
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='NaN '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='NaN '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34m != None and r34m != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34=' NaN , NaN , NaN , NaN ,'
        or34m='NaN , '
    
    got50=0
    if(r50m != None and r50m!= undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50=' NaN , NaN , NaN , NaN ,'
        or50m=' NaN , '
        if(got34):
            or50m='NaN , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth=' %s '%(depth)
        
    ostmid=stmid.lower()

    subo=ostmid[2].lower()
    sub1=stm1id[2].lower()
    sub9=stm9xid[2].lower()
    
    # -- 9X crossing basins
    #
    crossW2B=(sub1 == 'w' and sub9 == 'b')
    crossC2W=(sub1 == 'c' and sub9 == 'w')
    # -- only place to change subbasin id is in io and shem
    #
    basinID=(basin == 'io' or basin == 'shem')
    if(Is9X(stmid) and (subo != sub9) and basinID):
        if(stmDev == 'DEV'):
            ostmid=stm1id
        else:
            ostmid=stm9xid
        ostmid=ostmid.lower()
        if(warn): print '9999  mismatch input: ',stmid.lower(),' output: ',ostmid
            
    if(IsNN(stmid) and subo != sub1):
        ostmid=stm1id.lower()
        if(warn): print 'NNNN mismatch input : ',stmid.lower(),' output: ',ostmid
        
        
    odtgstm="%s , %s , %s ,"%(dtg,ostmid,osname)
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf=' NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    if(tdo == '---' or tdo == '   '): tdo='NaN'
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    return(ocard)
    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    basin=ss[-2]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        if(len(ss) == 5):
            sname="%s-%s"%(ss[2],ss[3])
        else:
            sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
        stm9xid=stm9xid.lower()
    elif(Is9X(stmid)):
        sname='9X-%s'%(ss[0])
        stm9xid=stmid
        stype=ss[2]
        if(stype == 'NONdev'):
            stm1id=stmid
        elif(stype == 'DEV'):
            stm1id="%s.%s"%(ss[-1],ss[1])
        else:
            stm1id='XXX.%s'%(ss[1])
            stm1id=stm1id
            
        stm1id=stm1id.lower()
        
    return(stype,stm1id,sname,stm9xid,basin)         
    
    
    
class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'doCarq':         ['q',0,1,'parse the cq0/12/24 and of12/24 objects on dds'],
            'doWorkingBT':    ['W',0,1,'using working/b*.dat for bdecks vice ./b*.dat'],
            'oPath':          ['o:',None,'a','write output to oPath'],
            'sumPath':        ['r:',None,'a','read path to generate summary card'],
            'doTrk':          ['T',0,1,'make the md3 trk from the -sum.txt files'],
            'doBdeck2':       ['2',0,1,'use bdeck2 vice bdeck'],
            }

        self.purpose='''
make mdeck3'''
        
        self.examples='''
%s -S 30w.19'''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(sumPath != None):
    
    rc=getStmids4SumPath(sumPath)
    (stmDev,ostm1id,sname,ostm9xid,basin)=rc
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()
        
    try:
        icards=open(sumPath).readlines()
    except:
        print """EEE can't read sumPath: %s -- sayounara"""%(sumPath)
        sye.exit()
    

    (sdir,sfile)=os.path.split(sumPath)
    #print 'sname: ',sname,stmDev
    if(verb):
        print 'spath: ',sumPath
    ostm1id=stm1id.replace('.','-')

    if(verb):
        print 'stm1id:  ',stm1id
        print 'stm9xid: ',stm9xid
        print 'sdir:    ',sdir
        print 'sfile:    ',sfile
        
    ofile="%s-md3.txt"%(ostm1id.upper())
    if(mf.find(sfile,'BT')):
        ofile="%s-md3-BT.txt"%(ostm1id.upper())
        
    ofileS=ofile.replace('md3','sum-md3')

    if(mf.find(sfile,'MRG')):
        ofileS=ofile.replace('md3','sum-md3-MRG')
    
    opathS="%s/%s"%(sdir,ofileS)
    opath="%s/%s"%(sdir,ofile)

    if(verb):
        print 'stm1id: ',stm1id
        print 'sname:  ',sname
        print 'stmDev: ',stmDev
        print 'sdir:   ',sdir
        print 'sfile:  ',sfile
        print 'ofile:  ',ofile
        print 'ofileS: ',ofileS
        
        print 'opath:  ',opath
        print 'opathS: ',opathS

    if(verb):    
        for icard in icards:
            print 'iii',icard[0:-1]
        
    ocards=[]
    md3=MD3trk(icards,stm1id,stm9xid,sname=sname,basin=basin,stmDev=stmDev)
    dtgs=md3.dtgs
    trk=md3.trk
    
    if(doTrk):
        ktrk=trk.keys()
        ktrk.sort()
        
        for kt in ktrk:
            ocard=parseDssTrkMD3(kt,trk[kt],stm1id,stm9xid,sname=sname)
            ocard=ocard.replace(' ','')
            if(verb): print 'ooo',ocard
            ocards.append(ocard)

        rc=MF.WriteList2Path(ocards, opath)
    
    m3sum=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+'\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    print m3sum[0:-1]

    sys.exit()
       



# -- dtgs
#
if(dtgopt != None):

    selectNN=1
    if(ls9x or doCARQonly): selectNN=0
    
    tcD=TcData(dtgopt=dtgopt,doWorkingBT=doWorkingBT,verb=verb)

# -- storms
#
if(stmopt != None):
    
    md3=Mdeck3(doBT=0,doSumOnly=1)
    
    tcD=TcData(stmopt=stmopt,doWorkingBT=doWorkingBT,doBdeck2=doBdeck2,verb=verb)
    stmids=tcD.makeStmListMdeck(stmopt,dobt=dobt,cnvSubbasin=0,verb=verb)
    
    for stmid in stmids:
          
        dobt=0      
        print 'stmid: ',stmid
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        
        dds=tcD.getDSsFullStm(stmid, dobt=dobt, doprint=0, set9xfirst=0, dowarn=0)
        scard=tcD.lsDSsStmSummary(dds,stmid,doprint=0)
        
        # -- bypass active storms
        #
        ss=scard.split()
        snumSum=ss[1]
        if(mf.find(snumSum,'*')):
            print 'WWW--stmid: ',stmid,"""is still active...don't make tdir yet...press..."""
            continue
        
        #dds.ls()
        sname=dds.sname
        
        try:
            stmid9x=dds.stmid9x.upper()
        except:
            stmid9x=None
            
        try:
            stmidNN=dds.stmidNN.upper()
        except:
            stmidNN=None
            
        try:
            stm1id=dds.stm1id
        except:
            stm1id=None
            
        
        if(IsNN(stmid)):
            tname=stmid.replace('.','-').upper()
            tname="%s-%s-%s"%(tname,sname.upper(),stmid9x[0:3].upper())
        elif(stmidNN != None):
            tname=stmid9x.replace('.','-').upper()
            tname="%s-DEV-%s"%(tname,stmidNN[0:3].upper())
        elif(stm1id != None):
            tname=stm1id.replace('.','-').upper()
            tname="%s-NONdev"%(tname)


        basin=md3.getBasin4b1id(b1id)
        tdir="%s/%s/%s"%(sbtSrcDir,year,basin)
        
        # -- look for existing tdir
        #
        b3id="%s%s"%(snum,b1id.upper())
        bd1mask="%s/%s*"%(tdir,b3id)
        bd1s=glob.glob(bd1mask)

        #print 'adsfasdf',stmid,bd1s
        #continue
        if(len(bd1s) == 1):
            tdirNew="%s/%s"%(tdir,tname)
            tdir=bd1s[0]
            if(tdir != tdirNew):
                print 'WWW-existing-tdir != current...'
                print 'WWW-tdirNew:   ',tdirNew
                if(doBdeck2):
                    print 'WWW-tdir(old): ',tdir,' rm -r'
                    cmd="rm -r %s"%(tdir)
                else:
                    print 'WWW-tdir(old): ',tdir,' rm -r -i'
                    cmd="rm -r -i %s"%(tdir)
                    
                mf.runcmd(cmd,ropt)
                tdir=tdirNew
            else:
                print 'III-tdir for: ',stmid,'already there: ',tdir
        else:
            tdir="%s/%s"%(tdir,tname)
            print 'WWW-tdir for: ',stmid,'...making target dir: ',tdir
            MF.ChkDir(tdir,'mk')
            
            

        oPath="%s/%s-sum.txt"%(tdir,b3id)
        oPathBT="%s/%s-sum-BT.txt"%(tdir,b3id)
        
        ocards=[]
        trk=dds.trk
        dtgs=dds.dtgs
        ktrk=trk.keys()
        ktrk.sort()

        for kt in ktrk:
            ocard=parseDssTrk(kt,trk[kt])
            if(verb): print ocard
            ocards.append(ocard)

        # -- write to oPath != None
        #
        if(oPath != None):
            MF.WriteList2Path(ocards,oPath,verb=1)
        
        if(IsNN(stmid)): 
            dobt=1
            ocards=[]
            dds=tcD.getDSsFullStm(stmid, dobt=dobt, doprint=0, set9xfirst=0, dowarn=0)
            trk=dds.trk
            dtgs=dds.dtgs
            ktrk=trk.keys()
            ktrk.sort()
    
            for kt in ktrk:
                ocard=parseDssTrk(kt,trk[kt])
                if(verb): print ocard
                ocards.append(ocard)
        
            if(oPathBT != None):
                MF.WriteList2Path(ocards,oPathBT,verb=1)
                


        if(doCarq): getCarq(dds)
        


