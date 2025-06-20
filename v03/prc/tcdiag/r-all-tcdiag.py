#!/usr/bin/env python

from sBT import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TcdiagCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doLog':            ['L',1,0,'do NOT do logfile to raid02/log'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'doBdeck2':         ['2',0,1,'using bdeck at command line vice in getYears4Opts'],
            'doLats4d':         ['4',1,0,'do NOT do lats4d of .dat -> .grb'],
            'lats4dInc':        ['I:',None,'i','dtg inc to output all grids using lats4d'],
            'doTcFc':           ['f',0,1,'''increase taus for forecasting purposes...'''],
            'doLocal':          ['C',0,1,'''run on local filesystem in /sbt/local'''],
            
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019
%s all -S 11p.98 # set dtgs with stmid
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TcdiagCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(dtgopt != None and mf.find(dtgopt,'all')):
    dtgopt=None

if(dtgopt != None): MF.sTimer('AAA-TCDIAG-%s'%(dtgopt))
if(stmopt != None): MF.sTimer('AAA-TCDIAG-%s'%(stmopt))

if(dtgopt != None and stmopt == None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
elif(stmopt != None and dtgopt == None):
    dtgs=None
else:
    print 'EEE--(%s) must set either dtgopt or stmopt alone...sayounara'%(CL.pyfile)
    sys.exit()

# -- get md3
#
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
doBT=0
if(doBdeck2): doBT=1
    
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
 
if(dtgs == None):
    syear=None
    dtgs=md3.getMd3StmDtgs4Stmopt(stmopt,syear=syear)
    
if(doLog):
    if(dtgopt != None and stmopt == None): 
        logName=dtgopt.replace('.','-')
        logName=logName.replace(',','-')
    elif(stmopt != None and dtgopt == None): 
        logName=stmopt.lower()
        logName=logName.replace(',','-')
    else:
        logName="%s-%s"%(dtgopt,stmopt)
    
    sbldir = sbtLogDir
    if(doLocal): sbldir = sbtLogDirL
         
    
    logPath="%s/loG-%s-sbt-tcdiag-%s.txt"%(sbldir,sbtHost,logName)
        
    # -- allways append
    #if(MF.ChkPath(logPath)):
        #cmd="rm -i %s"%(logPath)
        #mf.runcmd(cmd)
    
    print 'LLL -- logging to: %s'%(logPath)
    
if(doLog): 
    logOpt=">> %s 2>&1"%(logPath)
else:      
    logOpt=""

if(dtgopt != None): MF.sTimer('AAA-TCDIAG-%s'%(dtgopt))
if(stmopt != None): MF.sTimer('AAA-TCDIAG-%s'%(stmopt))

# -- options

oopt=''
if(override): oopt='-O'

# -- set stmopt to '' to tcdiag unless override
sopt=''
if(stmopt != None and override): sopt='-S %s'%(stmopt)

fopt=''
if(doTcFc): fopt='-f'
lopt = ''
if(doLocal): lopt ='-C'     
vopt=''
if(verb): vopt='-V'
    


if(lats4dInc != None):
    if(lats4dInc < 0):
        doLats4d=0
        lats4dInc=999
else:
    lats4dInc=18
    
    
bdtg = dtgs[0]

# -- use 010100 as the start for doing the all lats every 18 h
#
bdtgLats= "%s010100"%(bdtg[0:4])

for dtg in dtgs:
    
    tdtg=dtg
    if(IsBadEra5Dtg(tdtg) == 0):
        print 'EEE---BBB era5 dtg...press...'
        continue
    
    # -- set up doing lats4d
    #
    latsOpt=''
    if(doLats4d):
        
        if(lats4dInc <= 24):

            hourDtg = mf.dtgdiff(bdtgLats, dtg)
            doAutoLats = hourDtg % lats4dInc
            if(doLats4d and doAutoLats == 0): latsOpt = '-4'
            
        else:
            latsOpt=''
            
    # -- run tcdiag
    #
    MF.sTimer('sbt-TCDIAG-%s-lats: %s'%(dtg,latsOpt))
    cmd="s-sbt-tcdiag.py %s %s %s %s %s %s %s %s"%(dtg,sopt,fopt,oopt,lopt, latsOpt,logOpt,vopt)
    mf.runcmd(cmd,ropt)
    # -- sleep for 5 s to see if the coredumps on mike6 come from memory not cleaning
    #
    sleep(2)
    MF.dTimer('sbt-TCDIAG-%s-lats: %s'%(dtg,latsOpt))
    
if(dtgopt != None): MF.dTimer('AAA-TCDIAG-%s'%(dtgopt))
if(stmopt != None): MF.dTimer('AAA-TCDIAG-%s'%(stmopt))

sys.exit()


