#!/usr/bin/env python

from sBT import *

sbtDat3Dir='/dat3/dat/sbt-v03/superBT-V03-dat'
sbtHopperDir='/scratch/mfiorino/dat/superBT'

MF.ChangeDir(sbtDat3Dir)

sdir='src'
tdir="%s/src"%(sbtHopperDir)
rsyncOpt='-alv'
cmd='''rsync %s %s/ mfiorino@hopper1.orc.gmu.edu:/%s/'''%(rsyncOpt,sdir,tdir)
ropt=''
mf.runcmd(cmd,ropt)
    