#!/usr/bin/env python

from sBT import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

def parseInvPath(invpath):
    
    print
    print 'iii',invpath
    cards=open(invpath).readlines()
    for card in cards:

        if(mf.find(card,'vmax')):

            tt=card.split()
            stmid=tt[0]
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)

            # -- bypass bad era5 dtgs
            #
            dtg=tt[1]
            if(dtg in badEra5Dtgs):
                print 'bbb bypass bad dtg: ',dtg
                continue
                 
            
            rccode=tt[3]
            tvmax=tt[5]
            nl=int(tt[7])
            
            if(tvmax == "***"): 
                tvmax=-999
            else:
                tvmax=int(tvmax)
                
            
            (mrc,mtrk)=md3.getMd3track(stmid)
            rc=mtrk[dtg]
            (mlat,mlon,mvmax,mpmin)=rc[0:4]
            mtccode=rc[8]
            mwncode=rc[9]
            mlat=float(mlat)
            tmlat=abs(mlat)
            isTC=(IsTc(mtccode) == 1)
            isWN=(IsWarn(mwncode) == 1)
            
            
            lb2id=b2id.lower()

            # -- put cp in ep
            #
            if(lb2id == 'cp'): lb2id='ep'
                 
            #print 'ss',stmid,stm2id,lb2id,dtg
            MF.appendDictList(rall,(lb2id,dtg),(nl,stmid,tvmax,mlat,mlon,mvmax,mpmin,isTC,isWN))
            
    return(rall)



def anlInvByBasin(rall,r1latmax,r1vmin,verb=0):
    
    kk=rall.keys()
    
    nall={}
    t9all={}
    n9all={}
    
    rfail={}
    
    abids=[]
    adtgs={}
    for k in kk:
        bid=k[0]
        bdtg=k[1]
        abids.append(bid)
        MF.appendDictList(adtgs, bid, bdtg)
        
    abids=mf.uniq(abids)
    
    
    for abid in abids:

        nfail=0
        n999=0
        n999badLat=0
        n999badVmax=0
        n999badBoth=0
        ngood=0

        dtgs=adtgs[abid]
        dtgs=mf.uniq(dtgs)
        
        for dtg in dtgs:
            acs=rall[abid,dtg]
            for ac in acs:
                (nl,stmid,tvmax,mlat,mlon,mvmax,mpmin,isTC,isWN)=ac
                # -- bypass 9X
                #
                if(not(IsNN(stmid))):
                   continue

                if(nl == -999):
                    nfail=nfail+1
                    MF.appendDictList(rfail, abid, dtg)

                elif(nl == 999 or nl == -1):
                    n999=n999+1
                    amlat=abs(mlat)
                    badlat=0
                    badvmax=0
    
                    chkvmax=-999
                    if(tvmax != -999): chkvmax=tvmax
                    MF.appendDictList(t9all, abid, (stmid,dtg,chkvmax,mlat) )

                    if(amlat < r1latmax):
                        n999badLat=n999badLat+1
                        badlat=1
                        
                    if(tvmax != -999 and tvmax < r1vmin):
                        badvmax=1
                        n999badVmax=n999badVmax+1
                        
                    if(badlat and badvmax):
                        n999badLat=n999badLat-1
                        n999badVmax=n999badVmax-1
                        n999badBoth=n999badBoth+1
                        
                        
                    if(verb): print '999',stmid,dtg,amlat,r1latmax,mvmax,r1vmin

                elif(nl > 1):
                    ngood=ngood+1

                else:
                    print 'ooopppsss nl: ',dtg,nl
                
        n999sum=n999badLat+n999badVmax+n999badBoth
        nsum=ngood+n999+nfail
        
        ptrk=(float(ngood)/float(nsum))*100.0
        pnotrk=100.0-ptrk
        psignotrk=(float(n999sum)/float(nsum))*100.0
        
        poknotrk=pnotrk-psignotrk
        if(poknotrk < 0.0): poknotrk=0.0
             
        
        if(verb):
            print 'basin: ',abid,'Nsum: ',nsum,'ngood: ',ngood,'n999',n999,'nfail: ',nfail
            print 'n999badLat: ',n999badLat,' n999badVmax: ',n999badVmax,'n999badBoth',n999badBoth,\
                  'n999sum:',n999sum
            
        nall[abid]=(nsum,nfail,n999,ptrk,pnotrk,psignotrk,poknotrk)
        
    kk=t9all.keys()
    kk.sort()

    for k in kk:
        n9s=t9all[k]
        ntd=0
        nts=0
        nty=0
        nunk=0
        ntot=0

        for n9 in n9s:
            (stmid,dtg,vmax,blat)=n9
            #print 'asdfasdf',k,stmid,dtg,vmax,blat
            if(vmax > 0 and vmax < 35):
                ntd=ntd+1
            elif(vmax >= 35 and vmax < 65):
                nts=nts+1
            elif(vmax >= 65):
                nty=nty+1
            elif(vmax < 0):
                nunk=nunk+1
            else:
                print 'ooopppsss',n9
                sys.exit()
                
            ntot=ntot+1
            
        n9tot=ntd+nts+nty+nunk
        
        if(n9tot != ntot):
            print 'problem for basin ',k,'n9 by vmax failed'
            sys.exit()
            
        if(ntot > 0):
            
            pn9td=(float(ntd)/float(ntot))*100.0
            pn9ts=(float(nts)/float(ntot))*100.0
            pn9ty=(float(nty)/float(ntot))*100.0
            pn9unk=(float(nunk)/float(ntot))*100.0
            
            pn9all=nall[k][4]
            
            #print 'PP: %s notrk: %5.1f  td: %5.1f  ts: %5.1f ty: %5.1f  unk: %5.1f '%(k.upper(),pn9all,pn9td,pn9ts,pn9ty,pn9unk)
                
        n9all[k]=(pn9td,pn9ts,pn9ty,pn9unk,n9tot)
            
                
        #print 'NN99 basin: %s -- ntd: %4d  nts: %4d  nty: %4d nunk: %4d ntot: %4d %d'%(k.upper(),ntd,nts,nty,nunk,ntot,n9tot)
                
        
        
        
    return(nall,n9all,rfail)


