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
            'model':            ['m:','era5','a','model '],
            'doCatAll':         ['C',0,1,'cat f??? to single file'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'diag':             ['D',0,1,'turn on diag'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
filter era5 fields for wmo verification"""

        self.examples='''
%s 1953090700'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
def makeWmoFldList(dtg,model='era5',override=0,verb=0):

    def parseWgrbcards(ofilts,wgrbcards):
    
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
                
            elif(mf.find(tau,' acc') or mf.find(tau,' max') or mf.find(tau,' min')):
                tt=tau.split()
                tauunit=tt[1].split()[0]
                tau=tt[0].split('-')[0]
                if(tauunit == 'day'):
                    itau=24*int(tau)
                else:
                    itau=int(tau)
                    
            else:
                itau=tau.split()[0]
                itau=int(itau)
                
            if(mf.find(lev,'mean sea')):
                ilev=1013
            elif(mf.find(lev,'surface')):
                ilev=-999
            elif(mf.find(lev,'mb')):
                #lev=lev.strip()
                ilev=lev.split()[0].strip()
                ilev=int(ilev)
            elif(mf.find(lev,'10 m')):
                ilev='10'
                
            if(var in ovars.keys()):
                #print 'iii---vvv',var,ilev,ovars[var],itau,ww[0:-1]
                #nonmsl=(var == 'PRES' and lev != 1013)
                if( (ilev in ovars[var])  and (itau in otaus) ):
                    #print 'oooo---vvvv',var,lev,'ii',itau,ilev,'cccc',wcard[0:-1]
                    MF.appendDictList(ofilts,itau,wcard)
        return

    def getEcmtWgribList(tau,model,verb=0):

        ofilts={}

        if(model == 'ecmt'):
            
            grb2path="%s/%s.f%03d.grb2"%(sdir,grbbase,tau)
            wlstpath="%s/%s.f%03d.wgrib2.txt"%(sdir,grbbase,tau)
            
        elif(model == 'ecm6'):
            grb2path="%s/%s-%03d.grb2"%(sdir,grbbase,tau)
            wlstpath="%s/%s-%03d.wgrib2.txt"%(sdir,grbbase,tau)
        
        g2siz=MF.getPathSiz(grb2path)
        lssiz=MF.getPathSiz(wlstpath)
        
        if(verb):
            print 'ggggg',grb2path,g2siz
            print 'lllll',wlstpath,lssiz

        return(wlstpath,lssiz)
        

    def getOfilts(ofilts,wlstpath,lssiz,lsMinsiz,verb=0):
        
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
            
    
        rc=parseWgrbcards(ofilts, wgrbcards)
        
    
    
                    
        #oftaus=ofilts.keys()
        #oftaus.sort()
    
        
    
    def wmoCtl(model,dtg,omodel):
        
        ntimes=21
        
        gtime=mf.dtg2gtime(dtg)
        
        if(model == 'era5' or model == 'ecm5'):
            
            ctl="""dset  ^%s-w2flds-%s-ua-f%%f3.grb2
index ^%s-w2flds-%s-ua.gmp2
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
ENDVARS"""%(omodel,dtg,omodel,dtg,ntimes,gtime)
            
            
        elif(model == 'ecmt'):
            
            ctl="""dset  ^%s-w2flds-%s-ua-f%%f3.grb2
index ^%s-w2flds-%s-ua.gmp2
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
hus    9,100      0,  1,  0   ** Relative Humidity [%%]
z      9,100      0,  3,  5   ** Geopotential height [m]
ENDVARS"""%(omodel,dtg,omodel,dtg,ntimes,gtime)

        elif(model == 'ecm6'):
            
            ctl="""dset  ^%s-w2flds-%s-ua-f%%f3.grb2
index ^%s-w2flds-%s-ua.gmp2
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
z      9,100      0,  3,  5   ** Geopotential height [m]
ENDVARS"""%(omodel,dtg,omodel,dtg,ntimes,gtime)
            
            
        
        return(ctl)
        
    def sortUVOfilts(owfilts,verb=0):
        
        """ special routine to sort winds for wgrib2 -new_grid
"""
        ucards={}
        vcards={}
        outcards=[]
        
        for ow in owfilts:
            ww=ow.split(":")
            var=ww[3]
            lev=ww[4].split()[0]
            if(var[0] == 'U'):
                ucards[lev]=ow
            elif(var[0] == 'V'):
                vcards[lev]=ow
            else:
                outcards.append(ow)
                
        uvlevs=ucards.keys()
        uvlevs.sort()
        
        for uvlev in uvlevs:
            outcards.append(ucards[uvlev])
            outcards.append(vcards[uvlev])
        
        if(verb):
            for ocard in outcards:
                print ocard
            
        return(outcards)
            
        
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
    
    year=dtg[0:4]
    
    if(model == 'era5'):
        sbdir=era5DatDir
        tbdir=era5WmoDatDir
    elif(model == 'ecmt'):
        omodel='ecop'
        sbdir=ecmtDatDir
        tbdir=ecopWmoDatDir
    elif(model == 'ecm5'):
        omodel='ecop'
        sbdir=ecm5DatDir
        tbdir=ecopWmoDatDir
    elif(model == 'ecm6'):
        omodel='ecop'
        sbdir=ecm6DatDir
        tbdir=ecopWmoDatDir
        
    
    sdir="%s/%s/%s"%(sbdir,year,dtg)
    tdir="%s/%s/%s"%(tbdir,year,dtg)
    MF.ChkDir(tdir,'mk')
    if(verb):
        print 'sdir: ',sdir
        print 'tdir: ',tdir
        
    if(model == 'era5'):
        
        grbbase='era5-w2flds-%s-ua'%(dtg)
        grb2path="%s/%s.grb2"%(sdir,grbbase)
        ogrb2path="%s/%s.grb2"%(sdir,grbbase)
        wlstpath="%s/%s.wgrib2.txt"%(sdir,grbbase)
        lsMinsiz=83000
        
    elif(model == 'ecm5'):

        oftaus=None
        grbbase='ecm5-w2flds-%s-ua'%(dtg)
        ogrbbase='ecop-w2flds-%s-ua'%(dtg)
        grb2path="%s/%s.grb2"%(sdir,grbbase)
        wlstpath="%s/%s.wgrib2.txt"%(sdir,grbbase)
        regridopt='-set_grib_type c1 -new_grid_interpolation bilinear -new_grid latlon 0:720:0.5 -90:361:0.5 '
        lsMinsiz=83000

    elif(model == 'ecmt'):

        grbbase='ecmt.w2flds.%s'%(dtg)
        ogrbbase='ecop-w2flds-%s-ua'%(dtg)
        grb2path="%s/%s.grb2"%(sdir,grbbase)
        wlstpath="%s/%s.wgrib2.txt"%(sdir,grbbase)
        oftaus=otaus
        lsMinsiz=2300
        regridopt=None
        ovars={
            'HGT':(500,),
            'PRES':(1013,),
            'UGRD':(850,200),
            'VGRD':(850,200),
            'SPFH':(700,),
            'TMP':(700,)
          }

    elif(model == 'ecm6'):

        grbbase='ecm6-w2flds-%s'%(dtg)
        ogrbbase='ecop-w2flds-%s-ua'%(dtg)
        grb2path="%s/%s.grb2"%(sdir,grbbase)
        wlstpath="%s/%s.wgrib2.txt"%(sdir,grbbase)
        oftaus=otaus
        lsMinsiz=2800
        regridopt='-set_grib_type c1 -new_grid_interpolation bilinear -new_grid latlon 0:720:0.5 -90:361:0.5 '
        ovars={
            'HGT':(500,),
            'PRES':(1013,),
            'UGRD':(850,200),
            'VGRD':(850,200),
            'RH':(700,),
            'TMP':(700,)
          }


    else:
        print 'invalid model....',model,'press...'
        sys.exit()
        
    
    # -- aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa all taus in single file 
    # -- era5 & ecm5
    #
    if(oftaus == None):
        
        g2siz=MF.getPathSiz(grb2path)
        lssiz=MF.getPathSiz(wlstpath)
        
        
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


        rc=parseWgrbcards(ofilts, wgrbcards)
        
        oftaus=ofilts.keys()
        oftaus.sort()


    # -- ssssssssssssssssssssssssssssssssssssssssssss - taus in single individual files 
    # -- ecmt & ecm6
    #
    else:
        
        for tau in otaus:
            (wlstpath,lssiz)=getEcmtWgribList(tau,model)
            rc=getOfilts(ofilts,wlstpath,lssiz,lsMinsiz)

        oftaus=ofilts.keys()
        oftaus.sort()
        if(verb):
            
            for oftau in oftaus:
                print 'ooo',oftau,ofilts[oftau]

    
    # -- wwwwwwwwggggggggggggrrrrrrrrrrrrrrriiiiiiiiiiibbbbbbbbbbbbbbbb222222222222
    #
    # -- now do wgrib2 filt of fields for fldveri and regrid for ecm5 and ecm6
    #
    didgrb=0
    for oftau in oftaus:
        #print 'ooff',oftau,len(ofilts[oftau])
      
        gpath="%s/%s-f%03d.grb2"%(tdir,ogrbbase,oftau)
      
        if(model == 'ecmt'):
            gpath="%s/%s-f%03d.grb2"%(tdir,ogrbbase,oftau)
            grb2path="%s/%s.f%03d.grb2"%(sdir,grbbase,oftau)
        elif(model == 'ecm6'):
            gpath="%s/%s-f%03d.grb2"%(tdir,ogrbbase,oftau)
            grb2path="%s/%s-%03d.grb2"%(sdir,grbbase,oftau)
      
        tgpath="/tmp/tt-%s.grb2"%(dtg)
        wpath="/tmp/%s.%03d.txt"%(grbbase,oftau)
        gsiz=MF.getPathSiz(gpath)
        igsiz=MF.getPathSiz(grb2path)
        if(gsiz > 0 and not(override)):
            print 'WWW already done: ',gpath
            break
        elif(igsiz <= 0):
            print 'gpath missing...press...for dtg: ',dtg,'model: ',model
            didgrb=0
            override=0
            break
        
        # -- 20260326 -- sort fields to filter so u;v are together
        #
        owfilts=ofilts[oftau]
        owfilts=sortUVOfilts(owfilts)
        
        MF.WriteList2Path(owfilts,wpath,verb=0)
        
        if(regridopt != None):
            cmd="cat %s | wgrib2 -i %s -grib %s"%(wpath,grb2path,tgpath)
            mf.runcmd(cmd,ropt)
            # -- now regrid to 0.5 0.5
            cmd="wgrib2 %s %s %s"%(tgpath,regridopt,gpath)
            mf.runcmd(cmd,ropt)
            os.unlink(tgpath)
        else:
            cmd="cat %s | wgrib2 -i %s -grib %s"%(wpath,grb2path,gpath)
            mf.runcmd(cmd,ropt)

        os.unlink(wpath)
        didgrb=1

    if(didgrb or override):
        
        ctl=wmoCtl(model,dtg,omodel)
        octlpath="%s/%s.ctl"%(tdir,ogrbbase)
        rc=MF.WriteCtl(ctl,octlpath)
    
        cmd='gribmap -v -i %s'%(octlpath)
        mf.runcmd(cmd,ropt)
        
    
    return
    
    
argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(diag): MF.sTimer('ALL-wmo-%s'%(dtgopt))
dtgs=dtg_dtgopt_prc(dtgopt)
for dtg in dtgs:
    rc=makeWmoFldList(dtg,model=model,override=override)
if(diag): MF.dTimer('ALL-wmo-%s'%(dtgopt))
    