#!/usr/bin/env python

from sBT import *

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'doCatAll':         ['C',0,1,'cat f??? to single file'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
filter era5 fields for wmo verification"""

        self.examples='''
%s 1953090700'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
def makeWmoFldList(dtg,override=0,verb=0):
    
    def wmoCtl(dtg):
        
        ntimes=21
        
        gtime=mf.dtg2gtime(dtg)
        
        ctl="""dset  ^era5-w2flds-%s-ua-f%%f3.grb2
index ^era5-w2flds-%s-ua.gmp2
undef 9.999E+20
title t-era5-12-si.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
tdef  %d linear %s 12hr
* PROFILE hPa
zdef   9 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000
options pascals template
vars 6
psl    0,101      0,  3,  0   ** mean sea level Pressure [Pa]
ua     9,100      0,  2,  2   ** mponent of Wind [m/s]
va     9,100      0,  2,  3   ** V-Component of Wind [m/s]
ta     9,100      0,  0,  0   ** Temperature [K]
hura   9,100      0,  1,  1   ** Relative Humidity [%%]
zg     9,100      0,  3,  4   ** Geopotential [m^2/s^2]
ENDVARS"""%(dtg,dtg,ntimes,gtime)
        
        return(ctl)
        
        
    btau=0
    etau=240
    dtau=12
    otaus=range(btau,etau+1,dtau)
    
    ovars={
        'GP':(500,),
        'PRES':(1013,),
        'UGRD':(850,200),
        'VGRD':(850,200),
        'RH':(700,),
        'TMP':(700,)
      }
    
    ofilts={}
    
    #print otaus
    
    year=dtg[0:4]
    sbdir=era5DatDir
    tbdir=era5WmoDatDir
    
    sdir="%s/%s/%s"%(sbdir,year,dtg)
    tdir="%s/%s/%s"%(tbdir,year,dtg)
    MF.ChkDir(tdir,'mk')
    if(verb):
        print 'sdir: ',sdir
        print 'tdir: ',tdir
        
    grbbase='era5-w2flds-%s-ua'%(dtg)
    grb2path="%s/%s.grb2"%(sdir,grbbase)
    wlstpath="%s/%s.wgrib2.txt"%(sdir,grbbase)
    
    g2siz=MF.getPathSiz(grb2path)
    lssiz=MF.getPathSiz(wlstpath)

    lsMinsiz=83000
    # check if wgrib2.txt path ok...if not redo
    #
    if(lssiz < lsMinsiz):
        print 'WWW-need to redo %s ...'%(wlstpath)
        cmd='wgrib2 %s > %s'%(grb2path,wlstpath)
        mf.runcmd(cmd)
        lssiz=MF.getPathSiz(wlstpath)
        if(lssiz < lsMinsiz):
            card='NNooJJooYY %s FU...'%(grb2path)
            print card
            fu2path="%s/grb2-FU-%s"%(tdir,dtg)
            cmd='touch %s'%(fu2path)
            mf.runcmd(cmd)
            return
        else:
            print 'III-redo of %s is GOOD '%(wlstpath)
            wgrbcards=open(wlstpath).readlines()
    else:
        wgrbcards=open(wlstpath).readlines()

    for wcard in wgrbcards:
        ww=wcard.split(":")
        if(len(ww) >= 7):
            var=ww[3].strip()
            lev=ww[4]
            tau=ww[5]
        else:
            print 'BBB wcard: ',wcard,'press...'
            continue

        if(tau == 'anl'):
            itau=0
        else:
            itau=tau.split()[0]
            itau=int(itau)
            
        if(mf.find(lev,'mean sea')):
            ilev=1013
        elif(mf.find(lev,'mb')):
            #lev=lev.strip()
            ilev=lev.split()[0].strip()
            ilev=int(ilev)

        elif(mf.find(lev,'10 m')):
            ilev='10'
        if(var in ovars.keys()):
            #print 'vvv',var,'ii',ilev,'kk','oo',ovars[var]
            if( (ilev in ovars[var])  and (itau in otaus) ):
                if(verb): print 'oooo---vvvv',var,lev,'ii',itau,ilev,'cccc',wcard[0:-1]
                MF.appendDictList(ofilts,itau,wcard)
                
    oftaus=ofilts.keys()
    oftaus.sort()

    didgrb=0
    
    # -- all path for ensemble
    #
    agpath="%s/%s.grb2"%(tdir,grbbase)
    asiz=MF.getPathSiz(agpath)
    doCat=1
    if(asiz > 0):
        print 'WWW -- all file already done...',agpath
        doCat=0
        return
    print 'CCC--CCC doCat: ',doCat
        
    for oftau in oftaus:
        #print 'ooff',oftau,len(ofilts[oftau])
        gpath="%s/%s-f%03d.grb2"%(tdir,grbbase,oftau)
        wpath="/tmp/%s.%03d.txt"%(grbbase,oftau)
        gsiz=MF.getPathSiz(gpath)
        if(doCat and gsiz > 0):
            cmd="cat %s >> %s"%(gpath,agpath)
            mf.runcmd(cmd,ropt)
        if(gsiz > 0 and not(override)):
            print 'WWW already done: ',gpath
            continue
            
        MF.WriteList2Path(ofilts[oftau],wpath,verb=0)
        cmd="cat %s | wgrib2 -i %s -grib %s"%(wpath,grb2path,gpath)
        mf.runcmd(cmd,ropt)
        os.unlink(wpath)
        didgrb=1
        
    if(didgrb):
        
        ctl=wmoCtl(dtg)
        octlpath="%s/%s.ctl"%(tdir,grbbase)
        rc=MF.WriteCtl(ctl,octlpath)
    
        cmd='gribmap -v -i %s'%(octlpath)
        mf.runcmd(cmd,ropt)
        
    
    return
    
    
argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer('ALL-wmo-%s'%(dtgopt))
dtgs=dtg_dtgopt_prc(dtgopt)
for dtg in dtgs:
    rc=makeWmoFldList(dtg,override=override)
MF.dTimer('ALL-wmo-%s'%(dtgopt))
    
