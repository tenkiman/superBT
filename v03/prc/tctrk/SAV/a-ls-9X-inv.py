#!/usr/bin/env python

from sbt import *

cards=open('inv/inv-9X-999.txt').readlines()

for card in cards:
    #print card.strip()
    tt=card.split()
    dtg=tt[1]
    stmid=tt[2]
    vmax=tt[3]
    tccode=tt[-4]
    istc=IsTc(tccode)
    if(istc == 1):
        print 'PPProblem? ',dtg,stmid,vmax,tccode,istc
