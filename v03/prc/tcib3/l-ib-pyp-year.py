#!/usr/bin/env python3

from sBT import *
from ibtracs import Ibtracs
import pickle

I = Ibtracs()
print(I.possible_basins)
print(I.possible_subbasins)

def convertIb2AtcfId(tc):
    
    if(tc.basin == 'NA'): 
        sid='l'
    elif(tc.basin == 'WP'): 
        sid='w'
    elif(tc.basin == 'EP'):
        if(tc.subbasin == 'CP'): 
            sid='c'
        else:
            sid='e'

    elif(tc.basin == 'NI'):
        if(tc.subbasin == 'BB'): 
            sid='b'
        elif(tc.subbasin == 'AS'): 
            sid='a'
        else:
            sid='i'
            
    elif(tc.basin == 'SI'): 
        sid='s'
    elif(tc.basin == 'SP'): 
        sid='p'
    elif(tc.basin == 'SA'): 
        sid='q'
    else:
        print ('ooopppsss: tc.basin = ',tc.basin)
        sys.exit()
    return(sid)
        
        
        
        
    

#I.load_all_storms()

ddir='/w21/dat/tc/ib3/'

#for tc in I.storms:
#    print (tc.ID,tc.season)
    
#sb=I.possible_subbasins
#print(sb)

byear=1945
eyear=1950
eyear=2024
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

year=1945
atcfID={}
noatcfID={}
for tc in aTCs[year]:
    sid=convertIb2AtcfId(tc)
    if(tc.ATCF_ID != None):
        MF.appendDictList(atcfID, sid, tc.ATCF_ID)
    else:
        MF.appendDictList(noatcfID, sid,tc.genesis )
        
        
    print('basin:subbasin: ',tc.ATCF_ID,tc.basin,tc.subbasin,'sid: %s.%d'%(sid,year))

kk=atcfID.keys()
kk=mf.uniq(list(kk))
for k in kk:
    stm2ids=atcfID[k]
    stm2ids.sort()
    for stm2 in stm2ids:
        print('k: ',k,stm2)
        
kk=noatcfID.keys()
kk=mf.uniq(list(kk))
for k in kk:
    stm2ids=noatcfID[k]
    stm2ids.sort()
    for stm2 in stm2ids:
        print('NO-k: ',k,stm2)


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
