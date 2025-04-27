#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

# -- in *3
#year=2020   # -- GOOD ;
#year=2019   # -- GOOD ;
#year=2018   # -- GOOD ; missed
#year=2014   # -- GOOD ;
#year=2015   # -- GOOD ;
#year=2017   # -- GOOD ;
#year=2016   # -- GOOD ;  missed *4
#year=2013   # -- GOOD ; 1 miss! good
#year=2012   # -- GOOD ;
#year=2011   # -- GOOD ; 1 miss! good
#year=2010   # -- GOOD ;
#year=2009   # -- GOOD ; miss 133
#year=2008   # -- GOOD ; miss 134
#year=2007   # -- GOOD ; miss 134
#year=2006   # -- GOOD ; miss 106
#year=2021   # -- GOOD ;
#year=2022   # -- GOOD 01-11 ; miss 108
#year=2005   # -- GOOD ;
#year=2004   # -- GOOD ;
#year=2003   # -- GOOD ;
#year=2002   # -- GOOD ;
#year=2023 # --GOOD 2023010100-053123
year=2024

ibdir='/w21/dat/pr/imerg/cmorph_grid/'
ibdir='/data/w22/dat/pr/imerg/cmorph_grid/'
MF.ChangeDir(ibdir)
nfiles=glob.glob("%d/*.nc4"%(year))

syear=str(year)
MF.ChangeDir(syear,verb=1)

imergtxt="imerg-%s.txt"%(syear)
if(year == 2022): imergtxt="imerg-%s-01-11.txt"%(syear)
if(year == 2023): imergtxt="imerg-%s-0101-0531.txt"%(syear)
if(year == 2024): imergtxt="imerg-%s-01-11.txt"%(syear)
wlines=open(imergtxt).readlines()
wfiles={}
for wline in wlines[2:]:
    #print wline
    tt=wline.split('?')
    for t in tt:
        if(mf.find(t,'LABEL')):
            #print t
            ww=t.split('%')
            for w in ww:
                if(mf.find(w,'LABEL')):
                    #print w
                    ll=w.split('&')
                    for l in ll:
                        if(mf.find(l,'LABEL')):
                            #print 'll',len(ll),'--',l
                            wfile=l.split('=')[-1].strip()
                            wfiles[wfile]=wline


kk=wfiles.keys()
kk.sort()
nwfiles=len(kk)
nnfiles=len(nfiles)

print 'NN comp for %s: NW: ',nwfiles,' NNC: ',nnfiles,' diff: ',nwfiles-nnfiles

doMiss=1
if(nwfiles != nnfiles and doMiss):
    mpath='imerg-missing-%s-V1.txt'%(syear)
    mm=open(mpath,'w')

    for wfile in kk:
        siz=MF.getPathSiz(wfile)
        if(siz <= 0):
            ifile=wfiles[wfile]
            print siz,wfile,ifile
            mm.writelines(ifile)
            
        # -- kill off 0 size .nc4
        if(siz == 0):
            cmd="rm -i %s"%(wfile)
            mf.runcmd(cmd,ropt)
        


