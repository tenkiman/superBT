#!/usr/bin/env python

from sBT import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'doWBTonly':        ['W',0,1,'do WorkingBT only (no -BT or -MRG'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
create big .csv with all md3 and md3-BT by year"""

        self.examples='''
%s 2007.2022'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tt=yearOpt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=mf.yyyyrange(byear, eyear)
    oyearOpt="%s-%s"%(byear,eyear)

elif(len(tt) == 1):

    years=[yearOpt]
    oyearOpt=yearOpt

else:
    print 'EEE -- invalid yearOpt: ',yearOpt

# -- merge/BT options
#
    
MF.sTimer('AAA-cvs')

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']

headAll='h-md3-all.txt'
headSum='h-md3-sum.txt'

rc=setCvsYearOptPaths(sbtSrcDir,oyearOpt,headAll,headSum,doMergeOnly=0)
(allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)=rc

for year in years:
    
    tdir="%s/%s"%(sbtSrcDir,year)
    if(not(MF.ChkDir(tdir))):
        print 'tdir not there...'
        sys.exit()

    for basin in basins:

        btdir="%s/%s"%(tdir,basin)
        if(not(MF.ChkDir(btdir))):
            print 'btdir not there...'
            sys.exit()

        MF.sTimer("csv-%s-%s"%(basin,year))
        
        smask="%s/%s/*"%(tdir,basin)
        spaths=glob.glob(smask)
        spaths.sort()

        # -- ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # -- first summary
        #
        for spath in spaths:
            
            smpathBD2s=glob.glob("%s/???-%s-sum-md3-BT.txt"%(spath,year))
            if(len(smpathBD2s) == 1): smpathBD2=smpathBD2s[0]
            else: smpathBD2=None
            
            if(smpathBD2 == None):
                print 'problem in smpathMGR: ',smpathBD2,' with smpathBD2s: ',smpathBD2s,' sayounara'
                sys.exit()
            else:
                cmd="cat %s >> %s"%(smpathBD2,sumCvsPathBT)
                mf.runcmd(cmd,ropt)

        # -- aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # -- now do file with all
        #
        for spath in spaths:
            
            mpathBD2s=glob.glob("%s/???-%s-md3-BT.txt"%(spath,year))
            if(len(mpathBD2s) == 1): mpathBD2=mpathBD2s[0]
            else: mpathBD2=None
    
            if(mpathBD2 == None):
                print 'EEE-%s find in mpathBD2 for spath: %s year: %s ...Sayounara...'%(pypath,spath,year)
                sys.exit()
            else:
                cmd="cat %s >> %s"%(mpathBD2,allCvsPathBT)
                mf.runcmd(cmd,ropt)
                      
        MF.dTimer("csv-%s-%s"%(basin,year))
        
# now cp over to sbt dir
#
cmd="cp %s %s/."%(allCvsPathBT,sbtVerDirDat)
mf.runcmd(cmd,ropt)

cmd="cp %s %s/."%(sumCvsPathBT,sbtVerDirDat)
mf.runcmd(cmd,ropt)
MF.dTimer('AAA-cvs')

