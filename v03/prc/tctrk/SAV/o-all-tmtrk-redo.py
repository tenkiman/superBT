#!/usr/bin/env python

from M import *
MF=MFutils()

def getDtgMissingInv(year,basin):

    dtgs={}
    bdir='../../inv/lsdiag/'
    mpath="%s/inv-missing-lsdiag-%s-%s.txt"%(bdir,year,basin)
    cards=open(mpath).readlines()
    for card in cards:
        tt=card.split()
        dtg=tt[-1].strip()
        stmid=tt[2]
        dtgs[stmid]=dtg
    return(dtgs)

byear=2007
eyear=2021
years=mf.yyyyrange(byear,eyear)
basins=['wpac','lant','epac','io','shem']

ropt='norun'
ropt=''

MF.sTimer('AAA-TMTRK')
for year in years:
    MF.sTimer('YYYY-%s'%(year))

    for basin in basins:
        MF.sTimer('BBYY-%s-%s'%(year,basin))
        
        dtgs=getDtgMissingInv(year, basin)
        
        stmids=dtgs.keys()
        stmids.sort()
        
        for stmid in stmids:
            dtg=dtgs[stmid]
            cmd="s-sbt-tmtrkN.py %s -S %s -T"%(dtg,stmid)
            mf.runcmd(cmd,ropt)

        MF.dTimer('BBYY-%s-%s'%(year,basin))

    MF.dTimer('YYYY-%s'%(year))

MF.dTimer('AAA-TMTRK')

sys.exit()


