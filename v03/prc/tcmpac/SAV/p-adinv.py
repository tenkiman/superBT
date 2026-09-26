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
    
    (aidstrs,tstmids,faidstr)=getAidstrs(stmopt,aidStms,verb=verb)
    aidsStmOpt[stmopt]=(aidstrs,faidstr)
              
MF.sTimer('AV-inv-All')              
for stmopt in stmopts:
    
    (aidstrs,faidstr)=aidsStmOpt[stmopt]

    ptype=None
    if(doVdeck and not(doAdeck)): ptype='vdeck'
    if(doAdeck and not(doVdeck)): ptype='adeck'
    if(doAdeck and doVdeck):      ptype='both'
        
    rc=aidstrAnl(aidstrs,faidstr,add00=add00,verb=verb)
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
