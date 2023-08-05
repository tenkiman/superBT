#!/usr/bin/env pythonw

from sBT import *

sMdesc=lsSbtVars()

def makeMD3(mpath,override=0,verb=0):

    isBT=0
    isDEV=0
    
    if(mf.find(mpath, '-BT.txt')):  isBT=1

    rc=getStmids4SumPath(mpath)
    (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()
        isDEV=1
        
    try:
        icards=open(mpath).readlines()
    except:
        print """EEE can't read mpath: %s -- sayounara"""%(mpath)
        sys.exit()
    
    (sdir,sfile)=os.path.split(mpath)

    if(verb):
        print 'spath: ',mpath
    ostm1id=stm1id.replace('.','-')

    if(verb):
        print 'stm1id:  ',stm1id
        print 'stm9xid: ',stm9xid
        print 'sdir:    ',sdir
        print 'sfile:    ',sfile
        
    ofile="%s-md3.txt"%(ostm1id.upper())
    if(mf.find(sfile,'BT')):
        ofile="%s-md3-BT.txt"%(ostm1id.upper())
        
    ofileS=ofile.replace('md3','sum-md3')

    opathS="%s/%s"%(sdir,ofileS)
    opath="%s/%s"%(sdir,ofile)
    
    opathSThere=(MF.getPathNlines(opathS) > 0)
    opathThere=(MF.getPathNlines(opath) > 0)
    
    if(not(override) and opathSThere and opathThere):
        print 'WWW md3 paths already there...and override=0...return opath'
        return(opath)

    opathSTmp="/tmp/%s"%(ofileS)
    opathTmp="/tmp/%s"%(ofile)

    print
    print 'spath:  ',mpath
    print 'opath:  ',opath
    print 'opathS: ',opathS

    if(verb):
        print 'stm1id: ',stm1id	
        print 'sname:  ',sname
        print 'stmDev: ',stmDev
        print 'sdir:   ',sdir
        print 'sfile:  ',sfile
        print 'ofile:  ',ofile
        print 'ofileS: ',ofileS
        
        print 'opath:  ',opath
        print 'opathS: ',opathS

    if(verb):    
        for icard in icards:
            print 'iii',icard[0:-1]
        
    ocards=[]
    dom3=0
    md3=MD3trk(icards,stm1id,stm9xid,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    dtgs=md3.dtgs
    trk=md3.trk
    basin=md3.basin
    
    # -- analyze the stm to make summary card
    #
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    if(isBT):
        print '222-BBB',rcsum,m3sum[0:-1]
    else:
        print '222-999',rcsum,m3sum[0:-1]

    # -- now do trk
    #

    ktrk=trk.keys()
    ktrk.sort()
    ocards=[]
    
    for kt in ktrk:
        ocard=parseDssTrkMD3(kt,trk[kt],stm1id,stm9xid,basin,rcsum=rcsum,sname=sname)
        ocard=ocard.replace(' ','')
        if(verb): print 'ooo---iii',ocard,len(ocard.split(','))
        ocards.append(ocard)

    rc=MF.WriteList2Path(ocards, opathTmp,verb=verb)
    (m3trk,m3info)=getMd3trackSpath(opathTmp,verb=verb)
    m3trki=setMd3track(m3trk,stm1id,verb=verb)
    dtgs=m3trki.keys()
    dtgs.sort()
    
    m3cards=[]
    for dtg in dtgs:
        try:
            m3i=m3info[dtg]
            m2trk=trk[dtg]
        except:
            None
            #m3i=['','']
        im3trk=m3trki[dtg]
        #print im3trk[0:5],m3i,len(m3trk),len(m3i)
        m3card=makeMd3Card(dtg,im3trk, m3i,m2trk,verb=verb)
        m3cards.append(m3card)
    #md3.m3tri=m3trki
    rc=MF.WriteList2Path(m3cards, opath,verb=verb)

    md3=MD3trk(m3cards,stm1id,stm9xid,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    if(isBT):
        print '333-NNN',rcsum,m3sum[0:-1]
    else:
        print '333-999',rcsum,m3sum[0:-1]
        
    return(opath)
    

def mergeMD3(mpath3,mpath3BT,doM2=0,verb=0):
    
    # -- write out mpath -> opath for 9X; mergeMd3Cvs handles no BT
    #
    rc=getStmids4SumPath(mpath3)
    (stmDev,stm1id,sname,stm9xid,basin,sdir)=rc
    isBT=0
    if(stmDev == 'NN'):  isBT=1
    
    opath3=None
    (odir,ofile)=os.path.split(mpath3)
    (obase,oext)=os.path.splitext(ofile)
    opath3="%s/%s-MRG.txt"%(odir,obase)
    opath3S=opath3.replace('md3','sum-md3')

    if(doM2):
        # -- if do merge with md2 do merge here, just make the md3 and sum 
        #
        ocards=open(mpath3).readlines()
        
    else:
        # -- merge md3   
        #
        if(isBT):
            ocards=mergeMd3CvsBT(mpath3,mpath3BT,opath3,verb=verb)
        else:
            ocards=mergeMd3Cvs9X(mpath3,mpath3BT,opath3,verb=verb)

    MF.WriteList2Path(ocards, opath3,verb=verb)
    md3=MD3trk(ocards,stm1id,stm9xid,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opath3S)
    if(isBT):
        print '333-NNN-MRG',rcsum,m3sum[0:-1]
    else:
        print '333-999-MRG',rcsum,m3sum[0:-1]
    
    return(opath3)
    
def mergeMD(mpath,mpathBT,verb=0):
    
    # -- write out mpath -> opath for 9X; mergeMd3Cvs handles no BT
    #
    rc=getStmids4SumPath(mpath)
    (stmDev,stm1id,sname,stm9xid,basin,sdir)=rc
    isBT=0
    if(stmDev == 'NN'):  isBT=1
    
    opath=None
    (odir,ofile)=os.path.split(mpath)
    (obase,oext)=os.path.splitext(ofile)
    opath="%s/%s-M2B.txt"%(odir,obase)

    if(isBT):
        ocards=mergeMdCvsBT(mpath,mpathBT,opath,verb=verb)
    else:
        ocards=mergeMdCvs9X(mpath,mpathBT,opath,verb=verb)

    MF.WriteList2Path(ocards, opath,verb=verb)

    return(opath)
    
    
def getStmidsDirs(years,basins):
    
    ostmids=[]
    osdirs={}
    for year in years:
        sdir="%s/%s"%(sbtSrcDir,year)
        if(not(MF.ChkDir(sdir))):
            print 'sdir not there...'
            sys.exit()
        
        for basin in basins:
            bsdir="%s/%s"%(sdir,basin)
            if(not(MF.ChkDir(bsdir))):
                print 'bsdir not there...'
                sys.exit()
            
            smask="%s/%s/*"%(sdir,basin)
            sdirs=glob.glob(smask)
            sdirs.sort()
            for sdir in sdirs:
                ss=sdir.split('/')
                stm=ss[-1]
                sss=stm.split('-')
                stmid="%s.%s"%(sss[0].lower(),sss[1])
                ostmids.append(stmid)
                osdirs[stmid]=sdir
                
    return(ostmids,osdirs)

def doTrkPlot(mpath,plttag=None,override=1,doM3=0,doX=1):

    xgrads='grads'
    xgrads=setXgrads(useX11=0,useStandard=0)
    zoomfact=None
    background='black'
    dtgopt=None
    ddtg=6
    dtg0012=0
    
    rc=getStmids4SumPath(mpath)
    (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()

    icards=open(mpath).readlines()

    if(doM3):
        md3=MD3trk(icards,stm1id,stm9xid,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    else:
        md3=MD3trk(icards,stm1id,stm9xid,dom3=0,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
        
    dtgs=md3.dtgs
    btrk=md3.trk
    basin=md3.basin
    
    # -- make the plot
    MF.sTimer('trkplot')
    tP=TcBtTrkPlot(stm1id,btrk,dobt=0,
                   Window=0,Bin=xgrads,
                   zoomfact=zoomfact,override=override,
                   background=background,dopbasin=0,
                   dtgopt=dtgopt,pltdir=sdir,
                   plttag=plttag)

    tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg)
    MF.dTimer('trkplot')
    if(doX): tP.xvPlot(zfact=0.75)
    



def chkSpdDirMd3Mrg(mpath3,mpath,
                    mpathBT=None,
                    doRedo=0,
                    bspdmax=30.0,
                    bspdmaxNN=40.0,
                    latMaxNN=35.0,
                    verb=0,
                    killSngl=1,
                    ):


    exDtgs=[]
    qcM3Cards={}
    
    qcpath="%s-QC-%02.0f"%(mpath,bspdmax)

    pp=mpath.split('/')
    ss=pp[-2][0:8].replace('-','.')
    stmid=ss.lower()
    
    posits={}
    spds={}
        
    m3cards=open(mpath3).readlines()
    mcards=open(mpath).readlines()
    if(mpathBT != None):
        mcardsBT=open(mpathBT).readlines()
    
    nm3=len(m3cards)
    nm=len(mcards)
    
    if(nm == 1):
        (sdir,sfile)=os.path.split(mpath)
        if(killSngl):
            ropt=''
            rc=raw_input("KILL-SSSIIInngggllleeetttooonnn? y|n  ")
            if(rc.lower() == 'y'):
                cmd="rm -r %s"%(sdir)
                mf.runcmd(cmd,ropt)
        else:
            print 'EEE-SSSIIInngggllleeetttooonnn: ',mpath
            
        return(2,None)
            
        
    if(nm3 != nm and verb):
        print 'EEE??? -- nm3 ',nm3,' != nm ',nm,' for m3: ',mpath3,' m: ',mpath
    
    for m3card in m3cards:

        mm=m3card.split(',')
        
        (dtg,rlat,rlon,vmax,pmin,
         tdir,tspd,r34m,r50m,tcstate,warn,
         roci,poci,alf,depth,eyedia,
         tdo,ostmid,ostmname,r34,r50)=parseMd3Card(mm)
        blat=rlat
        blon=rlon
        bvmax=vmax
        posits[dtg]=(blat,blon,bvmax)
        qcM3Cards[dtg]=m3card
        
    for mcard in mcards:
        mm=mcard.split(',')
        dtg=mm[0].strip()
        #qcM3Cards[dtg]=mcard

    dtgs=posits.keys()
    dtgs.sort()
    
    ndtgs=len(dtgs)
    
    for n in range(0,ndtgs):
        
        odtg=dtgs[n]
        if(ndtgs == 1):
            dtgm1=dtgs[0]
            dtg=dtgs[0]
        elif(n == 0 and ndtgs > 1):
            dtgm1=dtgs[0]
            dtg=dtgs[n+1]
        else:
            dtgm1=dtgs[n-1]
            dtg=dtgs[n]

        blat=posits[dtg][0]
        blatm1=posits[dtgm1][0]

        blon=posits[dtg][1]
        blonm1=posits[dtgm1][1]

        (bdir,bspd,bu,bv)=rumhdsp(blatm1,blonm1,blat,blon,6)

        obspd=bspd
        spds[odtg]=bspd

        stmidNN=stmid
        
            
        stest9X=(bspd > bspdmax)
        stestNN=(bspd > bspdmaxNN)
        ltest=(abs(blat) < latMaxNN)
        ntest=IsNN(stmid)
        
        dtest=(stest9X and not(ntest))
        btest=(stestNN and ltest and ntest)
        if(dtest or btest):
            exDtgs.append(dtg)
    
    # -- if have a problem...
    #
    oqcpath=None
    if(len(exDtgs) > 0):
        oqccards=[]
        for dtg in dtgs:
            try:
                oqccard="%4.0f %s"%(spds[dtg],qcM3Cards[dtg])
            except:
                continue
            oqccards.append(oqccard)

        rc=MF.WriteList2Path(oqccards,qcpath,verb=0)
        oqcpath=qcpath
        
    if(oqcpath == None):
        print '<<<<<QC pass for stmid: ',stmid
        return(1,None)
        
    else:
        print '>>>>>>>>>>>>>>>>>>>>>QC FFAAIILL for stmid: ',stmid
        return(0,oqcpath)
    

def doQCTrk(mpath3,mpath,mpathBT,qcpath,savPath,plttag=None):
    
    rc=doTrkPlot(mpath3,doM3=1,plttag=plttag)
    
    print 'doing edit of mpath: ',mpath
    if(mpathBT != None):
        cmd='meld %s %s %s'%(qcpath,mpath,mpathBT)
    else:
        cmd='meld %s %s'%(qcpath,mpath)
    mf.runcmd(cmd,ropt)
    
    cmd='diff %s %s'%(savPath,mpath)
    rc=MF.runcmdLog(cmd)
    lrc=len(rc)
    
    if(lrc == 1):
        rcQC=1
        print 'NNNNN No changes made...'
        
        #rc=raw_input("NNNNN No change made and still okay? ")
        #if(rc.lower() == 'y'):
            #mf.runcmd("rm -i %s"%(qcpath),ropt)
    else:
        rcQC=0
        print "YYYYY You changed the sum.txt file..."
        #rc=raw_input("YYYYY You changed the sum.txt file...y/n to del ")
        #if(rc.lower() == 'y'):
            #mf.runcmd("rm -i %s"%(qcpath),ropt)

    #cmd='rm -i %s'%(qcpath)
    #mf.runcmd(cmd,ropt)

    return(rcQC)
    
def doMd2Md3Mrg(stmid,doM2=1,doRedo=0,qc2paths=1,override=0):
    
    (mpath,mpathBT)=getSrcSumTxt(stmid,verb=0)
    
    savPath="%s-SAV"%(mpath)
    if(mpathBT != None):
        savPathBT="%s-SAV"%(mpathBT)
    else:
        savPathBT=None
        savThereBT=0
    
    savThere=(MF.getPathNlines(savPath) > 0)
    if(not(savThere)):
        cmd="cp %s %s"%(mpath,savPath)
        mf.runcmd(cmd,ropt)
        
    # -- BT
    if(mpathBT != None):
        savThereBT=(MF.getPathNlines(savPathBT) > 0)
        if(not(savThereBT)):
            cmd="cp %s %s"%(mpathBT,savPathBT)
            mf.runcmd(cmd,ropt)
            
    if(doRedo):
        if(savThere):
            cmd="cp -i %s %s"%(savPath,mpath)
            mf.runcmd(cmd,ropt)
        if(savThereBT):
            cmd="cp -i %s %s"%(savPathBT,mpathBT)
            mf.runcmd(cmd,ropt)
                        
            
 
    mpathm=mpath
    if(doM2):
        mpathm=mergeMD(mpath, mpathBT)
        
    mpath3=makeMD3(mpathm,override=override,verb=verb)
    if(mpathBT != None): mpath3BT=makeMD3(mpathBT,override=override,verb=verb)

    if(verb):
        print 'mpath:   ',mpath
        print 'mpath3:  ',mpath3
        print 'mpathBT: ',mpathBT
        print 'mpath3BT: ',mpath3BT

    opath3=opath39X=None
    if(mpathBT != None):
        opath3=mergeMD3(mpath3, mpath3BT,doM2=doM2,verb=verb)
    else:
        opath3=mpath3
    
    rc=(opath3,mpath,mpathBT,savPath,savPathBT)
    return(rc)
     

    
class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'basinOpt':       ['B:',None,'a','basin opt'],
            'yearOpt':        ['Y:',None,'a','yearOpt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'doMeld':         ['M',0,1,'do meld of md3.txt and md3-MRG.txt'],
            'doQC':           ['Q',0,1,'do meld of big spd jumps in sum.txt'],
            'doRedo':         ['R',0,1,'start from -SAV file'],
            'bspdmax':        ['m:',30.0,'f',' max 6-h speed'],
            }

        self.purpose='''
make mdeck3'''
        
        self.examples='''
%s -S 30w.19'''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(basinOpt != None):
    basins=[basinOpt]
else:
    basinOpt='all'
    basins=['wpac','lant','epac','io','shem']

years=[]
if(yearOpt != None):
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=mf.yyyyrange(byear, eyear)

    elif(len(tt) == 1):
        years=[yearOpt]
    else:
        print 'EEE -- invalid yearopt: ',yearOpt



if(stmopt != None):
    
    md3=Mdeck3(doBT=0,doSumOnly=1)
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,verb=verb)
        
elif(len(years) > 0):
    
    (stmids,sdirs)=getStmidsDirs(years,basins)

    
if(stmopt != None):
    ostmopt=stmopt
    ostmopt=ostmopt.replace(',','-')
    invPath="../qcinv/qcspd-%i-%s.txt"%(int(bspdmax),ostmopt)
    
elif(yearOpt != None):
    oyearOpt=yearOpt.replace('.','-')
    invPath="../qcinv/qcspd-%i-YEAR-%s-BASIN-%s.txt"%(int(bspdmax),oyearOpt,basinOpt)
    
qccards=[]
for stmid in stmids:
    
    qc2paths=0
    if(doRedo or override): qc2paths=1
    rc=doMd2Md3Mrg(stmid,doRedo=doRedo,qc2paths=qc2paths,override=override)
    (opath3,mpath,mpathBT,savPath,savPathBT)=rc
    
    #plttag=None
    #rc=doTrkPlot(opath3,plttag=plttag, override=1, doM3=1, doX=1)

    #print 'opath3:    ',opath3
    #print 'mpath:     ',mpath
    #print 'mpathBT:   ',mpathBT
    
    # -- QC
    #
    (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,bspdmax=bspdmax,verb=verb)
    if(rcc == 0):
        qccards.append('qc-fail: %s'%(stmid))
    elif(rcc == 2):
        print 'SSSSSSSSingleton for: ',stmid
        continue
    if(rcc == 0 and doQC):
        rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath)
        rc=doMd2Md3Mrg(stmid,qc2paths=qc2paths,override=override)
        (opath3,mpath,mpathBT,savPath,savPathBT)=rc
        (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,verb=verb)
        plttag='pass1'
        rc=doTrkPlot(opath3,plttag=plttag, override=1, doM3=1, doX=1)
        #if(rcc == 0):
            #(opath3,mpath,mpathBT)=doMd2Md3Mrg(stmid,override=override)
            #(rcc,qcpath,savPath,savPathBT)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,verb=verb)
            #plttag='pass2'
            #rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath,plttag=plttag)

        
rc=MF.WriteList2Path(qccards,invPath,verb=1)
sys.exit()
    
    
