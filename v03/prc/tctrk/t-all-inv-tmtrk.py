#!/usr/bin/env python

from sBT import *

byear=2011
eyear=2014
years=range(byear,eyear+1)

ropt='norun'
ropt=''

for year in years:
    cmd="r-inv-tmtrk.py %s01.%s12.6 "%(str(year),str(year))
    mf.runcmd(cmd,ropt)
