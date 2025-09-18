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

#byear=eyear=2000
#byear=eyear=1953
#byear=eyear=1981

MF.sTimer('md2-%s-%s'%(byear,eyear))
years=range(byear,eyear+1)
oMD2s={}

for year in years:
        
    syear=str(year)
    
    b2mask="%s/%s/b????????.dat"%(bdirj,syear)
    bd2s=glob.glob(b2mask)
    bd2s.sort()
    
    for bd2 in bd2s:
        
        (bdir,bfile)=os.path.split(bd2)
        afile=bfile.replace('b','a')
        ad2="%s/%s/%s"%(adirj,syear,afile)
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
            
        abcards=acards+bcards
        bd=MDdeck(abcards,b2id,snum,syear)
        bd.getDtgRangeNN(bd.mD,nhours=48,verb=verb,warn=verb)
        bdtgs=list(bd.mD.uniqStmdtgs.keys())
        bdtgs.sort()
        
        if(len(bdtgs) == 0):
            print('WWW for: %s  no bdtgs! .. press... '%(tstmid))
            continue

        # -- case for dtg breaks in bdeck
        #
        bd.mD.dtgs=bd.mD.uniqStmdtgs[bdtgs[-1]]

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
    
        oMD2s[tstmid]=m2trk
        
        #print('ttt',tstmid,m2trk)
        
        
# -- now pickle dump
#
P=open('%s/iTC-md2-jtwc-%s-%s.pyp'%(ddir,byear,eyear),'wb')
pickle.dump(oMD2s,P)
P.close()
MF.dTimer('md2-%s-%s'%(byear,eyear))
        
sys.exit()
