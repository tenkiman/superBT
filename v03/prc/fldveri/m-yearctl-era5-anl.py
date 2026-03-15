#!/usr/bin/env python

from sBT import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doDaily':          ['d',0,1,'run daily ave script'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
redo atcf-form for era5"""

        self.examples='''
%s -Y 1945.1950'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

def makeEra5AnlCtl(year,ropt='',override=0):

    tdir=era5AnlDatDir

    def setCtl(year,ntimes):
        
        gmpfile='era5-anl-%s-ua.gmp2'%(year)
        gmppath='%s/%s'%(tdir,gmpfile)
        gsiz=MF.getPathSiz(gmppath)
        if(gsiz > 0 and not(override)):
            print 'WWW -- gmppath exists and not(override)'
            ctl=[]
            return(ctl)
        
        ctl='''dset  ^%%y4/%%y4%%m2%%d2%%h2/era5-anl-%%y4%%m2%%d2%%h2-ua.grb2
index ^%s
undef 9.999E+20
title t-era5-12-si.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
tdef  %d linear 00Z01Jan%s 12hr
* PROFILE hPa
zdef   9 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000
options pascals template
vars 11
psl    0,101      0,  3,  0   ** mean sea level Pressure [Pa]
uas    0,103,10   0,  2,  2   ** 10 m above ground mponent of Wind [m/s]
vas    0,103,10   0,  2,  3   ** 10 m above ground V-Component of Wind [m/s]
prw    0,1      192,128,137   ** surface desc [unit]
prc    0,1        0,  1, 10   ** surface Convective Precipitation [kg/m^2]
pr     0,1        0,  1, 52,1 ** surface Total Precipitation [kg/m^2]
ua     9,100      0,  2,  2   ** mponent of Wind [m/s]
va     9,100      0,  2,  3   ** V-Component of Wind [m/s]
ta     9,100      0,  0,  0   ** Temperature [K]
hura   9,100      0,  1,  1   ** Relative Humidity [%%]
zg     9,100      0,  3,  4   ** Geopotential [m^2/s^2]WmoStats
ENDVARS'''%(gmpfile,ntimes,year)
    
        return(ctl)

    
    tdir=era5AnlDatDir
    
    ntimes=365*2
    if(IsLeapYear(year)): ntimes=366*2
    
    # -- add begining of next year
    #
    ntimes=ntimes+2
    
    ctl=setCtl(year,ntimes)
    ctlpath="%s/era5-anl-%s-ua.ctl"%(tdir,year)
    
    if(len(ctl) > 0):
        
        rc=MF.WriteCtl(ctl,ctlpath,verb=1)
        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)
        
    return(1)
    
    
argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(mf.find(yearOpt,'-')):
    tt=yearOpt.split('-')
    byear=int(tt[0])
    eyear=int(tt[1])
elif(mf.find(yearOpt,'.')):
    tt=yearOpt.split('.')
    byear=int(tt[0])
    eyear=int(tt[1])
else:
    byear=int(yearOpt)
    eyear=int(yearOpt)
    
years=mf.yyyyrange(byear,eyear)

MF.sTimer('ALL-ALL')
for year in years:
    
    MF.sTimer('ALL-%s'%(year))
    
    # -- make yearly ctl
    #
    rc=makeEra5AnlCtl(year,override=override)

    # -- make daily mean of select vars
    #
    if(doDaily):
        MF.sTimer('daily-%s'%(year))
        tdirDaily="%s/da/%s"%(era5AnlDatDir,year)
        MF.ChkDir(tdirDaily,'mk')
        cmd='''grads -lbc "m-daily.gs %s"'''%(year)
        mf.runcmd(cmd,ropt)
        MF.dTimer('daily-%s'%(year))
    MF.dTimer('ALL-%s'%(year))
    

MF.dTimer('ALL-ALL')
