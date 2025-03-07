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
            1:['yearOpt',    'yearOpt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
only creates -MRG.txt"""

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

    
MF.sTimer('AAA-MRG')

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']


# -- don't make -BT.csv just .csv and -MRG.csv
#

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

        MF.sTimer("MRG-%s-%s"%(basin,year))
        
        smask="%s/%s/*"%(tdir,basin)
        spaths=glob.glob(smask)
        spaths.sort()

        mpathBT=None
        mergecards=[]

        # -- first summary
        #
        for spath in spaths:
            
            mmask="%s/???-%s-md3.txt"%(spath,year)
            mpaths=glob.glob(mmask)
            if(len(mpaths) == 1): mpath=mpaths[0]
            else: mpath=None
            
            if(mpath == None): 
                print 'mmm',mmask
                print 'problem in spath: ',spath,' with mpaths: ',mpaths,' sayounara'
                sys.exit()

            mpathBTs=glob.glob("%s/???-%s-md3-BT.txt"%(spath,year))
            if(len(mpathBTs) == 1): mpathBT=mpathBTs[0]
            else: mpathBT=None

            # -- only does merge of -BT.txt into .txt to make -MRG.txt
            #
            (odir,ofile)=os.path.split(mpath)
            (obase,oext)=os.path.splitext(ofile)
            opath="%s/%s-MRG.txt"%(odir,obase)

            # -- write out mpath -> opath for 9X; mergeMd3Cvs handles no BT
            #
            ocards=mergeMd3Cvs(mpath,mpathBT,opath)
            MF.WriteList2Path(ocards, opath,verb=verb)

            mpathMRGs=glob.glob("%s/???-%s-md3-MRG.txt"%(spath,year))
            if(len(mpathMRGs) == 1): mpathMRG=mpathMRGs[0]
            else: mpathMRG=None
            
            # -- check again after making
            #
            if(mpathMRG == None): 
                print 'problem in spath: ',spath,' with mpathMRG: ',mpathMRG
                sys.exit()
                
            # -- now do the summary
            #
            vopt=''
            if(verb): vopt='-V'

            cmd="m-mdeck3.py -r %s %s -Y %s"%(mpathMRG,vopt,year)
            #mf.runcmd(cmd,'quiet')
            mf.runcmd(cmd,ropt)
            

                
        MF.dTimer("MRG-%s-%s"%(basin,year))

MF.dTimer('AAA-MRG')

