#!/usr/bin/env python

from sBT import *

byear=2007
eyear=2022
years=range(byear,eyear+1)
ropt='norun'
ropt=''
for year in years:
    cmd="r-all-pr.py -S all.%s -O"%(str(year))
    mf.runcmd(cmd,ropt)
    