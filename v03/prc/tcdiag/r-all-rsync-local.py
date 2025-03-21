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
            'ymdOpt':           ['Y:',None,'a','ymdOpt for setting dirs to rsync'],
            'rType':            ['R:',None,'a','type of rsync dat | prod'],
           
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by ymdOpt and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TcdiagCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(rType == None or (rType != 'dat' and rType != 'prod')):
    print 'EEE -R must be either dat or prod'
    sys.exit()


app="r-rsync-tcdiag-local-output.py"

ropt='norun'
rsyncOpt="-Y %s -d -R %s -N"%(ymdOpt,rType)

if(doIt):
    rsyncOpt="-Y %s -d -R %s -X"%(ymdOpt,rType)
    ropt=''

lsOpts=[
    "-Y %s -d -R %s -l | wc -l"%(ymdOpt,rType),
    "-Y %s -d -R %s -L | wc -l"%(ymdOpt,rType),
]

killOpt="-Y %s -d -R %s -K -X"%(ymdOpt,rType)


MF.sTimer("all-rsync-%s"%(ymdOpt))
cmd="%s %s"%(app,rsyncOpt)
mf.runcmd(cmd, ropt)
    
roptls=''
localls=-999
remotels=-999
for lsOpt in lsOpts:
    cmd="%s %s"%(app,lsOpt)
    #mf.runcmd(cmd, ropt)
    rc=mf.runcmd2(cmd, roptls, verb=verb, lsopt='', prefix='', postfix='', ostdout=1, wait=False)
    if(rc[0] == 1):
        if(mf.find(lsOpt,'-l | ')):
            localls=int(rc[1][0])
            #print 'lll',localls
        if(mf.find(lsOpt,'-L | ')):
            remotels=int(rc[1][0])
            #print 'LLL',remotels

print 'lll: ',localls,' LLL: ',remotels            
cmd="%s %s"%(app,killOpt)
if(localls == remotels):
    mf.runcmd(cmd, ropt)
else:
    print 'WWW -- diff in # of local v remote'
    mf.runcmd(cmd, 'norun')

MF.sTimer("all-rsync-%s"%(ymdOpt))

sys.exit()


