from sBT import *
from ibtracs import Ibtracs
import pickle

verb=0
I = Ibtracs()

if(verb):
    print(I.possible_basins)
    print(I.possible_subbasins)
    print(I.possible_classifications)
    print(I.possible_agencies)

ddir='/w21/dat/tc/ib3/'
# -- bdecks
#
bdirj='/w21/dat/tc/bdeck2/jtwc'
bdirn='/w21/dat/tc/bdeck2/nhc'
# -- adecks
#
adirj='/w21/dat/tc/adeck/jtwc'
adirn='/w21/dat/tc/adeck/nhc'

class bdeck(MFutils):
    
    basin=' '
    cy=' '
    yyyymmddhh=' '
    technum=' 03' # bdeck3 from ibtracs
    tech='BEST'
    tau='   0'
    lat=' '
    lon=' '
    vmax=' '
    mslp=' '
    ty=' '
    
    rad=' '
    windcode=' '
    rad1=' '
    rad2=' '
    rad3=' '
    rad4=' '
    
    radp=' '
    rrp=' '
    mrd=' '
    gusts=' '
    eye=' '
    subregion=' '
    maxseas=' '
    initials=' '
    dir=' '
    speed=' '
    stormname=' '
    depth=' '
    seas=' '
    seascode=' '
    seas1=' '
    seas2=' '
    seas3=' '
    seas4=' '
    userdefined=' '
    userdata=' '
    
    def __init__(self,tc,sid,sid2,
                 dx=None,
                 dy=None):
        
        print (sid)
        return
        
        
    
    

def convertIb2AtcfId(tc,tstmid=None,verb=0):
    
    year=tc.season
    atcfid=tc.ATCF_ID
    
    if(tc.basin == 'NA'): 
        sid='l'
        sid2='AL'
    elif(tc.basin == 'WP'): 
        sid='w'
        sid2='WP'
    elif(tc.basin == 'EP'):
        if(tc.subbasin == 'CP'): 
            sid='c'
            sid2='CP'
        else:
            sid='e'
            sid2='EP'

    elif(tc.basin == 'NI'):
        if(tc.subbasin == 'BB'): 
            sid='b'
        elif(tc.subbasin == 'AS'): 
            sid='a'
        else:
            sid='i'
        sid2='IO'
            
    elif(tc.basin == 'SI'): 
        sid='s'
        sid2='SH'
    elif(tc.basin == 'SP'): 
        sid='p'
        sid2='SH'
    elif(tc.basin == 'SA'): 
        sid='q'
        sid2='SL'
    else:
        print ('ooopppsss: tc.basin = ',tc.basin)
        sys.exit()
        
    snum='99'
    if(atcfid != None):
        snum=atcfid[2:4]
        
    astmid="%s%s.%s"%(snum,sid,year)
        
    return(sid,sid2,astmid)
        
def getIb3aTCs(byear=1940, eyear=2024):
    
    years=range(byear,eyear+1)

    MF.sTimer('pyp-load')
    aTCs={}
    for year in years:
        
        syear=str(year)
        #TCs=[tc for tc in I.storms if tc.season == year]
        P=open('%s/iTC%s.pyp'%(ddir,syear),'rb')
        TCs=pickle.load(P)
        #print ('year: ',year,len(TCs))
        aTCs[year]=TCs
        P.close()
    MF.dTimer('pyp-load')
    
    return(aTCs)
    
def isNHC(sid):
    isnhc=0
    if(sid == 'l' or sid == 'q' or sid == 'e' or sid == 'c'):
        isnhc=1
    return(isnhc)