class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'dtgopt':           ['d:',None,'a','dtgopt'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'ls9only':          ['9',0,1,'ls9only'],
            'ls1only':          ['1',0,1,'ls1only'],
            'lsAll':            ['A',0,1,'ls all'],
            'doSig':            ['G',0,1,'ls only Sig'],
            'do9Xonly':         ['X',0,1,'ls only Sig'],
            'doReRun':          ['R',0,1,'rerun failed trkers'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

r9vmin=35
r9latmax=40.0
r1vmin=35
r1latmax=40.0

if(mf.find(yearOpt,'-')):
    tt=yearOpt.split('-')
    byear=int(tt[0])
    eyear=int(tt[1])
    
else:
    byear=int(yearOpt)
    eyear=int(yearOpt)


for iyear in range(byear,eyear+1):

    rall={}

    year=str(iyear)
    dtgopt="%s01.%s12.6"%(iyear,iyear)
    
    doInvPath=1
    yearOpt=None
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1


    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    
    invpath=getInvPath4Dtgopt(dtgopt,invdir='./inv',getonly=1)
    
    rall=parseInvPath(invpath)
    
    (nall,n9all,rfail)=anlInvByBasin(rall,r1latmax,r1vmin,verb=verb)
    
    abids=nall.keys()
    abids.sort()
    
    rfailDtgs=[]

    if(len(rfail) != 0):
        print 'adf',rfail
        for abid in abids:
            try:
                fdtgs=rfail[abid]
            except:
                continue
                
            rfailDtgs=rfailDtgs+fdtgs
        
        rfailDtgs.sort()
        rfailDtgs=mf.uniq(rfailDtgs)

        # -- reran both tmtrk and tcdiag
        #
        #MF.ChangeDir('../tcdiag')  # tctrk
        #MF.ChangeDir('../tcdiag')  # tcdiag
        
        for fdtg in rfailDtgs:
            if(doReRun):
                cmd='r-all-tmtrk.py %s -T'%(fdtg)  # tctrk
                #cmd='r-all-tcdiag.py %s -C -L'%(fdtg)  # tcdiag
                mf.runcmd(cmd,ropt)
            else:
                cmd='s-sbt-tmtrkN.py %s -i'%(fdtg)
                mf.runcmd(cmd,ropt)
        
                
                
            
        
    
    for abid in abids:
        (nsum,nfail,n999,ptrk,pnotrk,psignotrk,poknotrk)=nall[abid]
        (pn9td,pn9ts,pn9ty,pn9unk,n9tot)=n9all[abid]
        
        pcard=' ptrk: %4.1f pNOtrk: %4.1f pNOsig: %4.1f  pNOok: %4.1f'%(ptrk,pnotrk,psignotrk,poknotrk)
        opn9unk=''
        if(pn9unk != 0.0):
            opn9unk="UNK: %5.1f"%(pn9unk)
        pcard9=' pNObyVmax  td: %5.1f ts: %5.1f TY: %5.1f %s'%(pn9td,pn9ts,pn9ty,opn9unk)
        print '%s %s  N: %5d.%-5d %s  %s'%(abid,iyear,nsum,nfail,pcard,pcard9)

sys.exit()


