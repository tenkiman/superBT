#!/usr/bin/env python3

from ibvm import *

usePy=1

if(not(usePy)):
    MF.sTimer('load-ib')
    I.load_all_storms()
    MF.dTimer('load-ib')

ddir='/w21/dat/tc/ib3/'


byear=1940

#eyear=1944

byear=1940
eyear=2023

byear=2000
eyear=2023

years=range(byear,eyear+1)

for year in years:
        
    syear=str(year)

    # -- use existing pickle dump by year
    if(usePy):

        P=open('%s/iTC%s.pyp'%(ddir,syear),'rb')
        TCs=pickle.load(P)
        P.close()

    else:
    
        TCs=[tc for tc in I.storms if tc.season == year]
        print ('year: ',year,len(TCs))
        P=open('%s/iTC%s.pyp'%(ddir,syear),'wb')
        pickle.dump(TCs,P)
        P.close()

    nTCs=len(TCs)
    atcfID={}
    noatcfID={}
    for n in range(0,nTCs):
        tc=TCs[n]
        print('nnn',year,n,tc)
        (sid,sid2,astmid)=convertIb2AtcfId(tc)
        if(verb): print('tc sid',n,sid,sid2,tc.ID,tc.ATCF_ID,tc.genesis)
        #continue
        #rc=getibTCs4aTCs(aTCs,year,basin,tstmids)
        #sys.exit()
        #continue
        if(tc.ATCF_ID != None):
            stmid=getStm1id4Atcfid(tc.ATCF_ID,sid)
            if(verb): print ('atcf-stmid: ',stmid)
            #if(domd3):
                #(rc,md3trk)=md3.getMd3track(stmid,dobt=1,verb=verb)
                #dtgs=list(md3trk.keys())
                #print (dtgs)
                #dtgs.sort()
                #rc=md3trk[dtgs[0]]
                #print ('rc: ',rc)
                
            #(lat,lon,mslp,wind,time)=getITCvars(tc)
            #print(time)
            
            #sys.exit()
            ##stmid="%2s%s.%s"
            atcfID[n]=tc
            
        else:
            noatcfID[n]=tc
            
        if(verb):    
            print('n: basin : subbasin: ',n,tc.ATCF_ID,tc.basin,tc.subbasin,'sid: %s.%d'%(sid,year))
    
    # -- out as dict with stmid as key
    #
    
    oTCs={}
    
    # -- first the ones with ATCF_ID
    #
    kk=atcfID.keys()
    for k in kk:
        tc=atcfID[k]
        (sid,sid2,astmid)=convertIb2AtcfId(tc)
        oTCs[astmid]=tc
        print ('yyyy: ',k,sid,sid2,astmid)

    # -- now the ones with out a stmid... start at 51 in each basin
    #
    sids=[]
    snums={}
    kk=noatcfID.keys()
    for k in kk:
        tc=noatcfID[k]
        (sid,sid2,astmid)=convertIb2AtcfId(tc)
        sids.append(sid)
        MF.appendDictList(snums,sid,k)
        
    sids=mf.uniq(sids)
    for sid in sids:
        bsnums=snums[sid]
        inum=51
        for bsnum in bsnums:
            tc=noatcfID[bsnum]
            byear=tc.season
            (sid,sid2,astmid)=convertIb2AtcfId(tc)
            bstmid="%s%s.%s"%(inum,sid,byear)
            oTCs[bstmid]=tc
            print('nnnn: ',bsnum,sid,sid2,bstmid)
            inum=inum+1
            

    # -- now pickle dump
    #
    P=open('%s/iTC%s-stmid.pyp'%(ddir,syear),'wb')
    pickle.dump(oTCs,P)
    P.close()
            


#I.storms
#I.possible_basins
#I.possible_subbasins
#print([a for a in dir(I) if not a.startswith('_')])
#query = 'SELECT DISTINCT name,genesis FROM storms WHERE season=2005 AND basin="NA" AND lat>20 AND lat<30 AND lon>260 AND lon<280 ORDER BY genesis'
#for row in I.db.execute(query):
    #print(row)
#> ('ARLENE', '2005-06-08 18:00:00')
#> ('BRET', '2005-06-28 18:00:00')
#> ('CINDY', '2005-07-03 18:00:00')
#> ('DENNIS', '2005-07-04 18:00:00')
#> ('EMILY', '2005-07-11 00:00:00')
#> ...
#query = 'SELECT DISTINCT name,genesis FROM storms WHERE season=2005 AND basin="NA" AND lat>20 AND lat<30 AND lon>260 AND lon<280 ORDER BY genesis'
#rows=I.db.execute(query)
#rows
#print(rows)
#I.load_all_storms()
#TCs = [tc for tc in I.storms if tc.season == 2005]
#import pickle as pck
#for tc in TCs:
         #print(tc.name)
#TCs = [tc for tc in I.storms if tc.season == 1945]
#for tc in TCs:
         #print(tc.name)
#for tc in TCs:
         #print(tc.id)
#tc0=TCs[0]
#tc0
#tc0.attr
#tc0.ACE
#tc0.lat
#tc0.lon
#tc0.wind
#tc0.ATCF_ID
#tc0.metadata
#tc0.ID
#tc0.basin
#tc0.subbasin
#tc0.subbasins
#TC2005s = [tc for tc in I.storms if tc.season == 2005]
#TC1945s = [tc for tc in I.storms if tc.season == 1945]
#for tc in TC2005s:
    #print tc.ID
#for tc in TC2005s:
    #print(tc.ID,tc.ATCF_NAME)
#for tc in TC2005s:
    #print(tc.ID,tc.ATCF_ID)
#tc0=TC2005s[0]
#tc0.subbasin
#tc0.basin
#tc0.basin
#tc0.lat
#tc0.lon
#tc0.times
#tc0.q
#tc0.data_at_time()
#tc0.to_json()
#tc0=TC1945s[0]
#tc0.to_json
#tc0.lat
#tc0.lon
#tc0.ATCF_ID
#tc0.ID
#P=open('.dat/ib-1945.pyp','wb')
#P=open('./dat/ib-1945.pyp','wb')
#pck.dump(TC1945s,P)
#P.close()
#P=open('./dat/ib-1945.pyp','rb')
#tc45s=pck.load(P)
#tc2=tc45s[0]
#tc2.v
#print(len(tc45s))
#print(I.logfile)
#help
#help()
#get_ipython().run_line_magic('save', '')
