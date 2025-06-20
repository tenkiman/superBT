#!/usr/bin/env python

from sBT import *

def getAdeckTcdiag4Stmid(tstmid,verb=0,verbose=0):

    # -- get track
    #
    rc=md3.getMd3track(tstmid,dobt=0,verb=verb)
    astmids=[]

    if(rc[0]):
        m3trk=rc[1]
        m3dtgs=m3trk.keys()
        m3dtgs.sort()
        
        for m3dtg in m3dtgs:
            astmid=m3trk[m3dtg][-4]
            astmids.append(astmid)
            #print 'asdf---',m3dtg,astmid,m3trk[m3dtg]
    else:
        print 'EEE -- no track for tstmid: ',tstmid
        sys.exit()
        
    astmids=mf.uniq(astmids)
            
    adecks=[]
    for astmid in astmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(astmid)
        sdir="%s/%s"%(abdirStm,year)
        stm1=stm1id.upper()
        amask="%s/tctrk.atcf.*.%s"%(sdir,stm1)
        ndecks=glob.glob(amask)
        if(verb): print 'amask: ',amask,len(ndecks)
        adecks=adecks+ndecks
    adecks.sort()
    adecks=mf.uniq(adecks)
    
    adtgs=[]
    for adeck in adecks:
        nladeck=MF.getPathNlines(adeck)
        (adir,afile)=os.path.split(adeck)
        aa=afile.split('.')
        adtg=aa[2]
        adtgs.append(adtg)
        atype='tmtrkN'
        if(nladeck <= 4): atype='best'
        adStat[tstmid,adtg]=(1,atype,nladeck)    
            
    # -- missing adecks
    #
    
    missdtgs=[]
    for m3dtg in m3dtgs:
        if(not(m3dtg in adtgs)): missdtgs.append(m3dtg)
            
    rdtgs=[]
    missOK=1
    for missdtg in missdtgs:
        myear=missdtg[0:4]
        sfiles=[]
        for astmid in astmids:
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(astmid)
            mmask="%s/%s/%s/*%s%s.txt"%(tmtrkbdir,myear,missdtg,snum,b1id)
            sfiles=sfiles+glob.glob(mmask)
            if(verb): print 'MMM',mmask,missdtg,sfiles
             
        if(len(sfiles) >= 1):
            if(verb): print 'std there...trk was run for ',missdtg
            adtgs.append(missdtg)
            adStat[tstmid,missdtg]=(1,'stdout')
        else:
            # -- worse case -- tracker not run at all
            #
            adtgs.append(missdtg)
            adStat[tstmid,missdtg]=(0,'miss')
            rdtgs.append(missdtg)
            missOK=0

    if(verbose):
        adtgs.sort()
        for adtg in adtgs:
            print 'getAD: ',tstmid,adtg,adStat[tstmid,adtg]
        print
        print
            
            

    # -- now go after tcdiag decks...
    #
    for astmid in astmids:
        rc=getTcdiagFiles(m3dtgs,astmid,tstmid,verb=verb)

    for dtg in m3dtgs:
        try:
            td=tcdStat[tstmid,dtg]
        except:
            tcdStat[tstmid,dtg]=(0,dtg)
            
        if(verbose): print 'getTD: ',tstmid,dtg,tcdStat[tstmid,dtg]
    
    return(missOK)



def getTcdiagFiles(m3dtgs,astmid,tstmid,verb=0):
    

    # -- relabel with tstmid for 9X for year >= 2007
    #
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(astmid)

    sdir=tsbdbdir
    for dtg in m3dtgs:
        myear=dtg[0:4]
        mmask="%s/%s/%s/era5/tcdiag*%s%s*.txt"%(sdir,myear,dtg,snum,b1id)
        tfile=glob.glob(mmask)
        tcdsiz=len(tfile)
        tcdtype=''
        #print 'ttt',mmask,tfile,tcdsiz,tcdtype
        
        if(tcdsiz == 1):
            tt=tfile[0].split('.')
            tcdtype=tt[-2].split('-')[-1]
            tcdStat[tstmid,dtg]=(tcdsiz,tcdtype)

    rc=1
    return(rc)
    
    
        
def getStmopts(stmopt,verb=0):
    
    ttc=stmopt.split(',')
    
    if(len(ttc) > 1):
        stmopts=[]
        for ss in ttc:
            sopts=getStmopts(ss)
            stmopts=stmopts+sopts

        return(stmopts)
    
    tt=stmopt.split('.')
    yy=tt[-1]
    bb=tt[0]
    tt=bb.split(',')
    if(len(tt) > 1):
        bbs=tt
    else:
        bbs=[bb]
    
    tt=yy.split('-')
    if(len(tt) == 2):
        y0=int(tt[0])
        y1=int(tt[1])
        yys=range(y0,y1+1)
    else:
        yys=[yy]
    
    if(mf.find(stmopt,'all')):
        bbs=['h','i','w','c','e','l']
        
    stmopts=[]
    for yy in yys:
        syy=str(yy)
        iyy=int(yy)
        for bb in bbs:
            # -- epac best track starts in 1949
            #
            if(verb): print iyy,bb,(iyy >= 45 and iyy <= 48 and bb == 'e')
            if(iyy >= 45 and iyy <= 48 and bb == 'e'):
               continue 
            stmopts=stmopts+[
                '%s.%s'%(bb,syy),
            ]
    
    return(stmopts)

