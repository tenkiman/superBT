#!/usr/bin/env python

from ad2vm import *
import jclip


def setClp3(dtg,ataus,adkcs,bposit,stmid,verb=0):
    
    lasttau=int(ataus[-1])
    if(lasttau > 72):
        lasttau=72

    lstau12=lasttau%12
    lasttau=lasttau-lstau12

    eadeck={}
    eataus=[]
    eadeckin=adkcs[dtg]
    for acard in eadeckin:
        aa=acard.split(',')
        tau=aa[5].strip()
        itau=int(tau)
        if(itau%12 == 0 and itau <= lasttau):
            eataus.append(itau)
            eadeck[itau]=acard
            
    #for eatau in eataus:
    #    print eadeck[eatau]

    
    sid=stmid[0:2]
    lat0=bposit[0]
    lon0=bposit[1]
    tcvmax=bposit[2]
    tcdir=bposit[3]
    tcspd=bposit[4]
    idtg=dtg[2:]
    
    print 'setClp3 for ',stmid,' lasttau: ',lasttau
    
    (latm12,lonm12)=rumltlg(tcdir,tcspd,-12.0,lat0,lon0)
    (latm24,lonm24)=rumltlg(tcdir,tcspd,-24.0,lat0,lon0)
    
    if(verb):
        print "M12: %6.1f  %6.1f"%(latm12,lonm12)
        print "M24: %6.1f  %6.1f"%(latm24,lonm24)
    
    center='JTWC'
    basin=tcbasin(lat0,lon0)
    
    if(basin == 'EPC' or basin == 'ATL'):
    
        # convert lon to deg W for input
        clipMod='nhc.clipper.x'
        
        nclipIN="%s %s %s %03.0f %5.2f %5.2f"%(idtg,sid,basin,tcvmax,tcdir,tcspd)
        nclipIN="%s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f"%(nclipIN,lat0,lon0,latm12,lonm12,latm24,lonm24)
    
        if(basin == 'EPC'):
            if(verb): print "EEEEEEEEEEEEEEE"
            cmd="%s %s"%(clipMod,nclipIN)
            cards=MF.runcmdLog(cmd,quiet=1)
            acards=parseClipCards(cards,lasttau,dtg,stmid,tcvmax,eadeck,verb=verb)
    
        elif(basin == 'ATL'):
            if(verb): print "LLLLLLLLLLLLLLLLL"
            cmd="%s %s"%(clipMod,nclipIN)
            cards=MF.runcmdLog(cmd,quiet=1)
            acards=parseClipCards(cards,lasttau,dtg,stmid,tcvmax,eadeck,verb=verb)
    
    else:
    
        #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
        #
        #  JTWC clipers
        #
        #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
        
        #
        #  calculate appropriate cliper model
        #
        
        nsind=-999
        
        
        if( lat0>  1.0 and lat0< 60.0 ):
            if( lon0>=100.0 and lon0 <=180.0):
                clipermodel='wpclpr'
        #  NIO
        #
            elif(lon0>  0.0 and lon0 < 100.0):
                clipermodel='oclip'
                nsind=1
        
        #  CPAC
        #
            elif(lon0>180.0 and lon0 <=220.0):
                clipermodel='oclip'
                nsind=4
                
        elif( lat0>-60.0 and lat0< -1.0 ):
    
        #  SWPAC
        #
            if( lon0>=140.0 and lon0 <=225.0 ):
                clipermodel='swpclp'
                nsind=-3
        #  SEIO
        #
            elif( lon0>=100.0 and lon0 <140.0 ):
                clipermodel='seiclp'
                nsind=-2
                
        # -- old clipper
        #
            else:
                clipermodel='oclip'
                nsind = -1 # swio
                
        else:
            print "WWWW no jtwc cliper for: ",lat0,lon0
            sys.exit()
        
        print "CCCCC ",clipermodel,nsind,tcvmax
        
        if(clipermodel == 'wpclpr'):
            jclip.wpclpr (idtg,lat0,lon0,latm12,lonm12,latm24,lonm24,tcvmax)
            lalo=jclip.wpclpfcst.cfcst
        
        elif(clipermodel == 'swpclp'):
            jclip.swpclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,tcvmax)  # wants + lats
            lalo=jclip.swpclpfcst.cfcst
            for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S
            
        elif(clipermodel == 'seiclp'):
            jclip.seiclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,tcvmax)  # wants + lats
            lalo=jclip.seiclpfcst.cfcst
            for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S
            
        
        elif(clipermodel == 'oclip'):
        
            # nsind = -3 spac (lon >= 135.0)
            # nsind = -2 seio (lon >= 100 and lon < 135)
            # nsind = -1 swio (lon < 100)
            # nsind = 4 epac (lon > 220)
            # nsind = 3 cpac (lon > 180 and lon <= 220)
            # nsind = 2 wpac (lon > 100 and lon <= 180)
            # nsind = 1 nio (lon <=100)
        
            print "QQQ ",nsind
            if(nsind < 0):
                jclip.oclip (nsind,idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24)
            else:
                jclip.oclip (nsind,idtg,lat0,lon0,latm12,lonm12,latm24,lonm24)
            
            lalo=jclip.oldclpfcst.cfcst
        
            #
            # tau 72 in tau 60 for SIO, interpolate
            #
            
            if(nsind == -1):
                print "NNNNN"
                lalo[8]=(lalo[6]+lalo[8])*0.5
                lalo[9]=(lalo[7]+lalo[9])*0.5
            

        
        if(clipermodel == 'wpclpr' or clipermodel == 'swpclp' or clipermodel == 'seiclp'
           or clipermodel == 'oclip' ):
        
            #print lalo
        
            tau=0
            # 12 HR =  66.4 N   19.7 W

            ccards=[]
            ccard=setNhcClipOut(tau,lat0,lon0)
            ccards.append(ccard)

            for i in range(6):
                lat=lalo[2*i]
                lon=lalo[2*i+1]
                tau=tau+12
                ccard=setNhcClipOut(tau,lat,lon)
                ccards.append(ccard)
                
            #for ccard in ccards:
            #    print ccard
                
            acards=parseClipCards(ccards,lasttau,dtg,stmid,tcvmax,eadeck,verb=verb)
    
    return(acards)
        
    
