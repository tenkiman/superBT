#!/usr/bin/env python

from sBT import *

#sMdesc=lsSbtVars()

stmids=[
    #'09e.1990',
    #'18w.1991',
    #'16w.1995',
    #'06l.1997',
    #'32h.1998',
    #'03h.2002',
    #'06l.2003',  # edit adeck by hand to take out very eary posit
    #'10l.2005',
    #'04l.2017',
    #'16l.2021',
    ]


lpy2='w2-tc-dss-md2-anl.py'
lopt2='-s -b -2'
lpath2='bad222-ls.txt'
if(MF.getPathSiz(lpath2) > 0):
    os.unlink(lpath2)

lpy3='p-md3-ls.py'
lopt3='-s -b -D -2'
lpath3='bad333-ls.txt'
if(MF.getPathSiz(lpath3) > 0):
    os.unlink(lpath3)


mpy='w2-tc-dss-md2.py'
mpy='m-md3-from-md2-bd2.py'
mpy='m-md3-stm-dir-sum-bd2.py'
cpy='m-md3-csv-ALL-bd2.py'
doFix=1
doFix=0
ropt='norun'
ropt=''

for stmid in stmids:
    
    (snum,b1id,syear,b2id,stm2id,stm1id)=getStmParams(stmid)
    basin=Basin1toFullBasin[b1id.upper()]

    if(MF.getPathSiz(lpath2) > 0):   os.unlink(lpath2)
    if(MF.getPathSiz(lpath3) > 0):   os.unlink(lpath3)

    cmd2="%s -S %s.%s %s >> %s"%(lpy2,b1id,syear,lopt2,lpath2)
    cmd3="%s -S %s.%s %s >> %s"%(lpy3,b1id,syear,lopt3,lpath3)
    cmdF="%s %s -B %s"%(mpy,syear,basin)
    cmdC="%s -Y %s"%(cpy,syear)
    cmdM="meld %s %s"%(lpath2,lpath3)
    
    if(doFix):
        
        mf.runcmd(cmdF,ropt)
        mf.runcmd(cmdC,ropt)
        mf.runcmd(cmd2)
        mf.runcmd(cmd3)
        mf.runcmd(cmdM)
        
    else:
        
        mf.runcmd(cmd2)
        mf.runcmd(cmd3)
        mf.runcmd(cmdM)
    
    
sys.exit()
    

    
    
    
