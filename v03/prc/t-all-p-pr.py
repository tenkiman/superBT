#!/usr/bin/env python

from sBT import *

byear=2008
eyear=2015
years=range(byear,eyear+1)
ropt='norun'
ropt=''
for year in years:
    cmd="r-all-pr.py -S all.%s"%(str(year))
    mf.runcmd(cmd,ropt)
    