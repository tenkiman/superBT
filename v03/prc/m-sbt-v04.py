#!/usr/bin/env python

from sBT import *

def cpActualBdeck(tyear,ostmid,doit=1,warn=0):
    
    tcDatDir='/w21/dat/tc'
    # -- add real bdeck to sbt/v10 dir
    #
    bBTmask="%s/bdeck/*/%s/b%s.dat"%(tcDatDir,tyear,ostmid)
    bBTmask2="%s/bdeck2/*/%s/b%s.dat"%(tcDatDir,tyear,ostmid)
    bdecks=glob.glob(bBTmask)
    bdecks2=glob.glob(bBTmask2)

    bdeck=None
    gotbD2=gotbD=0
    if(len(bdecks2) == 1):
        bdeck=bdecks2[0]
        gotbD2=1
    elif(len(bdecks2) == 2):
        bdeck=None
        for bb in bdecks2:
            if(mf.find(bb,'jtwc') and isjtwc): bdeck=bb
            if(mf.find(bb,'nhc') and isnhc): bdeck=bb
        if(bdeck == None):
            if(warn): print 'EEE no joy find bdeck2 for:',tstmid
        else:
            gotbD2=1    
            
    if(bdeck == None):
        if(len(bdecks) == 1):
            bdeck=bdecks[0]
            gotbD=1
        elif(len(bdecks) == 2):
            bdeck=None
            for bb in bdecks2:
                if(mf.find(bb,'jtwc') and isjtwc): bdeck=bb
                if(mf.find(bb,'nhc') and isnhc): bdeck=bb
            if(bdeck == None):
                if(warn): print 'EEE no joy find bdeck1 for:',tstmid
            else:
                gotbD=1    
        
    if(bdeck == None):
        if(warn): print "WWW no bdecks for in: ",bBTmask,' or: ',bBTmask2
        
    print 'cpActualBdeck gotbD2: ',gotbD2,' gotbD: ',gotbD
    
    if(bdeck != None and doit):
        cmd="cp %s %s/."%(bdeck,tdirSbt)
        mf.runcmd(cmd,'quiet')


