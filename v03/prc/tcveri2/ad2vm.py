from sBT import *
from ATCF import AidProp

clpAids=['clp3','clip','clim','hpac','c120','clp5',
         #'tclp'
         ]
humAids=['ofcl','jtwc']
modAids=['avno','ngps','nvgm','hwrf','otcm','ntcm']
ecmAids=['tecmt','tera5','tecmt','ecmo','emdt','edet','ecmf','tecm5','tecm4','emx']

allAids=ecmAids+modAids+humAids+clpAids

# -- make .pyp for all years did once...
#

def parseAd2Inv(year,sdir='./adinv',override=1,verb=0):
    
    adpath='%s/adinv-%s.txt'%(sdir,year)
    #MF.sTimer('getAd2inv-%s'%(year))
    cards=open(adpath).readlines()
    adpyp='%s/adinv-%s.pyp'%(sdir,year)
    
    PS=open(adpyp,'w')
    #MF.dTimer('getAd2inv-%s'%(year))

    aidStm={}
    
    for card in cards:

        t1=card.split('::')
        #print 't1',len(t1)
        if(len(t1) == 1): continue
        
        if(len(t1) == 2):
            print t1     
                
        aid=t1[0].strip()
        adesc=t1[1]
        
        t2=t1[2].split()
        #print 't2',len(t2)

        astmid=t2[1].strip()
        andtgs=t2[3].strip()
        
        #print """aa-- %s %s %s '%s'"""%(aid,astmid,andtgs,adesc)
        
        rc=appendDictList(aidStm, astmid, (aid,andtgs))

    
    #MF.dTimer('getAd2inv-%s'%(year))
    astmids=aidStm.keys()
    astmids.sort()

    if(verb):
        for astmid in astmids:
            if(isShemBasinStm(astmid)): 
                print astmid,len(aidStm[astmid])
        
    pyp=(aidStm,astmids)
    pickle.dump(pyp,PS)
    return(aidStm,astmids)

def yearOptPrc(yearOpt):
    
    yy=yearOpt.split('.')
    aa=yearOpt.split(',')

    if(len(aa) > 1):
        years=aa
        years.sort()
        return(years)
        
    if(len(yy) == 1):
        years=[yearOpt]
    elif(len(yy) == 2):
        byear=int(yy[0])
        eyear=int(yy[1])
        iyears=range(byear,eyear+1)
        years=[]
        for iyear in iyears:
            
            iyear=get4digitYearFrom2DigitYear(iyear)
            year=str(iyear)
            years.append(year)
            
        years.sort()
            
    return(years)
    
def getEcmwfAid(aids,year,verb=1):
    
    year=int(year)

    oaids=[]
    for aid in aids:
        if(aid[0] in ecmAids):
            oaids.append(aid)
            
    keepaids=[]
    opaids=[]
    nopaids={}
    
    if(verb):
        print 'getEC aids: ',oaids
         
    for oaid in oaids:
        taid=oaid[0]
        naid=int(oaid[1])
        
        # -- always keep
        #
        if(taid == 'emdt'):
            keepaids.append(taid)
        elif(taid == 'tera5'):
            keepaids.append(taid)
         
        # -- other tracker aids done by me or ncep using tmtrkN
        #
        elif(taid == 'tecm5'):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'tecmt' and year < 2024):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'ecmo'):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'edet'):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'ecmf'):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'tecm4'):
            opaids.append(taid)
            nopaids[taid]=naid
        elif(taid == 'emx'):
            opaids.append(taid)
            nopaids[taid]=naid
    
    nmax=-999
    if(len(opaids) > 0):
        
        nmaxs=[]
        maxopaids={}
        
        for opaid in opaids:
            npaid=nopaids[opaid]
            nmaxs.append(npaid)
            MF.appendDictList(maxopaids,npaid,opaid)
            
        # -- sort
        #
        nmaxs.sort()

        # -- pick the biggest and by
        #
        nmax=nmaxs[-1]
        nmaxaids=maxopaids[nmax]

        # -- check for ties ... if so select priority ecm5, ecmt, ecm4, ecmo
        #
        if(len(nmaxaids) > 1):
            
            gotomax=0
            for nn in nmaxaids:
                if(nn == 'tecm5'):
                    onmaxaid=nn
                    gotomax=1

            for nn in nmaxaids:
                if(nn == 'tecmt' and year < 2024 and gotomax == 0):
                    onmaxaid=nn
                    gotomax=1

            for nn in nmaxaids:
                if(nn == 'tecm4' and gotomax == 0):
                    onmaxaid=nn
                    gotomax=1

            for nn in nmaxaids:
                if(nn == 'ecmo' and gotomax == 0):
                    onmaxaid=nn
                    gotomax=1

            for nn in nmaxaids:
                if(nn == 'edet' and gotomax == 0):
                    onmaxaid=nn
                    gotomax=1

            for nn in nmaxaids:
                if(nn == 'ecmf' and gotomax == 0):
                    onmaxaid=nn
                    gotomax=1


        else:
            onmaxaid=nmaxaids[0]
                
    # -- make op string
    #
    adopstr=''
    if(nmax > 0):
        adopstr="%s:ecop"%(onmaxaid)

    # -- make final all ec aids string
    #
    adecstr=''    
    for keepaid in keepaids:
        if(adecstr == ''):
            if(len(keepaids) > 1 or nmax > 0):
                adecstr="%s,"%(keepaid)
            else:
                adecstr="%s"%(keepaid)
        else:
            adecstr="%s%s,"%(adecstr,keepaid)
            
    adecstr=adecstr+adopstr
    
    if(verb):
        print 'getECMWFAid str: ',adecstr
    
    return(adecstr)
            
def getClipperAid(aids,verb=1):

    clpstr=''
    for aid in aids:
        if(aid[0] in clpAids):
            oaid=aid[0]
            if(aid[0] == 'c120'):
                oaid="%s:clp5"%(aid[0])
                
            if(clpstr == ''):
                clpstr='%s'%(oaid)
            else:
                clpstr='%s,%s'%(clpstr,oaid)
            
    if(verb):
        print 'getClipAids: ',clpstr
        
    return(clpstr)

def getHumanAid(aids,verb=1):
    
    humstr=''
    for aid in aids:
        oaid=aid[0]
        if(aid[0] in humAids):
            if(humstr == ''):
                humstr='%s'%(oaid)
            else:
                humstr='%s,%s'%(humstr,oaid)
    if(verb):
        print 'getHumanAids: ',humstr
        
    return(humstr)

def getModelAid(aids,verb=1):

    modstr=''
    for aid in aids:
        oaid=aid[0]
        if(aid[0] in modAids):
            if(modstr == ''):
                modstr='%s'%(oaid)
            else:
                modstr='%s,%s'%(modstr,oaid)

    # -- relabel navgem and nogaps to 'navy'
    #
    mm=modstr.split(',')
    nns=[]
    for m in mm:
        gotnav=gotnav1=gotnav2=0
        if(mf.find(m,'nvgm')):
            gotnav1=1
            gotnav2=0
            nn="%s:navy"%(m)
        if(mf.find(m,'ngps')):
            gotnav2=1
            gotnav1=0
            nn="%s:navy"%(m)
            
        if(gotnav == 0 and gotnav1 == 0 and gotnav2 == 0):
            nns.append(m)
        
        if(gotnav1 and gotnav == 0):
            nns.append(nn)
        if(gotnav2 and not(gotnav1)):
            nns.append(nn)
    
    modstr=''
    for nn in nns:
        if(modstr == ''):
            modstr='%s'%(nn)
        else:
            modstr='%s,%s'%(modstr,nn)
    
    if(verb):
        print 'getModelAids: ',modstr
        
    return(modstr)

def loadVd2Stats(pstat,sdir='./vd2stat',byear=1945,eyear=2024):
    
    vd2pyp='%s/vd2Stat-%s-all-%s-%s.pyp'%(sdir,pstat,str(byear),str(eyear))
    if(os.path.exists(vd2pyp)):
        PS=open(vd2pyp)
        vd2Stats=pickle.load(PS)
    else:
        print 'ooopppsss no pyp: ',vd2pyp
        sys.exit()
            
    return(vd2Stats)
            

def loadAd2Inv(years,sdir='./adinv'):
    
    aidStms={}
    
    for iyear in years:
        
        year=str(iyear)

        adpyp='%s/adinv-%s.pyp'%(sdir,year)
        if(os.path.exists(adpyp)):
            PS=open(adpyp)
            (aidStm,astmids)=pickle.load(PS)
            aidStms[year]=(aidStm,astmids)
            
        else:
            print 'ooopppsss no pyp for year',year
            sys.exit()
            
    return(aidStms)
        
def cnvAidList2Str(vaids,add00=0):
    
    def cnvL2S(vaids):
        vaids=str(vaids)
        vaids=vaids.replace(' ','')
        vaids=vaids.replace("""'""",'')
        vaids=vaids[1:-1]
        
        return(vaids)
        
        
        
    vaids00=[]
    if(add00):
        for vaid in vaids:
            vv=vaid.split(":")
            if(len(vv) == 2):
                vaid001="%s00"%(vv[0])
                vaid002="%s00"%(vv[1])
                vaid00="%s:%s"%(vaid001,vaid002)
            else:
                vaid00="%s00"%(vaid)
                
            vaids00.append(vaid00)
            
            
        
    vaids=cnvL2S(vaids)
    vaids00=cnvL2S(vaids00)
    
    return(vaids,vaids00)


def makeAidStr(aids,doall=0):
    
    aidstr=''
    for aid in aids:
        aaid=aid[0]
        naid=int(aid[1])
        if(aaid in allAids or doall):
            if(aidstr == ''):
                aidstr="%5s:%2d "%(aaid,naid)
            else:
                aidstr="%s %5s:%2d "%(aidstr,aaid,naid)
            
    return(aidstr)
            
        
