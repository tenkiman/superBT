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
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doIt':             ['X',0,1,' execute'],
            'doDelete':         ['d',0,1,' use -d to delete files on the targe if not on the source'],
            'doKill':           ['K',0,1,' do kill if # of files the same on both local/remote'],
            'ymdOpt':           ['Y:',None,'a','ymdOpt for setting dirs to rsync'],
            'rType':            ['R:',None,'a','type of rsync dat | prod'],
           
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by ymdOpt and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

def getLsTdiagLocalRemote(app,ymdOpt, doPrint= 0):

    lsOpts=[
        "-Y %s -R %s -l | wc -l"%(ymdOpt,rType),
        "-Y %s -R %s -L | wc -l"%(ymdOpt,rType),
    ]
    
    roptls=''
    localls=-999
    remotels=-999
    for lsOpt in lsOpts:
        cmd="%s %s"%(app,lsOpt)
        rc=mf.runcmd2(cmd, roptls, verb=verb, lsopt='q', prefix='', postfix='', ostdout=1, wait=False)
        if(rc[0] == 1):
            if(mf.find(lsOpt,'-l | ')):
                localls=int(rc[1][0])
            if(mf.find(lsOpt,'-L | ')):
                remotels=int(rc[1][0])
                
    if(doPrint):
        print 'lll--local  ls: ', localls
        print 'LLL--remote ls: ', remotels
        
        
    return(localls,remotels)



argv=sys.argv
CL=TcdiagCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(rType == 'all'):
    rTypes=['dat','prod']
else:
    rTypes=[rType]
    
ymdOpts=ymdOpt.split(',')

if(not(mf.find(str(rTypes),'dat') or mf.find(str(rTypes),'prod'))):
    print 'EEE -R must be either dat or prod'
    sys.exit()


app="r-rsync-tcdiag-local-output.py"

ropt='norun'

MF.sTimer('AAA-RRR-%s'%(str(ymdOpts)))

delOpt=''
if(doDelete): delOpt='-d'
    
# -- do rsync of local to remote with option to delete not on remote (-d)
#
ropt = 'norun'
didRsync = 0
if(doIt): ropt = ''
     
for rType in rTypes:
    for ymdOpt in ymdOpts:

        # -- bypass actual rsync...if doing kill or 'norun'
        #
        if(doKill): continue

        rsyncOpt="-Y %s %s -R %s -N"%(ymdOpt,delOpt,rType)
        if(doIt):
            rsyncOpt="-Y %s %s -R %s -X"%(ymdOpt,delOpt,rType)
                 
        MF.sTimer("all-rsync-%s-%s"%(ymdOpt,rType))
        cmd="%s %s"%(app,rsyncOpt)
        mf.runcmd(cmd, ropt)
        MF.dTimer("all-rsync-%s-%s"%(ymdOpt,rType))
        
        # -- set rsync flag
        #
        if(doIt): didRsync = 1
        
        
# -- do listing and kill of local files
#
ropt = 'norun'
if(didRsync): doIt = 0

for rType in rTypes:
    
    for ymdOpt in ymdOpts:

        if(doIt): ropt = ''
             
        rsyncOpt="-Y %s %s -R %s -N"%(ymdOpt,delOpt,rType)
        killOpt="-Y %s %s -R %s -K -X"%(ymdOpt,delOpt,rType)
        killOptNorun="-Y %s %s -R %s -K -N"%(ymdOpt,delOpt,rType)
        
        (localls,remotels)=getLsTdiagLocalRemote(app,ymdOpt)
        print '%4s ymd: %s   lll-local: %6d'%(rType,ymdOpt,localls),' LLL-remote: %6d'%(remotels)
        cmd="%s %s"%(app,killOpt)
        cmdno="%s %s"%(app,killOptNorun)
        
        if(doKill and doIt):
            mf.runcmd(cmd, ropt)
            (localls,remotels)=getLsTdiagLocalRemote(app,ymdOpt)
            print 'AfterKill -- %4s ymd: %s   lll-local: %6d'%(rType,ymdOpt,localls),' LLL-remote: %6d'%(remotels)
        else:
            mf.runcmd(cmdno, 'norun',lsopt='q')


MF.dTimer('AAA-RRR-%s'%(str(ymdOpts)))

sys.exit()