def HolidayAtkinsonPsl2Vmax(psl):

    vmax=0.0
    if(psl < 880.0):
        vmax=154.0
    elif(psl >= 880.0 and psl < 885.0):
        vmax=150.0
    elif(psl >= 850.0 and psl < 890.0):
        vmax=146.0
    elif(psl >= 890.0 and psl < 895.0):
        vmax=142.0
    elif(psl >= 895.0 and psl < 900.0):
        vmax=138.0
    elif(psl >= 900.0 and psl < 905.0):
        vmax=134.0
    elif(psl >= 905.0 and psl < 910.0):
        vmax=130.0
    elif(psl >= 910.0 and psl < 915.0):
        vmax=126.0
    elif(psl >= 915.0 and psl < 920.0):
        vmax=122.0
    elif(psl >= 920.0 and psl < 925.0):
        vmax=117.0
    elif(psl >= 925.0 and psl < 930.0):
        vmax=113.0
    elif(psl >= 930.0 and psl < 935.0):
        vmax=108.0
    elif(psl >= 935.0 and psl < 940.0):
        vmax=103.0
    elif(psl >= 940.0 and psl < 945.0):
        vmax=99.0
    elif(psl >= 945.0 and psl < 950.0):
        vmax=94.0
    elif(psl >= 950.0 and psl < 955.0):
        vmax=88.0
    elif(psl >= 955.0 and psl < 960.0):
        vmax=83.0
    elif(psl >= 960.0 and psl < 965.0):
        vmax=78.0
    elif(psl >= 965.0 and psl < 970.0):
        vmax=72.0
    elif(psl >= 970.0 and psl < 975.0):
        vmax=66.0
    elif(psl >= 975.0 and psl < 980.0):
        vmax=60.0
    elif(psl >= 980.0 and psl < 985.0):
        vmax=53.0
    elif(psl >= 985.0 and psl < 990.0):
        vmax=46.0
    elif(psl >= 990.0 and psl < 995.0):
        vmax=38.0
    elif(psl >= 995.0 and psl < 1000.0):
        vmax=30.0
    elif(psl >= 1000.0 and psl < 1005.0):
        vmax=22.0
    elif(psl >= 1005.0):
        vmax=20.0

    return(vmax)

    
def CourtneyKnaffPminVmax(pmin,cnv10t1=(1.0/0.88)):
    
    # -- courtney and knaff 2009
    #
    
    #1.5 22 64    7.2 28.3  4.6   24.2 1004.7 4.4 33 28.8 5.0
    #2.0 26 139   7.9 31.8  5.5   27.2 1004.2 4.2 92 31.9 5.9
    #2.5 31 332   7.7 36.7  7.0   32.1 1002.5 4.8 244 37.5 7.4
    #3.0 40 372   9.2 43.4  7.2   38.2  999.2 6.3 294 44.3 7.7
    #3.5 48 286   9.5 49.5  7.6   44.2  994.1 7.0 210 50.5 8.0
    #4.0 57 228  10.3 56.2  7.8   50.7  988.2 7.8 161 58.1 8.0
    #4.5 68 267  10.7 68.1  11.4  62.5  977.8 11.9 178 69.1 11.9
    #5.0 79 242  11.0 76.6  10.6  70.9  969.4 11.6 146 78.3 11.1
    #5.5 90 165  10.7 86.7  11.4  80.9  958.3 10.9 105 88.4 12.4
    #6.0 101 188 10.7 99.1  11.7  93.5  945.9 12.5 113 101.6 11.8
    #6.5 112 207 10.0 108.7 11.0 103.2  934.5 13.9 118 111.3 12.0
    #7.0 123 84  10.4 115.3 11.4 109.6  923.5 13.2 41 122.2 10.3
    #7.5 136 15   7.0 127.2 8.4 122.8   910.2 11.1 6 134.2 2.2    
    
    pmvm={
        
        1004.7:28.3,
        1004.2:31.8,
        1002.5:36.7,
        999.2:43.4,
        994.1:49.5,
        988.2:56.2,
        977.8:68.1,
        969.4:76.6,
        958.3:86.7,
        945.9:99.1,
        934.5:108.7,
        923.5:115.3,
        910.2:122.8,
    }
    

    pmins=list(pmvm.keys())
    pmins.reverse()
    npms=len(pmins)
    pminmax=pmins[-1]
    
    # -- max pressure, check if above...
    #
    if(pmin >= pminmax):
        vmax=pmvm[pminmax]
        return(vmax)

    # -- got through the C# pmin-vmax
    #
    for n in range(0,npms):
        pm=pmins[n]
        nm1=n-1
        if(nm1 < 0): nm1=0
            
        if(pmin <= pm):
            pm0=pmins[nm1]
            vm=pmvm[pm]
            vm0=pmvm[pm0]
            dp=(pm-pm0)
            dv=(vm0-vm)
            if(dp != 0.0):
                dfact=(pm-pmin)/dp
                dvadd=dv*dfact
                vmax=vm+dvadd
            elif(dp == 0.0):
                vmax=vm
                
            #print('ppp--',pmin,n,pm0,pm,vm0,vm,'ddd',dp,dv,dfact)
            #print('vvv---',dvadd,vm0,vmax)
            return(vmax)

    
    
