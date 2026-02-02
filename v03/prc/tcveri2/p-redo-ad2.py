#!/usr/bin/env python

from tcbase import *

byearER=1945 ; eyearER=2024

byearER=1946 ; eyearER=2022 # did 1945 and 2023-24 by hand

byearER=1946 ; eyearER=1978 # 2012 sec
byearER=1979 ; eyearER=2000 # 3442 sec
byearER=2001 ; eyearER=2022 # 5933 sec

byearTM=1979 ; eyearTM=eyearER
byearNH=1954 ; eyearNH=eyearER
byearJT=1961 ; eyearJT=eyearER
byearECMWF=2006 ; eyearECMWF=2017
byearECWMO=2023 ; eyearECWMO=2024

yearsER=range(byearER,eyearER+1)
yearsTM=range(byearTM,eyearTM+1)
yearsNH=range(byearNH,eyearNH+1)
yearsJT=range(byearJT,eyearJT+1)
yearsECMWF=range(byearECMWF,eyearECMWF+1)
yearsECWMO=range(byearECWMO,eyearECWMO+1)



ropt='norun'
ropt=''

ad2py="w2-tc-dss-ad2.py"
bd2py="w2-tc-dss-bd2.py"

# -- 20260131 -- added ec-wmo and ecmwf sources AFTER doing the
#    souces='tmtrkN' and 'jt-nhc'
#    found another ecmwf aid 'emx'
#
# -- just ECWMO
#
source='ec-wmo'
MF.sTimer("ALL-ad2-%dd-%d"%(byearECWMO,eyearECWMO))
for year in yearsECWMO:

    cmd="%s %s -S all.%d -O1"%(ad2py,source,year)
    MF.sTimer("ad2-%d"%(year))
    mf.runcmd(cmd,ropt)
    MF.dTimer("ad2-%d"%(year))

sys.exit()

# -- just ECMWF
#
source='ecmwf'
MF.sTimer("ALL-ad2-%dd-%d"%(byearECMWF,eyearECMWF))
for year in yearsECMWF:

    cmd="%s %s -S all.%d -O1"%(ad2py,source,year)
    MF.sTimer("ad2-%d"%(year))
    mf.runcmd(cmd,ropt)
    MF.dTimer("ad2-%d"%(year))

sys.exit()

MF.sTimer("ALL-ad2-bd2-%d-%d"%(byearER,eyearER))
for year in yearsER:
    
    gotTM=0 
    if(year in yearsTM): gotTM=1
    gotJT=0
    if(year in yearsJT): gotJT=1
    gotNH=0
    if(year in yearsNH): gotNH=1

    source='era5'
    if(gotTM): source="%s,%s"%(source,'tmtrkN')
    if(gotJT or gotNH and not(mf.find(source,'jt-nhc'))): source="%s,%s"%(source,'jt-nhc')
    
    cmd="%s %s -S all.%d -O1"%(ad2py,source,year)
    MF.sTimer("ad2-%d"%(year))
    mf.runcmd(cmd,ropt)
    MF.dTimer("ad2-%d"%(year))

    # -- use m-sbt-bd2.py vice bd2 for md2
    #
    #cmd="%s -S all.%d"%(bd2py,year)
    #MF.sTimer("bd2-%d"%(year))
    #mf.runcmd(cmd,ropt)
    #MF.dTimer("bd2-%d"%(year))

MF.dTimer("ALL-ad2-bd2-%d-%d"%(byearER,eyearER))
    
        