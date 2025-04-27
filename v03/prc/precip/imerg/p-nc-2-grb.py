#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

year=2020
year=2014
year=2021 # done 20221223
year=2020 # done
year=2019 # done
year=2018 # done
year=2017 # done
year=2016 # done
year=2015 # done
year=2021

def makeImergGrbCtl(year,tbdir,ropt=''):

    yearm1=int(year)-1
    syearm1=str(yearm1)
    
    syear=str(year)
    gtime="00:00z1jan%s"%(syear)
    nt=MF.nDayYear(year)*48
    gtime="00:00z31Dec%s"%(syearm1)
    nt=MF.nDayYear(year)*48+48
    print 'nnnnnn',nt,gtime
    
    ctlpath="%s/imerg-grb-%s.ctl"%(tbdir,year)
    ctlfile="""dset ^%%y4/imerg-%%y4%%m2%%d2-%%h2-%%n2.grb
index ^imerg-grb-%s.gmp
undef 9.999E+20
title imerg-20211004-10-00.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
ydef  480 linear  -59.875 0.25
xdef 1440 linear -180.000 0.25
#tdef 1 linear 00:00Z01jan2021 30mn
tdef %d linear %s 30mn
zdef 1 linear 1 1
vars 1
pr  0 59,1,0  ** Precipitation rate [mm/h]
ENDVARS
"""%(syear,nt,gtime)
    
    print ctlpath
    print ctlfile
    
    rc=MF.WriteString2Path(ctlfile,ctlpath,verb=1)
    cmd='gribmap -v -i %s'%(ctlpath)
    mf.runcmd(cmd,ropt)
    
    return
    
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearOpt',    'no default'],
            }

        self.defaults={
            'zy0x1w2':'zy0x1w2',
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doCtlOnly':        ['G',0,1,"""just make ctl/gribmap"""],
            'doYearCtlOnly':    ['Y',0,1,'make yearctl only'],

            }

        self.purpose='''
make cpc qmorph products'''

        self.examples="""
%s cur"""


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main
#
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

prcdir=curdir
table="-table %s/lats.pr.table.txt"%(prcdir)

tt=yearOpt.split('.') 

if(len(tt) == 2):
    byear=int(tt[0])
    eyear=int(tt[1])
    years=range(byear,eyear+1)
    
else:
    years=[yearOpt]

for year in years:

    syear=str(year)
    
    MF.sTimer('NC2GRB-%s'%(syear))
    MF.ChangeDir(syear,verb=1)
    source='imerg'
    sbdir="%s/%s/cmorph_grid"%(w2.PrDatRoot,source)
    tbdir="%s/%s/grib"%(w2.PrDatRoot,source)
    print 'sbdir',sbdir
    print 'tbdir',tbdir
    sdir="%s/%s"%(sbdir,syear)
    tdir="%s/%s"%(tbdir,syear)
    
    print 'sss',sdir
    print 'ttt',tdir
    
    MF.ChkDir(tdir,'mk')

    if(doCtlOnly):
        rc=makeImergGrbCtl(syear,tbdir,ropt)

    else:    
    
        npaths=glob.glob("%s/*%s*.nc4"%(sdir,syear))
        npaths.sort()
        latscmd="lats4d.sh -ftype sdf -format grib"
        for npath in npaths:
            (sdir,sfile)=os.path.split(npath)
            ss=sfile.split('.')
            yyyymmdd=ss[4][0:8]
            hhmn=ss[4][10:14]
            hh=hhmn[0:2]
            mn=hhmn[2:4]
            tfile='imerg-%s-%s-%s'%(yyyymmdd,hh,mn)
            spath=npath
            tpath="%s/%s"%(tdir,tfile)
            gpath="%s.grb"%(tpath)
            tsiz=MF.getPathSiz(gpath)
            if(tsiz <= 0 or override):
                cmd="%s %s -i %s -o %s "%(latscmd,table,spath,tpath)
                #cmd='ln -s %s %s'%(spath,tpath)
                mf.runcmd(cmd,ropt)
            else:
                print 'AAA already done: ',sfile
        
    MF.dTimer('NC2GRB-%s'%(year))
        
sys.exit()