def conv10minto1min(dist2land,sid,
                    nearland=20.0,  # km
                    useStandard=1,
                    ):

    # -- nhc
    if(isNHC(sid)):
        kfact=1.0
        return(kfact)
        
    # -- at sea
    if(dist2land > nearland):
        kfact=(1.0/0.92)
    
    # -- offshore near coastline
    if(abs(dist2land) <= nearland and dist2land > 0.0):
        kfact=(1.0/0.90)
    
    # -- inland near coastline    
    if(abs(dist2land) <= nearland and dist2land <= 0.0):
        kfact=(1.0/0.87)
        
    # -- inland
    if(abs(dist2land) > nearland and dist2land < 0.0):
        kfact=(1.0/0.84)
    
    if(useStandard):
        kfact=(1.0/0.88)
        
    return(kfact)
        
        
        
def getStm1id4Atcfid(atcfid,sid):
    year=atcfid[-4:]
    snum=atcfid[2:4]
    stm1id="%2s%1s.%s"%(snum,sid,year)
    return(stm1id)

def convertItime2Dtg(tt):
    tt=str(tt).split('-')
    yy=tt[0]
    mm=tt[1]
    dd=tt[2][0:2]
    hh=tt[2][3:5]
    dtg="%s%s%s%s"%(yy,mm,dd,hh)
    return(dtg)

def nearest5kts(vmax):

    ivmax=int(vmax)
    vv=vmax%5.0
    if(vv >= 2.5):
        ovmax=vmax-vv
        ovmax=ovmax+5.0
    else:
        ovmax=vmax-vv
        
    return(ovmax)
    
    
        
def getRadii(tc,n):
    
    def gotRad(r34):
        gotR=0
        for r in r34:
            if(r != 0):gotR=1
            
        return(gotR)
                
        
    r34=[0,0,0,0]
    r50=[0,0,0,0]
    r64=[0,0,0,0]
    
    if(not(isnan(tc.R34_NE[n]))): r34[0]=int(tc.R34_NE[n])
    if(not(isnan(tc.R34_SE[n]))): r34[1]=int(tc.R34_SE[n])
    if(not(isnan(tc.R34_SW[n]))): r34[2]=int(tc.R34_SW[n])
    if(not(isnan(tc.R34_NW[n]))): r34[3]=int(tc.R34_NW[n])
       
    if(not(isnan(tc.R50_NE[n]))): r50[0]=int(tc.R50_NE[n])
    if(not(isnan(tc.R50_SE[n]))): r50[1]=int(tc.R50_SE[n])
    if(not(isnan(tc.R50_SW[n]))): r50[2]=int(tc.R50_SW[n])
    if(not(isnan(tc.R50_NW[n]))): r50[3]=int(tc.R50_NW[n])

    if(not(isnan(tc.R64_NE[n]))): r64[0]=int(tc.R64_NE[n])
    if(not(isnan(tc.R64_SE[n]))): r64[1]=int(tc.R64_SE[n])
    if(not(isnan(tc.R64_SW[n]))): r64[2]=int(tc.R64_SW[n])
    if(not(isnan(tc.R64_NW[n]))): r64[3]=int(tc.R64_NW[n])
    
    gotR34=gotRad(r34)
    gotR50=gotRad(r50)
    gotR64=gotRad(r64)
    
    return(gotR34,gotR50,gotR64,r34,r50,r64)

    #R50_SE
    #R64_SE
    #R34_SW
    #R50_SW
    #R64_SW
    #R34_NE
    #R50_NE
    #R64_NE
    #R34_NW
    #R50_NW
    #R64_NW
    
    
    #ace=tc.ACE()
    #basin=tc.basin
    #dist2land=tc.dist2land
    #agencies
    #basins
    #genesis
    #q
    #name
    #ATCF_ID
    #classification
    #ID
    #metadata
    #radii_attrs
    #attr
    #data_at_time()
    #intersect_box()
    #mslp
    #rmw
    #season
    #speed
    #subbasin
    #subbasins
    #time
    #wind

    #R34_SE
    #R50_SE
    #R64_SE
    #R34_SWibtrk
    #R50_SW
    #R64_SW
    #R34_NE
    #R50_NE
    #R64_NE
    #R34_NW
    #R50_NW
    #R64_NW

