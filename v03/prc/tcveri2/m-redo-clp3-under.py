#!/usr/bin/env python

from ad2vm import *

def redoByStmopt(stmopt,basin,year,ropt):
    
    # -- first do bd2
    #
    MF.sTimer('bd2-%s'%(stmopt))
    cmd='m-sbt-bd2.py -S %s'%(stmopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('bd2-%s'%(stmopt))
    
    # -- then clp3
    #
    MF.sTimer('clp3-%s'%(stmopt))
    MF.ChangeDir('../tcclp3')
    cmd='p-clp3.py -S %s'%(stmopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('clp3-%s'%(stmopt))
    
    MF.ChangeDir('../tcveri2')
    
    # -- then ad2
    #
    MF.sTimer('ad2-%s'%(stmopt))
    cmd='m-ad2inv.py -Y %s -B %s -E -C -0'%(year,basin)
    mf.runcmd(cmd,ropt)
    MF.dTimer('ad2-%s'%(stmopt))
    
    MF.sTimer('vd2-%s'%(stmopt))
    cmd='m-vdinv.py -Y %s -B %s -O'%(year,basin)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vd2-%s'%(stmopt))
    
    MF.sTimer('vd2-z0012-%s'%(stmopt))
    cmd='m-vdinv.py -Y %s -B %s -f z0012'%(year,basin)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vd2-z0012-%s'%(stmopt))
    
    
    return(1)

def redoByStmid(stmopt,basin,year,ropt):

    def anlLog(cards,tstmid,dols=0,dobad=0):
        badtstmids=[]
        badcards=[]
        for card in cards:
            
            aidtest=mf.find(card,'clp3')
            if(dols or (not(dols) and dobad)): 
                aidtest=(mf.find(card,'clp3') or mf.find(card,'tera5'))
                
            if(mf.find(card,'pod') and 
               aidtest and
               not(mf.find(card,'nada')) and
               not(mf.find(card,' 96')) and
               not(mf.find(card,' 120')) and
               not(mf.find(card,' 100.0 N')) 
               ):
                ocard="%s %s"%(tstmid,card[20:])
                if(dols):
                    print ocard
                if(dobad):
                    if(dols): print ocard
                    badcards.append(ocard)
                badtstmids.append(tstmid)
                
        badtstmids=mf.uniq(badtstmids)
        #if(len(badtstmids) > 0): print 'bbb',badtstmids
        return(badtstmids,badcards)
        
    prcdir='/w21/prc/tcdat'
    vapp='w2-tc-dss-vd2-anl.py'
    vdaid='clp3,tera5'

    dtgopt=None
    yearOpt=year
    dobt=1
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
    doBT=0
    if(doBdeck2): doBT=1
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    tstmids=md3.getMd3Stmids(stmopt,dobt=dobt,verb=verb)
    
    MF.sTimer('vd2-%s'%(stmopt))
    badtstmids=[]
    for tstmid in tstmids:
        cmd='''%s/%s -S %s -T %s -p pod'''%\
            (prcdir,vapp,tstmid,vdaid)
        cards=MF.runcmdLog(cmd,ropt,quiet=1)
        (obadtstmids,obadcards)=anlLog(cards,tstmid,dols=0,dobad=0)
        badtstmids=badtstmids+obadtstmids
    MF.dTimer('vd2-%s'%(stmopt))
        
    badtstmids=mf.uniq(badtstmids)
    badcards=[]
    for badtstmid in badtstmids:
        cmd='''%s/%s -S %s -T %s -p pod'''%\
            (prcdir,vapp,badtstmid,vdaid)
        cards=MF.runcmdLog(cmd,ropt,quiet=1)
        (obadtstmids,obadcards)=anlLog(cards,badtstmid,dols=0,dobad=1)        
        badcards=badcards+obadcards
        
    badcards=mf.uniq(badcards)
    return(badcards)
    
    

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
            'stmopt':           ['S:',None,'a','stmopt to process'],
            'byStm':            ['Y',0,1,' run process to dectect problem stmid'],
            'podmin':           ['P:',98.5,'f',' set the minimum pod for find unders...'],
            'targetTau':        ['t:',None,'i',' set the target taus'],
        }

        self.purpose="""
redo clp3 for stmops with under 100%% PoD"""

        self.examples='''
%s -S w.2009'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)

if(stmopt == None):
    print 'you must set stmopt'
    sys.exit()
else:
    (basin,year)=stmopt.split('.')
    
tauopt=''
if(targetTau != None):
    tauopt='-t %d'%(targetTau)
    otargetTau=str('%d'%(targetTau))
else:
    targetTau=''
    otargetTau=''
    
print 'otargetTau',otargetTau

bversion='v01'
MF.sTimer('ALL-%s'%(stmopt))
if(not(byStm)):
    rc=redoByStmopt(stmopt,basin,year,ropt)
else:
    opodmin="%4.1f"%(float(podmin))
    opodmin=opodmin.replace('.','p')
    ostmopt=stmopt.replace('.','-')
    badpath='underinv/bad-%s-%s-%s-%s.txt'%(ostmopt,opodmin,otargetTau,bversion)
    badcards=redoByStmid(stmopt,basin,year,ropt)
    for badcard in badcards:
        print 'oo',badcard
    MF.WriteList2Path(badcards,badpath)
    
MF.dTimer('ALL-%s'%(stmopt))