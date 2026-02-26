#!/usr/bin/env python

from ad2vm import *

def getDsbdir(dssDir):
    
    if(dssDir != None):
        dsbdir=dssDir
        
    else:
        # -- local for DSs or DSs-local in .
        #
        dsbdir="%s/DSs"%(TcDataBdir)
        localDSs=os.path.abspath('./DSs')
        localDSsLocal=os.path.abspath('./DSs-local')
        
        if(os.path.exists(localDSs) and dolocalDSs):
            print 'llllllllllll',localDSs
            dsbdir=localDSs
            
        elif(os.path.exists(localDSsLocal) and dolocalDSs):
            print 'llllllllllll--------lllllllllll',localDSsLocal
            dsbdir=localDSsLocal
    
        else:
            dsbdir="%s/DSs"%(TcDataBdir)
            
    return(dsbdir)
        

def getBd2Years(tstmids,dsbdir,override=0,rmInteractive=0):
    
    byears=[]
    for tstmid in tstmids:
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        byears.append(byear)
        
    byears=mf.uniq(byears)
    print 'bd2year     bd2siz     bdpath'
    for byear in byears:
        bd2path="%s/bd2-%s.pypdb"%(dsbdir,byear)
        bsiz=MF.getPathSiz(bd2path)
        bsiz=float(bsiz)/(1024)
        print '%s        %5dK     %s'%(byear,mf.nint(bsiz),bd2path)
        if(override):
            rmopt=''
            if(rmInteractive): rmopt='-i'
                 
            mf.runcmd("rm %s %s"%(rmopt,bd2path))
            bsiz=MF.getPathSiz(bd2path)
            bsiz=float(bsiz)/(1024)
            print 'override=1  new bd2path...'
            print '%s        %5dK     %s'%(byear,mf.nint(bsiz),bd2path)
            
    
    return(byears)
    
def getBdeck2s(fstmids,md3,domiss=0,
                warn=0,verb=0):
    
    bd2s={}
    
    m3stmids={}
    
    for fstmid in fstmids:
        (tstmid,m2stmid)=fstmid
        m3stmids[tstmid]=m2stmid

    tstmids=m3stmids.keys()
    tstmids.sort()

    byears=[]
    for tstmid in tstmids:
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        byears.append(byear)
        
    byears=mf.uniq(byears)
    print byears
    
    return
        
        
    for tstmid in tstmids:
        
        
        # -- get stmcards
        #
        (rc,m3cards)=md3.getMd3Cards(tstmid)
        #print 'stmcards',len(m3cards)
        (smeta,smetacard)=md3.getMd3StmMeta(tstmid)
        ss9=smeta[-2]
        stmDev=None
        ss=ss9.split( )
        stm9xid="%s.%s"%(ss[-1],byear)
        sname=smeta[4]
        basin=sbtB1id2Basin[b1id]
        useVmax4TcCode=1
        m3trk=MD3trk(m3cards,stm1id,stm9xid,dom3=1,isBD2=1,sname=sname,basin=basin,stmDev=stmDev,
                     useVmax4TcCode=useVmax4TcCode,
                     verb=verb)        
    
        utstmid=tstmid.upper()
        MF.sTimer('bds-%s'%(utstmid))
        bd2s[utstmid]=Bdeck2(m3trk,tstmid,verb=0)
        MF.dTimer('bds-%s'%(utstmid))

        # -- look for alternate stmid
        #
        m3stmid=m3stmids[tstmid].upper()
        if(m3stmid != utstmid):
            MF.sTimer('bds-%s'%(m3stmid))
            print 'WWW add md2 stmid ',m3stmid,' bd2 -- the same bd2 as md3 stmid ',utstmid
            bd2s[m3stmid]=Bdeck2(m3trk,tstmid,verb=0)
            MF.dTimer('bds-%s'%(m3stmid))
                    
        continue
        
    return(bd2s)


def getBD2Ss(stmopt,verb=0):
    
    B2DSs={}
    # -- specific for making bd2 .. always best track posits only
    #
    dobt=1
    dofilt9x=0
    doNNand9X=0
    
    tstmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

    # -- get bd2 years and paths and optionally rm -i to start with fresh files
    #
    byears=getBd2Years(tstmids,dsbdir)
    
    for byear in byears:
        dbtype='bd2'
        for byear in byears:
            dbfile="%s-%s.pypdb"%(dbtype,byear)
            B2DS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
            B2DSs[byear]=B2DS
            
    return(B2DSs,tstmids)
        
    

