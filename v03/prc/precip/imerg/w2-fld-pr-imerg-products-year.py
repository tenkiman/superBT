#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#

def parseGradsLog(lines,verb=0):
    rc=1
    for line in lines:
        if(verb): print line
        if(mf.find(line,'ttttt')): print line
        if(mf.find(line,'RRRCCC')): print line
        if(mf.find(line,'WWWWWW no data') or mf.find(line,'Open Error')): 
            rc=0
            return(rc)
    return(rc)


def GetExistingDtgs(pdir,dtgs,pbase,thours=None):

    pdtgs=[]
    dpaths=[]
    for dtg in dtgs:
        year=dtg[0:4]
        yymmdd=dtg[0:8]
        mask="%s/%s/%s_%s??.grb"%(pdir,year,pbase,yymmdd)
        dpaths=dpaths+glob.glob(mask)
        
    dpaths=mf.uniq(dpaths)
    dpaths.sort()

    for dpath in dpaths:
        (ddir,ffile)=os.path.split(dpath)
        dtg=ffile.split('_')[2][0:10]
        pdtgs.append(dtg)
    
    if(len(pdtgs) == 0):
        pdtgb=curdtg
        thours=0
    else:
        pdtgb=pdtgs[0]
        pdtge=pdtgs[-1]
        if(thours != None):
            pdtgb=mf.dtginc(pdtge,-thours)
        else:
            thours=mf.dtgdiff(pdtgb,pdtge)
            
    return(pdtgs)


def MakeProductCtl(pdir,pbase,bdtg,thours,tbdir,ddtg=6,setYear=None):

    if(setYear != None):
        
        bdtg="%s010100"%(setYear)
        edtg="%s123118"%(setYear)
        dtgopt="%s.%s.%d"%(bdtg,edtg,ddtg)
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        tsteps=len(dtgs)+1
        # -- add 72 h
        #
        tsteps=tsteps+72/ddtg
        
        dset="^grib/%%y4/%s_%%y4%%m2%%d2%%h2.grb"%(pbase)
        index="^%s-%s.gmp1"%(pbase,setYear)
        
        ctlpath="%s/%s-%s.ctl"%(tbdir,pbase,setYear)
        gtime=mf.dtg2gtime(bdtg)
        
    else:

        dset="^grib/%%y4/%s_%%y4%%m2%%d2%%h2.grb"%(pbase)
        index="^%s.gmp1"%(pbase)
        ctlpath="%s/%s.ctl"%(tbdir,pbase)
        tsteps=int(thours/ddtg)+1
        gtime=mf.dtg2gtime(bdtg)
    
    ctl="""dset %s
index %s
undef 9.999E+20
title prq_a06h_2009031812.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
ydef  480 linear  -59.875 0.25
xdef 1440 linear -180.0   0.25
tdef   %d linear %s %dhr
zdef 1 linear 1 1
vars 1
pr  0 59,1,0  ** Precipitation rate [kg/m^2/s]
ENDVARS"""%(dset,index,tsteps,gtime,ddtg)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    
def makeYearCtl(grbdir,pbase,bdtg,thours,tbdirProd,setYear,ropt=''):
    MF.sTimer('GGGMMM-%s'%(setYear))    
    pctl=MakeProductCtl(grbdir,pbase,bdtg,thours,tbdir=tbdirProd,
                        setYear=setYear)
            
    grbopt=''
    cmd="gribmap %s -i %s"%(grbopt,pctl)
    mf.runcmd(cmd,ropt)
    MF.dTimer('GGGMMM-%s'%(setYear))    
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'prcopt':'all',
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'setYear':          ['y:',None,'a',"""force using yearly files for 30min data"""],

            }

        self.purpose='''
make imerg products year .ctl'''

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

MF.sTimer('all')


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main loop
# -- set xgrads
#
xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)

pdir=w2.PrcDirFlddatW2
pdir='.'

source='imerg'
sbdir  ="%s/pr/%s/grib"%(w2.W2BaseDirDat,source)
tbdir="%s/pr/model/pr_imerg"%(w2.W2BaseDirDat)
grbdir="%s/grib"%(tbdir)
prodpre="pr%s"%(source[0])

# -- use yearly .ctl if old...
#
pbases=['pri_a06h','pri_a12h']
pbases=['pri_a06h']
pbase=pbases[0]

curhrdtg=mf.dtg('dtgcurhr')

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
# 
# grib

thours=None

grbdiryy="%s/%s"%(grbdir,setYear)
MF.ChkDir(grbdiryy,'mk')

tt=setYear.split('.')
if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
else:
    byear=setYear
    eyear=setYear
    
for setYear in mf.yyyyrange(byear,eyear):

    MF.sTimer('AAA-%s'%(setYear))
    bdtg='%s010100'%(setYear)
    rc=makeYearCtl(grbdir,pbase,bdtg,thours,tbdir,setYear,ropt)
    MF.dTimer('AAA-%s'%(setYear))
    
sys.exit()