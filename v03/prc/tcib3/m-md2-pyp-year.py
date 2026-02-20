#!/usr/bin/env python3

from ibvm import *

usePy=1

if(not(usePy)):
    MF.sTimer('load-ib')
    I.load_all_storms()
    MF.dTimer('load-ib')

ddir='/w21/dat/tc/ib3/'

pybyear=1940
pyeyear=2023
PA=open('%s/iTC-%s-%s.pyp'%(ddir,pybyear,pyeyear),'rb')
aTCs=pickle.load(PA)
PA.close()
astmids=list(aTCs.keys())

PN=open('%s/iTC-tcnamesAll.pyp'%(ddir),'rb')
tcnamesAll=pickle.load(PN)
PN.close()

byear=1980
eyear=1980

# -- 20250916 -- redo to keep do correct SH/IO number >= 51
#
byear=1940
eyear=2023

byear=1980
eyear=1980

byear=1945
eyear=2023

#byear=eyear=1953
#byear=eyear=1981

# -- 20251009 -- redo to keep with nhc adecks
#
byear=1940
eyear=2023

#byear=eyear=2010
#byear=eyear=1954
verb=0

MF.sTimer('md2-%s-%s'%(byear,eyear))
years=range(byear,eyear+1)
oMD2s={}

for year in years:
        
    syear=str(year)
    
    b2maskj="%s/%s/b????????.dat"%(bdirj,syear)
    b2maskn="%s/%s/b????????.dat"%(bdirn,syear)
    bd2s=glob.glob(b2maskj) + glob.glob(b2maskn)
    bd2s.sort()
    
    for bd2 in bd2s:
        
        ad2='/tmp/zy0x122'
        (bdir,bfile)=os.path.split(bd2)
        b2id=bfile[1:3]
        bnum=bfile[3:5]
        isnhc=IsNhcBasin(b2id)

        afile=bfile.replace('b','a')
        ad2j="%s/%s/%s"%(adirj,syear,afile)
        ad2n="%s/%s/%s"%(adirn,syear,afile)
        
        if(MF.ChkPath(ad2j) and not(isnhc)):
            ad2=ad2j
        if(MF.ChkPath(ad2n) and isnhc):
            ad2=ad2n
            
        print ('bbb222',bd2,'aaa222',ad2,'isnhc',isnhc,'bnum: ',bnum)
        #print ('bb',bfile,'aa',afile,'ad2:',ad2)
        

        bb=bfile.split('.')
        bstmid=bb[0][1:]
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(bstmid)
        #tstmids=MakeStmList(stm1id,tcnamesAll=tcnamesAll)
        print ('WWWooorrrkkking: ',bstmid,stm1id)
        tstmid=stm1id.lower()

        acards=MF.ReadFile2String(ad2,warn=0)
        bcards=MF.ReadFile2String(bd2)
        
        #try:
            #bcards=open(bd2).readlines()
        #except:
            #bcards=[]
    
        #try:
            #acards=open(ad2).readlines()
        #except:
            #acards=[]
        print ('aaa',b2id,snum,syear,len(acards))
        print ('bbb',len(bcards))
        abcards=acards+bcards
        
        bd=MDdeck(abcards,b2id,snum,syear)
        #bd.getDtgRangeNN(bd.mD,nhours=48,verb=verb,warn=verb)
        #bdtgs=list(bd.mD.uniqStmdtgs.keys())
        
        # -- only use the best track dtgs
        #
        bdtgs=list(bd.mD.best.keys())
        bdtgs.sort()
        
        # -- set the mD dtgs to best track
        #
        bd.mD.dtgs=bdtgs
        
        if(len(bdtgs) == 0):
            print('WWW for: %s  no bdtgs! .. press... '%(tstmid))
            continue

        # -- case for dtg breaks in bdeck
        #
        #bd.mD.dtgs=bd.mD.uniqStmdtgs[bdtgs[-1]]

        smD=bd.mD
        smDBT=copy.deepcopy(bd.mD)
    
        #smD.setMDtrk(verb=verb)
        #smD.cleanMD()
    
        # -- btonly bbbbbbbbbbbbbbbbbbb
        #
        smDBT.setMDtrk(verb=verb,docq00=0,btonly=1)
        # -- put BT to pypdb
        #
        smDBT.cleanMD()
        
        #print('smD',len(smD.dtgs))
        #print('smDBT',len(smDBT.dtgs))
        #for dtg in smDBT.dtgs:
        #    print('dd',dtg)
            
        m2trk={}
        m2trk=smDBT.getMDtrk()
        
        #if(stm1id == '01L.1954'):
            #print(abcards)
            #print(bdtgs)
            #bd.mD.ls()
            #(trk,dtgs)=m2trk
            #dtgs.sort()
            #for dtg in dtgs:
                #print(dtg,trk[dtg])
            ##bd.ls()
            #sys.exit()
        
    
        oMD2s[tstmid]=m2trk
        
        
# -- now pickle dump
#
P=open('%s/iTC-md2-jtwc-nhc-%s-%s.pyp'%(ddir,byear,eyear),'wb')
pickle.dump(oMD2s,P)
P.close()
MF.dTimer('md2-%s-%s'%(byear,eyear))
        
sys.exit()