def getBd2(BD2Ss,bstmid):
    (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(bstmid)
    bstmid=bstmid.upper()
    bd2=B2DSs[byear].db[bstmid]
    return(bd2)
    

def loadBgrd(B2DSs,bstmid,bgrd,doGrd=1,verb=0):
    
    (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(bstmid)

    def getTau00(btrk,bdtg):

        try:
            (blat,blon,bvmax,bpmin,bdir,bspd,btcstate,bwnstat)=btrk[bdtg]
            #print '000',bdtg,blat,blon
            bgot=1

            if(bvmax < 0):
                btc=1
            elif(bvmax >= vmaxMin):
                btc=1
            else:
                btc=0
                
        except:
            bgot=0
            
        ii00=jj00=None
        if(bgot and btc):
            blon00=blon
            blat00=blat
            (i,j,ii00,jj00)=bgrd.ll2ij(blon00,blat00)
            
        return(ii00,jj00,bvmax)
            
            

    def getTau(btrk,bdtg,btau,ii00,jj00,bvmax00,warn=0):
        
        vbdtg=mf.dtginc(bdtg,btau)
        try:
            (blat,blon,bvmax,bpmin,bdir,bspd,btcstate,bwnstat)=btrk[vbdtg]
            bgot=1

            if(bvmax < 0):
                btc=1
            elif(bvmax >= vmaxMin):
                btc=1
            else:
                btc=0
                
        except:
            bgot=0
            
        ndx=bval=None
            
        if(bgot and btc):
            
            (i,j,ii,jj)=bgrd.ll2ij(blon,blat)
            
            mm=int(bdtg[4:6])

            test00=(ii00 >= 0 and ii00 < bgrd.ni) and (jj00 >= 0 and jj00 < bgrd.nj)
            testiijj=(ii >= 0 and ii < bgrd.ni) and (jj >= 0 and jj < bgrd.nj)
            
            if(test00 and testiijj):
                ndx=(ii00,jj00,mm)
                bval=(blat,blon,bvmax,bdir,bspd,bstmid)
            else:
                if(ii00 == None):
                    if(warn):
                        print 'WWW--000 tau0 not a tc vmax %3.0f < %3.0f stmid: %s'%(bvmax00,vmaxMin,bstmid)
                else:
                    if(warn):
                        print 'WWW--OOOBBB',blat,blon,bstmid
            
        return(ndx,bval)

    bd2=getBd2(B2DSs,bstmid)
    btrk=bd2.BT.btrk
    bdtgs=btrk.keys()
    bdtgs.sort()

    for bdtg in bdtgs:
        #print 'bbb',bdtg,bstmid,btrk[bdtg]
        # -- get tau 0 ii,jj
        (ii00,jj00,bvmax00)=getTau00(btrk,bdtg)
        
        for btau in btaus:
            (ndx,bval)=getTau(btrk,bdtg, btau,ii00,jj00,bvmax00)
            if(ndx != None and ii00 != None):
                
                (ii,jj,mm)=ndx
                if(verb): print 'btau: ',btau,'ndx: ',ndx,' bval: ',bval
                
                tvals=None
                if(len(ogrd[ii,jj,mm,btau]) > 0):
                    tvals=ogrd[ii,jj,mm,btau]
                    
                    
                gottvals=0
                gotit=0
                if(tvals != None):
                    gottvals=1
                    ntvals=len(tvals)
                    for tt in tvals:
                        if(tt == bval):
                            gotit=1
                            continue
                            #print 'ttbb',tt,bval,ntvals
                            #ogrd[ii,jj,mm,btau].append(bval)
                        
                        
                if(gottvals == 0 or (gotit == 0 and gottvals)):
                    if(verb): print 'tt0000',bval
                    ogrd[ii,jj,mm,btau].append(bval)
                    
                    
    return(1)

def lsOgrd(ondx,ovals,bgrd):
    (i,j,m,tau)=ondx
    (olat,olon)=bgrd.ij2ll(i,j)
    no=len(ovals)
    (clat,clon)=Rlatlon2Clatlon(olat,olon,dodec=1)
    ocard="     I:J:MM:tau: %3d %3d %2d %3d lat/lon: %4s %s | N: %3d"%(i,j,m,tau,clat,clon,no)
    bstmids=[]
    #print 'nnnn',no,str(ovals)
    for n in range(0,no):
        oval=ovals[n]
        (blat,blon,bvmax,bdir,bspd,bstmid)=oval
        bstmids.append(bstmid)
        sep='|'
        #if(n == no-1):
        #    sep=''
        #print 'asdf',n,tau,blat,blon,bstmid
        ocard="%s %4.1f %5.1f %s"%(ocard,blat,blon,sep)
        
    bstmids=mf.uniq(bstmids)
    ocard="%s SS: %s"%(ocard,str(bstmids))

    print ocard
    return(ocard)

def lsMnOgrd(ondx,ovals,bgrd):
    (i,j,m,tau)=ondx
    (olat,olon)=bgrd.ij2ll(i,j)
    (clat,clon)=Rlatlon2Clatlon(olat,olon,dodec=1)
    ocard="Mean I:J:MM:tau: %3d %3d %2d %3d lat/lon: %s %s |"%(i,j,m,tau,clat,clon)
    no=len(ovals)

    ss=sgrd[ondx][0]
    oo=ogrd[ondx]
    no=ss[0]
    mnlat=ss[1]
    mnlon=ss[2]
    (cmnlat,cmnlon)=Rlatlon2Clatlon(mnlat,mnlon,dodec=1)
    mnvmax=ss[3]
    mndir=ss[4]
    mnspd=ss[5]
    mnu=ss[6]
    mnv=ss[7]
    bstmids=ss[-1]
    #ocardoo="ooo: %s %s"%(ocard,str(oo))
    #ocardss="sss: %s %s"%(ocard,str(ss))
    #print ocardoo
    #print ocardss
    bstmids=mf.uniq(bstmids)
    ocard="%s N: %3d ll: %s %s vm: %3.0f ds: %3.0f %2.0f uv: %4.1f %4.1f %s "%(ocard,\
                                                         no,cmnlat,cmnlon,\
                                                         mnvmax,mndir,mnspd,mnu,mnv,\
                                                         str(bstmids))
    
    print ocard
    return(ocard)
    
def datMnOgrd(oo,sgrd,bgrd):
    ondx=keys()
    (i,j,m,tau)=ondx
    (olat,olon)=bgrd.ij2ll(i,j)
    (clat,clon)=Rlatlon2Clatlon(olat,olon,dodec=1)
    ocard="Mean I:J:MM:tau: %3d %3d %2d %3d lat/lon: %s %s |"%(i,j,m,tau,clat,clon)
    no=len(ovals)

    ss=sgrd[ondx][0]
    oo=ogrd[ondx]
    no=ss[0]
    mnlat=ss[1]
    mnlon=ss[2]
    (cmnlat,cmnlon)=Rlatlon2Clatlon(mnlat,mnlon,dodec=1)
    mnvmax=ss[3]
    mndir=ss[4]
    mnspd=ss[5]
    mnu=ss[6]
    mnv=ss[7]
    bstmids=ss[-1]
    #ocardoo="ooo: %s %s"%(ocard,str(oo))
    #ocardss="sss: %s %s"%(ocard,str(ss))
    #print ocardoo
    #print ocardss
    bstmids=mf.uniq(bstmids)
    ocard="%s N: %3d ll: %s %s vm: %3.0f ds: %3.0f %2.0f uv: %4.1f %4.1f %s "%(ocard,\
                                                         no,cmnlat,cmnlon,\
                                                         mnvmax,mndir,mnspd,mnu,mnv,\
                                                         str(bstmids))
    
    print ocard
    return(ocard)



def setMnOgrd(ondx,ovals,bgrd,verb=0):
    
    (i,j,m,tau)=ondx
    (olat,olon)=bgrd.ij2ll(i,j)

    no=len(ovals)

    mnlat=mnlon=0.0
    mnvmax=0.0
    mndir=0.0
    mnspd=0.0
    mnu=0.0
    mnv=0.0
    
    bstmids=[]
    for n in range(0,no):
        oval=ovals[n]
        (blat,blon,bvmax,bdir,bspd,bstmid)=oval
        bstmids.append(bstmid)
        
        # -- convert heading to meteorological direction the wind coming from
        #
        bdir=bdir-180.0
        obdir=bdir
        if(bdir < 0.0): obdir=bdir+180.0
            
        (bu,bv)=dirspd2uv(bdir,bspd,doheading=0)
        if(verb): print 'ssss','obdir: ',obdir,'bdir: ',bdir,'bspd: ',bspd,'uv',bu,bv
        
        mnlat=mnlat+blat
        mnlon=mnlon+blon
        mnvmax=mnvmax+bvmax
        mnu=mnu+bu
        mnv=mnv+bv
        
    bstmids=mf.uniq(bstmids)
    
    mnlat=mnlat/no
    mnlon=mnlon/no
    mnvmax=mnvmax/no
    mnu=mnu/no
    mnv=mnv/no
    
    (mndir,mnspd)=uv2dirspd(mnu,mnv)
    
    # -- turn into heading
    #mndir=mndir+180.0
    
    if(verb): print 'mmnn',mndir,mnspd,'uv',mnu,mnv
    
    stats=[no,mnlat,mnlon,mnvmax,mndir,mnspd,mnu,mnv,bstmids]
    sgrd[ondx].append(stats)
    
    return(1)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'override':            ['O',0,1,'override and delete previous bd2'],
            'ropt':                ['N','','norun',' norun is norun'],
            'basin':               ['b:',None,'a',"""set basin h,i,w,e,l | 'all'"""],
            'vmaxMin':             ['I:',35,'i',"""set vmaxMin default is 35 kts"""],
            'yearOpt':             ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'doPyp':               ['p',1,0,'pickle result'],
            'doDat':               ['D',0,1,'make .dat floar arrays'],
            'dols':                ['l',0,1,'list full ogrd'],
            'doLS':                ['L',0,1,'list summary only'],
            'dolocalDSs':          ['x',1,0,'do NOT use local DSs dir'],
            'warn':                ['W',1,0,'do NOT use bdeck2 (ln -s for 2024->)'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- bd2 from sBT vice mD2 %s'''
        self.examples='''
%s -S w.15
'''



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    
# -- defaults

dssDir=None
dtgopt=None

dsbdir=getDsbdir(dssDir)

# -- error
#
if(basin == None):
    print '''-b must be set'''
    sys.exit()

# -- define the 2D grid global dx x dy
#
dx=dy=2.5
dx=dy=2.0
basinsAll=['h','i','w','e','l']
basinOpts={
    'h':(('h'),      (  30.0,210.,-50.0,0.0)),
    'i':(('i'),      (  40.0,110.,  0.0,30.0)),
    'w':(('a,b,w,e'),( 100.0,210.,  0.0,50.0)),
    'e':(('w,e'),    (180.0,-60.,  0.0,40.0)),
#    'l':(('w,e,l'),  (-100.0,  0.,  0.0,50.0)),
    'l':(('l'),      (-100.0,  0.0, 0.0,50.0)),
    }
    

if(basin == 'all'):
    basins=basinsAll
else:
    basins=[basin]
    

# -- define the taus
#
btau=0
btinc=24
btaue=120
btaus=range(btau,btaue+1,btinc)

# -- define min vmax as command line arg
#
if(yearOpt == None):
    print 'EEE must set yearOpt'
    sys.exit()

if(mf.find(yearOpt,'.')):
    yy=yearOpt.split('.')
elif(mf.find(yearOpt,'-')):
    yy=yearOpt.split('-')
else:
    yy=[yearOpt]

if(len(yy) == 2):
    byear=yy[0]
    eyear=yy[1]
elif(len(yy) == 1):
    byear=eyear=yearOpt
    
years=MF.YearRange(byear, eyear)

print 'yyyyy',years

for basin in basins:
    

    # -- make bgrd area
    #
    bb=basinOpts[basin]
    stmbasin=bb[0]	
    lonW=float(bb[1][0])
    lonE=float(bb[1][1])
    latS=float(bb[1][2])
    latN=float(bb[1][3])
    lsMnOgrd
    stmbasins=stmbasin.split(',')

    bgrd=W2areas(lonW,lonE,latS,latN,dx=dx,dy=dy)
    #bgrd.ls()
    #print bgrd.ll2ij(280.0,35.0)
    #sys.exit()

    # -- initialize 2-d out float array
    #
    sdat2d={}
    for i in bgrd.iis:
        for j in bgrd.jjs:
            sdat2d[i,j]=bgrd.undef
    
    
    pypPath='./mf-tc-climo-%s-%s-%s.pyp'%(basin,byear,eyear)
    datPath='./mf-tc-climo-%s-%s-%s.dat'%(basin,byear,eyear)
    B=open(datPath,'wb')
    
    # -- open pyp
    #
    if(MF.getPathSiz(pypPath) > 0 and not(override) and doPyp):
        PS=open(pypPath,'r')
        MF.sTimer('init--open')
        (ogrd,sgrd)=pickle.load(PS)
        PS.close()
        if(dols or doLS):
            oo=ogrd.keys()
            oo=sorted(oo, key=lambda x: x[3])
            
            for o in oo:
                if(len(ogrd[o]) > 0):
                    if(dols): lsOgrd(o,ogrd[o],bgrd)
                    if(doLS): lsMnOgrd(o,sgrd[o],bgrd)
            sys.exit()
            
        elif(doDat):
            
            #print sgrd
            mm=9
            cmm='%02d'%(mm)
            btime="15%s%s"%(mname3[cmm],byear)
            btinc='1mo'
            print btime
            rc=bgrd.setCtlTemplate(datPath,btime,btinc)

            btau=0
            ostat=0
            
            # -- load array first
            #
            for j in bgrd.jjs:
                for i in bgrd.iis:
                    
                    try:
                        stat=sgrd[i,j,mm,btau]
                    except:
                        stat=None

                    if(stat != None and len(stat) > 0):
                        (olat,olon)=bgrd.ij2ll(i,j)
                        (clat,clon)=Rlatlon2Clatlon(olat,olon,dodec=1)
                        dstat=stat[0][ostat]
                        sdat2d[i,j]=float(dstat)
                        
                        if(verb): 
                            print 'iiuummbb %3d %3d '%(i,j),'lat,lon: %s %s '%(clat,clon),\
                                  'mm,btau,ostat: ',mm,btau,btau,'sss',dstat,sdat2d[i,j]
                        
            ij=0
            for j in bgrd.jjs:
                for i in bgrd.iis:
                    obdat=sdat2d[i,j]
                    b=struct.pack('1f',obdat)
                    B.write(b)
                    ij=ij+1
                    if(obdat != bgrd.undef and verb):
                        print 'bbbbb--i,j',i,j,ij,obdat
                    
                    
            B.close()
            
            sys.exit()
                        

        PS=open(pypPath,'w')
        MF.dTimer('init--open')

    else:
        MF.sTimer('init-CREATE')
        PS=open(pypPath,'w')
        ogrd={}
        sgrd={}
        for i in bgrd.iis:
            for j in bgrd.jjs:
                for m in range(1,12+1):
                    for btau in btaus:
                        ogrd[i,j,m,btau]=[]
                        sgrd[i,j,m,btau]=[]
                
        pickle.dump((ogrd,sgrd),PS)
        PS.seek(0)
        MF.dTimer('init-CREATE')
        
    
    MF.sTimer('ALL-bd2-tc-climo-%s-%s-%s'%(basin,byear,eyear))
    for year in years:
    
        MF.sTimer('bd2-tc-climo-%s'%(year))

        stmopt='%s.%s'%(stmbasin,year)
		
        #stmopt=''
        #nn=len(stmbasins)
        #for n in range(0,nn):
            #stmbasin=stmbasins[n]
            #stmopt='%s%s.%s'%(stmopt,stmbasin,year)
            #if(n < nn-1):
                #stmopt="%s,"%(stmopt)
                

        yearopt=None
        (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearopt)
        if(doBdeck2): doBT=1
        
        # -- get Mdeck3 with tc best track
        #
        verbmd=0
        md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verbmd)
    
        # -- get B2DSs
        #
        verbbd=0
        if(stmopt != None):
            (B2DSs,tstmids)=getBD2Ss(stmopt,verb=verbbd)
            
        MF.sTimer('load-%s'%(stmopt))
        for bstmid in tstmids:
            rc=loadBgrd(B2DSs,bstmid,bgrd,verb=verbbd)
        MF.dTimer('load-%s'%(stmopt))
        
        MF.dTimer('bd2-tc-climo-%s'%(year))
            
    
    oo=ogrd.keys()
    
    # -- do sum stat grid
    #
    for o in oo:
        if(len(ogrd[o]) > 0):
            rc=setMnOgrd(o,ogrd[o],bgrd)
    

    
    if(verb):
        oo=sorted(oo, key=lambda x: x[3])
        for o in oo:
            if(len(ogrd[o]) > 0):
                lsOgrd(o,ogrd[o],bgrd)
                lsMnOgrd(o,sgrd[o],bgrd)
        
    MF.sTimer('dump-%s'%(yearOpt))     
    pickle.dump((ogrd,sgrd),PS)
    PS.close()    
    MF.dTimer('dump-%s'%(yearOpt))     
    
    MF.dTimer('ALL-bd2-tc-climo-%s-%s-%s'%(basin,byear,eyear))
    
sys.exit()