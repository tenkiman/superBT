#!/usr/bin/env python

from sBT import *

byear=10
eyear=12
years=range(byear,eyear+1)

for year in years:
    cmd="p-lsdiag.py -S all.%s"%(str(year))
    mf.runcmd(cmd)