def aidstrAnl(aidstrs,faidstr=None,add00=0,verb=0):

    tstmids=[]
    faids={}

    if(faidstr == None):

        for aidstr in aidstrs:
            tstmid=aidstr[0]
            tstmids.append(tstmid)
            aidstr1=aidstr[1]
            if(aidstr1[0] == ','):
                aidstr1=aidstr1[1:]
            aa=aidstr1.split(',')
            laa=len(aa)
            faids[tstmid]=(laa,aidstr1)
            print 'aa',laa,'aa--',tstmid,aa,'aidstr',aidstr1
    
        fnmax=-999
        fnmin=999
        fntot=0
        tstmids.sort()
        fnmaxs=[]
        fnmins=[]
        
        nfs={}
        ftaids={}
    
        for tstmid in tstmids:
            naids=faids[tstmid][0]
            if(naids > fnmax): fnmax=naids
            if(naids < fnmin): fnmin=naids       
            fntot=fntot+1
            
        nfmaxs=nfmins=nfunks=0
        taidsmax=taidsmin=taidsunk=''
    
        for tstmid in tstmids:
            naids=faids[tstmid][0]
            if(naids == fnmax): 
                nfmaxs=nfmaxs+1
                if(taidsmax == ''):
                    taidsmax=faids[tstmid][1]
            elif(naids == fnmin): 
                nfmins=nfmins+1
                if(taidsmin == ''):
                    taidsmin=faids[tstmid][1]
            else:
                nfunks=nfunks+1
                if(taidsunk == ''):
                    taidsunk=faids[tstmid][1]
            
    
        if(verb):
            print 'nnff max ',nfmaxs,taidsmax
            print 'nnff min ',nfmins,taidsminaidstrAnl
            print 'nnff UNK ',nfunks,taidsunk
    
        # -- find faids with max number
        #
        
        nfs[0]=nfmaxs
        nfs[1]=nfmins
        nfs[2]=nfunks
        
        ftaids[0]=taidsmax
        ftaids[1]=taidsmin
        ftaids[2]=taidsunk
        
        # -- invert dict
        #
        nfs1 = {v: k for k, v in nfs.items()}
        
        nfsmaxval=max(nfs.values())
        nfsmax=nfs1[nfsmaxval]
        taidsFinal=ftaids[nfsmax].split(",")
        
    else:
        
        for aidstr in aidstrs:
            tstmid=aidstr[0]
            tstmids.append(tstmid)
        
        taidsFinal=faidstr.split(',')

    # -- make lists for ad2-ls,ad2-ph0,vd2
    #
    vaidsFinal=[]
    aaidsFinal=[]
    for taid in taidsFinal:
        tt=taid.split(':')
        if(len(tt) == 2):
            faid=tt[1]
            aaidsFinal.append(tt[0])
            vaidsFinal.append(faid)
        else:
            faid=taid
            vaidsFinal.append(faid)
            aaidsFinal.append(faid)

    (taids,taids00)=cnvAidList2Str(taidsFinal,add00=add00)
    (vaids,vaids00)=cnvAidList2Str(vaidsFinal,add00=add00)
    (aaids,aaids00)=cnvAidList2Str(aaidsFinal,add00=add00)
    
    return(taids,vaids,aaids,
           taids00,vaids00,aaids00,
           tstmids)

def getAidStrMax(ecmstrS):
    
    necmM=-999
    if(len(ecmstrS) == 0):
        return(necmM,'')
        
    
    for ecm in ecmstrS:
        necm=len(ecm)
        if(necm > necmM):
            necmM=necm
            ecmM=ecm
    return(necmM,ecmM)

