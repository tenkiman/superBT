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
            'doDelete':         ['d',0,1,' use --delete option'],
            'doRmvSrcFiles':    ['r',0,0,' NEVER use ...remove locally'],
            'doCleanLocal':     ['K',0,1,' rm */*/* local'],
            'doLsLocal':        ['l',0,1,' do local ls -la'],
            'doLsRemote':       ['L',0,1,' do ls -la on RAID02'],
           
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

# -- set rsync type
#
if(doIt and ropt == ''): 
    rsyncType='-alv'
elif(doIt and ropt == 'norun'):
    rsyncType='-alvn'
    ropt=''
else:
    rsyncType='-alvn'

# -- clean local
#
if(doCleanLocal):
    if(doIt):
        ropt=''
    else:
        ropt='norun'
    
# -- set source/target dirs
#
if(rType == 'dat'):
    sdir=sbtDatDirL
    tdir=sbtDatDir
    exOpt='--exclude INV'
    exOpt=''
    
elif(rType == 'prod'):
    sdir=sbtProdDirDiagL
    tdir=sbtProdDirDiag

else:
    print """EEE -- invalid rType -- must be either 'dat' | 'prod'"""
    sys.exit()

# -- set rsync opts
#
rsfOpt=''
if(doRmvSrcFiles):
    rsfOpt='--remove-source-files'

delOpt=''
if(doDelete):delOpt='--delete'

exOpt=''
#if(rType == 'dat'): exOpt='--exclude INV'
     
rsyncOpt="%s %s %s %s"%(rsyncType,rsfOpt,delOpt,exOpt)
    
year=ymdOpt[0:4]
tymd="%s/"%(year)
if(len(ymdOpt) == 4):
    symd="%s/"%(year)
elif(len(ymdOpt) == 5):
    symd='''%s/%s?????'''%(year,ymdOpt)
elif(len(ymdOpt) == 6):
    symd='''%s/%s????'''%(year,ymdOpt)
elif(len(ymdOpt) == 7):
    symd='''%s/%s???'''%(year,ymdOpt)
elif(len(ymdOpt) == 8):
    symd='''%s/%s??'''%(year,ymdOpt)
elif(len(ymdOpt) == 9):
    symd='''%s/%s?'''%(year, ymdOpt)
else:
    print 'EEE bad ymdOpt',ymdOpt,' must be between 4,6,7,8,9 len'
    sys.exit()
    
    
if(rType == 'dat'): 
    sdir="%s/tcdiag"%(sdir)
    tdir="%s/tcdiag"%(tdir)

if(verb):
    print 'SSS: ',sdir
    print 'TTT: ',tdir
    print 'YMD: ',symd
    print 'RRR: ',rsyncOpt

MF.sTimer('rsync-%s-%s-%s'%(sbtHost,ymdOpt,rType))
cmd="rsync %s %s/%s %s/%s"%(rsyncOpt,sdir,symd,tdir,tymd)
if(doCleanLocal):  
    cmd="rm %s/%s/*/*"%(sdir,symd)
    cmd='''for f in %s/%s/*/* ; do echo rm $f ; rm $f ; done'''%(sdir,symd)
    cmd2='''for f in %s/%s/*/*/* ; do echo rm $f ; rm $f ; done'''%(sdir,symd)
elif(doLsLocal):
    cmd="ls -la %s/%s/*"%(sdir,symd)
elif(doLsRemote):
    cmd="ls -la %s/%s/*"%(tdir,symd)
    
#print 'ccc: ',cmd,'ropt: ',ropt,' <==='
if(rType == 'prod'):
    cmd=cmd2
mf.runcmd(cmd,ropt)
mf.runcmd(cmd2,ropt)
    

    
MF.dTimer('rsync-%s-%s-%s'%(sbtHost,ymdOpt,rType))
    

sys.exit()


