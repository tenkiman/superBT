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

rc=setCvsYearOptPaths(sbtSrcDir,oyearOpt,headAll,headSum,doWBTonly=doWBTonly)
(allCvsPathMRG,sumCvsPathMRG)=rc

# -- don't make -BT.csv just .csv and -MRG.csv
#

for year in years:
    
    rc=setCvsYearOptPaths(sbtSrcDir,year,headAll,headSum,doMergeOnly=0)
    (allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)=rc
    print 'yyyy----',year,allCvsPath

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
            
            smpaths=smpathsBTs=[]
            smpathMRGs=glob.glob("%s/???-%s-sum-md3-MRG.txt"%(spath,year))
            if(len(smpathMRGs) == 1): smpathMRG=smpathMRGs[0]
            else: smpathMRG=None
            
            if(smpathMRG == None):
                print 'problem in smpathMGR: ',smpathMRG,' with smpathMRGs: ',smpathMRGs,' sayounara'
                sys.exit()
            else:
                cmd="cat %s >> %s"%(smpathMRG,sumCvsPathMRG)
                mf.runcmd(cmd,ropt)

        # -- aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # -- now do file with all
        #
        # -- MMMMRRRGGG - merge has aready been done using m-md3-mrg-stm-dir-sum.py
        #
        for spath in spaths:
            
            mpathMRGs=glob.glob("%s/???-%s-md3-MRG.txt"%(spath,year))
            if(len(mpathMRGs) == 1): mpathMRG=mpathMRGs[0]
            else: mpathMRG=None
    
            if(mpathMRG == None):
                print 'EEE-%s find in mpathMRG for spath: %s year: %s ...Sayounara...'%(pypath,spath,year)
                sys.exit()
            else:
                cmd="cat %s >> %s"%(mpathMRG,allCvsPathMRG)
                mf.runcmd(cmd,ropt)
                      
            
        if(doWBTonly):
            
            # -- DOOOOOOOOOOOMMMMMMEEEEEEERRRRRRRRRRGGGGGGGEEEEEEEEE
            # -- do md3 md3-BT and make md3-MRG
            # -- first all working
            #
            for spath in spaths:
                
                mpaths=glob.glob("%s/???-%s-md3.txt"%(spath,year))
    
                if(len(mpaths) == 1): mpath=mpaths[0]
                else: mpath=None
    
                if(mpath == None): 
                    print 'problem in spath: ',spath,' with mpaths: ',mpaths,' sayounara'
                    sys.exit()
    
                cmd="cat %s >> %s"%(mpath,allCvsPath)
                mf.runcmd(cmd,ropt)
                
        MF.dTimer("csv-%s-%s"%(basin,year))
        
# now cp over to sbt dir
#
cmd="cp %s %s/."%(allCvsPathMRG,sbtVerDirDat)
mf.runcmd(cmd,ropt)
cmd="cp %s %s/."%(sumCvsPathMRG,sbtVerDirDat)
mf.runcmd(cmd,ropt)

MF.dTimer('AAA-cvs')

