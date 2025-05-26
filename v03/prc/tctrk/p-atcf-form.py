#!/usr/bin/env python

from sBT import *

def getAdecksStmid(tstmid,redoTrk=0,ropt='',qropt='quiet',verb=0,override=0):
    
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
    sdir="%s/%s"%(abdirStm,year)
    stm1=stm1id.upper()
    adecks=glob.glob("%s/tctrk.atcf.*.%s"%(sdir,stm1))
    adecks.sort()
    adtgs=[]
    for adeck in adecks:
        (adir,afile)=os.path.split(adeck)
        aa=afile.split('.')
        adtg=aa[2]
        adtgs.append(adtg)
        
    odir="%s/%s/era5"%(abdirAtcf,year)
    MF.ChkDir(odir,'mk')
    ofile='a%s%s%s.dat'%(b2id.lower(),stm2id[2:4],year)
    opath="%s/%s"%(odir,ofile)

    # -- get track
    #
    rc=md3.getMd3track(tstmid,dobt=dobt,verb=verb)
    if(rc[0]):
        m3trk=rc[1]
        m3dtgs=m3trk.keys()
        m3dtgs.sort()
        
    missdtgs=[]
    for m3dtg in m3dtgs:
        if(not(m3dtg in adtgs)): missdtgs.append(m3dtg)
            

    rdtgs=[]
    missOK=1
    for missdtg in missdtgs:
        myear=missdtg[0:4]
        mmask="%s/%s/%s/*%s%s.txt"%(tmtrkbdir,myear,missdtg,snum,b1id)
        sfiles=glob.glob(mmask)
        if(verb): print 'MMM',mmask,missdtg,sfiles
             
        if(len(sfiles) == 1):
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
    
MF.sTimer('atcf-ALL-%s'%(istmopt))
for stmopt in stmopts:
    
    MF.sTimer('atcf-stmopt-%s'%(stmopt))
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    
    for tstmid in tstmids:
        
        rc=getAdecksStmid(tstmid,redoTrk=redoTrk,override=override,verb=verb)
        
        if(rc == 0):
            print 'EEE -- still missing trackers for : ',tstmid,' press...'
    
        if(rc == 2):
            print 'RRR -- reran tracker... now redo...'
            rc=getAdecksStmid(tstmid,redoTrk=0,override=1,verb=verb)
            print 'RRR -- rc after rerun: ',rc
            
    MF.dTimer('atcf-stmopt-%s'%(stmopt))
                
MF.dTimer('atcf-ALL-%s'%(istmopt))
        
sys.exit()


