#!/usr/bin/env python

from sBT import *

abdirAtcfW21='/w21/dat/tc/adeck/atcf-form'

def getAdecksStmid(tstmid,redoTrk=0,dryRun=0,
                   ropt='',qropt='quiet',verb=0,override=0):

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
    #if(isShemBasinStm(tstmid)):
        #nstmids=[]
        #for astmid in astmids:
            #if(astmid[2] == 'p'): nstmid=astmid.replace('p','s')
            #if(astmid[2] == 's'): nstmid=astmid.replace('s','p')
            #print 'asdfasdfsdaf',astmid,nstmid
            #nstmids.append(astmid)
            #nstmids.append(nstmid)
            
        #astmids=nstmids
            
    adecks=[]
    for astmid in astmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(astmid)
        sdir="%s/%s"%(abdirStm,year)
        stm1=stm1id.upper()
        amask="%s/tctrk.atcf.*.%s"%(sdir,stm1)
        if(verb): print 'amask: ',amask
        adecks=adecks+glob.glob(amask)
    adecks.sort()
    adecks=mf.uniq(adecks)
    adtgs=[]
    for adeck in adecks:
        (adir,afile)=os.path.split(adeck)
        aa=afile.split('.')
        adtg=aa[2]
        adtgs.append(adtg)
        
    odir="%s/%s/era5"%(abdirAtcf,year)
    MF.ChkDir(odir,'mk')
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
    ofile='a%s%s%s.dat'%(b2id.lower(),stm2id[2:4],year)
    opath="%s/%s"%(odir,ofile)

    adtgs=mf.uniq(adtgs)
    missdtgs=[]
    for m3dtg in m3dtgs:
        if(not(m3dtg in adtgs)): missdtgs.append(m3dtg)
            
    # -- dryrun
    #
        
    if(dryRun):
        
        finalMissDtgs=[]
        
        for missdtg in missdtgs:
            myear=missdtg[0:4]
            sfiles=[]
            for astmid in astmids:
                (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(astmid)
                mmask="%s/%s/%s/*%s%s.txt"%(tmtrkbdir,myear,missdtg,snum,b1id)
                sfiles=sfiles+glob.glob(mmask)
                 
            if(len(sfiles) >= 1):
                adtgs.append(missdtg)
            else:
                finalMissDtgs.append(missdtg)
                

        adtgs.sort()        
        nmiss=len(finalMissDtgs)
        
        nlAdecks=0
        nsAdecks=0
        if(nmiss == 0):
            for adeck in adecks:
                nlAdecks=nlAdecks+MF.getPathNlines(adeck)
                nsAdecks=nsAdecks+MF.getPathSiz(adeck)
                
            if(MF.ChkPath(opath)):
                onl=MF.getPathNlines(opath)
                osz=MF.getPathSiz(opath)
            
            print 'tstmid: ',tstmid,' astmids: ',astmids,' N adtgs: ',len(adtgs),' N m3dtgs: ',len(m3dtgs),' N miss: ',\
                  nmiss,'nlAdecks: ',nlAdecks,' nsAdecks: ',nsAdecks
            print 'opath: ',opath,' onl: %4d'%(onl),' osz: %6d'%(osz)
            
        elif(nmiss > 0):
            print 'MMMMMMMMM for ',tstmid
        
        return(1)
        
        
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
        else:
            rdtgs.append(missdtg)
            missOK=0
            
    #-- print out
    #
    rdtgs.sort()
    if(len(rdtgs) > 0):
        print 'RR-- for stmid: ',tstmid
        print 'RR-- redo dtgs: ',rdtgs
        
    
    if(missOK):
        rmOpt='-i'
        if(override): rmOpt=''
        if(MF.ChkPath(opath)):
            cmd="rm %s %s ; touch %s"%(rmOpt,opath,opath)
        else:
            cmd="touch %s"%(opath)
        mf.runcmd(cmd,qropt)
        for adeck in adecks:
            cmd='cat %s >> %s'%(adeck,opath)
            mf.runcmd(cmd,qropt)
            
        onl=MF.getPathNlines(opath)
        osz=MF.getPathSiz(opath)
        
        print 'opath: ',opath,' onl: %4d'%(onl),' osz: %6d'%(osz)
        return(1)
        
    else:
        
        if(redoTrk):
            #ropt='norun'
            for rdtg in rdtgs:
                cmd='s-sbt-tmtrkN.py %s -T -O'%(rdtg)
                mf.runcmd(cmd,ropt)
            return(2)
        else:
            print 'EEE problem with trackers for tstmid: ',tstmid
            return(0)
        
def getStmopts(stmopt,verb=0):
    
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
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'redoTrk':          ['R',0,1,' run tracker for missing dtgs'],
            'rsyncOnly':        ['s',0,1,' only do rsync to /w21/dat/tc/'],
            'dryRun':           ['D',0,1,' do a dryRun'],
            
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

if(rsyncOnly):

    cmd="rsync -alv %s/ %s/"%(abdirAtcf,abdirAtcfW21)
    mf.runcmd(cmd,ropt)
    sys.exit()


MF.sTimer('atcf-ALL-%s'%(istmopt))
for stmopt in stmopts:
    
    MF.sTimer('atcf-stmopt-%s'%(stmopt))
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    
    for tstmid in tstmids:
        
        rc=getAdecksStmid(tstmid,redoTrk=redoTrk,dryRun=dryRun,override=override,verb=verb)
        
        if(rc == 0):
            print 'EEE -- still missing trackers for : ',tstmid,' press...'
    
        if(rc == 2):
            print 'RRR -- reran tracker... now redo...'
            rc=getAdecksStmid(tstmid,redoTrk=0,override=1,verb=verb)
            print 'RRR -- rc after rerun: ',rc
            
    MF.dTimer('atcf-stmopt-%s'%(stmopt))
                
MF.dTimer('atcf-ALL-%s'%(istmopt))

# -- rsync from sbt to /w21/dat/tc/adeck/atcf-form/
#
cmd="rsync -alv %s/ %s/"%(abdirAtcf,abdirAtcfW21)
mf.runcmd(cmd,ropt)
        
sys.exit()


