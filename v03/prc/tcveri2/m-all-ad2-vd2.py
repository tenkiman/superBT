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
            'basinOpt':         ['B:',None,'a',""" default is None | a..."""],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
        }

        self.purpose="""
make era5 ad2  and inventory in both .txt and .pyp"""

        self.examples='''
%s -Y 2016 -B w'''
    

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

years=yearOptPrc(yearOpt)

bopt=''
if(basinOpt != None):
    bopt='-B %s'%(basinOpt)
    
MF.sTimer('ALL-ad2-vd2')
for year in years:
    
    MF.sTimer('ad2-vd2-%s'%(year))
    
    if(doAD2):
        
        MF.sTimer('ad2inv-%s'%(year))
        cmd="m-ad2inv.py -C -E -0 -Y %s"%(year)
        mf.runcmd(cmd,ropt)
        MF.dTimer('ad2inv-%s'%(year))
        
    MF.sTimer('vdinv-%s'%(year))
    cmd="m-vdinv.py -Y %s %s -O"%(year,bopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vdinv-%s'%(year))

    MF.sTimer('vdinv-z0012-%s'%(year))
    cmd="m-vdinv.py -Y %s %s -f z0012 -O"%(year,bopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('vdinv-z0012-%s'%(year))

    MF.dTimer('ad2-vd2-%s'%(year))
    
MF.dTimer('ALL-ad2-vd2')