def getAidstrs(stmopt,aidStms,dobt=1,lsProb=1,lsAll=0,verb=0,warn=1):
    
    dtgopt=yearOpt=None
    istmopt=stmopt
    
    aidstrs=[]
    MF.sTimer('atcf-stmopt-%s'%(stmopt))
    faidstr=''
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    
    ecmstrS=[]
    clpstrS=[]
    humstrS=[]
    modstrS=[]
    
    for tstmid in tstmids:
    
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
        (aidStm,astmids)=aidStms[year]
        utstmid=tstmid.upper()
        
        ecmstr=clpstr=humstr=modstr=''
        
        if(utstmid in astmids):
            aids=aidStm[utstmid]
            if(lsAll and not(lsProb)):
                aidstr=makeAidStr(aids,doall=0)
                print 'tstmid: ',tstmid,'  aids: %s'%(aidstr[0:120])
            else:
                ecmstr=getEcmwfAid(aids,year,verb=verb)
                clpstr=getClipperAid(aids,verb=verb)
                humstr=getHumanAid(aids,verb=verb)
                modstr=getModelAid(aids,verb=verb)
                ecmstrS.append(ecmstr)
                clpstrS.append(clpstr)
                humstrS.append(humstr)
                modstrS.append(modstr)
                
        else:
            
            # -- mislabelling between md2 and md3 :(
            #
            tstmid2=tstmid
            if(isShemBasinStm(tstmid)):
                (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
                if(b1id == 's'):
                    b1id2='p'
                elif(b1id == 'p'):
                    b1id2='s'
                tstmid2=tstmid.replace(b1id,b1id2)
                
                if(lsProb or lsAll): 
                    aidpre='SSS222'
                    
                
            elif(isIOBasinStm(tstmid)):
    
                if(b1id == 'a'):
                    b1id2='b'
                elif(b1id == 'b'):
                    b1id2='a'
                tstmid2=tstmid.replace(b1id,b1id2)
                if(lsProb or lsAll):
                    aidpre='III222'
            
            utstmid2=tstmid2.upper()
            getEcmwfAid
            try:
                aids=aidStm[utstmid2]
            except:
                #if(warn): 
                #    print 'really no trackers for tstmid: ',tstmid
                continue
            
            if(len(aids) == 0):
                if(warn): print 'no aids for tstmid: ',tstmid,'tstmid2: ',tstmid2
                continue
    
            if(lsAll):
                aidstr=makeAidStr(aids)
                print 'tstmid: ',tstmid2,'  %s aids: %s'%(aidpre,aidstr[0:120])
            else:
                ecmstr=getEcmwfAid(aids,year,verb=verb)
                clpstr=getClipperAid(aids,verb=verb)
                humstr=getHumanAid(aids,verb=verb)
                modstr=getModelAid(aids,verb=verb)
                ecmstrS.append(ecmstr)
                clpstrS.append(clpstr)
                humstrS.append(humstr)
                modstrS.append(modstr)
                
    
        if(not(lsAll)):
    
            aidstr="%s,%s,%s,%s"%(ecmstr,clpstr,humstr,modstr)
            aidstr=aidstr.replace(',,',',')
            aidstr=aidstr.replace(',,','')
            if(len(aidstr) > 0):
                if(aidstr[-1] == ','): aidstr=aidstr[0:-1]
            aidstrs.append((tstmid,aidstr))
            if(verb): print 'AAA: ',tstmid,aidstr
            
    if(len(tstmids) > 0):
        
        (necmM,ecmM)=getAidStrMax(ecmstrS)
        (nhumM,humM)=getAidStrMax(humstrS)
        (nclpM,clpM)=getAidStrMax(clpstrS)
        (nmodM,modM)=getAidStrMax(modstrS)
        
            
        faidstr="%s,%s,%s,%s"%(ecmM,clpM,humM,modM)
        faidstr=faidstr.replace(',,',',')
        faidstr=faidstr.replace(',,','')
        if(len(faidstr) > 0):
            if(faidstr[-1] == ','): faidstr=faidstr[0:-1]
    
        if(verb):
            
            print 'EEE',necmM,ecmM
            print 'HHH',nhumM,humM
            print 'CCC',nclpM,clpM
            print 'MMM',nmodM,modM
            print 'FFFFFFFFFFFFFFFff',faidstr
            
                
    return(aidstrs,tstmids,faidstr)
    
    
def parseStatCards(cards,basin,year,statsAll,pstat='pe',override=0):

        
    for card in cards:

        if(mf.find(card,'SSSHHH')):
            tt=card.split()
                
            if(pstat == 'pod'):
                # -- no load
                pod=-99.0
                np=0
                nfc=0

                aid=tt[1]
                tau=int(tt[2])
                var=tt[3]
                spod=tt[4]
                if(spod == '--'):
                    print '-- basin: %s year: %s'%(basin,year),'tt: ',tt
                else:
                    pod=float(spod)
                    np=int(tt[6])
                    try:
                        nfc=int(tt[8])
                    except:
                        print 'pod noload',tt
            else:
                aid=tt[1]
                tau=int(tt[2])
                var=tt[3]
                smean=tt[4]
                if(smean == '--'):
                    mean=-999.0
                else:
                    mean=float(smean)
                np=int(tt[6])
                medn=float(tt[15])
            
            skey=(var,basin,year,aid,tau)
            
            try:
                val=statsAll[skey]
                print 'from pyp: ',skey,'val: ',val
            except:
                if(pstat == 'pod'):
                    val=(pod,np,nfc)
                else:
                    val=(mean,np,medn)
                    
                statsAll[skey]=val
                print 'make skey: ',skey,'val: ',val
                
            if(override):
                statsAll[skey]=val
                print 'override skey: ',skey,'val: ',val
            
def getPvarivars(ptype,pcase,toptitle1):

    doErrBar=0
    do2ndplot=0
    do2ndval=0
    toptitle2=None

    if(ptype == 'pe' or ptype == 'gainxype'):
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxype'): doErrBar=0

    elif(ptype == 'fe' or ptype == 'gainxyfe'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxyfe'): doErrBar=0
        
    elif(ptype == 'te' or ptype == 'gainxyte'):
        pverikey='te'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxyte'): doErrBar=0
        
    elif(ptype == 'pe-line'):
        ptype='pe'
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe-line'):
        ptype='fe'
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe0'):
        ptype='fe'
        pverikey='fe'
        pverikey1='fe0'
        do1stplot=1
        do2ndplot=2
        do2ndval=1
        doErrBar=0
        
    elif(ptype == 'pe-fe'):
        ptype='pe'
        pverikey='pe'
        pverikey1='fe'
        do1stplot=1
        do2ndplot=2
        do2ndval=1
        doErrBar=0

    elif(ptype == 'spe'):
        pverikey='spe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'gainxyvmax'):
        pverikey='vme'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'pbetter'):
        pverikey=ptype
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'vbias'):
        pverikey='vbias'
        pverikey1='vme'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'rmspe'):
        pverikey='pe'
        pverikey1='rmspe'
        do1stplot=1
        do2ndplot=1
        do2ndval=-1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='RMS -- line ; Error = bar'

    elif(ptype == 'nice'):
        pverikey='niceb'
        pverikey1='nice'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pbias'):
        pverikey='pbias'
        pverikey1='pmine'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pod'):
        pverikey='pod'
        pverikey1='over'

        do1stplot=1
        do2ndplot=1
        do2ndval=-1 # have pod 1st in table cells

        toptitle2='Prob Of Detection [POD;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        doErrBar=0

    elif(ptype == 'pod-line'):
        ptype='pod'
        pverikey='pod'
        pverikey1='pod'

        do1stplot=1
        do2ndplot=0

    elif(ptype == 'pof'):
        pverikey='pod'
        pverikey1='over'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Prob Of Forecast [POF;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'

    elif(ptype == 'gainxyvbias'):
        pverikey='vbias'
        pverikey1='vbias'
        do1stplot=0
        do2ndplot=1

        toptitle2='Ratio abs(bias)/mean(abs) Intensity Error [%] :: percentage of Error from bias'

    elif(ptype == 'r34e'):
        pverikey='r34e'
        pverikey1='r34bt'
        do1stplot=1
        do2ndplot=1
        do2ndval=1
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

    rc=(pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,toptitle1,toptitle2)
    return(rc)





def combineSdicts(sAlldicts,otaus,verb=0):
    sdicts=[]
    s0=sAlldicts[otaus[0]]
    s1=sAlldicts[otaus[1]]
    
    if(verb):
        print '0000000000000000000000000000'
        for s in s0:
            print '000',s[0]
            print
            print '111',s[-1]
        print '1111111111111111111111111111111'
        for s in s1:
            print '000',s[0]
            print
            print '111',s[-1]
            
    sdicts.append((s0[0][0],s1[0][0]))
    return (sdicts)

def setDicts(SSMs,models,basins,times,otau,otaus,stype,doAllYears=1,iyear=None,verb=0):
    
    ndicts=[]
    sdicts=[]
    nbasin=len(basins)
        
    for model in models:
        
        dict1={}
        dict2={}
        ndict={}
        
        for time in times:

            oval1s={}
            oval2s={}
            ondicts={}
            
            for basin in basins:

                SSM=SSMs[basin,otau]

                itime=time
                itau=SSM.otau
                if(SSM.otau == 'all'): 
                    itau=int(time)
                    itime=SSM.byear
                    syear=str(time)+'h'
                else:
                    syear=str(time)
                
                if(iyear != None): 
                    itime=iyear
                    itau=str(time)
                    syear=str(time)
                    
                try:        
                    val=SSM.allStats[itime,model,itau,stype]
                except:
                    print 'nojoy',itime,model,itau,stype
                    val=(-999,0)
                    
                oval1s[basin]=val
                oval2s[basin]=val
                        
                if(stype == 'pod'):
                    
                    #dict2[syear]=val
                    oval2s[basin]=val
                    try:        
                        val=SSM.allStats[itime,model,itau,'poo']
                    except:
                        val=(-999,0)
                    
                    oval2s[basin]=val
                    #dict1[syear]=val
                    
                #else:
                    #dict1[syear]=val
                    #dict2[syear]=val
        
        
                if(val[0] != -999):
                    ondicts[basin]=val[1]
                    #ndict[syear]=val[1]
                else:
                    ondicts[basin]=0

            oval1=oval1s[basins[0]]
            oval2=oval2s[basins[0]]
            ondict=ondicts[basins[0]]

            ov1mean=0.0
            ov1n=0
            ov2mean=0.0
            ov2n=0

            for basin in basins:
                ov1=oval1s[basin]
                ov2=oval2s[basin]
                nv1=ov1[-1]
                nv2=ov2[-1]
                
                if(ov1[0] != undef):
                    ov1mean=ov1mean+ov1[0]*nv1
                    ov1n=ov1n+nv1
                
                if(ov2[0] != undef):
                    ov2mean=ov2mean+ov2[0]*nv2
                    ov2n=ov2n+nv2

            if(ov1n > 0):
                ov1mean=ov1mean/ov1n
            else:
                ov1mean=undef

            if(ov2n > 0):
                ov2mean=ov2mean/ov2n
            else:
                ov2mean=undef
                
            if(verb):
                print 'TTTT',itime,itau
                for basin in basins:
                    ov1=oval1s[basin]
                    ov2=oval2s[basin]
                    nv1=ondicts[basin]
                    
                    print 'bbbyyy',itime,itau
                    print 'bbb111',basin,ov1
                    print 'bbb222',basin,ov2
                    print 'bbbnnn',basin,nv1
            
                print 'mmm111',ov1mean,'n: ',ov1n
                print 'mmm222',ov2mean,'n: ',ov2n

            if(nbasin > 1 and ov1mean != undef):
                dict1[syear]=(ov1mean,ov1n)
                ndict[syear]=ov1n
            else:
                dict1[syear]=oval1
                ndict[syear]=ondict
            
            if(nbasin > 1 and ov2mean != undef):
                dict2[syear]=(ov2mean,ov2n)
            else:
                dict2[syear]=oval2
                

        if(stype != 'pod' and doAllYears):

            valalls={}
            for basin in basins:
                SSM=SSMs[basin,otau]
                print 'bbb',basin,otau,stype,SSM.yearStats.keys()
                valalls[basin]=SSM.yearStats[model,itau,stype]
                
            dict1['allyears']=valalls[basins[0]]
            dict2['allyears']=valalls[basins[0]]
            ndict['allyears']=valalls[basins[0]][1]
            
        sdicts.append((dict1,dict2))
        ndicts.append(ndict)
    
    return(sdicts,ndicts)
        



def getVerivars(ptype):

    verivars=[
        ('uuu','mean','uuu')
    ]

    if(ptype == 'pe' or ptype == 'pe-line'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-frac'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-pcnt'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-imp' or ptype == 'pe-imps'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'fe-imp' or ptype == 'fe-imps' or ptype == 'fe-norm'):
        verivars=[
            ('fe','mean','fe'),
        ]

    elif(ptype == 'fe' or ptype == 'fe-line'):
        verivars=[
            ('fe','mean','fe'),
        ]

    elif(ptype == 'fe0'):
        verivars=[
            ('fe0','mean','fe0'),
        ]

    elif(ptype == 'te'):
        verivars=[
            ('te','mean','te'),
        ]

    elif(ptype == 'pe-fe'):
        verivars=[
            ('pe','mean','pe'),
            ('fe','mean','fe'),
        ]

    elif(ptype == 'spe'):
        verivars=[
            ('spe','mean','spe'),
        ]

    elif(ptype == 'rmspe'):
        verivars=[
            ('pe','mean','pe'),
            ('pe','sigma','rmspe'),
        ]

    elif(ptype == 'gainxype'):
        verivars=[
            ('pe','gainxy','pe'),
        ]

    elif(ptype == 'gainxyfe'):
        verivars=[
            ('fe','gainxy','fe'),
        ]

    elif(ptype == 'gainxyte'):
        verivars=[
            ('te','gainxy','te'),
        ]
        
    elif(ptype == 'gainxyfe0'):
        verivars=[
            ('fe,fe0','mean','gainfe0'),
        ]

    elif(ptype == 'pod' or ptype == 'pod-line'):
        verivars=[
            ('pod','mean','pod'),
        ]

    elif(ptype == 'gainxyvmax'):
        verivars=[
            ('vme','gainxyvmax','vme'),
        ]

    elif(ptype == 'vbias'):
        verivars=[
            ('vme','mean','vbias'),
            ('vme','amean','vme'),
            ('fcvmax','mean','fcvm'),
        ]

    elif(ptype == 'nice'):
        verivars=[
            ('nice','amean','nice'),
            ('niceb','mean','niceb'),
        ]

    elif(ptype == 'pbias'):
        verivars=[
            ('pmine','mean','pbias'),
            ('pmine','amean','pmine'),
            ('fcpmin','mean','fcpmin'),
            ('btpmin','mean','btpmin'),
        ]

    elif(ptype == 'gainxyvbias'):
        verivars=[
            ('vme','gainxyvbias','vbias'),
            ('vme','gainxyvbias','vme'),
        ]

    elif(ptype == 'vmxmn'):
        verivars=[
            ('fcvmax','mean','fcvm'),
            ('btvmax','mean','btvm'),
        ]

    elif(ptype == 'r34e'):
        verivars=[
            ('r34e' ,'mean','r34e' ),
            ('r34bt','mean','r34bt'),
            ('r34fc','mean','r34fc'),
        ]   

    elif(ptype[0:2] == 'ls'):
        verivars=[
            ('pe','mean','pe'),
            ('cte','mean','cte'),
            ('ate','mean','ate'),
            ('btlat','mean','btlat'),
            ('btlon','mean','btlon'),
            ('btvmax','mean','btvmax'),
            ('tcflags','mean','tcflags'),
            ('vme','mean','vbias'),
            ('vme','amean','vme'),
            ('fcvmax','mean','fcvm'),
            ('pod','mean','pod'),
            ('vflag','mean','vflag'),
            ('bdtg','mean','bdtg'),   # -- get bdtg from VdeckS obj -- mod mfbase.SimpleListStats() to handle strings: val=undef
        ]
        doprint=0

    elif(ptype == 'pbetter'):
        verivars=[
            ('pe',ptype,ptype),
        ]

    return(verivars)



class SumStatMultiYear(MFbase):
    
    tausSR=[12,24]
    tausMR=[36,48]
    tausLR=[72,96,120]
    
    undef=-999.
    
    def __init__(self,byear,eyear,basin,setOpt,
                 baseModels,veriOpt,phrOpt,
                 veriStat,veriStatRead,
                 otau,pfilt,
                 veriLabel=None,
                 verirule='std',
                 verb=0,
                 ):

        self.byear=byear
        self.eyear=eyear
        self.years=range(byear,eyear+1)
        self.basin=basin
        self.setOpt=setOpt
        self.baseModels=baseModels
        self.verb=verb
        
        className=self.__class__.__name__
        
        if(verirule == 'std'):
            vlab1='all'
            if(pfilt != ''):
                vlab1=pfilt
                
        elif(verirule == 'ts'): 
            vlab1='all-ts'
        else:
            print 'EEE invalid verirun in SumStatMultiYear: ',verirule
            sys.exit()
            
        if( not((phrOpt == '') or (phrOpt == 0)) ):
            print 'EEE invalid phrOpt in SumStatMultiYear: ',phrOpt


        if(veriLabel == None):
            
            if(veriOpt == '-H'):
                vlab2='hetero'
        
            if(veriOpt == ''):
                vlab2='homo'

            veriLabel='%s-%s'%(vlab1,vlab2)
            
        else:
            # -- forced override of veriLabel
            #
            print 'WWW--forced override of veriLabel: %s in %s'%(veriLabel,className)
            
                
        if(phrOpt == '' or phrOpt == '0'):
            models=self.baseModels
        elif(phrOpt == 6):
            models=[]
            for model in self.baseModels:
                model=model+'06'
                models.append(model)
        
        self.phrOpt=phrOpt
        self.veriOpt=veriOpt
        self.veriStat=veriStat
        self.veriStatRead=veriStatRead
        self.veriLabel=veriLabel
        self.pfilt=pfilt
        self.models=models
        self.verirule=verirule
        self.otau=otau
        
        self.clipModel='clip5'
        self.navyModelG='gnav'
        self.ecmwfModel='tecmt'
        
        self.readStats()
        
        if(len(str(self.otau)) > 1 and str(self.otau)[1] == 'R'):
            if(self.otau == 'SR'): self.makeNetFe(self.tausSR,tauLabel=self.otau)
            if(self.otau == 'MR'): self.makeNetFe(self.tausMR,tauLabel=self.otau)
            if(self.otau == 'LR'): self.makeNetFe(self.tausLR,tauLabel=self.otau)
        
        #if(self.veriStat == 'gainxype' or self.veriStat == 'gainxyfe' or\
            #self.models=self.baseModels
            #self.makeGainxyFe(self.otau)
            
        self.makeYearStats(self.otau)
    
   
   
    def makeSingleYearStats(self,year):
        
        stype=self.veriStatRead
        
        for model in self.models:

            for tau in self.taus:
                try:
                    val=self.allStats[year,model,tau,stype]
                except:
                    val=(self.undef,0)
                    
                val2=val3=val4=val5=val6=self.undef

                if(val[0] != self.undef and len(val) == 2):
                    valR=val[0]
                    cntR=val[1]
                elif(len(val) == 7):
                    valR=val[0]
                    cntR=val[1]
                    valR2=val[2]
                    valR3=val[3]
                    valR4=val[4]
                    valR5=val[5]
                    valR6=val[6]
                                                                                
                self.yearStats[model,tau,stype]=oval
            
        


    def makeYearStats(self,tau):
        
        if(self.veriStat == 'gainxype'):
            stype=self.veriStat
        else:
            stype=self.veriStatRead

        modelMs=self.models
        if(self.veriStat == 'gainxyfe' or self.veriStat == 'gainxype' or self.veriStat == 'gainxyte'): modelMs=self.models[0:-1]
        
        for model in self.models:
            
            valSR=0.0
            cntSR=0
            val2=0.0
            val3=0.0
            val4=0.0
            val5=0.0
            val6=0.0
            val7=0.0
            
            for year in self.years:

                val=(self.undef,0)
                gotest=0
                for modelM in modelMs:
                    
                    try:
                        valM=self.allStats[year,modelM,tau,stype]
                    except:
                        valM=None
                
                    gotest=(valM == None or (valM != None and valM[0] == self.undef))        
                    if(gotest): break
                
                if(gotest): continue
                
                try:
                    val=self.allStats[year,model,tau,stype]
                except:
                    val=(self.undef,0)

                if(val[0] != self.undef and len(val) == 2):
                    valR=val[0]
                    cntR=val[1]
                    valSR=valSR+valR*cntR
                    cntSR=cntSR+cntR

                elif(len(val) == 8):
                    valR=val[0]
                    cntR=val[1]
                    valSR=valSR+valR*cntR
                    
                    valR2=val[2]
                    valR3=val[3]
                    valR4=val[4]
                    valR5=val[5]
                    valR6=val[6]
                    valR7=val[7]
                                                                            
                    val2=val2+valR2*cntR
                    val3=val3+valR3*cntR
                    val4=val4+valR4*cntR
                    val5=val5+valR5*cntR
                    val6=val6+valR6*cntR
                    val7=val7+valR7*cntR
                    
                    cntSR=cntSR+cntR
                    

            if(cntSR == 0 and len(val) == 2):
                valSR=self.undef
                oval=(valSR,cntSR)
                
            elif(cntSR == 0 and len(val) == 8):
                valSR=self.undef
                oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)
                
            elif(len(val) == 2):
                valSR=valSR/float(cntSR)
                oval=(valSR,cntSR)

            elif(len(val) == 8):
                valSR=valSR/float(cntSR)
                val2=val2/float(cntSR)
                val3=val3/float(cntSR)
                val4=val4/float(cntSR)
                val5=val5/float(cntSR)
                val6=val6/float(cntSR)
                val7=val7/float(cntSR)
                oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)

            self.yearStats[model,tau,stype]=oval
    
        
        
    
    def makeNetFe(self,tausSR,tauLabel='SR'):
        

        def doNetFe(tausSR,stype,tauLabel):
            
            for model in self.models:
                for year in self.years:
                    valSR=0.0
                    cntSR=0
                    val2=0.0
                    val3=0.0
                    val4=0.0
                    val5=0.0
                    val6=0.0
                    val7=0.0
                    
                    for tau in tausSR:
                        try:
                            val=self.allStats[year,model,tau,stype]
                        except:
                            val=(self.undef,0)
        
                        if(val[0] != self.undef and len(val) == 2):
                            valR=val[0]
                            cntR=val[1]
                            valSR=valSR+valR*cntR
                            cntSR=cntSR+cntR
                        elif(len(val) == 8):
                            valR=val[0]
                            cntR=val[1]
                            valSR=valSR+valR*cntR
                            
                            valR2=val[2]
                            valR3=val[3]
                            valR4=val[4]
                            valR5=val[5]
                            valR6=val[6]
                            valR7=val[7]
                                                                                    
                            val2=val2+valR2*cntR
                            val3=val3+valR3*cntR
                            val4=val4+valR4*cntR
                            val5=val5+valR5*cntR
                            val6=val6+valR6*cntR
                            val7=val7+valR7*cntR
                            
                            cntSR=cntSR+cntR
                            
        
                    if(cntSR == 0 and len(val) == 2):
                        valSR=self.undef
                        oval=(valSR,cntSR)
                        
                    elif(cntSR == 0 and len(val) == 7):
                        valSR=self.undef
                        oval=(valSR,cntSR,val2,val3,val4,val5,val6)
                        
                    elif(len(val) == 2):
                        valSR=valSR/float(cntSR)
                        oval=(valSR,cntSR)

                    elif(len(val) == 7):
                        valSR=valSR/float(cntSR)
                        val2=val2/float(cntSR)
                        val3=val3/float(cntSR)
                        val4=val4/float(cntSR)
                        val5=val5/float(cntSR)
                        val6=val6/float(cntSR)
                        val7=val7/float(cntSR)
                        oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)
        
                    self.allStats[year,model,tauLabel,stype]=oval
            
            

        stype=self.veriStatRead
        
        if(stype == 'pod'):
            doNetFe(tausSR,stype,tauLabel)
            doNetFe(tausSR,'poo',tauLabel)
        else:
            doNetFe(tausSR,stype,tauLabel)
            
    def makeGainxyFe(self,tau):
    
        tauLabel="%s-gainxyfe"%(str(tau))
    
        fixmodel=self.models[-1]
        for model in self.models[0:-1]:
            for year in self.years:
                valSR=0.0
                cntSR=0
                try:
                    val=self.allStats[year,model,tau,self.veriStatRead]
                except:
                    val=(self.undef,0)
                try:
                    valF=self.allStats[year,fixmodel,tau,self.veriStatRead]
                except:
                    valF=(self.undef,0)
    
                if(val[0] != self.undef and valF[0] != self.undef):
                    gainxy=((valF[0]-val[0])/valF[0])*100.0
                else:
                    gainxy=self.undef
                self.allStats[year,model,tauLabel,self.veriStatRead]=(gainxy,val[1])
                self.otauStats[year,model,tauLabel]=(gainxy,val[1])
                
        self.otau=tauLabel
    
    
    def readStats(self,doZip=0):
        
        self.allStats={}
        self.yearStats={}
        self.otauStats={}
        
        vdsdir='./vd2out'
        
        taus=[]
        veriread=self.veriStat
        if(self.veriStat == 'pe-line'):
            veriread=self.veriStatRead
        
        
        for year in self.years:
            
            cyear=str(year)

            ifile="%s/vd2out-%s.%s-%s-%s.txt"%(vdsdir,self.basin,cyear,veriread,self.veriLabel)
            print 'iii',ifile
            try:
                cards=open(ifile).readlines()
            except:
                cards=[]
                    
                
            
            #allstats[taid,tau,verikey]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
            #SSSSSHHHHH               hwrf   0         pe        11.0 n: 294    m,a,s,mn,p25,med,p75,p90,mx:   11.0   11.0   15.9  Dist:    0.0    0.0  MD:    6.0   13.3   26.2  132.3
            #'SSSSSHHHHH', 'hwrf', '0', 'pe', '11.0', 'n:', '294', 'm,a,s,mn,p25,med,p75,p90,mx:', '11.0', '11.0', '15.9', 'Dist:', '0.0', '0.0', 'MD:', '6.0', '13.3', '26.2', '132.3']

            if(len(cards) == 0):
                ostat=(-999.,0)
                tau=self.otau
                for model in self.models:
                    stype=veriread
                    self.allStats[year,model,tau,stype]=ostat
            else:
                
                for card in cards:
                    
                    if(mf.find(card,'nada')):continue
                    if(not(mf.find(card,'SSHH'))): continue
                        
                    tt=card.split()
                    if(self.verb): print 'card:',tt
                    n=1
                    model=tt[n]        ; n=n+1
                    tau=int(tt[n])     ; n=n+1  ; taus.append(tau)
                    stype=tt[n]        ; n=n+1
                    stat=float(tt[n])  ; n=n+2
                    ncounts=int(tt[n])

                    if(len(tt) == 9):
                        n=n+2
                        nfc=int(tt[n])
                        
                    # -- relabel models
                    
                    if(self.veriStat == 'gainxype' and stype == 'pe'): stype=self.veriStat
                    #print 'sss',veriread,stype,stat,model,cyear,len(tt)
                        
                    #
                    if(mf.find(model,'tecm')): model=self.ecmwfModel
                    if( (self.basin == 'l' or self.basin == 'e') and model == 'clp5'): model=self.clipModel
                    if( self.basin == 'w' and model == 'c120'):                        model=self.clipModel
                    if(model == 'ngps' or model == 'nvgm'):                            model=self.navyModelG
                    
                    # -- full stat record
                    
                    if(len(tt) >= 19):
                        n=n+2
                        mean=float(tt[n])    ; n=n+1
                        amean=float(tt[n])   ; n=n+1
                        sigma=float(tt[n])   ; n=n+2
                        minv=float(tt[n])    ; n=n+1
                        ptl25=float(tt[n])   ; n=n+2
                        median=float(tt[n])  ; n=n+1
                        ptl75=float(tt[n])   ; n=n+1
                        ptl90=float(tt[n])   ; n=n+1
                        maxv=float(tt[n])    ; n=n+1
                        
                        ostat=(stat,ncounts,minv,ptl25,median,ptl75,ptl90,maxv)
                        print 'oo--ss',year,model,tau,stype,ostat
                        self.allStats[year,model,tau,stype]=ostat
                        
                    else:
                        if(tau == self.otau and stype == self.veriStatRead):
                            print 'ss-oo-pod',year,model,tau,stype,stat,ncounts,nfc
                        ostat=(stat,ncounts)
                        self.allStats[year,model,tau,stype]=ostat
        
        taus=mf.uniq(taus)
        self.taus=taus
        



 
