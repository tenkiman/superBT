#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

def makeImergDatCtl(ofile,gtime,cfile,odir,ropt='',verb=0):

    ctlfile="""dset ^%s
undef 9.999E+20
title imerg-20211004-10-00.grb
*  produced by grib2ctl v0.9.12.5p16
ydef  480 linear  -59.875 0.25
xdef 1440 linear -180.000 0.25
tdef 1 linear %s 30mn
zdef 1 linear 1 1
vars 1
pr  0 0  ** Precipitation rate [mm/h]
ENDVARS
"""%(ofile,gtime)
    
    ctlpath="%s/%s"%(odir,cfile)
    
    print 'ctlpath: ',ctlpath
    
    rc=MF.WriteString2Path(ctlfile,ctlpath,verb=verb)
    
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
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            'zy0x1w2':'zy0x1w2',
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doCtlOnly':        ['G',0,1,"""just make ctl/gribmap"""],

            }

        self.purpose='''
use imerg gds to make .dat files in grads'''

        self.examples="""
%s 2024-12-01-00-30"""

def makeDtgs(dtgopt):
    
    dtgs=[]
    dtg=dtgopt+'00'
    dtgs.append(dtg)
    for h in range(1,24):
        dtg=mf.dtginc(dtg,1)
        dtgs.append(dtg)
        
    return(dtgs)
    

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
gsfile=pyfile.replace('.py','.gs')

source='imerg'
sbdir="%s/%s/cmorph_grid"%(w2.PrDatRoot,source)

dd=dtgopt.split('.')
if(len(dd) == 2):
    dd1=dd[0]
    dd2=dd[1]
    if(not(len(dd1) == 8 and len(dd2) == 8)):
        print 'EEE bad dtgopt: ',dtgopt
        sys.exit()
        
    idd1=int(dd[0][-2:])
    idd2=int(dd[1][-2:])

    dtgs=[]
    idds=range(idd1,idd2+1)

    for idd in idds:
        tdtgopt="%s%02d"%(dd1[0:6],idd)
        #print 'ii',idd,tdtgopt,dd1
        adtgs=makeDtgs(tdtgopt)
        dtgs=dtgs+adtgs
        
elif(len(dtgopt) == 8):
    dtgs=makeDtgs(dtgopt)

else:
    dtgs=mf.dtg_dtgopt_prc(dtgopt)

dtgmns=[]

for dtg in dtgs:
    dtgmn="%s00"%(dtg)
    dtgmns.append(dtgmn)
    dtgmn="%s30"%(dtg)
    dtgmns.append(dtgmn)
    
MF.sTimer('DAT2grb-%s'%(dtgopt))
for dtgmn in dtgmns:
    
    #print 'dtgmn: ',dtgmn,len(dtgmn)
        
    dtg=dtgmn[0:10]
    yyyy=dtgmn[0:4]
    mm=dtgmn[4:6]
    dd=dtgmn[6:8]
    hh=dtgmn[8:10]
    mn=dtgmn[10:12]
    
    gtime=mf.dtg2gtime(dtg)
    gtime=gtime.replace('Z',':%sZ'%(mn))
    ofile="imerg-v7-%s-%s-%s-%s-%s.dat"%(yyyy,mm,dd,hh,mn)
    cfile="imerg-v7-%s-%s-%s-%s-%s.ctl"%(yyyy,mm,dd,hh,mn)
    
    sdir="%s/%s"%(sbdir,yyyy)
    opath="%s/%s"%(sdir,ofile)
    osiz=MF.getPathSiz(opath)

    if(osiz <= 0 or override):
        cmd='''grads -lbc "run %s %s %s"'''%(gsfile,gtime,opath)
        mf.runcmd(cmd,ropt)
    else:
        print 'AAA already done: ',opath
    
    rc=makeImergDatCtl(ofile,gtime,cfile,sdir,ropt=ropt)
    
MF.dTimer('DAT2grb-%s'%(dtgopt))

sys.exit()
