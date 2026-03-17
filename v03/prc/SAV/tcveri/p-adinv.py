#!/usr/bin/env python

from ad2vm import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['v',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a','stmopt1:stmopt2:stmopt3...'],
            'lsAll':            ['a',0,1,'list all aids'],
            'lsProb':           ['p',0,1,'only list problems'],
            'dobt':             ['b',1,0,'only do NN is the default'],
            'add00':            ['0',0,1,'add 00 to aids for bias-corrected'],
            'doVdeck':          ['V',0,1,' make vdecks'],
            'doAdeck':          ['A',0,1,' make ad2 with 0 interp'],
            'pStat':            ['s:','pe','a',' type of stat'],
        }

        self.purpose="""'
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
    
years=range(1945,2024+1)
aidStms=loadAd2Inv(years)

aidstrs=[]
aidsStmOpt={}

prcdir='/w21/prc/tcdat'

MF.sTimer('atcf-ALL-%s'%(istmopt))
for stmopt in stmopts:
    
    aidstrs=[]
    MF.sTimer('atcf-stmopt-%s'%(stmopt))
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt)
    
    for tstmid in tstmids:
        
        #if(Is9X(tstmid)): continue
            
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
            
            try:
                aids=aidStm[utstmid2]
            except:
                print 'really no trackers for tstmid: ',tstmid
                continue
            
            if(len(aids) == 0):
                print 'no aids for tstmid: ',tstmid,'tstmid2: ',tstmid2
                continue

            if(lsAll):
                aidstr=makeAidStr(aids)
                print 'tstmid: %s tstmid2: %s'%(tstmid,tstmid2),'  %s aids: %s'%(aidpre,aidstr[0:120])
            else:
                ecmstr=getEcmwfAid(aids,year,verb=verb)
                clpstr=getClipperAid(aids,verb=verb)
                humstr=getHumanAid(aids,verb=verb)
                modstr=getModelAid(aids,verb=verb)
                

        if(not(lsAll)):
    
            aidstr="%s,%s,%s,%s"%(ecmstr,clpstr,humstr,modstr)
            aidstr=aidstr.replace(',,',',')
            aidstr=aidstr.replace(',,','')
            if(len(aidstr) > 0):
                if(aidstr[-1] == ','): aidstr=aidstr[0:-1]
            aidstrs.append((tstmid,aidstr))
            if(verb): print 'AAA: ',tstmid,aidstr
            
    aidsStmOpt[stmopt]=aidstrs
              
MF.sTimer('AV-inv-All')              
for stmopt in stmopts:
    
    aidstrs=aidsStmOpt[stmopt]

    ptype=None
    if(doVdeck and not(doAdeck)): ptype='vdeck'
    if(doAdeck and not(doVdeck)): ptype='adeck'
    if(doAdeck and doVdeck):      ptype='both'
        
    rc=aidstrAnl(aidstrs,add00=add00,verb=verb)
    (taids,vaids,aaids,taids00,vaids00,aaids00,tstmids)=rc

    nstms=len(tstmids)

    if(ptype == None and not(lsAll)):
        
        print 'Nstms %2d for stmopt: %s aidopts: ' %(nstms,stmopt)
        print '   aaids: ',aaids
        print '   vaids: ',vaids
        print '   taids: ',taids
        
        print ' aaids00: ',aaids00
        print ' vaids00: ',vaids00
        print ' taids00: ',taids00
        

    if(ptype == 'adeck' or ptype == 'both'):

        if(nstms == 0):
            print
            print 'NNN no stms for stmopt: ',stmopt,'press...'
            print
            continue
        else:
            print 'AAA Nstms %2d for stmopt: %s doing: %s'%(nstms,stmopt,ptype)

        logpath='./vd2inv/ad2inv-%s.txt'%(stmopt)
        lsiz=MF.getPathSiz(logpath)
        print 'log for %s: lsiz: %4d'%(stmopt,lsiz)
        if(lsiz > 0 and not(override)):
            print 'WWW %s already done'%(stmopt)
            continue
        MF.sTimer('AD2-h0-%s'%(stmopt))
        aapp='w2-tc-dss-ad2.py'
        cmd='''%s/%s -S %s -T %s -h 0 -O1 -W -B | tee %s'''%(prcdir,aapp,stmopt,aaids,logpath)
        mf.runcmd(cmd,ropt)
        MF.dTimer('AD2-h0-%s'%(stmopt))
        

    if(ptype == 'vdeck' or ptype == 'both'):

        if(nstms == 0):
            print 'NNN no stms for stmopt: ',stmopt,'press...'
            continue
        else:
            print 'VVV Nstms %2d for stmopt: %s doing: %s'%(nstms,stmopt,ptype)

        if(pStat == 'pod'):
            logpath='./vd2inv/vd2inv-%s-pod.txt'%(stmopt)
            psopt='-p pod'
            taopt=vaids
            taopt00=vaids00
        else:
            logpath='./vd2inv/vd2inv-%s.txt'%(stmopt)
            psopt=''
            taopt=taids
            taopt00=taids00
        lsiz=MF.getPathSiz(logpath)
        print 'log for %s: lsiz: %4d'%(stmopt,lsiz)
        
        ovopt=''
        if(lsiz > 0 and not(override)):
            print 'WWW %s already done'%(stmopt)
            continue

        if(lsiz <= 0 or override):
            ovopt='-O'
        
        if(pStat == 'pod' and not(override)):
            ovopt=''
            
        MF.sTimer('vd2-%s'%(stmopt))
        vapp='w2-tc-dss-vd2-anl.py'
        cmd='''%s/%s -S %s -T %s %s %s -H | tee %s'''%\
            (prcdir,vapp,stmopt,taopt,ovopt,psopt,logpath)
        mf.runcmd(cmd,ropt)
        if(add00):
            cmd='''%s/%s -S %s -T %s %s %s -H | tee -a %s'''%\
                (prcdir,vapp,stmopt,taopt00,ovopt,psopt,logpath)
            mf.runcmd(cmd,ropt)
        MF.dTimer('vd2-%s'%(stmopt))
        
MF.dTimer('AV-inv-All')              
        
sys.exit()
