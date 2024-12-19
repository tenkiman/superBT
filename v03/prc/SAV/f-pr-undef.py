#!/usr/bin/env python

from sbt import *

ropt='norun'
ropt=''

cards=open('inv/bad-pr-undef2.txt').readlines()

stmids=[]
for card in cards:
    tt=card.split()
    if(len(tt) > 2):
        stmid=tt[1]
        stmids.append(stmid)

stmids=mf.uniq(stmids)

for stmid in stmids:
    cmd="r-all-pr.py -S %s -O"%(stmid)
    mf.runcmd(cmd,ropt)
    
    cmd="m-sbt-v03.py -S %s -O"%(stmid)
    mf.runcmd(cmd,ropt)
