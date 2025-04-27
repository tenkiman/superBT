#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

def makeGaveCtl(tdir,pre,source,year):

    ctlfile="%s-gave-%s.ctl"%(pre,year)
    ctlpath="%s/%s"%(tdir,ctlfile)
    
    nt=MF.nDayYear(year)
    nt=nt*4+1
    
    ctl="""dset ^gave-%s-%s.dat
undef -9.99e+08
title global ave pr
ydef     1 linear -59.875 0.25
xdef     1 linear   0.125 0.25
tdef  %4d linear 00Z01Jan%s 6hr
zdef 1 linear 1 1
vars 1
pr  0 0  ** Precipitation rate [mm/d]
ENDVARS"""%(source,year,nt,year)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    print 'ccc',ctlpath
    return(ctlpath)
    


    
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
            }

        self.purpose='''
make gave of pr products'''

        self.examples="""
%s 2007"""


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main
#
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
   
tdir='/sbt/superBT-V04/v03/prc/precip/dat'
tt=yearOpt.split('.') 

srcpre={
    'prg':'gsmap',
    'prgv6':'gsmapV6',
    'prc':'cmorph',
    'pri':'imerg',
}

# -- 2024 update
srcpre={
#    'prg':'gsmap',
    'prgv6':'gsmapV6',
    'prg8':'gsmapV8',
    'prg8g':'gsmapV8-G',
    'pri':'imerg',
}

if(len(tt) == 2):
    byear=int(tt[0])
    eyear=int(tt[1])
    years=range(byear,eyear+1)
    
else:
    years=[yearOpt]

for year in years:

    syear=str(year)
    iyear=int(year)
    
    kk=srcpre.keys()
    for k in kk:
        if( (iyear <= 2000 or iyear >= 2023) and k == 'prgv6'):
            print 'no data for %s in %s'%(k,syear)
            continue
            
            
        pre=k
        source=srcpre[k]
        rc=makeGaveCtl(tdir,pre,source,syear)
        
sys.exit()

