#!/usr/bin/env python

from ad2vm import *

byear=1945
byear=2007
eyear=2024
years=range(1945,eyear+1)
#years=range(1950,2024+1)
#years=range(1945,1950)


#rsync -alv /sbt/superBT-V04/dat-v03/atcf-form/1945/clp3/ /w21/dat/tc/adeck/atcf-form/1945/clp3/
sbdir='/sbt/superBT-V04/dat-v03/atcf-form'
tbdir='/w21/dat/tc/adeck/atcf-form'
model='clp3'
rsyncOpt='-alv'
#rsyncOpt='-alvn'
#ropt='norun'
ropt=''
MF.sTimer('ALL-rsync-clp3')
for year in years:
    MF.sTimer('rsync-clp3-%d'%(year))
    cmd="rsync %s %s/%s/%s/ %s/%s/%s/"%(rsyncOpt,sbdir,year,model,tbdir,year,model)
    mf.runcmd(cmd,ropt)
    MF.dTimer('rsync-clp3-%d'%(year))
MF.dTimer('ALL-rsync-clp3')