def getBlatBlonBdirspd(dtg,m3trk):
    
    try:
        tt=m3trk[dtg]
    except:
        print 'WWW -- no m3trk for: ',dtg
        bposit=None
        sys.exit()
        return(bposit)
    blat=float(tt[0])
    blon=float(tt[1])
    bvmax=float(tt[2])
    if(bvmax < 0):
        bvmax=35.0
    bdir=float(tt[4])
    bspd=float(tt[5])
    bposit=(blat,blon,bvmax,bdir,bspd)
    return(bposit)
    
def parseClipCards(cards,lasttau,dtg,stmid,tcvmax,eadeck,verb=0):

    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)

    acards=[]
    acardhead='%s, %s, %s, 03, clp3'%(b2id,snum,dtg)
    for card in cards:
        acard=acardhead
        if(mf.find(card,'HR')):
            
            tt=card.split()
            tau=int(tt[0])
            lat=tt[3]
            latb=tt[4]
            lon=tt[5]
            lonb=tt[6]
            lat=lat.replace('.','')+latb
            lon=lon.replace('.','')+lonb
            acard="%s, %03d, %4s, %5s"%(acard,tau,lat,lon)
            if(tau <= lasttau):
                #print card
                ecard=eadeck[tau]
                if(verb): print ecard
                acard="%s, %3d,     , XX,  34, NEQ, 0000, 0000, 0000, 0000,"%(acard,tcvmax)
                if(verb): print acard
                acards.append(acard)
        
    return(acards)

        
