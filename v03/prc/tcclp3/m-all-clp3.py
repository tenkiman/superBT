#!/usr/bin/env python

from ad2vm import *

years=range(1945,2024+1)
years=range(1950,2024+1)
years=range(2007,2024+1)

ropt='norun'
ropt=''
MF.sTimer('ALL-clp3')
for year in years:
    MF.sTimer('clp3-%d'%(year))
    cmd="p-clp3.py -S all.%d"%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('clp3-%d'%(year))
MF.dTimer('ALL-clp3')