class SumStatsPlot(MFbase):


    def __init__(self,models,vstmids,
                 pcase,
                 ptype,
                 doland=1,
                 pdir='/tmp',
                 doMetric=0,
                 ):

        # -- 20190905 -- handle pcase with a directory
        #
        (ppdir,pfile)=os.path.split(pcase)
        
        if(len(ppdir) > 0): 
            pdir=ppdir
            pname="%s.%s"%(ptype,pfile)
        else:
            pname='%s.%s'%(ptype,pcase)
            
        self.models=models
        self.vstmids=vstmids
        self.pcase=pcase
        self.ptype=ptype
        self.doMetric=doMetric
        
        if(doland == 0):
            pname="%s-noland"%(pname)
            
        self.ppaths=[
            '%s/%s.png'%(pdir,pname),
            '%s/%s.eps'%(pdir,pname),
            '%s/%s.txt'%(pdir,pname),
            ]


        self.pvartagopt=None


    def reducestmids(self,stmids,filter9x=1):

        ostmids=[]
        for stmid in stmids:
            tt=stmid.split('.')
            stm3id=tt[0]
            stmnum=int(stm3id[0:2])
            if(filter9x and stmnum >= 90): continue
            stmyear=tt[1]
            ostmid="%s.%s"%(stm3id,stmyear[2:4])
            ostmids.append(ostmid)
            
        return(ostmids)


    def setPlottitles(self,
                      toptitle1=None,
                      toptitle2=None,
                      taus=None,
                      xlab=None,
                      ):

        models=self.models

        #
        # main title
        #
        if(toptitle1 == None):
            t1='please add using -1 command line option....'
        else:
            t1=toptitle1

        if(toptitle2 != None):
            t1=t1+'\n'+toptitle2


        #
        # subtitle
        #


        lmodel=models[-1]
        if(hasattr(self,'vstmids')):
            if(len(self.vstmids) > 0):
                ovstmids=self.reducestmids(self.vstmids)
            else:
                ovstmids=[]
        else:
            ovstmids=[]

        if(mf.find(self.ptype,'gainxype')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'
            
        if(mf.find(self.ptype,'gainxyte')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
                t2a=t2a+'\n'
                
        if(self.ptype == 'gainxyfe'):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
                t2a=t2a+'\n'
                
        if(self.ptype == 'gainxyfe0'):
            t2a="Gain [%%] FE(IE=0) Relative FE"

                    
        if(mf.find(self.ptype,'pbetter')):
            t2a="%% cases better Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            if(len(taus) == 1):
                t2a="%s tau= %s"%(t2a,taus[0])
            t2a=t2a+'\n'

        elif(mf.find(self.ptype,'gainxyvmax')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'

        elif(mf.find(self.ptype,'gainxyvbias')):
            t2a='Ratio of bias/mean(abs) [%]'
            for model in models[0:]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'

        else:
            t2a='Models: '
            for model in models:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'
            

        ns=len(ovstmids)
        nsmax=18
        if(ns > 0):
            t2b="Storms[N] [%d]: "%(ns)
        else:
            t2b=''

        if(ns > nsmax):
            n1b=0
            n1e=nsmax/2
            n2b=ns-nsmax/2
            n2e=ns

            for n in range(n1b,n1e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

            t2b="%s ..."%(t2b)

            for n in range(n2b,n2e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

        else:
            for n in range(0,ns):
                ovstmid=ovstmids[n]
                if(n%20 == 0 and n != 0): t2b=t2b+'\n'
                t2b="%s %s"%(t2b,ovstmid)


        if(self.ptype == 'pbetter'):
            t2=t2a+t2b
        else:
            t2=t2b

        if(self.ptype == 'pe' or self.ptype == 'pe-line'):
            ylab='PE [nm]'
            if(self.doMetric): ylab='PE [km]'

        if(self.ptype == 'pe-frac'):
            ylab='% PE '
            
        if(self.ptype == 'pe-pcnt'):
            ylab='% cases '

        if(self.ptype == 'pe-imp'):
            ylab='% PE Improve over Mean '
            
        if(self.ptype == 'pe-imps'):
            ylab='% PE Improve over Mean - Scaled by N '

        if(self.ptype == 'fe-imp'):
            ylab='% FE Improve over Mean '
            
        if(self.ptype == 'fe-imps'):
            ylab='% FE Improve over Mean - Scaled by N '

        if(self.ptype == 'fe' or self.ptype == 'fe-line'):
            ylab='FE [TJ]'
            if(self.doMetric): ylab='FE [TJ]'
        
        if(self.ptype == 'fe-norm'):
            ylab='FE normalized to [nmi]'
            if(self.doMetric): ylab='FE normalized to [nmi]'

        if(self.ptype == 'fe0'):
            ylab='FE0 [TJ]'
            if(self.doMetric): ylab='FE0 [TJ]'
        
        if(self.ptype == 'te'):
            ylab='TE [nm]'
            if(self.doMetric): ylab='TE [km]'
        
            
        if(self.ptype == 'pe-fe'):
            ylab='PE [nmi] FE [TJ]'
            if(self.doMetric): ylab='PE [km] FE [TJ]'

        if(self.ptype == 'spe'):
            ylab='PE scaled by length of track [%]'

        if(self.ptype == 'rmspe'):
            ylab='RMS PE [nm]'
            if(self.doMetric): ylab='RMS PE [km]'

        elif(self.ptype == 'vme'):
            ylab='VmaxE [kt]'
            if(self.doMetric): ylab='VmaxE [m/s]'

        elif(self.ptype == 'vbias'):
            ylab='Vmax MeanE(Bias)/AbsMeanE [kt]'
            if(self.doMetric): ylab='Vmax MeanE(Bias)/AbsMeanE [m/s]'

        elif(self.ptype == 'nice'):
            ylab='NICK MeanE(Bias)/AbsMeanE [kt]'
            if(self.doMetric): ylab='NICK MeanE(Bias)/AbsMeanE [m/s]'

        elif(self.ptype == 'pbias'):
            ylab='Pmin(Bias) [mb]'

        elif(self.ptype == 'pod-line'):
            ylab='POD (line) [%]'

        elif(self.ptype == 'pod'):
            ylab='POD (bar) ; POO (line) [%]'
            ylab='PoD (line) [%]'

        elif(self.ptype == 'pof'):
            ylab='POF (bar) ; POO (line) [%]'

        elif(self.ptype == 'gainxype'):
            ylab='Gain PE [%]'

        elif(self.ptype == 'gainxyte'):
            ylab='Gain TE [%]'

        elif(self.ptype == 'gainxyfe'):
            ylab='Gain FE [%]'

        elif(self.ptype == 'gainxyfe0'):
            ylab='Gain  [%]'

        elif(self.ptype == 'gainxyte'):
            ylab='Gain  [%]'


        elif(self.ptype == 'pbetter'):
            ylab='% better'
            if(len(taus) == 1):
                ylab="%s tau=%d"%(ylab,taus[0])

        elif(self.ptype == 'gainxyvmax'):
            ylab='Gain VmaxError [%]'

        elif(self.ptype == 'gainxyvbias'):
            ylab='Ratio abs(bias)/mean(abs) [%]'

        elif(self.ptype == 'ct-ate'):
            ylab='CT (track) bias [nm; line]; AT (speed) bias [nm; bar]'
            if(self.doMetric): ylab='CT (track) bias [km; line]; AT (speed) bias [km; bar]'
            
        elif(self.ptype == 'at-cte'):
            ylab='AT (speed) bias [nm; line]; CT (track) bias [nm; bar]'
            if(self.doMetric): ylab='AT (speed bias) [km; line]; CT (speed) bias [km; bar]'

        elif(self.ptype == 'r34e'):
            ylab='R34 fractional area error [%]'

        self.ptitles=(t1,t2,ylab)
        self.xlab=xlab




    def renamemodel(self,ol):

        rol='XXXX'

        if(ol == 'gfsn'): rol='GFS'
        if(ol == 'ecmo'): rol='ECMWF'
        if(ol == 'ukmo'): rol='UKMO'
        if(ol == 'ecmo'): rol='ECMWF'
        if(ol == 'ngps'): rol='NOGAPS'
        if(ol == 'gfdl'): rol='GFDL'
        if(ol == 'ofcl'): rol='OFCL'
        if(ol == 'bcon'): rol='BCON'
        if(ol == 'clip'): rol='CLIPER'
        if(ol == 'egrr'): rol='UKMO'

        return(rol)


    def isundef(self,val,undef=None):

        if(val == None):
            return(1)

        if(undef != None):
            undefs=[undef]
        else:
            undefs=[-999.,999.]
        rc=0
        for undef in undefs:
            if(val == undef): rc=1
        return(rc)


    def iszero(self,val):
        rc=0
        if(fabs(val) == 0): rc=1
        return(rc)


    def smooth(self,x,window_len=10,window='hanning'):
        """smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal 
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.

        input:
            x: the input signal 
            window_len: the dimension of the smoothing window
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.

        output:
            the smoothed signal

        example:

        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

        see also: 

        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter

        TODO: the window parameter could be the window itself if an array instead of a string   
        """

        import numpy

        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."

        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."


        if window_len<3:
            return x


        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


        s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w=numpy.ones(window_len,'d')
        else:
            w=eval('numpy.'+window+'(window_len)')

        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len-1:-window_len+1]



    def setControls(self,controlsVar=None):
        
        if(self.ptype == 'pe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'pe-line'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,300.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'fe-line'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,200.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'pe-frac'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-pcnt'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-imp'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'pe-imps'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-imp'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'fe-imps'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-norm'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'fe'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'te'):
            ptype1='te'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,1000.0,100],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'fe0'):
            ptype1='fe0'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'pe-fe'):
            ptype1='pe'
            ptype2='fe'
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)
            
        elif(self.ptype == 'spe'):
            ptype1='spe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,110.0,10],lgndloc)

        elif(self.ptype == 'rmspe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)

        elif(self.ptype == 'vme'):
            ptype1='amvme'
            ptype2='mvme'
            lgndloc=0
            controls=([-50.0,50.0,10.0],lgndloc)

        elif(self.ptype == 'vbias'):
            ptype1='mvme'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)
            if(self.doMetric): controls=([-25.0,35.0,10.0],lgndloc)

        elif(self.ptype == 'nice'):
            ptype1='nice'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pbias'):
            ptype1='pmin'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pod'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)
            
        elif(self.ptype == 'pod-line'):
            ptype1='pods'
            ptype2='pods'
            lgndloc=2
            controls=([0.0,125.0,25],lgndloc)
        

        elif(self.ptype == 'pof'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)

        elif(self.ptype == 'gainxype'):
            ptype1='gainxype'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)

        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe0'):
            ptype1='gainxyfe0'
            ptype2=ptype1
            lgndloc=0
            controls=([-10.0,30.0,5.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
            
        elif(self.ptype == 'pbetter'):
            ptype1=self.ptype
            ptype2=ptype1
            lgndloc=0
            controls=([0.0,110.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvmax'):
            ptype1='gainxyvmax'
            ptype2=ptype1
            lgndloc=2
            controls=([-70.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvbias'):
            ptype1='gainxyvbias'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,120.0,10.0],lgndloc)

        elif(self.ptype == 'ct-ate'):
            ptype1='mcte'
            ptype2='mate'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'at-cte'):
            ptype1='mate'
            ptype2='mcte'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'r34e'):
            ptype1='r34e'
            ptype2='r34bt'
            lgndloc=0
            controls=([-200.0,200.0,25.0],lgndloc)

        else:
            print 'EEE invalid plot ptype in PlotsumStat: ',self.ptype
            sys.exit()

        if(controlsVar != None): controls=controlsVar
        self.controls=controls

    def setbarlineprops(self,n,np,pvartagopt=None):

        lstyle='-'
        wline=2.0

        if(pvartagopt == '00_12zv06_18z'):
            if(n%2 == 0):
                alphabar=alphaline=0.75
                lstyle='-'
            else:
                alphabar=alphaline=1.0
                lstyle=':'

        if(np >= 4):
            if(n%2 == 0):
                alphabar=alphaline=0.5
                lstyle=':'
            else:
                alphabar=alphaline=1.0
                lstyle='-'

        if(np == 4 and pvartagopt == '00_06_12_18z'):
            if(n == 3):
                alphabar=alphaline=0.25
                lstyle='-'
            elif(n == 2):
                alphabar=alphaline=0.5
                lstyle=':'
            elif(n == 1):
                alphabar=alphaline=0.75
                lstyle='-'
            elif(n == 0):
                alphabar=alphaline=1.0
                lstyle=':'

        if(pvartagopt == '00_12z'):
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphabar=0.5
                alphaline=1.0
                lstyle=':'

        else:
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphaline=1.0
                alphabar=1.0
                alphabar=0.85
                lstyle=':'
                lstyle='-'
                lstyle='--'


        return(lstyle,wline,alphabar,alphaline)


    def simpleplot2axis(self,
                        models,
                        dicts,
                        cnts,
                        labels,
                        irowc=None,
                        irowt=None,
                        irowl=None,
                        irowll=None,
                        do1stplot=1,
                        do2ndplot=0,
                        doBarplot=0,
                        ilstyle=None,
                        ilwidth=None,
                        ilmarker=None,
                        ialphaline=None,
                        ialphabar=None,
                        reversedirection=0,
                        dopng=0,doeps=0,doxv=0,dopdf=0,
                        useroverride=0,
                        doshow=0,
                        verb=0,
                        dotable=1,
                        countonly=0,
                        docp=0,
                        domodelrename=0,
                        do2ndval=0,
                        doline=0,
                        doErrBar=1,
                        undef=-999,
                        maxcounts=2000,
                        dosmooth=0,
                        ):
        
        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()

        from numpy import array
        import matplotlib.lines as mlines
        
        self.do2ndval=do2ndval
        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        from pylab import array,arange
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        from natsort import natsorted
        import matplotlib.patches as mpatch

        C2hex=w2Colors().chex

        # setup input
        #

        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        cnts0=cnts[0]
        cnts1=cnts[1]

        taus=cnts0.keys()
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)
        

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0'):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1


        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        xaxisTs=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts0
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]
            xaxisT=[]

            nxpts=nts
            #if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]
                if(verb): print 'nnn',nt,tau,val1,val2

                if(len(dict1[tau]) > 2):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=''
                    cval1=''
                else:
                    row1.append(val1)
                    xval1=0.5+(nt-1)
                    xaxis.append(xval1)
                    xaxisT.append(int(tau))

                if(self.isundef(val2) or nc == 0):
                    val2=''
                    cval2=''
                else:
                    row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            if(n == 0):
                vals1.append(row1)
                print '1111----',n,vals1
            elif(n == 1):
                vals2.append(row2)
                print '2222----',n,vals2
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)
            xaxisTs.append(xaxisT)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        xydim=(10.5,8.25)
        fig, ax = plt.subplots(figsize = xydim)
        
        mpl.rcParams.update(params)
        ax2 = ax.twinx()
        
        lgndc=[]

        xtaus0=[]
        xtaus1=[]
        ycnts0=[]
        ycnts1=[]
        ycnts=[]
        
        if(doBarplot): np=np+1

        for tau in taus:
            if(mf.find(tau,'all')):  
                continue
            else:                    
                itau=int(tau)
                ycnt0=cnts0[tau]
                ycnt1=cnts1[tau]
                ycnts0.append(ycnt0)
                ycnts1.append(ycnt1)
                xtaus0.append(itau)
                xtaus1.append(itau)

        if(verb):
            print 'XXXTTT--0000',n,xtaus0
            print 'CCCCCC--0000',n,ycnts0
            print 'XXXTTT--1111',n,xtaus1
            print 'CCCCCC--1111',n,ycnts1

        # -- !!!!!! force two plots !!!!!!!!!!!!!!!!!!!
        #
        np=2

        # -- first plot the two time series
        #
        for n in range(0,np):

            if(n == 0): ys=vals1[n]
            elif(n == 1): ys=vals2[0]
            xaxisT=copy.copy(xaxisTs[0])
            xaxisT=copy.copy(xtaus0)
            
            if(verb):
                print 'xxxx',n,xaxisT
                print 'yyyy',n,ys
                 
            nxy=n
            rc=ax.plot(xaxisT,ys,
                       color=rowc[nxy],
                       linestyle=lstyle[nxy],
                       marker=lmarker[nxy],
                       linewidth=lwidth[nxy],
                       alpha=alphaline[nxy]
                       )

        if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or self.ptype == 'pod-line'):
            ax.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)
            

        # -- now do the smoothed time series if dosmooth=1
        #
        for n in range(0,np):

            if(n == 0): ys=vals1[n]
            elif(n == 1): ys=vals2[0]
            xaxisT=copy.copy(xtaus0)
            
            if(verb):
                print 'xxxx',n,xaxisT
                print 'yyyy',n,ys
                 
            
            if(dosmooth):
                ys=array(ys)
                yss=smooth(ys,window_len=7)
                rc=ax.plot(xaxisT,yss,
                           #color='black',
                           color=rowc[n],
                           linestyle='-',
                           marker='',
                           linewidth=lwidth[n],
                           alpha=1.0
                           )
                
        # -- now the count bars
        #
        rc=ax2.bar(xtaus0,ycnts0,
                   width=0.9,
                   color=rowc[0],
                   alpha=0.7,
                   #color='grey',
                   )
        
        rc=ax2.bar(xtaus0,ycnts1,
                   width=0.5,
                   color=rowc[1],
                   alpha=0.9,
                   #color='black',
                   )
        
        ax2.set_ylabel('N',fontsize=15)
        ax2.set_ylim(0,maxcounts)
        if(maxcounts <= 2000):
            ax2.set_yticks([0,50,100,200])
        else:
            ax2.set_yticks([0,250,500])
            
            
        
        ax2.grid()
        

        # -- set the xticks
        #
        xtbeg=xtaus0[0]
        xtend=xtaus0[-1]
        nxpts=len(xtaus0)

        if(nxpts >= 40):
            xtinc=5
        elif(nxpts >=30 and nxpts < 40):
            xtinc=4
        elif(nxpts >= 20 and nxpts < 30):
            xtinc=3
        elif(nxpts >= 10 and nxpts < 20):
            xtinc=2
        elif(nxpts < 10):
            xtinc=1

        xts=arange(xtbeg,xtend,xtinc)
        
        ax.set_xlim(xtaus0[0]-0.7,xtaus0[-1]+0.7)
        ax.set_xticks(xts)
        ax.set_ylim(yb,ye)
        ax.set_yticks(yts)

        fig.suptitle(t1,fontsize=13)
        ax.set_title(t2,size=8)

        ax.set_ylabel(ylab,fontsize=15)
        if(xlab != None): ax.set_xlabel(xlab,fontsize=15)
        
        
        ax.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            fig.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            fig.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)

    # -- plot method
    #

    def cformatVal(self,val1,val2,nc,diffv1v2=0,countonly=0):

        cval1=''
        if(val1 == None):
            return(cval1)
        
        if(val1 != ''):
            if(countonly):
                cval1="%d"%(nc)
            else:
                cval1="%4.0f[%d]"%(val1,nc)
                
        if(val1 != '' and val2 != '' and self.do2ndval != 0):
            if(countonly):
                cval1="%d"%(nc)
            else:
                if(self.do2ndval == -1):
                    cval1="%4.0f;%4.0f[%d]"%(val2,val1,nc)
                else:
                    cval1="%4.0f;%4.0f[%d]"%(val1,val2,nc)

        return(cval1)
    
    
    def setSumStatsPlotVals(self,nrows,dicts,cnts,labels):
        
        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts[n]
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]

            nxpts=nts
            
            # -- ????
            #if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]

                if(len(dict1[tau]) > 2):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=None
                    cval1=''
                
                row1.append(val1)
                xval1=0.5+(nt-1)
                xaxis.append(xval1)

                if(self.isundef(val2) or nc == 0):
                    val2=-999.
                    cval2=''
                    
                row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            vals1.append(row1)
            vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        np=len(vals1)

        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar

    

    def simpleplot(self,
                   models,
                   dicts,
                   cnts,
                   labels,
                   irowc=None,
                   irowt=None,
                   irowl=None,
                   irowll=None,
                   do1stplot=1,
                   do2ndplot=0,
                   ilstyle=None,
                   ilwidth=None,
                   ilmarker=None,
                   ialphaline=None,
                   ialphabar=None,
                   reversedirection=0,
                   dopng=0,doeps=0,doxv=0,dopdf=0,
                   useroverride=0,
                   doshow=0,
                   verb=0,
                   dotable=1,
                   countonly=0,
                   docp=0,
                   domodelrename=0,
                   do2ndval=0,
                   doline=0,
                   doErrBar=1,
                   undef=-999,
                   dosmooth=0,  # -- 20240704 used for plotting era5 pe
                   ):

        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()
        
        from numpy import array
        import matplotlib.lines as mlines

        self.do2ndval=do2ndval
        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        
        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        import numpy
        
        from pylab import arange
        import pylab as P
        from natsort import natsorted
        
        import matplotlib.patches as mpatch
        
        # -- moved to w2base.py from VT.py
        #
        C2hex=w2Colors().chex

        # -- setup output
        #
        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        taus=cnts[0]
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0'):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1

        
        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts[n]
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]

            nxpts=nts
            
            # -- ????
            #if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]

                if(len(dict1[tau]) > 2):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=None
                    cval1=''
                
                row1.append(val1)
                xval1=0.5+(nt-1)
                xaxis.append(xval1)

                if(self.isundef(val2) or nc == 0):
                    val2=-999.
                    cval2=''
                    
                row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            vals1.append(row1)
            vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        np=len(vals1)

        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        P.rcParams.update(params)


        xydim=(10.5,8.25)
        F=P.figure(figsize=xydim)

        leftsubplot=0.10
        bottomsubplot=0.15
        if(np > 6):
            bottomsubplot=0.20

        F.subplots_adjust(top=0.9,bottom=bottomsubplot,left=leftsubplot,right=0.95,wspace=0.0,hspace=0.0)

        FP=F.add_subplot(111)

        lgndc=[]

        #
        # setup bars
        #

        dxofffraction=1.0
        dxofffraction=1.25

        barscale=0.8

        if(np == 1):
            dxofffraction=1.0


        barwidth=barscale/np
        pbarwidth=barwidth*dxofffraction
        xshift=(1.0-barscale)*0.5
        boxbarwidth=pbarwidth*0.50
        errbarwidth=boxbarwidth*0.75
        errcapsize=errbarwidth*25

        if(dxofffraction >= 1.5):
            alphabar=0.75

        leghandles=[]

        for n in range(0,np):

            ys=vals1[n]
            ymedian=v1medians[n]
                
            xaxisl=copy.copy(xaxiss[n])
            xaxisb=copy.copy(xaxiss[n])
            if(verb): print 'XXXLLL',n,xaxisl,ys
            
            leghand = mlines.Line2D([], [], color=rowc[n], marker='', ls=lstyle[n], label=olabels[n])
            leghandles.append(leghand)

            if(do1stplot):
                #adjustxaxis(n,xaxisl,barwidth,dxofffraction,center=1)
                rc=FP.plot(xaxisl,ys,
                           color=rowc[n],
                           linestyle=lstyle[n],
                           marker=lmarker[n],
                           linewidth=lwidth[n],
                           alpha=alphaline[n]
                           )

                # -- add smooth

                if(dosmooth):

                    # -- set the mask and make numpy empty array
                    #
                    
                    smoothys=numpy.empty([len(ys)])
                    maskys=[]
                    for i in range(0,len(ys)):
                        y=ys[i]
                        if(y == None):
                            maskys.append(1)
                            smoothys[i]=0.0
                        else:
                            maskys.append(0)
                            smoothys[i]=y

                    # -- make the masked array
                    #
                    nys=numpy.ma.array(smoothys,mask=maskys)

                    # -- smooth
                    #
                    win_len=7
                    if(len(xaxisl) < 7): win_len=4
                    yss=smooth(smoothys,window_len=win_len)
                    
                    # -- set undef points to None
                    #
                    for i in range(0,len(ys)):
                        my=maskys[i]
                        if(my == 1):
                           yss[i]=None
                           
                    # -- do the smooth plot
                    #
                    rc=FP.plot(xaxisl,yss,
                               color=rowc[n],
                               #color='black',
                               linestyle='-',
                               marker='',
                               linewidth=lwidth[n],
                               alpha=1.0
                               )

                if(n == np-1):
                    if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or self.ptype == 'pod-line'):
                        #FP.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)
                        FP.legend(loc=lgndloc,handles=leghandles)
                        

            do2ndplot=0
            if(do2ndplot > 0):

                if(do2ndplot == 2):
                    doline=1

                ys=vals2[n]
                for j in range(0,len(ymedian)):
                    ymedian[j]=v1medians[n][j]

                if(doline):
                    rc=FP.plot(xaxisl,ys,
                               color=rowc[n],
                               linestyle='--',
                               marker=lmarker[n],
                               linewidth=lwidth[n],
                               alpha=1.0
                               )
                    
                else:

                    rcBB=None
                    
                    if(len(ys) != len(xaxisl)): doErrBar=0
                    adjustxaxis(n,xaxisb,barwidth,dxofffraction)
                    
                    if(doErrBar):

                        yBBbot=v2ptl25s[n]
                        yBBtop=v2ptl75s[n]
                        ymax=v2maxs[n]
                        ymin=v2mins[n]
                        ymed=v2medians[n]
                        
                        ysBBrange=[]
                        
                        yBoxMedian=[]
                        
                        yerrMM=[]
                        yerrCenter=[]

                        yboxCenter=[]
                        yboxMM=[]
                        
                        yerrLowCenter=[]
                        yerrLowMM=[]
                        
                        yerrUpCenter=[]
                        yerrUpMM=[]

                        xaxisBB=copy.copy(xaxisb)
                        xaxisEB=copy.copy(xaxisb)
                        xaxisBBrange=[]
                        
                        lenX=len(xaxisBB)
                        for j in range(0,lenX):
                            xBB=xaxisBB[j]
                            x0BB=xBB+(pbarwidth-boxbarwidth)*0.5
                            x1BB=boxbarwidth
                            xaxisBBrange.append((x0BB,x1BB))
                            xaxisEB[j]=xaxisEB[j]+pbarwidth*0.5
                            #print 'xBB',j,xBB,xaxisBBrange[j],xaxisEB[j]
                            
                        lenY=len(row1median)
                        
                        for j in range(0,lenY):
                            
                            if(ymin[j] != undef):
                                
                                y0BB=yBBbot[j]
                                y1BB=yBBtop[j]-yBBbot[j]   
                                
                                if(ymed[j] == -999):
                                    y0BB=undef
                                    y1BB=undef
                                
                                ysBBrange.append((y0BB,y1BB))
    
                                yboxL=y1BB*0.5
                                yboxC=y0BB+yboxL
                                
                                if(ymed[j] == -999):
                                    yboxC=undef
                                    yboxL=undef
                                
                                yboxCenter.append(yboxC)
                                yboxMM.append(yboxL)
                                
                                yerrL=(ymax[j]-ymin[j])*0.5
                                yerrC=ymin[j]+yerrL
                                
                                if(ymed[j] == -999):
                                    yerrC=undef
                                    yerrL=undef
                                
                                yerrCenter.append(yerrC)
                                yerrMM.append(yerrL)
    
                                yerrLowL=(y0BB-ymin[j])*0.5
                                yerrLowC=ymin[j]+yerrLowL

                                if(ymed[j] == -999):
                                    yerrLowC=undef
                                    yerrLowL=undef

                                yerrLowCenter.append(yerrLowC)
                                yerrLowMM.append(yerrLowL)
                                
                                yerrUpL=(ymax[j]-yBBtop[j])*0.5
                                yerrUpC=yBBtop[j]+yerrUpL
                                
                                if(ymed[j] == -999):
                                    yerrUpC=undef
                                    yerrUpL=undef
                                    
                                yerrUpCenter.append(yerrUpC)
                                yerrUpMM.append(yerrUpL)
                                
                                yBoxMedian.append(ymed[j])
                                
                        nBB=len(xaxisBBrange)
                        
                        for j in range(0,nBB):
                            xBBs=[xaxisBBrange[j]]
                            xBBs1=[(xaxisb[j],pbarwidth)]
                            yBB=ysBBrange[j]
                            rcBB=FP.broken_barh(xBBs1,(0,ys[j]),facecolor=rowc[n],alpha=alphabar[n])
                            rcBB2576=FP.broken_barh(xBBs,yBB,alpha=0.5,facecolor=rowc[n],edgecolor='black',linewidth=1.0)

                        #rc=FP.errorbar(xaxisEB,yerrCenter,yerr=yerrMM,linestyle='None',capthick=2,capsize=errcapsize,
                        #               elinewidth=0.5,alpha=0.75,
                        #               ecolor=rowc[n])
                        
                        rcEB=FP.errorbar(xaxisEB,yBoxMedian,xerr=boxbarwidth*0.5,linestyle='None',capthick=0,capsize=errcapsize,
                                       elinewidth=2,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrLowCenter,yerr=yerrLowMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrUpCenter,yerr=yerrUpMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,alpha=0.5,
                                       ecolor='black')

                        #rc=FP.errorbar(xaxisEB,yboxCenter,yerr=yboxMM,linestyle='None',capthick=0,capsize=errcapsize,
                        #               elinewidth=1,alpha=1.0,
                        #               ecolor=rowc[n])
                            
                        
                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
               
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

                    else:

                        rc=FP.bar(xaxisb,ys,
                                  align='edge',
                                  color=rowc[n],
                                  width=pbarwidth,
                                  alpha=alphabar[n])

                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
                        
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

        # -- table
        #
        if(dotable):

            if(verb):
                print 'rowl: ',rowl
                print 'rowc: ',rowc
                for  i in range(0,len(cvals)):
                    print 'cvals',i,cvals[i]

            TT=P.table(cellText=cvals,loc='bottom',
                       cellLoc='center',
                       rowLabels=rowll,rowColours=rowt,
                       colLabels=ctaus)

            TT.set_fontsize(8)

            P.xticks(xaxis,ctausblank)


        # -- lineplot labels
        else:

            xaxisp=[]
            ctausp=[]
            
            nxpts=len(xaxis)
            if(nxpts >= 40):
                xtinc=5
            elif(nxpts >=30 and nxpts < 40):
                xtinc=4
            elif(nxpts >= 20 and nxpts < 30):
                xtinc=3
            elif(nxpts >= 10 and nxpts < 20):
                xtinc=2
            elif(nxpts < 10):
                xtinc=1

            for i in range(0,nxpts,xtinc):
                xaxisp.append(xaxis[i])
                
                # -- the last point is 'allyears' set to penultimate point
                #
                #if(i == nxpts-1):
                #    i=nxpts-2
                ctausp.append(ctaus[i])
                
            P.xticks(xaxisp,ctausp)

        if(self.ptype == 'vme' or self.ptype == 'ct-ate' or self.ptype == 'at-cte' or \
           self.ptype == 'vbias' or self.ptype == 'pbias' or mf.find(self.ptype,'gainxy')):
            draw0line(lcol='k')

        if(self.ptype == 'pod' or self.ptype == 'pof'):
            drawCritline(100.0,lcol='k')

        elif(self.ptype == 'pbetter'):
            drawCritline(50.0,lcol='k')

        elif(self.ptype == 'pod-line'):
            None
            #drawCritline(100.0,lcol='k')
            #drawCritline(95.0,lcol='k')


        #P.xlim(-1.0,len(taus)-1)
        P.xlim(-1.0,nxpts-1)
        P.ylim(yb,ye)
        P.yticks(yts)

        P.suptitle(t1,fontsize=13)
        P.title(t2,size=8)

        P.ylabel(ylab,fontsize=15)
        if(xlab != None): P.xlabel(xlab,fontsize=15)

        P.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            P.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            P.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            P.savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)

    #



