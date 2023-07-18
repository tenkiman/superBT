#!/usr/bin/env pythonw
from M import *
MF=MFutils()

basins=['w','e','l','h']
bvars=['mvmax','shr','tpw']

bvars=['rh700','cpshi','cpslo',
      'prg3','pri3','prc3',
      'prg5','pri5','prc5',
      'prg8','pri8','prc8',
      ]

ropt='norun'
ropt=''

for basin in basins:
    for var in bvars:
        cmd='''grads -lc "g-sbt-dev-non.gs %s %s"'''%(basin,var)
        mf.runcmd(cmd,ropt)