def getIntYears4oyearOpt(oyearOpt):
    
    yy=oyearOpt.split('.')
    if(len(yy) == 2):
        byear=yy[0]
        eyear=yy[1]
        iyears=yyyyrange(byear,eyear)
        years=[]
        for iyear in iyears:
            years.append(int(iyear))
    else:
        years=[int(oyearOpt)]
    
    return(years)

def getBasinYearsFromStmopt(stmopt,byear=1940,eyear=2023):
    
    tstmid=None
    basinsyears={
        1940:('l','w','i','h','a','b','s','p'),
        1941:('l','w','i','h','a','b','s','p'),
        1942:('l','w','i','h','a','b','s','p'),
        1943:('l','w','i','h','a','b','s','p'),
        1944:('l','w','i','h','a','b','s','p'),
        1945:('l','w','i','h','a','b','s','p'),
        1946:('l','w','i','h','a','b','s','p'),
        1947:('l','w','i','h','a','b','s','p'),
        1948:('l','w','i','h','a','b','s','p'),
        1949:('l','w','i','h','a','b','s','p','e','c'),
    }
    
    ss=stmopt.split('.')

    if(len(ss) != 2):
        print('stmopt: ',stmopt,'cannot be used in getBasinYearsFromStmopt...')
        sys.exit()
        
    else:
        # -- get year
        #
        domd3=1
        yopt=ss[1]
        yy=yopt.split('-')
        snum=None
        if(len(yy) > 1):
            print ('EEE--- cannot do more that one year at a time yopt: %s'%(yopt))
            sys.exit()
        if(len(yopt) == 4):
            year=yopt
        elif(len(yopt) == 2):
            year=add2000(yopt)
        else:
            print ('EEE--- invalid yopt: %s'%(yopt))
            sys.exit()

        year=int(year)
        basin=ss[0]
        bb=basin.split(',')
        
    
        if(len(bb) != 1):
            print('invalid basin in stmopt',stmopt)
            sys.exit()
        if(len(basin) == 3):
            snum=int(basin[0:2])
            basin=basin[-1:]
            tstmid="%s%s.%s"%(snum,basin,str(year))
            
    
    if(
        (year < byear or year > eyear) or
        (year >= 1945 and year <= 1949) and not(basin in basinsyears[year]) or
        (snum != None and snum >= 51)
        ):
        domd3=0
        
    return(domd3,basin,year,tstmid)
            
    
