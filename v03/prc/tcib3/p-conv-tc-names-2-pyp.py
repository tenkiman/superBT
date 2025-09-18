#!/usr/bin/env python3

from M3 import *
MF=MFutils()
import pickle,sys

byear=1900
#byear=2020
eyear=2024
# -- ran on 20250903
byear=2025
eyear=2026

# -- use the version in ndir to execute
#
ndir='/sbt/superBT-V04/dat-v03/tc/names'

byear=eyear=2025

ttypes=['names','stats']
#ttypes=['names']

MF.sTimer('pyp-ALL')
for iyear in range(byear,eyear+1):
    year=str(iyear)
    MF.sTimer('pyp-%s'%(year))
    print('doing year: %s.....'%(year))
    for ttype in ttypes:
        tcname='TC%s%s'%(ttype,year)
        otname='tc%s'%(ttype)
        pypname='TC%s%s.pyp'%(ttype,year)
        exec('from %s/%s import %s'%(tcname,otname))
        exec('kk=list(%s.keys())'%(otname))
        kk.sort()
        print ('iiiii-%s'%(otname),kk[-5:])
        P=open(pypname,'wb')
        exec('pickle.dump(%s,P)'%(otname))
        P.close()

        P=open(pypname,'rb')
        tc1=pickle.load(P)
        kk=tc1.keys()
        kk=list(kk)
        kk.sort()
        print('ooooo-%s'%(otname),kk[-5:])
        P.close()

    MF.dTimer('pyp-%s'%(year))

MF.dTimer('pyp-ALL')

    
    


