#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

def makeGribCtl(dtg,region,grb,gmp,verb=0):

    gtime=mf.dtg2gtime(dtg)
    nt=5

    if(region == 'nhem'):
        xydims='''xdef 1440 linear    0.00   0.250
ydef 361 linear  -10.00   0.250'''

    elif(region == 'global'):
        xydims='''xdef 1440 linear    0.00   0.250
ydef 481 linear  -60.00   0.250'''
        
    elif(region == 'shem'):
        xydims='''xdef 1440 linear    0.00   0.250
ydef 281 linear  -60.00   0.250'''

    else:
        print 'EEE invalid region: ',region
        sys.exit()

    ctl2="""dset ^%s
index ^%s
undef 9.999E+20
title grads.lats.grb2
* produced by g2ctl v0.1.8
* command line options: grads.lats.grb2
* griddef=1:0:(1440 x 361):grid_template=0:winds(N/S): lat-lon grid:(1440 x 361) units 1e-06 input WE:SN output WE:SN res 48 lat -10.000000 to 80.000000 by 0.250000 lon 0.000000 to 359.750000 by 0.250000 #points=519840:winds(N/S)
dtype grib2
%s
tdef %d linear %s 6hr
* PROFILE hPa
zdef 9 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000
options pascals
vars 28
uas     0,1   0,3,0  ** uas 10-m wind [m/s]
vas     0,1   0,3,1  ** vas 10-m wind [m/s]
psl     0,1   0,3,2  ** psl [mb]
pr      0,1   0,2,14 ** pr prev 6 h [mm/d]
prw     0,1   0,3,3  ** precip h2o [mm]
vrt925  0,1   0,3,4  ** rel vort 925 mb [*1e5 /s]
vrt850  0,1   0,3,5  ** rel vort 850 mb [*1e5 /s]
vrt700  0,1   0,3,6  ** rel vort 700 mb [*1e5 /s]
zthklo  0,1   0,3,7  ** 600-900 thick [m]
zthkup  0,1   0,14,0 ** 300-600 thick [m] 
z900    0,1   0,0,0  ** 900 mb z [m]
z850    0,1   0,0,1  ** 850 mb z [m]
z800    0,1   0,0,2  ** 800 mb z [m]
z750    0,1   0,0,3  ** 750 mb z [m]
z700    0,1   0,0,4  ** 700 mb z [m]
z650    0,1   0,0,5  ** 650 mb z [m]
z600    0,1   0,0,6  ** 600 mb z [m]
z550    0,1   0,0,7  ** 550 mb z [m]
z500    0,1   0,0,8  ** 500 mb z [m]
z450    0,1   0,19,0 ** 450 mb z [m]
z400    0,1   0,15,6 ** 400 mb z [m]
z350    0,1   0,15,7 ** 350 mb z [m]
z300    0,1   0,15,8 ** 300 mb z [m]
ua      9,100 0,7,0  ** ua [m/s]
va      9,100 0,0,9  ** va [m/s]
hur     9,100 0,3,8  ** RH [%%]
ta      9,100 0,3,9  ** ta [K]
zg      9,100 10,0,0 ** z [m]
ENDVARS"""%(grb,gmp,xydims,nt,gtime)
    
    if(verb):
        print ctl2
        
        
    return (ctl2)
    

    ctl="""^%s
defined parameter table (center 100-2 table 128), using NCEP-opn
dset ^grads.lats.grb
index ^grads.lats.grb.idx
undef 9.999E+20
title grads.lats.grb
*  produced by grib2ctl v0.9.12.5p16

defined parameter table (center 100-2 table 128), using NCEP-opn
dtype grib 255
ydef 361 linear -10.000000 0.25
xdef 1440 linear 0.000000 0.250000
tdef 5 linear 00Z10oct2021 6hr
zdef 9 levels
1000 925 850 700 500 400 300 250 200
vars 28
uas       0  1,1,0  ** uas [m/2]    
vas       0  2,1,0  ** vas [m/2]
psl       0  3,1,0  ** Pressure tendency [Pa/s]
pr        0  4,1,0  ** Pot. vorticity [km^2/kg/s]
prw       0  5,1,0  ** ICAO Standard Atmosphere Reference Height [M]
vrt925    0  6,1,0  ** Geopotential [m^2/s^2]
vrt850    0  7,1,0  ** Geopotential height [gpm]
vrt700    0  8,1,0  ** Geometric height [m]
zthklo    0  9,1,0  ** Std dev of height [m]
zthkup    0 10,1,0  ** Total ozone [Dobson]
z900      0 11,1,0  ** zg 900 [m]
z850      0 12,1,0  ** zg 900 [m]
z800      0 13,1,0  ** z
z750      0 14,1,0  ** Pseudo-adiabatic pot. temp. [K]
z700      0 15,1,0  ** Max. temp. [K]
z650      0 16,1,0  ** Min. temp. [K]
z600      0 17,1,0  ** Dew point temp. [K]
z550      0 18,1,0  ** Dew point depression [K]
z500      0 19,1,0  ** Lapse rate [K/m]
z450      0 20,1,0  ** Visibility [m]
z400      0 21,1,0  ** Radar spectra (1) [non-dim]
z350      0 22,1,0  ** Radar spectra (2) [non-dim]
z300      0 23,1,0  ** Radar spectra (3) [non-dim]
ua        9 24,100,0 ** ua [m/s]
sva        9 26,100,0 ** va [m/s]
hur       9 25,100,0 ** RH [%%]
ta        9 27,100,0 ** ta [K]
zg        9 28,100,0 ** zg [m]
ENDVARS"""



