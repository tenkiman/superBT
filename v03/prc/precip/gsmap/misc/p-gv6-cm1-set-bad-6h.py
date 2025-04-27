#!/usr/bin/env python

from M import *
MF=MFutils()

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

#source='gv6' ; year='2008'
#source='gv6' ; year='2020'
source='cm1' ; year='2020'
source='cm1' ; year='2021'
source='cm1' ; year='2022'
ropt='norun'
#ropt=''

if(source == 'gv6'):
    undefPath="%s-%s-undef.txt"%(source,year)
elif(source == 'cm1'):
    undefPath="%s-%s-undef.txt"%(source,year)
    
ulines=open(undefPath).readlines()

baddtgs=[]
for uline in ulines:
    uu=uline.split()
    dd=uu[0].split(":")
    #print dd
    dtg="%4d%0.2d%0.2d%.2d"%(int(dd[0]),int(dd[1]),int(dd[2]),int(dd[3]))
    if(mf.find(uu[1],'e')):
        baddtgs.append(dtg)
        #print dtg,uu[1]
        
baddtgs.sort()

if(source == 'gv6'):    
    gmask='/dat21/dat/pr/pr_gsmapV6/grib/%s/prg_a06h*.grb'%(year)
elif(source == 'cm1'):
    gmask='/dat21/dat/pr/pr_cmorph/grib/%s/prc_a06h_%s*.grb'%(year,year)
    
gmask="%s-BAD"%(gmask)
print 'ggg',gmask
grbpaths=glob.glob(gmask)
grbpaths.sort()

gpaths={}
for gpath in grbpaths:
    (gdir,gfile)=os.path.split(gpath)
    gdtg=gfile.split('.')[0].split('_')[-1]
    #print gfile,gdtg
    gpaths[gdtg]=gpath

gdtgs=gpaths.keys()
gdtgs.sort()

print 'BBB %s %s n: %3d'%(source,year,len(gdtgs))
sys.exit()
for gdtg in gdtgs:
    print gpaths[gdtg]

sys.exit()

for bdtg in baddtgs:
    if(bdtg in gdtgs):
        bpath=gpaths[bdtg]
        opath="%s-BAD"%(bpath)
        gsiz=MF.getPathSiz(bpath)
        cmd="mv %s %s"%(bpath,opath)
        mf.runcmd(cmd,ropt)


sys.exit()




nfiles=glob.glob("%d/*.nc4"%(year))

syear=str(year)
MF.ChangeDir(syear,verb=1)

imergtxt="imerg-%s.txt"%(syear)
if(year == 2022): imergtxt="imerg-%s-01-11.txt"%(syear)
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
        


