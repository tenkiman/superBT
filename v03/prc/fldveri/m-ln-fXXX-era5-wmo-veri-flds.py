#!/usr/bin/env python

from sBT import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'doCatAll':         ['C',0,1,'cat f??? to single file'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
filter era5 fields for wmo verification"""

        self.examples='''
%s 1953090700'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

overrideLN=0
if(override):
    overrideLN=overrideGM=1
        
        
dtgs=mf.dtg_dtgopt_prc(dtgopt)
btau=0
etau=240
dtau=12
otaus=range(btau,etau+1,dtau)

ovars={
    'GP':(500,),
    'PRES':(1013,),
    'UGRD':(850,200),
    'VGRD':(850,200),
    'RH':(700,),
    'TMP':(700,)
  }

ofilts={}

#print otaus
MF.sTimer('ALL-xxx-%s'%(dtgopt))
for dtg in dtgs:
    
    year=dtg[0:4]
    sbdir=era5DatDir
    tbdir=era5WmoDatDir
    
    sdir="%s/%s/%s"%(tbdir,year,dtg)
    
    print 'ddd',sdir
    
    fpaths=glob.glob("%s/*-f*.grb2"%(sdir))
    fpaths.sort()

    for fpath in fpaths:
        (fdir,ffile)=os.path.split(fpath)
        (fbase,fext)=os.path.splitext(ffile)
        ff=ffile.split('-')
        fdtg=ff[2]
        fxxx=fbase[-4:]
        ftau=int(fxxx[-3:])
        vdtg=mf.dtginc(dtg,ftau)
        vyear=vdtg[0:4]
        
        tdir="%s/%s/%s"%(tbdir,fxxx,vyear)
        MF.ChkDir(tdir,'mk')
        tfile=ffile.replace('-%s'%(fxxx),'')
        tfile=tfile.replace(dtg,vdtg)
        tpath="%s/%s"%(tdir,tfile)
        cmd="ln -s %s %s"%(fpath,tpath)
        mf.runcmd(cmd,ropt)
    
MF.dTimer('ALL-xxx-%s'%(dtgopt))

sys.exit()