class SumStats(MFutils):

    def __init__(self,
                 taids,
                 tstmids,
                 verivars,
                 ostats,
                 cases,
                 casedtgs,
                 ):


        self.taids=taids
        self.tstmids=tstmids
        self.verivars=verivars
        self.ostats=ostats
        self.cases=cases
        self.casedtgs=casedtgs

        self.initStorms()
        self.initAidStorms()


    def initStorms(self):

        vstmids=[]
        vdtgs=[]
        vvmaxs=[]
        kk=self.cases.keys()
        
        for k in kk:
            vstmids.append(self.cases[k][0])
            vdtgs.append(self.cases[k][1])
            vvmaxs.append(self.cases[k][2])

        self.vstmids=self.uniq(vstmids)
        self.vdtgs=self.uniq(vdtgs)
        self.vvmaxs=self.uniq(vvmaxs)

        
    def initAidStorms(self,verb=0):
        
        models=[]
        labaids=[]
        colaids=[]
        markaids=[]
        
        for taid in self.taids:
            ap=AidProp(taid)
            labaids.append(ap.label)
            colaids.append(ap.color)
            models.append(ap.oname)
            markaids.append(ap.mark)

        self.models=models
        self.labaids=labaids
        self.colaids=colaids
        self.markaids=markaids

        if(not(hasattr(self,'verivars'))): return

            
        # force specific marker for intensity plots
        #
        for n in range(0,len(markaids)):
            markaid=markaids[n]
            if(verb): print 'III(initAidStorms) ',self.verivars[0],markaid
            if(self.verivars[0] == 'vbias' and markaid != 'd'):
                markaid=markaid
            else:
                markaid='+'

            markaids[n]=markaid

        if(verb): print 'III(initAidSTorms) final markaids: ',markaids