def getibTCs4aTCs(aTCs,year,basin,tstmids):
    
    atBasins=[]
    noBasins=[]
    atStmids=[]
    noStmids=[]
    
    atTCs={}
    noTCs={}
    
    nobnum=51
    for tc in aTCs[year]:
        #(sid,sid2)=convertIb2AtcfId(tc)
        #rc=getITCvars(tc,sid,sid2)
        
        #sys.exit()
        
        if(sid != basin): continue
        
        if(tc.ATCF_ID != None):
            
            atBasins.append(sid)
            stmid=getStm1id4Atcfid(tc.ATCF_ID,sid)
            
            if(tstmids != None and not(stmid in tstmids)):
                print ('WWWWWWW---ibtracs atcf NOT in bdeck2')
                sys.exit()
            
            atStmids.append(stmid)
            atTCs[stmid]=tc
            
            print('YYEESS stmid',stmid,tc.ID,tc.ATCF_ID,tc.genesis,'ace %5.1f'%(tc.ACE()))
        else:
            noBasins.append(sid)
            stmid='%02i%s.%s'%(nobnum,sid,str(year))
            noStmids.append(stmid)
            print('NNNOOO stmid',stmid,tc.ID,'        ',tc.genesis,'ace %5.1f'%(tc.ACE()))

            noTCs[stmid]=tc
            nobnum=nobnum+1
            
            
    atBasins=mf.uniq(atBasins)
    noBasins=mf.uniq(noBasins)
    
    print('aaaa',atBasins)
    print('nnnn',noBasins)
            
def getAgency(ags,verb=0):
    
    ibAgency=None
    if(len(ags) == 1):
        if(ags[0] == ''):
            ibAgency='jtwc'
        else:
            ibAgency=ags[0]
        
    elif(len(ags) == 2):
        if(ags[0] == ''):
            ibAgency=ags[1]
        else:
            ibAgency=ags[0]

    elif(len(ags) == 3):
        if(ags[0] == ''):
            ibAgency="%s-%s"%(ags[-2],ags[-1])
        else:
            ibAgency=str(ags)

    if(verb):
        print ('jjjjjjjjjjjjjj',tstmid,ibAgency,ags)
        
    return(ibAgency)

def getMD2trk(md2trk):
    
    (rlat,rlon,vmax,pmin,
     dir,spd,
     tccode,wncode,
     trkdir,trkspd,dirtype,
     b1id,tdo,ntrk,ndtgs,
     r34m,r50m,alf,sname,
     r34,r50,depth,
     ) = md2trk
    
    posit=(rlat,rlon,vmax,pmin,tccode,wncode,trkdir,trkspd,r34)
    return(posit)

    
    
