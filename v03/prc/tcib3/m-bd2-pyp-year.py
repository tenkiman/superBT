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

byear=eyear=2000

MF.sTimer('bd2-%s-%s'%(byear,eyear))
years=range(byear,eyear+1)

for year in years:
        
    syear=str(year)
    
    b2mask="%s/%s/b????????.dat"%(bdirj,syear)
    bd2s=glob.glob(b2mask)
    oBD2s={}
    
    for bd2 in bd2s:
        (bdir,bfile)=os.path.split(bd2)

        bb=bfile.split('.')
        bstmid=bb[0][1:]
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(bstmid)
        #tstmids=MakeStmList(stm1id,tcnamesAll=tcnamesAll)
        print ('bd2: ',bstmid,stm1id)
        tstmid=stm1id.lower()

        try:
            bcards=open(bd2).readlines()
        except:
            bcards=[]
    
        bd2=None
        if(len(bcards) > 0):
            bd2=AdeckFromCards(bcards)
            b2trks=bd2.aidtrks
            bb=list(b2trks.keys())
            b2key=bb[0]
            b2trk=b2trks[b2key]
            
        if(bd2 == None):
            b2trk={}
    
        oBD2s[tstmid]=b2trk
        

P=open('%s/iTC-bd2-jtwc-%s-%s.pyp'%(ddir,byear,eyear),'wb')
pickle.dump(oBD2s,P)
P.close()
MF.dTimer('bd2-%s-%s'%(byear,eyear))