def setNhcClipOut(tau,lat,lon):
    (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(lat,lon,dotens=1)
    rlat=ilat*0.1
    rlon=ilon*0.1
    ccard=" %2d HR = %5.1f %s %6.1f %s"%(tau,rlat,hemns,rlon,hemew)
    return(ccard)
    
    
def getEra5Adeck(stmid,m3trk,verb=0):
    
    abdir='/sbt/superBT-V04/dat-v03/atcf-form'
    amodel='era5'
    cmodel='clp3'
    rc=getStmParams(stmid)
    bnum=rc[0]
    year=rc[2]
    b2id=rc[3]
    adir="%s/%s/%s"%(abdir,year,amodel)
    cdir="%s/%s/%s"%(abdir,year,cmodel)
    MF.ChkDir(cdir,'mk')
    apath="%s/a%s%s%s.dat"%(adir,b2id.lower(),bnum,year)
    cpath="%s/a%s%s%s.dat"%(cdir,b2id.lower(),bnum,year)
    
    
    if(MF.getPathSiz(apath) > 0):
        acards=open(apath).readlines()
    else:
        print 'no joy finding era5 adeck: ',apath
        sys.exit()
        
    adts={}
    adkcs={}
    
    for acard in acards:
        aa=acard.split(',')
        tau=aa[5].strip()
        dtg=aa[2].strip()
        alat=aa[6].strip()
        alon=aa[7].strip()
        MF.appendDictList(adts,dtg,tau)
        MF.appendDictList(adkcs,dtg,acard[0:120])
        
    dtgs=adts.keys()
    dtgs.sort()
    ccards=[]
    for dtg in dtgs:
        ataus=adts[dtg]
        ntau=len(ataus)
        if(ntau > 1):
            bposit=getBlatBlonBdirspd(dtg,m3trk)
            ccards=ccards+setClp3(dtg,ataus,adkcs,bposit,stmid,verb=verb)
    
    rc=MF.WriteList2Path(ccards, cpath, append=0, verb=verb, warnonly=1)
            
            #for acard in acards:
            #    print acard
                
            #print 'adtg: ',dtg,'ntau: ',ntau,'adks: ',len(adkcs[dtg]),bposit
            
        
    
    
    
class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','norun',1,'ropt'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'stmopt':           ['S:',None,'a',' stmid target'],
        }

        self.purpose="""
run clipper for stms/dtgs in era5
-S by storm
-d by dtg or date-time-group or YYYYMMDDHH"""

        self.examples='''
%s -S w.19 -s       # list just the summary for ALL WPAC storms in 2019 including 9Xdev and 9Xnon and NN
%s -S w.19 -s -B    # list the summary for only numbered or NN WPAC storms in 2019 w/o summary of 9Xdev
%s -S 20w.19        # list all posits for supertyphoon HAGIBIS -- the largest TC to hit Tokyo
%s -S l.18-22 -s -B # list all atLANTic storms 2018-2022
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

yearOpt=None
doBT=1
dobt=0
dofilt9x=0
sumonly=0
domiss=0

(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)

if(verb):
    print 'sss---',stmopt
    print 'ddd---',dtgopt
    print 'yyy---',yearOpt
    
    print 'ooo---yyy',oyearOpt
    print 'ooo---BBB',doBdeck2
    
doBTMd3=0
if(doBdeck2): doBTMd3=1
    
if(verb): MF.sTimer('ALL')
if(verb): MF.sTimer('md3-load')
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
if(verb): MF.dTimer('md3-load')

dtgs=None
if(dtgopt != None):
    dtgs=dtg_dtgopt_prc(dtgopt)
    for dtg in dtgs:
        (dtgstms,m3trks)=md3.getMd3tracks4dtg(dtg,dobt=dobt,doBdeck2=doBdeck2, 
                                              verb=verb)
        for stmid in dtgstms:
            card=printMd3Trk(m3trks[stmid],dtg)
            print card
        
            
stmids=None
if(stmopt != None):
    
    if(doBT):
        if(doBdeck2):
            dobt=1
            dofilt9x=1
            doNNand9X=0
        else:
            dobt=1
            dofilt9x=0
            doNNand9X=0
    # -- dobt for stmid, but dobtTrk=0 for track positis
    #
    dobtTrk=0
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

    for stmid in stmids:
        #print 'sss',stmid,dobt,dofilt9x
        #continue
        
        # -- get track
        #
        (rc,m3trk)=md3.getMd3track(stmid,dobt=dobtTrk,verb=verb,domiss=domiss)
        if(rc == 1):
            rc=getEra5Adeck(stmid,m3trk,verb=verb)
        else:
            print 'EEE no m3trk for this stmid: ',stmid
            sys.exit()


if(verb): MF.dTimer('ALL')



sys.exit()


