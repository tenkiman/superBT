#!/usr/bin/env pythonw

from sBT import *

sMdesc=lsSbtVars()
    
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
            'doRedo':         ['R',0,1,'start from -SAV file'],
            'bspdmax':        ['m:',30.0,'f',' max 6-h speed'],
            'passNumber':     ['P:',None,'a',' passNumber'],
            'bd2Update':      ['2',0,1,'update using -BT2.txt vice BT.txt'],
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


if(basinOpt != None and basinOpt != 'all'):
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
 
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt=None,yearOpt=None)
    doMd3Only=0
    doBT=0
    if(bd2Update):
        doBdeck2=1
        doMd3Only=0
        doBT=1
        dobt=1
        
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,doMd3Only=doMd3Only,doSumOnly=1,verb=verb)
    #md3=Mdeck3(doBT=0,doSumOnly=1)
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        #dobt=0
        print 'qqq',stmopt
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,verb=verb)
        
elif(len(years) > 0):
    
    print 'bbb',basins
    (stmids,sdirs)=getStmidsDirs(years,basins,doQC=1,bspdmax=bspdmax)
    if(len(stmids) == 0):
        print 'GGGG no storms to QC for years: %s  basins: %s'%(str(years),str(basins))
        print 'GGGG Youkata ne!'
        sys.exit()
    else:
        nstmids=len(stmids)
        print 'will QC %4d storms for years: %s  basins: %s'%(nstmids,str(years),str(basins))
        if(ropt == 'norun'):
            sys.exit()
    
if(stmopt != None):
    ostmopt=stmopt
    ostmopt=ostmopt.replace(',','-')
    
elif(yearOpt != None):
    oyearOpt=yearOpt.replace('.','-')
   

print 'sss---',stmids 
for stmid in stmids:
    
    if(ropt == 'norun'):
        print 'QC stmid: ',stmid
        continue
    
    qc2paths=0
    if(doRedo): override=1
    if(doRedo or override): qc2paths=1

    # -- 000000 make md3 and and check
    #
    
    print 'Pass 0000 for ',stmid
    
    rc=doMd2Md3Mrg(stmid,doRedo=doRedo,qc2paths=qc2paths,
                   bd2Update=bd2Update,
                   override=1)
    (opath3,mpath,mpathBT,savPath,savPathBT)=rc
    (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,bspdmax=bspdmax,verb=verb)
    rccQC=setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=0,bspdmax=bspdmax,override=0)
    
    if(rccQC == 0):
        print 'problem in setQcPassPath...sayounara...'
        sys.exit()

    # -- passes QC... make a plot
    #
    if(rccQC == 1):
        
        
        plttag0='pass01'
        title20='RCC=1111111111 PASS 000000000000'
        rc=doTrkPlot(opath3,override=1,doM3=1,doX=1,
                     plttag=plttag0,title2=title20)

    # -- first fail point
    #
    elif(rccQC == 2):
        
        plttag='pass0'
        title20='RCC=1 PASS 000000000000000'
        rc=doMd2Md3Mrg(stmid,doRedo=0,qc2paths=qc2paths,override=1)
        (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,bspdmax=bspdmax,verb=verb)
        rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath,
                   plttag=plttag0,title2=title20)
        rc=doMd2Md3Mrg(stmid,doRedo=doRedo,qc2paths=qc2paths,override=1)
        (opath3,mpath,mpathBT,savPath,savPathBT)=rc
        (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,bspdmax=bspdmax,verb=verb)
        rccQC=setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=1,bspdmax=bspdmax,override=0)

        print '00000000000011111111111111111',rcc,qcpath,'rccQC: ',rccQC
        
        if(rcc):
            qinput="QC-1111 pass2222 returned qcpath...okay? delete? y/n  "
        else:
            qinput="QC-0000 pass2222 still bad... delete? y/n  "
            
        rc=raw_input(qinput)
        if(rc.lower() != 'n'):
            mf.runcmd("rm -i %s"%(qcpath),ropt)
        else:
            print 'WWWWW continue to next storm...catch on the second pass through'
            continue
 
    else:
        
        # -- FFFF fail
        #
        qcpath0=qcpath
        if(rcc == 2):
            print 'SSSSSSSSingleton for: ',stmid
            sys.exit()
    
        if(rcc == 0):
            
            # -- 11111111111111111111111111111 first pass
            #
            plttag1='pass1'
            title21='RCC=0 PASS 1111111111111111'
            rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath,
                       plttag=plttag1,title2=title21)
            
            rc=doMd2Md3Mrg(stmid,qc2paths=qc2paths,override=1)
            (opath3,mpath,mpathBT,savPath,savPathBT)=rc
            (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,verb=verb)
            rccQC=setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=2,bspdmax=bspdmax,override=0)
    
            delQC=0
            doQC2=1
            
            if(rcc):
    
                plttag1='pass1'
                title21='RCC=111111111111 PASS 1111111111111111'
                rc=doTrkPlot(opath3,override=1,doM3=1,doX=1,
                             plttag=plttag1,title2=title21)
                rc=raw_input("QC pass1 is okay? (rcc == 1) delete? y/n  ")
                if(rc.lower() != 'n'):
                    delQC=1
                    mf.runcmd("rm -i %s"%(qcpath),ropt)
                    continue
                else:
                    rc=raw_input("do you want to another 2nd pass here in pass1? y/n  ")
                    if(rc.lower() == 'n'):
                        doQC2=0
                        mf.runcmd("rm -i %s"%(qcpath0),ropt)
                    else:
                        plttag2='pass2'
                        title22='RCC=0 11111111111 PASS 222222222222222'
                        rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath,
                                   plttag=plttag1,title2=title21)
                        rc=doMd2Md3Mrg(stmid,qc2paths=qc2paths,override=1)
                        (opath3,mpath,mpathBT,savPath,savPathBT)=rc
                        (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,verb=verb)
                        rccQC=setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=2,bspdmax=bspdmax,override=0)
                        
                        if(rcc):
                            plttag21='pass20'
                            title221='RCC=%d PASS 222222220000000000'%(rcc)
                            rc=doTrkPlot(opath3,override=1,doM3=1,doX=1,
                                         plttag=plttag21,title2=title21)
                        
                        rc=raw_input("QC pass2 okay to delete? 222 rcc: %d y/n  "%(rcc))
                        if(rc.lower() == 'y'):
                            mf.runcmd("rm -i %s"%(qcpath0),ropt)
                        continue
                        
                    
            else:
                # -- 2222222222222222222222222222222 2nd pass
                #
                if( (rcc == 0 and not(delQC)) or not(doQC2)):
                    plttag2='pass2'
                    title22='RCC=0 PASS 222222222222222'
                    rc=doQCTrk(opath3,mpath,mpathBT,qcpath,savPath,
                               plttag=plttag2,title2=title22)
                    rc=doMd2Md3Mrg(stmid,qc2paths=qc2paths,override=1)
                    (opath3,mpath,mpathBT,savPath,savPathBT)=rc
                    (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,verb=verb)
                    rccQC=setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=3,bspdmax=bspdmax,override=0)
                    
                    plttag21='pass21'
                    title221='RCC=%d PASS 22222222211111111'%(rcc)
                    rc=doTrkPlot(opath3,override=1,doM3=1,doX=1,
                                 plttag=plttag21,title2=title21)
    
                    rc=raw_input("QC pass2 rc=%d to delete? 222 y/n  "%(rcc))
                    if(rc.lower() == 'y'):
                        mf.runcmd("rm -i %s"%(qcpath0),ropt)
                                

        
sys.exit()
    
    
