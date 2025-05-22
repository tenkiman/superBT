#!/usr/bin/env python

from sBT import *

def getAdecksStmid(tstmid,ropt='',qropt='quiet',verb=0,override=0):
    
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
            
        
    missOK=1
    for missdtg in missdtgs:
        myear=missdtg[0:4]
        mmask="%s/%s/%s/*%s%s.txt"%(tmtrkbdir,myear,missdtg,snum,b1id)
        sfiles=glob.glob(mmask)
        if(verb): print 'MMM',mmask,missdtg,sfiles
             
        if(len(sfiles) == 1):
            if(verb): print 'std there...trk was run for ',missdtg
        else:
            missOK=0
            
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
        
        print 'opath: ',opath,' onl: ',onl,' osz: ',osz
        
    else:
        print 'EEEE problem with trackers for tstmid: ',tstmid
        sys.exit()
        
        
    
    
            
            
        
            
    
        

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

(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
doBT=0
if(doBdeck2): doBT=1

md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)

for tstmid in tstmids:
    rc=getAdecksStmid(tstmid,override=override,verb=verb)
        
        
sys.exit()