def getTClatlonMd3(dtg,m3trk,verb=0):
        
    
    rc=m3trk[dtg]
    (blat,blon,bvmax,bpmin,bdir,bspd,br34m,r50m,btccode,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=rc
    if(br34m == None):br34m=-99.
    rc=(blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m)    
    return(rc)


def parsePr(oPrpath,verb=0):
    #n:  0   30w.2017 
    #n:  1  2017111200 
    #n:  2  BT:
    #n:  3   17.7 
    #n:  4  112.9 
    #n:  5  265 
    #n:  6  E5:
    #n:  7   17.6 
    #n:  8  112.7 
    #n:  9  235 
    #n:  10  obBT
    #n:  11  C2.5   
    #n:  12  G0.6   
    #n:  13  I7.2   
    #n:  14  C7.4   
    #n:  15  G5.3   
    #n:  16  I12.3  
    #n:  17  C4.1   
    #n:  18  G3.4   
    #n:  19  I6.8   
    #n:  20   obE5
    #n:  21  C2.3   
    #n:  22  G0.4   
    #n:  23  I6.5   
    #n:  24  C6.3   
    #n:  25  G4.5   
    #n:  26  I10.1  
    #n:  27  C4.1   
    #n:  28  G3.4   
    #n:  29  I6.8   
    #n:  30   E5pr
    #n:  31    4.6 
    #n:  32     35 
    #n:  33    5.9 
    #n:  34     44 
    #n:  35    4.3 
    #n:  36     53 

    oPrs={}
    cards=open(oPrpath).readlines()
    for card in cards:
        tt=card.split(',')
        #for n in range(0,len(tt)):
            #print 'n: ',n,tt[n]

        dtg=tt[1].strip()  ; n=3
        blat=float(tt[n]) ; n=n+1
        if(blat == -99.): continue
            
            
        blon=float(tt[n]) ; n=n+1
        bdir=float(tt[n]) ; n=n+2
        elat=float(tt[n]) ; n=n+1
        elon=float(tt[n]) ; n=n+1
        edir=float(tt[n]) ; n=n+1
        btedist=gc_dist(blat,blon,elat,elon)
        btedist=mf.nint(btedist)*1.0
        
        n=n+1

        c3=tt[n].strip() ; oc3=float(c3[1:]) ; n=n+1
        g3=tt[n].strip() ; og3=float(g3[1:]) ; n=n+1
        i3=tt[n].strip() ; oi3=float(i3[1:]) ; n=n+1
        c5=tt[n].strip() ; oc5=float(c5[1:]) ; n=n+1
        g5=tt[n].strip() ; og5=float(g5[1:]) ; n=n+1
        i5=tt[n].strip() ; oi5=float(i5[1:]) ; n=n+1
        c8=tt[n].strip() ; oc8=float(c8[1:]) ; n=n+1
        g8=tt[n].strip() ; og8=float(g8[1:]) ; n=n+1
        i8=tt[n].strip() ; oi8=float(i8[1:]) ; n=n+1

        n=n+1

        c3=tt[n].strip() ; ec3=float(c3[1:]) ; n=n+1
        g3=tt[n].strip() ; eg3=float(g3[1:]) ; n=n+1
        i3=tt[n].strip() ; ei3=float(i3[1:]) ; n=n+1
        c5=tt[n].strip() ; ec5=float(c5[1:]) ; n=n+1
        g5=tt[n].strip() ; eg5=float(g5[1:]) ; n=n+1
        i5=tt[n].strip() ; ei5=float(i5[1:]) ; n=n+1
        c8=tt[n].strip() ; ec8=float(c8[1:]) ; n=n+1
        g8=tt[n].strip() ; eg8=float(g8[1:]) ; n=n+1
        i8=tt[n].strip() ; ei8=float(i8[1:]) ; n=n+1

        n=n+1
        
        e3=tt[n].strip() ; e3=float(e3[0:]) ; n=n+1
        re3=tt[n].strip() ; re3=float(re3[0:]) ; n=n+1
        e5=tt[n].strip() ; e5=float(e5[0:]) ; n=n+1
        re5=tt[n].strip() ; re5=float(re5[0:]) ; n=n+1
        e8=tt[n].strip() ; e8=float(e8[0:]) ; n=n+1
        re8=tt[n].strip() ; re8=float(re8[0:]) ; n=n+1

        if(verb):
            
            print 'DTG:',dtg
            print 'lat',blat,elat
            print 'lon',blon,elon
            print 'dir',bdir,edir,btedist
            
            print '88oo',oc8,og8,oi8,'e',e8
            print '55oo',oc5,og5,oi5,'e',e5
            print '33oo',oc3,og3,oi3,'e',e3
    
            print '88ee',ec8,eg8,ei8,'e',e8
            print '55ee',ec5,eg5,ei5,'e',e5
            print '33ee',ec3,eg3,ei3,'e',e3
        
        rc=(blat,blon,btedist,
            oc3,og3,oi3,ec3,eg3,ei3,
            oc5,og5,oi5,ec5,eg5,ei5,
            oc8,og8,oi8,ec8,eg8,ei8,
            e3,e5,e8,re3,re5,re8)
        
        prcardo3="O3 , %5.1f, %5.1f, %5.1f"%(oc3,og3,oi3)
        prcardo5="O5 , %5.1f, %5.1f, %5.1f"%(oc5,og5,oi5)
        prcardo8="O8 , %5.1f, %5.1f, %5.1f"%(oc8,og8,oi8)
        prcardo="%s, %s, %s"%(prcardo3,prcardo5,prcardo8)
        prcarde3="OE3 , %5.1f, %5.1f, %5.1f, E3 ,%5.1f ,%5.0f"%(ec3,eg3,ei3,e3,re3)
        prcarde5="OE5 , %5.1f, %5.1f, %5.1f, E5 ,%5.1f ,%5.0f"%(ec5,eg5,ei5,e5,re5)
        prcarde8="OE8 , %5.1f, %5.1f, %5.1f, E8 ,%5.1f ,%5.0f"%(ec8,eg8,ei8,e8,re8)
        prcarde="%s, %s, %s"%(prcarde3,prcarde5,prcarde8)
        prcard="%s,%s"%(prcardo,prcarde)
        prcard=prcard.replace(" ",'')
        #print prcard
        
        oPrs[dtg]=prcard

    return(oPrs)    
    
def parseLs(oLspath):
    """
0 lsdiag:
1 2019101318
2 20W.2019
3 S:
4 land:
5 561
6 max_wind:
7 40
8 shr_mag:
9 79
10 sst:
11 10.5
12 tpw:
13 35
14 C:
15 ssta:
16 0.6
17 r34m:
18 9999
19 cps_b:
20 119
21 cps_lo:
22 -316
23 cps_hi:
24 -396
25 D:
26 R_700
27 46
28 R_500
29 36
30 R_850
31 71
32 Poci_roci:
33 990_84
34 Poci_roci_p1:
35 992_114
new 20230401

0 lsdiag:
1 2017110900
2 30w.2017
3 S:
4 200dvrg:
5 81
6 850vort:
7 64
8 land:
9 16
10 max_wind:
11 24
12 shr_dir:
13 236
14 shr_mag:
15 6
16 sst:
17 28.5
18 stm_hdg:
19 280
20 stm_spd:
21 18
22 tpw:
23 65
24 C:
25 ssta:
26 0.0
27 r34m:
28 -999
29 cps_b:
30 -2
31 cps_lo:
32 28
33 cps_hi:
34 21
35 D:
36 R_700
37 71
38 R_500
39 61
40 R_850
41 81
42 Poci_roci:
43 1008_110
44 Poci_roci_p1:
45 1006_13

0 lsdiag:
1 2017110900
2 30w.2017
3 S:
4 200dvrg:
5 81
6 850vort:
7 64
8 land:
9 16
10 max_wind:
11 24
12 shr_dir:
13 236
14 shr_mag:
15 6
16 sst:
17 28.5
18 stm_hdg:
19 280
20 stm_spd:
21 18
22 tpw:
23 65
24 C:
25 ssta:
26 0.0
27 r34m:
28 -999
29 cps_b:
30 -2
31 cps_lo:
32 28
33 cps_hi:
34 21
35 D:
36 R_850
37 81
38 U_850
39 -141
40 V_700
41 41
42 R_700
43 71
44 U_700
45 -134
46 V_500
47 97
48 U_500
49 -138
50 R_500
51 61
52 V_850
53 4
54 Poci_roci:
55 1008_110
56 Poci_roci_p1:
57 1006_13

"""
    oLss={}
    cards=open(oLspath).readlines()
    for card in cards:
        tt=card.split()
        #for n in range(0,len(tt)):
            #print n,tt[n]
        #print 'dddd',len(tt)
        if(len(tt) != 58):
            print 'problem with lsdiag card: ',card,'len(tt): ',len(tt)
            continue
            
        dtg=tt[1].strip()
        dvrg200=tt[5].strip()
        vort850=tt[7].strip()
        land=tt[9].strip()
        mvmax=tt[11].strip()
        shrdir=tt[13].strip()
        shrspd=tt[15].strip()
        sst=tt[17].strip()
        stmdir=tt[19].strip()
        stmspd=tt[21].strip()
        tpw=tt[23].strip()
        ssta=tt[26].strip()
        r34m=tt[28].strip()
        cpsb=tt[30].strip()
        cpslo=tt[32].strip()
        cpshi=tt[34].strip()
        n=37
        rh85=tt[n].strip() ; n=n+2
        u85=tt[n].strip() ; n=n+2
        v70=tt[n].strip() ; n=n+2
        rh70=tt[n].strip() ; n=n+2
        u70=tt[n].strip() ; n=n+2
        v50=tt[n].strip() ; n=n+2
        u50=tt[n].strip() ; n=n+2
        rh50=tt[n].strip() ; n=n+2
        v85=tt[n].strip() ; n=n+2
        rp1=tt[n].strip()  ; rr=rp1.split('_') ; roci1=rr[0] ; poci1=rr[1] ; n=n+2
        rp0=tt[n].strip()  ; rr=rp0.split('_') ; roci0=rr[0] ; poci0=rr[1] ; n=n+2
        
        if(poci1 == '999'): poci1='-999'
        if(poci0 == '999'): poci0='-999'

        oLss[dtg]=(dvrg200,vort850,land,mvmax,shrdir,shrspd,sst,stmdir,stmspd,tpw,ssta,
                   r34m,cpsb,cpslo,cpshi,rh85,rh70,rh50,u85,u70,u50,v85,v70,v50,roci1,poci1,roci0,poci0)
        
        #print oLss[dtg]
        #sys.exit()
#            land,mvmax,shr,sst,ssta,tpw,cpsb,cpslo,cpshi,r70,r85,rp0,rp1)
    return(oLss)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.defaults={
            #'version':'v01',
            }

        self.argv=argv
        self.argopts={
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doCycle':          ['C',0,1,'cycle through stmids'],
            'dobt':             ['b',0,1,'dobt or NN storms'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'startGenDtg':      ['G',0,1,'1 - do start the NN dtgs with gendtg'],
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

# -- make version 04
#
version='v04'
sbtVerDir="%s/%s"%(sbtRoot,version)

MF.sTimer('md3')
md3=Mdeck3(verb=verb)

dtgs=None
if(dtgopt != None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    tstmids=[]
    for dtg in dtgs:
        tstmids=tstmids+md3.getMd3Stmids4dtg(dtg,dobt=dobt)
    

stmids=None
if(stmopt != None):
    tstmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)
        
    if(verb):
        for stmid in tstmids:
            (rc,m3trk)=md3.getMd3track(stmid)
            m3dtgs=m3trk.keys()
            m3dtgs.sort()
            
MF.dTimer('md3')



ocards=[]

for tstmid in tstmids:

    rc=getStmParams(tstmid)
    b1id=rc[1]
    
    isjtwc=IsJtwcBasin(b1id)
    isnhc=IsNhcBasin(b1id)
    
    # -- name of o-file like bdecks...
    #
    atcfstmid=rc[-2].replace('.','')
    stm3id="%s%s"%(rc[0],b1id)
    stm3id=stm3id.upper()
    tyear=rc[2]
   
    smask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
    
    opaths=glob.glob("%s"%(smask))
    
    # -- 20230412 -- handle case where one 9X is the one for two NN storms
    #    happens in the LANT/EPAC several times, 2016

    sdirPrs=[]
    
    if(len(opaths) == 1):
        sdirPrs.append(opaths[0])
    elif(len(opaths) == 2):
        sdirPrs.append(opaths[0])
        sdirPrs.append(opaths[1])
    else:
        print 'EEE no or more than 2 sbt/src output dirs for: ',tstmid,' tmask: ',tmask
        sys.exit()
        
    if(len(sdirPrs) == 2):
        print 'III'
        print 'III -- multiple DEV from ONE 9X -- happens in LANT/EPAC...for tstmid: ',tstmid
        print 'III'

        
    for sdirPr in sdirPrs:

        # -- output dir based on the src dir
        #
        tdirSbt=sdirPr.replace(sbtSrcDir,sbtVerDir)
        MF.ChkDir(tdirSbt,'mk')
    
        if(IsNN(tstmid)):
            oPrpath="%s/pr-%s-md3-BT.txt"%(sdirPr,stm3id)
            oLspath="%s/lsdiag-md3-%s-MRG.txt"%(sdirPr,stm3id)
        else:
            oPrpath="%s/pr-%s-md3.txt"%(sdirPr,stm3id)
            oLspath="%s/lsdiag-md3-%s-MRG.txt"%(sdirPr,stm3id)
            
        sMD3path="%s/%s-%s-md3-MRG.txt"%(sdirPr,stm3id,tyear)
        smd3siz=MF.getPathSiz(sMD3path)

        oMD3path=None
        if(smd3siz > 0):
            oMD3path="%s/%s-%s-md3-MRG.txt"%(tdirSbt,stm3id,tyear)
            
    
        if(verb):
            print 'SSSSSS',sdirPr
            print 'TTTTTT',tdirSbt
    
        
        # -- output like atcf bdeck but with version #
        #
        sBTpath="%s/s%s-%s.txt"%(tdirSbt,atcfstmid,version)
            
        # -- simpler md3
        #
        dbt=0
        if(IsNN(tstmid)):  dbt=1
        (rc,m3trk)=md3.getMd3track(tstmid,dobt=dbt)
        m3meta=md3.stmMetaMd3[tstmid]
        m3stmid=m3meta[0]
        m3tcType=m3meta[1]
        m3stmType=m3meta[2]
        m3stm9x=m3meta[-3]
        
        dtgs=m3trk.keys()
        dtgs.sort()
    
        prsiz=MF.GetPathSiz(oPrpath)
        lssiz=MF.GetPathSiz(oLspath)
        sbtSiz=MF.getPathSiz(sBTpath)
        
        if(verb):
            print 'ppp',oPrpath,'siz: ',prsiz
            print 'lll',oLspath,'siz: ',lssiz
            print 'sss',sBTpath,'siz: ',sbtSiz
            print '333',oMD3path,'siz: ',smd3siz
    
        if(sbtSiz > 0 and not(override)):
            print 'WWW already run for tstmid: ',tstmid
            continue
            
        prS=parsePr(oPrpath,verb=verb)
        prSdtgs=prS.keys()
        prSdtgs.sort()
        
        sizLs=MF.getPathSiz(oLspath)
        if(sizLs > 0):
            lsS=parseLs(oLspath)
            lsSdtgs=lsS.keys()
            lsSdtgs.sort()
        else:
            lsSdtgs=[]
    
        sbtcards=[]
        #keyS='       dtg,   lat,    lon, Vmx, r34, dir,  spd, TCc,   op3,   op5,   op8,   ep3,   ep5,   ep8, land,   shr,   p/rocip1,    p/roci0,'
        #sbtcards.append(keyS)
    
        for dtg in dtgs:
    
            sbtcard=''
            rc=getTClatlonMd3(dtg,m3trk)
             
            (blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m)=rc
            #print 'dd',dtg,blat,blon,bvmax,br34m,bdir,bspd,btccode
            sbtcard0="%s, %s, %s, %s, %5.1f, %6.1f, %3.0f, %4.0f, %3.0f, %3.0f, %3s, %4.1f"%\
                (m3stmid,m3tcType,m3stmType,dtg,blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m)
            sbtcard0=sbtcard0.replace(' ','')
            #sbtcard0=sbtcard0.replace('-999.0','NaN')
    
            sbtPrcard="NaN"
            if(dtg in prSdtgs):
                sbtPrcard=prS[dtg]
    
                
            #land=mvmax=shr=sst=ssta=tpw=cpsb=cpslo=cpshi=r70=r85=rp0=rp1='NaN'
            #if(dtg in lsSdtgs):
                #(land,mvmax,shr,sst,ssta,tpw,cpsb,cpslo,cpshi,r70,r85,rp0,rp1)=lsS[dtg]
            #sbtLscard="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%10s, %10s"%(land,mvmax,shr,sst,ssta,tpw,cpsb,cpslo,cpshi,r70,r85,rp1,rp0)
            
            dvrg200=vort850=land=mvmax=shrdir=shrspd=sst=stmdir=stmspd=tpw=ssta='NaN'
            r34m=cpsb=cpslo=cpshi='NaN'
            rh70=rh50=rh85='NaN'
            u70=u50=u85='NaN'
            v70=v50=v85='NaN'
            roci0=poci0=roci1=poci1='NaN'
            
            if(dtg in lsSdtgs):        
                (dvrg200,vort850,land,mvmax,shrdir,shrspd,sst,stmdir,stmspd,tpw,ssta,
                 r34m,cpsb,cpslo,cpshi,
                 rh85,rh70,rh50,u85,u70,u50,v85,v70,v50,
                 roci1,poci1,roci0,poci0)=lsS[dtg]
    
                #(dvrg200,vort850,land,mvmax,shrdir,shrspd,sst,stmdir,stmspd,tpw,ssta,
                # r34m,cpsb,cpslo,cpshi,rh70,rh50,rh85,roci0,poci0,roci1,poci1)=lsS[dtg]
             
            #if(r34m == -999): r34m='NaN'   
            
            sbtLscard1="%s, %s, %s, %s, %s, %s, %s, %s, %s, "%(land,mvmax,r34m,shrspd,shrdir,
                                                               stmspd,stmdir,sst,ssta)
            sbtLscard2="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"%(vort850,dvrg200,
                                                                         cpsb,cpslo,cpshi,tpw,
                                                                         rh85,rh70,rh50,
                                                                         u85,u70,u50,
                                                                         v85,v70,v50,
                                                                         roci1,poci1,roci0,poci0)
            sbtLscard="%s %s"%(sbtLscard1,sbtLscard2)
            sbtLscard=sbtLscard.replace(' ','')
            #sbtLscard=sbtLscard.replace('-999','NaN')
            
            sbtcard="%s,%s,%s"%(sbtcard0,sbtLscard,sbtPrcard)
            #tt=sbtcard.split(',')
            #sbtcard=sbtcard+sbtLscard
            #print 'lll',dtg,sbtcard
            sbtcard=sbtcard.replace('NaN','-999')
            if(dtgs.index(dtg) == 0):
                print len(sbtcard.split(',')),sbtcard
            sbtcards.append(sbtcard)
    
        if(sbtSiz <= 0 or override):
            MF.WriteList2Path(sbtcards, sBTpath, verb=verb )
            rc=cpActualBdeck(tyear,atcfstmid)
            
            # -- cp the md3 file
            #
            if(oMD3path != None):
                cmd="cp %s %s"%(sMD3path,oMD3path)
                mf.runcmd(cmd,ropt)
            


    