def getFstmids4Tstmids(tstmids,aidStms,verb=0):

    fstmids=[]
    for tstmid in tstmids:
        
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
        (aidStm,astmids)=aidStms[year]
        
        utstmid=tstmid.upper()
        gotmd2=gotmd3=0
    
        aids=[]
        if(utstmid in astmids):
            aids=aidStm[utstmid]
            aidstr=makeAidStr(aids,doall=0)
            if(verb): print 'tstmid: ',tstmid,'  aids: %s'%(aidstr[0:120])        
            fstmid=tstmid
            gotmd3=1
            
        if(not(gotmd3)):

            # -- mislabelling between md2 and md3 :(
            #
            tstmid2=tstmid
            gotsh=0
            gotio=0
            
            if(isShemBasinStm(tstmid)):
                (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
                if(b1id == 's'):
                    b1id2='p'
                elif(b1id == 'p'):
                    b1id2='s'
                tstmid2=tstmid.replace(b1id,b1id2)
                gotsh=1
        
            elif(isIOBasinStm(tstmid)):
        
                if(b1id == 'a'):
                    b1id2='b'
                elif(b1id == 'b'):
                    b1id2='a'
                tstmid2=tstmid.replace(b1id,b1id2)
                gotio=1
        
            utstmid2=tstmid2.upper()
            
            aidpre=''
            try:
                aids=aidStm[utstmid2]
                gotmd2=1
                fstmid=tstmid2
            except:
                #print 'really no trackers for tstmid: ',tstmid
                fstmid=tstmid
                gotmd2=0
                
        
        #print 'mmmm222',gotmd2,'mmmm333',gotmd3
    
        if(len(aids) == 0):
            print 'no aids for tstmid: ',tstmid,'tstmid2: ',tstmid2
            fstmid=tstmid
        else:
            aidstr=makeAidStr(aids)
            if(verb): print 'fff fstmid: %s'%(fstmid),'aids: %s'%(aidstr[0:120])
        
        fstmids.append((tstmid,fstmid))
        
    return(fstmids)
        
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
        
def tcbasin(lat,lon):

    basin='00'

    if(lat > 0.0 and lon >= 40.0 and lon < 75.0 ):
        basin='NIA'
        
    if(lat > 0.0 and lon >= 75.0 and lon < 100.0 ):
        basin='NIB'


    if(lat > 0.0 and lon >= 100.0 and lon < 180.0):
        basin='WPC'

    # 20011029
    # Jim Gross says that for cliper purposes CPC=EPC
    #

    if( (lat > 0.0 and lat <= 90.0 ) and (lon >= 180.0 and lon < 258.0) ):
        basin='EPC'

    if( (lat > 0.0 and lat <= 17.0 ) and (lon >= 258.0 and lon < 270.0) ):
        basin='EPC'
    elif( (lat > 17.0) and (lon >= 258.0 and lon < 270.0) ):
        basin='ATL'
    
    if( (lat > 0 and lat <= 14.0 ) and (lon >= 270 and lon < 275) ):
        basin='EPC'
    elif( (lat > 14) and (lon >= 270 and lon < 275) ):
        basin='ATL'
        
    if( (lat > 0 and lat <= 9 ) and (lon >= 275 and lon < 285) ):
        basin='EPC'
    elif( (lat > 9) and (lon >= 275 and lon < 285) ):
        basin='ATL'


    if( lat > 0 and lon >= 285):
        basin='ATL'


    if( lat < 0 and lon >= 135):
        basin='SEP'

    if( lat < 0 and ( lon > 40 and lon < 135) ):
        basin='SIO'
        
    return(basin)

    
def cliperinput(dtg,source='neumann'):

    verb=0
    
    tcs=findtc(dtg)
    if(verb): print tcs

    f=string.atof
    
    o=open('/tmp/clip.input.txt','w')

    for tc in tcs:
        if(verb): print tc
        tt=string.split(tc)
        sname=tt[1]
        vmax=f(tt[2])
        lat0=f(tt[4])
        lon0=f(tt[5])
        dir=f(tt[8])
        spd=f(tt[9])

        (latm12,lonm12)=rumltlg(dir,spd,-12,lat0,lon0)
        (latm24,lonm24)=rumltlg(dir,spd,-24,lat0,lon0)

        basin=tcbasin(lat0,lon0)
        if(verb): print "ssss ",sname,vmax,lat0,lon0,dir,spd
        if(verb): print "mmmm ",latm12,lonm12,latm24,lonm24
        part1="%10s %3s %3s  vmax: %03d "%(dtg,sname,basin,vmax)
        part2="motion: %6.2f %5.2f  tau0: %5.1f %6.1f "%(dir,spd,lat0,lon0)
        part3="taum12: %5.1f %6.1f  taum24: %5.1f %6.1f"%(latm12,lonm12,latm24,lonm24)
        clipcard=part1+part2+part3+'\n'

        print part1,part2,part3

        o.writelines(clipcard)
        
    o.close()