def getITCvars(tc,tstmid,m2trk=None,sundef='-999',
               m2distMax=100.0,
               verb=0,doprint=1):
    
    (sid,sid2,astmid)=convertIb2AtcfId(tc,tstmid,verb=verb)
    

    ags=mf.uniq(tc.agencies)
    ibAgency=getAgency(ags)
    
    if(verb):
        print('sidsid2 ',sid,sid2,astmid,'tstmid: ',tstmid)
        print('agencies',tc.agencies,mf.uniq(tc.agencies))
        print('aaggeennccy: ',ibAgency)
    
    
    m2dtgs=list(m2trk.keys())
    m2dtgs.sort()
    #for m2dtg in m2dtgs:
    #    print('mm22',m2dtg,m2trk[m2dtg])
        
    #if(b2trk == None):
    #    b2trk=getB2trk(tstmid)

    lats=tc.lat
    lons=tc.lon
    mslps=tc.mslp
    winds=tc.wind
    times=tc.time
    metas=tc.metadata
    spds=tc.speed
    agencies=tc.agencies
    dist2lands=tc.dist2land
    tctypes=tc.classification
    rmws=tc.rmw
    kk=metas.keys()
    
    if(verb):
        print (kk)
        for k in kk:
            print (k,metas[k])
    
    dtgs=[]
    ibtrk={}
    dirspd={}
    radii={}
    
    for n in range(0,len(times)):
        tt=times[n]
        dtg=convertItime2Dtg(tt)
        dtgs.append(dtg)

        b2lat=b2lon=b2mslp=b2wind=undef
        r34=r50=r64=None
        b2tccode=b2wncode='--'
        
        try:
            md2posit=getMD2trk(m2trk[dtg])
            #print('md2posit',md2posit)
            
            b2lat=md2posit[0]
            b2lon=md2posit[1]
            b2wind=md2posit[2]
            b2slp=md2posit[3]
            b2dir=md2posit[6]
            b2spd=md2posit[7]
            b2tccode=md2posit[4]
            b2wncode=md2posit[5]
            ib2lat=int(b2lat*10.0)
            b2lat=ib2lat/10.0
            ib2lon=int(b2lon*10.0)
            b2lon=ib2lon/10.0
            #if(b2slp > 0.0):
                #b2mslp=int(b2mslp)
            #else:
                #b2mslp=undef
        except:
            None
            
        lat=lats[n]
        lon=lons[n]
        
        ilat=int(lat*10.0)
        lat=ilat/10.0
        ilon=int(lon*10.0)
        lon=ilon/10.0
        
        mslp=mslps[n]
        dojtwc=0
        if(b2lat != undef):
            b2dist=gc_dist(lat,lon,b2lat,b2lon)
            #print('b2dist %4.0f'%(b2dist),lat,lon,b2lat,b2lon,b2wind,b2slp)
            
            if(b2dist <= m2distMax):
                dojtwc=1

        wind=winds[n]
        tctype=tctypes[n]
        agency=agencies[n]
        if(agency == ''):
             agency='jtwc'
        #print('qqq',dtg,lat,b2lat,lon,b2lon,mslp,b2mslp,wind,b2wind,agency)
        d2land=dist2lands[n]
        rmw=rmws[n]
        
        # -- data check
        #
        if(isnan(mslp)):
            mslp=sundef
            cmslp=' -999'
        else:
            cmslp='%5.0f'%(mslp)
        if(isnan(wind)):
            wind=sundef
        if(isnan(rmw)):
            rmw=' '
            crmw='   '
        else:
            crmw="%3.0f"%(rmw)
        
        # -- convert to 1-min ave wind
        #
        wind0=wind1=-999
        kfact1=conv10minto1min(d2land, sid, useStandard=1)
        kfact0=conv10minto1min(d2land, sid, useStandard=0)
        if(wind != sundef):    
            wind0=wind*kfact0
            wind0=nearest5kts(wind0)
            
            wind1=wind*kfact1
            wind1=nearest5kts(wind1)
            
        # -- get vmax from lookup table at jtwc
        #
        vmaxha=-999.0
        vmaxck=-999.0
        if(mslp != sundef):
            vmaxha=HolidayAtkinsonPsl2Vmax(mslp)
            vmaxha=nearest5kts(vmaxha)
            vmaxck=CourtneyKnaffPminVmax(mslp)
            vmaxck=nearest5kts(vmaxck)
            

            
        (clat,clon)=Rlatlon2Clatlon(lat,lon,dodec=0)
        ibtrk[dtg]=(lat,lon,wind,mslp,clat,clon)
        if(doprint):
            print ('dtg: ',sid,dtg,'%5s %6s %s'%(clat,clon,cmslp),'w0-1 %5.0f %5.0f  '%(wind0,wind1),\
                   'ha %5.0f ck %5.0f %3s %-10s'%(vmaxha,vmaxck,tctype,agency),'%6.0f %s'%(d2land,crmw),\
                   'm2: %5.0f tc: %s wn: %s'%(b2wind,b2tccode,b2wncode),\
                   'dojtwc',dojtwc)
        
    # -- get prev 12-h track dir/spd
    #
    dtgs.sort()
    ndtgs=len(dtgs)

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
            trkdir=undef
            trkspd=undef
        else:
            
            rlatm1=lats[nm1]
            rlonm1=lons[nm1]
            rlat0=lats[n0]
            rlon0=lons[n0]
            
            dt=mf.dtgdiff(dtgs[nm1],dtgs[n0])
            (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
    
        #print('dddd',dtgs[n],dt,nm1,n0,trkdir,trkspd,spds[n])
        dirspd[dtg]=(trkdir,trkspd)        
        
        (gotR34,gotR50,gotR64,r34,r50,r64)=getRadii(tc,n)
        radii[dtg]=(gotR34,gotR50,gotR64,r34,r50,r64)
        
        if(verb):
            if(gotR34 == 0 and gotR50 == 0 and gotR64 == 0):
                print('rrrnnnooo',dtgs[n],n)
    
            if(gotR34):
                print('rrr333444',dtgs[n],n,r34)
                
            if(gotR50):
                print('rrr555000',dtgs[n],n,r50)
    
            if(gotR64):
                print('rrr666444',dtgs[n],n,r64)
    

    return(ibtrk,dirspd,radii)

def getB2trk(tstmid,oBD2s):

    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
    if(b2id == 'SH'):
        tstmid="%s%s.%s"%(snum,'s',year)
    if(b2id == 'IO'):
        tstmid="%s%s.%s"%(snum,'i',year)
            
        
    kk=oBD2s.keys()
    #for k in kk:
        #if(mf.find(k,'1980')):
            #if(mf.find(k,'s') or mf.find(k,'p')):
                #print('k: ',k)obj
    try:
        b2trk=oBD2s[tstmid]
    except:
        b2trk={}
        
    bdtgs=[]
    if(len(b2trk) > 0):
        ob2trk={}
        bdtgs=list(b2trk.keys())
        bdtgs.sort()
        for bdtg in bdtgs:
            ob2trk[bdtg]=b2trk[bdtg][0]
    else:
        ob2trk={}
            
    return(ob2trk,bdtgs)

def getM2trk(tstmid,oMD2s):

    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
    if(b2id == 'SH'):
        tstmid="%s%s.%s"%(snum,'s',year)
    if(b2id == 'IO'):
        tstmid="%s%s.%s"%(snum,'i',year)
            
        
    kk=oMD2s.keys()
    #for k in kk:
        #if(mf.find(k,'1980')):
            #if(mf.find(k,'s') or mf.find(k,'p')):
                #print('k: ',k)obj
    try:
        m2=oMD2s[tstmid]
    except:
        m2={}
    
    if(len(m2) > 0):
        m2trk=m2[0]
        m2dtgs=m2[0]
    else:
        m2trk={}
        m2dtgs={}
        
    return(m2trk,m2dtgs)

def getB2dtgsByYear(oBD2s,tstmid):

    (snum,b1id,iyear,ib2id,stm2id,stm1id)=getStmParams(tstmid)

    kk=oBD2s.keys()
    b2dtgs={}

    for k in kk:
        (snum,b1id,kyear,kb2id,stm2id,stm1id)=getStmParams(k)
        if(kyear == iyear):
            if(ib2id == kb2id):
                #print(k,kb2id,ib2id)
                dtgs=list(oBD2s[k].keys())
                dtgs.sort()
                b2dtgs[k]=dtgs
                
    return(b2dtgs)

def getM2dtgsByYear(oMD2s,tstmid):

    (snum,b1id,iyear,im2id,stm2id,stm1id)=getStmParams(tstmid)

    kk=oMD2s.keys()
    m2dtgs={}

    for k in kk:
        (snum,b1id,kyear,km2id,stm2id,stm1id)=getStmParams(k)
        if(kyear == iyear):
            if(im2id == km2id):
                #print(k,km2id,im2id)
                dtgs=list(oMD2s[k][1])
                dtgs.sort()
                m2dtgs[k]=dtgs
                
    return(m2dtgs)

def getBD2ForIB(itc,oBD2s,tstmid,b2dtgs):
    
    itimes=list(itc.time)
    idtgs=[]
    for itime in itimes:
        dtg=convertItime2Dtg(itime)
        idtgs.append(dtg)
        
    mstms=[]
    stms=b2dtgs.keys()
    for stm in stms:
        bdtgs=b2dtgs[stm]
        for idtg in idtgs:
            if(idtg in bdtgs):
                mstms.append(stm)
                
    mstms=mf.uniq(mstms)
    
    if(len(mstms) == 1):
        mstmid=mstms[0]
        b2trk=getB2trk(mstmid,oBD2s)
        #print('bbb',b2trk)
    
def getMD2ForIB(itc,oMD2s,tstmid,m2dtgs,aTCs,distMax=100.0,pcmd2Min=50.0,verb=0):
    
    idtgs=[]
    iposit={}

    for n in range(0,len(itc.time)):

        itime=itc.time[n]
        dtg=convertItime2Dtg(itime)
        idtgs.append(dtg)

        ilat=itc.lat[n]
        ilon=itc.lon[n]
        iposit[dtg]=(ilat,ilon)
        
        if(verb): print('ibtrac',tstmid,n,dtg,'%4.1f %5.1f'%(ilat,ilon))
        
    nidtgs=len(idtgs)
    m2trk={}
    stms=m2dtgs.keys()
    mstmids=[]
    cnts={}
    for stm in stms:
        mdtgs=m2dtgs[stm]
        mtrk=oMD2s[stm][0]

        for idtg in idtgs:
            
            if(idtg in mdtgs):

                (mlat,mlon)=mtrk[idtg][0:2]
                (ilat,ilon)=iposit[idtg]
                idist=gc_dist(ilat,ilon,mlat,mlon)
                #print('iadf---',stm,idtg,ilat,ilon,mlat,mlon,idist)
                if(idist <= distMax):
                    if(verb): print('iii--mmm',tstmid,stm,idtg,'iii %4.1f %5.1f mmm %4.1f %5.1f ddd: %6.0f'%(ilat,ilon,mlat,mlon,idist))
                    try:
                        cnts[stm]=cnts[stm]+1
                    except:
                        cnts[stm]=1
                        
                    m2trk[idtg]=mtrk[idtg]
                    mstmids.append(stm)
                    
    mstmids=mf.uniq(mstmids)
    if(verb):
        for mstmid in mstmids:
            print('cccnnn',mstmid,cnts[mstmid],'nndd',nidtgs)
        print('111ssstttmmm',tstmid,mstmids)
    
    pcmd2=-99
    if(len(mstmids) == 1):
        
        mstmid=mstmids[0]
        try:
            mitc=aTCs[mstmid]
            mtrk=getIBtrack(mitc)
            mcnt=len(mtrk)
        except:
            mcnt=-999
            
        nddiff=nidtgs-cnts[mstmid]
        pcmd2=(float(cnts[mstmid])/float(nidtgs))*100.0
        if(verb): print ('lllllllllllll',tstmid,mstmid,cnts[mstmid],nidtgs,'mmm',mcnt,'nddiff',nddiff,pcmd2)
        if(mcnt > 0 or pcmd2 < pcmd2Min):
            mstmid=None
            m2trk={}
        else:
            if(verb): print('mmmssstttmmm',tstmid,mstmid,'cnts: ',cnts[mstmid],'ndtgs: ',nidtgs,'mitc:',len(mtrk))
    else:
        mstmid=None
        m2trk={}
        
    return(mstmid,m2trk,pcmd2)

    
def lsIBtrack(itc,tstmid):
    
    idtgs=[]
    iposit={}

    for n in range(0,len(itc.time)):

        itime=itc.time[n]
        dtg=convertItime2Dtg(itime)
        idtgs.append(dtg)

        ilat=itc.lat[n]
        ilon=itc.lon[n]
        iposit[dtg]=(ilat,ilon)
        
        print('ibtrac',tstmid,n,dtg,iposit[dtg])
        
    
def getIBtrack(itc):
    
    idtgs=[]
    iposit={}

    for n in range(0,len(itc.time)):

        itime=itc.time[n]
        dtg=convertItime2Dtg(itime)
        idtgs.append(dtg)

        ilat=itc.lat[n]
        ilon=itc.lon[n]
        iposit[dtg]=(ilat,ilon)
        
    return(iposit)
        
def getMD2stmid(mmstmid,tcnamesAll,verb=0):
    
    istmid=mmstmid[0]
    astmid=mmstmid[1]
    istmids=MakeStmList(istmid,tcnamesAll,verb=verb)
    istmid=istmids[0]
    (isnum,ib1id,year,nb2id,stm2id,stm1id)=getStmParams(istmid)
    (asnum,ab1id,year,nb2id,stm2id,stm1id)=getStmParams(astmid)
    ib1id=ib1id.lower()
    nstmid="%s%s.%s"%(asnum,ib1id,year)
    return(nstmid)
    
        
        
