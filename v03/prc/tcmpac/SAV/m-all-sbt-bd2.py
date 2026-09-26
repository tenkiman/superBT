#!/usr/bin/env python

from ad2vm import *


years=range(1945,2024+1)

ropt='norun'
ropt=''
MF.sTimer('ALL-sbt-bd2')
for year in years:
    MF.sTimer('sbt-bd2-%d'%(year))
    cmd="m-sbt-bd2.py -S all.%d"%(year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('sbt-bd2-%d'%(year))
MF.dTimer('ALL-sbt-bd2')
