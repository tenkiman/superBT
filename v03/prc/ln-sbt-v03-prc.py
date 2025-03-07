#!/usr/bin/env python

from WxMAP2 import *

sdir='/sbt/superBT-V04'

filesData=[
    'h-meta-md3-sum.csv',
    'h-meta-md3-vars.csv',
    'h-meta-sbt-v04-vars.csv',
]

filesPrc=[
    'mf.py',
    'p-md3-ls.py',
    'sBTcl.py',
    'sbtLocal.py',
    #'sbt.py,
    'sBT.py',
    'sBTvars.py',
    'sBTvm.py',
]

ropt='norun'
ropt=''

for filed in filesData:
    cmd='ln -s -f %s/dat/%s .'%(sdir,filed)
    mf.runcmd(cmd,ropt)

for filep in filesPrc:
    cmd='ln -s -f %s/py2/%s .'%(sdir,filep)
    mf.runcmd(cmd,ropt)
 
 # h-meta-md3-sum.csv -> /data/w22/superBT-V04/dat/h-meta-md3-sum.csv
 # h-meta-md3-vars.csv -> /data/w22/superBT-V04/dat/h-meta-md3-vars.csv
 # h-meta-sbt-v04-vars.csv -> /data/w22/superBT-V04/dat/h-meta-sbt-v04-vars.csv
 # mf.py -> /data/w22/superBT-V04/py2/mf.py
 # p-md3-ls.py -> /data/w22/superBT-V04/py2/p-md3-ls.py
 # sBTcl.py -> /data/w22/superBT-V04/py2/sBTcl.py
 # sbtLocal.py -> /data/w22/superBT-V04/py2/sbtLocal.py
 # sbt.py -> /data/w22/prj-superBT/sbt.py
 # sBT.py -> /data/w22/superBT-V04/py2/sBT.py
 # sBTvars.py -> /data/w22/superBT-V04/py2/sBTvars.py
 # sBTvm.py -> /data/w22/superBT-V04/py2/sBTvm.py
