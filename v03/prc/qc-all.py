#!/usr/bin/env python

from sBT import *

bopts=[
'l.07-22',
'e.07-22,c.07-22',
'w.07-22',
'i.07-22',
'h.07-22',
    ]

bmaxs=[
30,
35,
40,
45,
50,
    ]

ropt='norun'
ropt=''

for bmax in bmaxs:
    for bopt in bopts:
        cmd='ql-sbt-v03.py -S %s -m %i'%(bopt,bmax)
        runcmd(cmd,ropt)


