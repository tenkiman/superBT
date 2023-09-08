#!/usr/bin/env python

from sBT import *

byear=7
eyear=22
years=range(byear,eyear+1)
ropt='norun'
ropt=''
for year in years:
    cmd="p-lsdiag.py -S all.%02d -O"%(year)
    mf.runcmd(cmd,ropt)
