#!/usr/bin/env python

from ad2vm import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'doAD2':            ['A',0,1,'do AD2'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
        }

        self.purpose="""
make era5 ad2  and inventory in both .txt and .pyp"""

        self.examples='''
%s -Y 1969.1970'''
    

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

years=yearOptPrc(yearOpt)

MF.sTimer('ALL-ad2-vd2')
for year in years:
    
    MF.sTimer('ad2-vd2-%s'%(year))
    
    if(doAD2):
        
        MF.sTimer('ad2inv-%s'%(year))
        cmd="m-ad2inv.py -C -0 -Y %s"%(year)
        mf.runcmd(cmd,ropt)
        MF.dTimer('ad2inv-%s'%(year))
        
    MF.sTimer('vdinv-%s'%(year))
    cmd="m-vdinv.py -Y %s -O"%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vdinv-%s'%(year))

    MF.sTimer('vdinv-z0012-%s'%(year))
    cmd="m-vdinv.py -Y %s -f z0012"%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vdinv-z0012-%s'%(year))

    MF.dTimer('ad2-vd2-%s'%(year))
    
MF.dTimer('ALL-ad2-vd2')
