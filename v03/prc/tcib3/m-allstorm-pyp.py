#!/usr/bin/env python3

from ibvm import *

usePy=1

ddir='/w21/dat/tc/ib3/'

byear=1940
eyear=2023

years=range(byear,eyear+1)

aTCs={}
tcnamesAll={}

for year in years:
        
    syear=str(year)

    P=open('%s/iTC%s-stmid.pyp'%(ddir,syear),'rb')
    TCs=pickle.load(P)
    aTCs.update(TCs)
    P.close()
    kk=TCs.keys()
    for k in kk:
        tt=k.split('.')
        tyear=tt[1]
        tnum=tt[0]
        tkey=(tyear,tnum)
        tcnamesAll[tkey]=TCs[k].name
        print( 'kkk',tkey,tcnamesAll[tkey])

P=open('%s/iTC-tcnamesAll.pyp'%(ddir),'wb')
pickle.dump(tcnamesAll,P)
P.close()

P=open('%s/iTC-%s-%s.pyp'%(ddir,byear,eyear),'wb')
pickle.dump(aTCs,P)
P.close()

sys.exit()
