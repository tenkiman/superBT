#!/usr/bin/env python

from WxMAP2 import *
from sBT import *

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
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'redoClp3Ad2':      ['C',0,1,'redoClp3Ad2 only'],
            'doAd2Inv':         ['I',1,0,'do NOT do ad2inv'],
            'dobt':             ['b',1,0,'only do NN is the default'],
            'redoTrk':          ['R',0,1,' run tracker for missing dtgs'],
            'redoEra5Ad2':      ['E',0,1,' redoEra5Ad2 only'],
            'redoAd2':          ['2',0,1,' redo entire year of ad2...deleting old ones'],
            'redoAd2Phr0':      ['0',0,1,' only redo phr0 -- when we force use of bt in interp'],
            'doAd2InvOnly':     ['i',0,1,' ONLY do ad2inv'],
            
        }

        self.purpose="""
make era5 ad2  and inventory in both .txt and .pyp"""

        self.examples='''
%s -Y 1969.1970'''
    

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    

years=yearOptPrc(yearOpt)

def makeStmOptByBasin(year):
    basins=['i','h','w','c','e','l']
    stmopt=''
    for b in basins:
        if(stmopt == ''):
            stmopt="%s.%s"%(b,year)
        else:
            stmopt="%s,%s.%s"%(stmopt,b,year)
    return(stmopt)

if(doAd2InvOnly):
    redoAd2=0
    redoAd2Phr0=0
    doAtcf=0
    redoClp3Ad=0
    doAd2Inv=1

MF.sTimer('Mk-Ad-All')

for year in years:

    syear=str(year)
    opath='adinv/adinv-%s.txt'%(year)
    
    if(redoAd2):
        
        # -- kill previous ad2
        #
        dsbdir='/w21/dat/tc/DSs'
        dsbdir='./DSs-local'
        cmd='rm  %s/ad2-??-%s.pypdb'%(dsbdir,syear)
        mf.runcmd(cmd,ropt)

        cmd='rm -i %s/bd2-%s.pypdb'%(dsbdir,syear)
        mf.runcmd(cmd,ropt)

        MF.sTimer('redoAd2-%s'%(syear))
        cmd='/w21/prc/tcdat/w2-tc-dss-ad2.py all -o -S all.%s -O1 -W'%(syear)
        mf.runcmd(cmd,ropt)
        MF.dTimer('redoAd2-%s'%(syear))
    
    if(redoEra5Ad2):
        
        MF.sTimer('redoEra5Ad2-%s'%(syear))
        cmd='/w21/prc/tcdat/w2-tc-dss-ad2.py era5 -S all.%s -O1 -W'%(syear)
        mf.runcmd(cmd,ropt)
        MF.dTimer('redoEra5Ad2-%s'%(syear))


    if(redoClp3Ad2):
        
        MF.sTimer('atcf-CLP3-%s'%(syear))
        cmd='/w21/prc/tcdat/w2-tc-dss-ad2.py clp3 -S all.%s -O1 -s -W'%(syear)
        mf.runcmd(cmd,ropt)
        MF.dTimer('atcf-CLP3-%s'%(syear))

        MF.sTimer('adinv-%s'%(syear))
        cmd='/w21/prc/tcdat/w2-tc-dss-ad2.py -S all.%s -L > %s'%(syear,opath)
        mf.runcmd(cmd,ropt)
        MF.dTimer('adinv-%s'%(syear))
        
        if(ropt != 'norun'):
            MF.sTimer('adinv-pyp-%s'%(syear))
            rc=parseAd2Inv(syear)
            MF.dTimer('adinv-pyp-%s'%(syear))
        

    # -- now do the ad2 -h 0
    #
    if(redoAd2 or redoAd2Phr0):
        
        MF.sTimer('ad2-phr0-%s'%(syear))
        cmd='p-adinv.py -S all.%s -A -O'%(syear)
        mf.runcmd(cmd,ropt)
        MF.dTimer('ad2-phr0-%s'%(syear))
        
    # -- always do by default
    #
    if(doAd2Inv):
        
        MF.sTimer('adinv-%s'%(syear))
        cmd='/w21/prc/tcdat/w2-tc-dss-ad2.py -S all.%s -L > %s'%(syear,opath)
        mf.runcmd(cmd,ropt)
        MF.dTimer('adinv-%s'%(syear))
        
        if(ropt != 'norun'):
            MF.sTimer('adinv-pyp-%s'%(syear))
            rc=parseAd2Inv(syear)
            MF.dTimer('adinv-pyp-%s'%(syear))
        
        
        
    
MF.dTimer('Mk-Ad-All')
