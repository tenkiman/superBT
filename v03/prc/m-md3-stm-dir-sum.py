#!/usr/bin/env python

from sbt import *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['yearopt', 'bYYYY.eYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doTrk':            ['T',1,0,'do NOT make the track files'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=mf.yyyyrange(byear, eyear)
    
elif(len(tt) == 1):
    
    years=[yearopt]
    
else:
    print 'EEE -- invalid yearopt: ',yearopt


# -- work in the current version
#
sbtSrcDir=sbtSrcDir

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']

MF.sTimer('sum-md3-ALL')

for year in years:
    tdir="%s/%s"%(sbtSrcDir,year)
    MF.ChkDir(tdir,'mk')
    for basin in basins:

        btdir="%s/%s"%(tdir,basin)
        MF.ChkDir(btdir,'mk')

        bopt="%s.%s"%(basin[0],year)
        if(basin == 'epac'):
            bopt=bopt+',c.%s'%(year)
            
        if(basin == 'shem'):
            bopt='h.%s'%(year)
            
        smask="%s/%s/*"%(tdir,basin)
        
        sdirs=glob.glob(smask)
        sdirs.sort()

        MF.sTimer('sum-md3-%s-%s'%(basin,year))

        for sdir in sdirs:
            
            mpaths=glob.glob("%s/*-sum.txt"%(sdir))
            mpathBTs=glob.glob("%s/*-sum-BT.txt"%(sdir))
            mpathMBTs=glob.glob("%s/*-sum-MBT.txt"%(sdir))
                
            if(len(mpaths) == 1): mpath=mpaths[0]
            else: mpath=None

            if(len(mpathMBTs) == 1): 
                mpathBT=mpathMBTs[0]
                print 'III -- using bd2 for mpathBT: ',mpathBT
            elif(len(mpathBTs) == 1): 
                mpathBT=mpathBTs[0]
            else: 
                mpathBT=None

            if(mpath == None):
                print 'problem in sdir: ',sdir,' with mpaths: ',mpaths,' sayounara'
                cmd='rmdir %s'%(sdir)
                mf.runcmd(cmd,'norun')
                continue
                
            # -- do non-BT path
            #
            vopt=''
            if(verb): vopt='-V'
            topt=''
            if(doTrk): topt='-T'
            #print 'mmm',mpath,mpathBT,mpathMRG
            if(mpath != None):
                cmd="m-mdeck3.py -r %s %s %s"%(mpath,vopt,topt)
                #mf.runcmd(cmd,'quiet')
                mf.runcmd(cmd,ropt)
            
            if(mpathBT != None):
                cmd="m-mdeck3.py -r %s %s %s"%(mpathBT,vopt,topt)
                #mf.runcmd(cmd,'quiet')
                mf.runcmd(cmd,ropt)
            
        MF.dTimer('sum-md3-%s-%s'%(basin,year))
        
MF.dTimer('sum-md3-ALL')
                         
sys.exit()
    