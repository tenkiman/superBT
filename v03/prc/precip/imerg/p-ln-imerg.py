#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

year=2020
year=2014
year=2021 # done 20221223
year=2020 # done
year=2019 # done
year=2018 # done
year=2017 # done
year=2016 # done
year=2015 # done


syear=str(year)
MF.ChangeDir(syear,verb=1)
source='imerg'
sbdir="%s/%s/cmorph_grid"%(w2.PrDatRoot,source)
tbdir="%s/%s"%(w2.PrDatRoot,source)
print 'sbdir',sbdir
print 'tbdir',tbdir
sdir="%s/%s"%(sbdir,syear)
tdir="%s/%s"%(tbdir,syear)

print 'sss',sdir
print 'ttt',tdir

MF.ChkDir(tdir,'mk')

ropt='norun'
ropt=''
npaths=glob.glob("%s/*.nc4"%(sdir))
npaths.sort()

for npath in npaths:
    (sdir,sfile)=os.path.split(npath)
    ss=sfile.split('.')
    yyyymmdd=ss[4][0:8]
    hhmn=ss[4][10:14]
    hh=hhmn[0:2]
    mn=hhmn[2:4]
    tfile='imerg-%s-%s-%s.nc4'%(yyyymmdd,hh,mn)
    spath=npath
    tpath="%s/%s"%(tdir,tfile)
    cmd='ln -s %s %s'%(spath,tpath)
    mf.runcmd(cmd,ropt)

sys.exit()