def anlAdTdStat(tstmids,verb=1):

    redoAd=[]
    redoTd=[]
    
    for tstmid in tstmids:

        kk=tcdStat.keys()
        tdtgs=[]
        kk.sort()
        for k in kk:
            stmid=k[0]
            dtg=k[1]
            if(stmid == tstmid):
                tdtgs.append(dtg)
            
        tdtgs.sort()
        for tdtg in tdtgs:
            if(verb): 
                print 'stmid: ',tstmid,'tcd: ',tdtg,\
                      'ADstat: %-18s'%str(adStat[tstmid,tdtg]),\
                      'TDStat: %-18s'%(str(tcdStat[tstmid,tdtg]))
                
            td=tcdStat[tstmid,tdtg]
            ad=adStat[tstmid,tdtg]
                
            if(td[0] == 0):
                if(verb): print 'redoTD: ',tstmid,tdtg,td
                redoTd.append(tdtg)
            if(ad[0] == 0):
                if(verb): print 'redoAD: ',tstmid,tdtg,ad
                redoTd.append(tdtg)
    
    return(redoAd,redoTd)
    
        
            
    
        

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'verbose':          ['v',0,1,'verbose=1 is REALLY verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'rerunAdTd':        ['R',0,1,' run tcdiag and/or tracker for missing dtgs'],
            'doLog':            ['L',1,0,'do NOT do logfile to raid02/log'],
            'doLocal':          ['C',1,0,'''default is to run locally'''],
            
            
        }

        self.purpose="""
make atcf-form of trackers in adeck-stm"""

        self.examples='''
%s -S l.07  # dtgopt ignored'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgopt=yearOpt=None

istmopt=stmopt
stmopts=getStmopts(stmopt)

lopt='-L'
if(doLog): lopt=''

copt=''
if(doLocal): copt='-C'
    

tcdStat={}
adStat={}
aStmids=[]
MF.sTimer('aDtD-ALL-%s'%(istmopt))
for stmopt in stmopts:
    
    MF.sTimer('aDtD-stmopt-%s'%(stmopt))
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    aStmids=aStmids+tstmids
    
    tyears=[]
    for tstmid in tstmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
        tyears.append(year)
        rc=getAdeckTcdiag4Stmid(tstmid,verb=verb,verbose=verbose)
        
    MF.dTimer('aDtD-stmopt-%s'%(stmopt))
    
MF.sTimer('anl-adtd-%s'%(istmopt))
(redoAd,redoTd)=anlAdTdStat(aStmids,verb=verb)
MF.dTimer('anl-adtd-%s'%(istmopt))

if(len(redoAd) > 0):
    print 'AAADDD redo:',redoAd
else:
    print 'AAADDD -- trackers ALLGOOD   for istmopt: ',istmopt
    
if(len(redoTd) > 0):
    
    redoTd=mf.uniq(redoTd)
    print 'TTTDDD redo Nruns:',len(redoTd)
    
    # -- if do rerun...
    #
    if(rerunAdTd):
     
        MF.ChangeDir('tcdiag')
     
        MF.sTimer('redoTD-All')
        for dtg in redoTd:
            
            # -- check for bad dtgs
            #
            tdtg=dtg
            if(IsBadEra5Dtg(tdtg) == 0):
                print 'EEE---BBB era5 dtg...press...'
                continue
            
            MF.sTimer('redoTD-All-%s'%(dtg))
            cmd="r-all-tcdiag.py %s %s %s"%(dtg,lopt,copt)
            mf.runcmd(cmd,ropt)
            MF.dTimer('redoTD-All-%s'%(dtg))
     
        MF.dTimer('redoTD-All')
        
        # -- now sync over...
        #
        if(doLocal):
         
            tyears=mf.uniq(tyears)
            
            # -- always do the previous year in case of shem
            #
            tyearm1=int(tyears[0])-1
            tyearm1=str(tyearm1)

            tyears.append(tyearm1)
            
            for tyear in tyears:
                cmd='r-rsync-tcdiag-local-output.py -R dat -Y %s -X'%(tyear)
                mf.runcmd(cmd,ropt)
                cmd='r-rsync-tcdiag-local-output.py -R prod -Y %s -X'%(tyear)
                mf.runcmd(cmd,ropt)
                
        # -- go back up to man prc dir
        #
        MF.ChangeDir('../')
    
else:
    print 'TTTDDD -- diag files ALLGOOD for istmopt: ',istmopt


MF.dTimer('aDtD-ALL-%s'%(istmopt))
        
sys.exit()