from WxMAP2 import *
w2=W2()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
        }


        self.options={
            'doClean':          ['K',1,0,'do NOT clean .dat and .grb files'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
make inventory of era5 tmtrkN runs by year"""

        self.examples='''
%s cur12 ukm2 tukm2'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)


MF.sTimer("ALL-lats")
for dtg in dtgs:
    
    MF.sTimer("GRIB2-%s"%(dtg))
    year=dtg[0:4]
    eraDir='/braid1/mfiorino/w22/dat/tc/tcanal/%s/%s/era5'%(year,dtg)
    eraDir='/data/w22/dat/tc/tcanal/%s/%s/era5'%(year,dtg)
    
    emask="%s/era5.%s.*.ctl"%(eraDir,dtg)
    efiles=glob.glob(emask)
    n1=len(efiles)
    
    emask2="%s/era5.%s.*.ctl2"%(eraDir,dtg)
    efiles2=glob.glob(emask2)
    n2=len(efiles2)

    ctl1path2=None
    if(n1 == 1):
        ctl1path=efiles[0]
    elif(n1 == 2):
        ctl1path=efiles[0]
        ctl1path2=efiles[1]
       
    elif(n1 == 0 and n2 == 1):
        print '222 -- ALready DONE for dtg: ',dtg
        continue
    else:
        print '111 -- no tcanal files for dtg: ',dtg
        continue
        
    bases=[]
    (epath,efile)=os.path.split(ctl1path)
    (base,ext)=os.path.splitext(ctl1path)
    region=base.split('.')[-1]
    bases.append(base)

    region2=None
    base2=None
    if(ctl1path2 != None):
        (epath2,efile2)=os.path.split(ctl1path2)
        (base2,ext)=os.path.splitext(ctl1path2)
        region2=base2.split('.')[-1]
        bases.append(base2)

    if(verb):
        print 'bbb',base
        print 'eee',epath,efile
        print 'rrr',region
        if(base2 != None):
            print 'bbb222',base2
            print 'eee222',epath2,efile2
            print 'rrr222',region2

    for base in bases:
        grb1path="%s.grb"%(base)
        grb2path="%s.grb2"%(base)
        gmp2path="%s.gmp2"%(base)
        ctl2path="%s.ctl2"%(base)
        (gdir,grb2file)=os.path.split(grb2path)
        (gdir,gmp2file)=os.path.split(gmp2path)
        
        if(verb):
            print '111',grb1path
            print '222',grb2path,grb2file
            print '222',gmp2path,gmp2file
            print 'CCC',ctl2path
            
        rc=MF.ChkPath(grb2path)
    
        if(rc != 1 or override):
        
            ctl2=makeGribCtl(dtg,region,grb2file,gmp2file,verb=verb)
            MF.WriteCtl(ctl2, ctl2path)
            
            MF.sTimer("lats-%s"%(dtg))
            latscmd="lats4d.sh -i %s -format grib -precision 12 -o %s"%(ctl1path,grb1path)
            mf.runcmd(latscmd,ropt)
            MF.dTimer("lats-%s"%(dtg))
            
            MF.sTimer("grb2-%s"%(dtg))
            g2cmd="grb1to2.pl -o %s %s"%(grb2path,grb1path)
            mf.runcmd(g2cmd,ropt)
            MF.dTimer("grb2-%s"%(dtg))
            
            MF.sTimer("gmp2-%s"%(dtg))
            ctl2cmd="gribmap -v -i  %s"%(ctl2path)
            mf.runcmd(ctl2cmd,ropt)    
            MF.dTimer("gmp2-%s"%(dtg))
        
            MF.dTimer("GRIB2-%s"%(dtg))
            
        else:
            print 'III -lats for: ',dtg,' ALL ready done...'
            
        if(doClean):
            rc=MF.ChkPath(grb2path)
            dmask=("%s*.dat"%(base))
            ndats=glob.glob(dmask)
            
            # -- make sure the .grb2 file is there before blowing away .dat
            #
            if(rc and len(ndats) == 5 or ropt == 'norun'):
                MF.sTimer("clean .dat -- %s"%(dtg))
                cmd="rm  %s*.dat"%(base)
                mf.runcmd(cmd,ropt)
            
                cmd="rm  %s"%(grb1path)
                mf.runcmd(cmd,ropt)
                
                cmd="rm  %s"%(ctl1path)
                mf.runcmd(cmd,ropt)
    
                MF.dTimer("clean .dat -- %s"%(dtg))
    
MF.dTimer("ALL-lats")
    