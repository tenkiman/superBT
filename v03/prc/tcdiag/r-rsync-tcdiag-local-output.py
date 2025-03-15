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

print 'ddd',sbtDatDirL,sbtDatDir,'ppp',sbtProdDirL,sbtProdDir

if(doIt and ropt == ''): 
    rsyncType='-alv'
elif(doIt and ropt == 'norun'):
    rsyncType='-alvn'
    ropt=''
else:
    rsyncType='-alvn'
    
    
if(rType == 'dat'):
    sdir=sbtDatDirL
    tdir=sbtDatDir
    
elif(rType == 'prod'):
    sdir=sbtProdDirL
    tdir=sbtProdDir

else:
    print """EEE -- invalid rType -- must be either 'dat' | 'prod'"""
    sys.exit()

datDirs={
    'dat':('tcdiag','%s --remove-source-files --delete --exclude INV'%(rsyncType)),
    'prod':('','%s --remove-source-files'%(rsyncType)),
}

year=ymdOpt[0:4]
tymd="%s/"%(year)
if(len(ymdOpt) == 4):
    symd="%s/"%(year)
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
    
    
MF.sTimer('rsync-%s-%s-%s'%(sbtHost,ymdOpt,rType))
(datdir,rsyncOpt)=datDirs[rType]
cmd="rsync %s %s/%s/%s %s/%s/%s"%(rsyncOpt,sdir,datdir,symd,
                                        tdir,datdir,tymd)
mf.runcmd(cmd,ropt)
MF.dTimer('rsync-%s-%s-%s'%(sbtHost,ymdOpt,rType))
    

sys.exit()


