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
            'warn':             ['W',0,1,'warn if path not there'],
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

sizMin=300
headAll='h-md3-all.txt'
headSum='h-md3-sum.txt'

for year in years:
    
    rc=setCvsYearOptPaths(sbtSrcDir,year,headAll,headSum,doMergeOnly=0)
    (allCvsPath,allCvsPathBT,allCvsPathMRG,
     sumCvsPath,sumCvsPathBT,sumCvsPathMRG)=rc
    
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

            smpathMRGs=glob.glob("%s/???-%s-sum-md3-MRG.txt"%(spath,year))
            if(len(smpathMRGs) == 1): smpathMRG=smpathMRGs[0]
            else: smpathMRG=None
            
            if(smpathMRG == None):
                if(warn): print 'WWW in smpathMGR: ',smpathMRG,' with smpathMRGs: ',smpathMRGs,' sayounara'
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(smpathMRG,sumCvsPathMRG)
                mf.runcmd(cmd,ropt)
	
            
            smpathBD2s=glob.glob("%s/???-%s-sum-md3-BT.txt"%(spath,year))
            if(len(smpathBD2s) == 1): smpathBD2=smpathBD2s[0]
            else: smpathBD2=None
            
            if(smpathBD2 == None):
                if(warn): print 'WWW in smpathBD2: ',smpathBD2,' with smpathBD2s: ',smpathBD2s,' sayounara'
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(smpathBD2,sumCvsPathBT)
                mf.runcmd(cmd,ropt)

            smpaths=glob.glob("%s/???-%s-sum-md3.txt"%(spath,year))
            if(len(smpaths) == 1): smpath=smpaths[0]
            else: smpath=None
            
            if(smpath == None):
                if(warn): print 'WWW in smpath: ',smpath,' with smpaths: ',smpaths,' sayounara'
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(smpath,sumCvsPath)
                mf.runcmd(cmd,ropt)

        # -- aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # -- now do file with all
        #
        for spath in spaths:
            
            # -- all MRG
            #
            mpathMRGs=glob.glob("%s/???-%s-md3-MRG.txt"%(spath,year))
            if(len(mpathMRGs) == 1): mpathMRG=mpathMRGs[0]
            else: mpathMRG=None
    
            if(mpathMRG == None):
                if(warn): print 'EEE-%s find in mpathMRG for spath: %s year: %s ...Sayounara...'%(pypath,spath,year)
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(mpathMRG,allCvsPathMRG)
                mf.runcmd(cmd,ropt)

            # -- all BT
            #
            mpathBD2s=glob.glob("%s/???-%s-md3-BT.txt"%(spath,year))
            if(len(mpathBD2s) == 1): mpathBD2=mpathBD2s[0]
            else: mpathBD2=None
    
            if(mpathBD2 == None):
                if(warn): print 'EEE-%s find in mpathBD2 for spath: %s year: %s ...Sayounara...'%(pypath,spath,year)
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(mpathBD2,allCvsPathBT)
                mf.runcmd(cmd,ropt)

            # -- all plain
            #
            mpaths=glob.glob("%s/???-%s-md3.txt"%(spath,year))
            if(len(mpaths) == 1): mpath=mpaths[0]
            else: mpath=None
    
            if(mpath == None):
                if(warn): print 'EEE-%s find in mpath for spath: %s year: %s ...Sayounara...'%(pypath,spath,year)
                #sys.exit()
            else:
                cmd="cat %s >> %s"%(mpath,allCvsPath)
                mf.runcmd(cmd,ropt)
                      
                      
        MF.dTimer("csv-%s-%s"%(basin,year))
        
    # now cp over to sbt dir
    #
    
    sizM=MF.getPathSiz(allCvsPathMRG)
    sizB=MF.getPathSiz(allCvsPathBT)
    siz0=MF.getPathSiz(allCvsPath)
    
    print 'SSS M ',sizM,'B: ',sizB,' 0: ',siz0
    
    if(sizM > sizMin):
        cmd="cp %s %s/."%(allCvsPathMRG,sbtVerDirDat)
        mf.runcmd(cmd,ropt)
        cmd="cp %s %s/."%(sumCvsPathMRG,sbtVerDirDat)
        mf.runcmd(cmd,ropt)

    if(sizB > sizMin):
        cmd="cp %s %s/."%(allCvsPathBT,sbtVerDirDat)
        mf.runcmd(cmd,ropt)
        cmd="cp %s %s/."%(sumCvsPathBT,sbtVerDirDat)
        mf.runcmd(cmd,ropt)
        
    if(siz0 > sizMin):
        cmd="cp %s %s/."%(allCvsPath,sbtVerDirDat)
        mf.runcmd(cmd,ropt)
        cmd="cp %s %s/."%(sumCvsPath,sbtVerDirDat)
        mf.runcmd(cmd,ropt)
        
        
MF.dTimer('AAA-cvs')

