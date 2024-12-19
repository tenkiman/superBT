#!/usr/bin/env python

from sBT import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.defaults={
            #'version':'v01',
        }
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
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

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=mf.yyyyrange(byear, eyear)
    oyearOpt="%s-%s"%(byear,eyear)

elif(len(tt) == 1):

    years=[yearopt]
    oyearOpt=yearopt

else:
    print 'EEE -- invalid yearopt: ',yearopt

MF.sTimer('AAA-sBT-cvs')

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']

# -- make version 04
#
version='v04'
sbtVerDir="%s/%s"%(sbtRoot,version)


headAll='h-sbt-%s-vars-csv.txt'%(version)

(allCvsPath,sumCvsPath)=setCvsSbtYearOptPaths(sbtVerDir,oyearOpt,version,headAll,dorm=1)

for year in years:
    
    tdir="%s/%s"%(sbtVerDir,year)
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
        #
        for spath in spaths:
            smask="%s/s*-%s.txt"%(spath,version)
            sbtpaths=glob.glob(smask)
            if(len(sbtpaths) == 1): sbtpath=sbtpaths[0]
            else: sbtpath=None
            
            if(sbtpath != None):
                cmd="cat %s >> %s"%(sbtpath,allCvsPath)
                mf.runcmd(cmd,ropt)
                
        MF.dTimer("csv-%s-%s"%(basin,year))
        

# -- cp over to superBT/
#
(adir,afile)=os.path.split(allCvsPath)
cmd="cp %s %s/%s"%(allCvsPath,sbtDatDir,afile)
mf.runcmd(cmd,ropt)


MF.dTimer('AAA-sBT-cvs')

