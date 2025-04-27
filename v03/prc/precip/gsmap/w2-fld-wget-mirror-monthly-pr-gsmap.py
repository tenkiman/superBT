#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M import *
MF=MFutils()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.options={
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doit':          ['X',0,1,' norun is norun'],
            'yearOpt':       ['Y:',None,'a',' yearopt'],
            'doGauge':       ['G',0,1,'do doGauge'],
            'doWget':        ['W',0,1,'do wget of monthly .dat files'],
            
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''


def makeGsmapMonthlyCtl(year):
    
    
    dmask="*%s*dat"%(year)
    dfiles=glob.glob(dmask)
    ddf=dfiles[0]
    print ddf
    dd=ddf.split('.')
    gsversion=ddf[-13:-4]
    gsversion="%s.%s.%s"%(dd[-4],dd[-3],dd[-2])
    gsname=dd[0]
    print 'gggg',gsversion,ddf
    print 'gsname:',gsname,ddf.split('.')

    ctlpath="pr-gsmap-%s.ctl"%(year)
    nt=12
    prdtg="%s010100"%(year)
    gtime=mf.dtg2gtime(prdtg)
    
    ctl='''DSET ^%s.%%y4%%m2.0.1d.monthly.v8.dat
TITLE  GSMaP_MVK 0.1deg Hourly (ver.8)
OPTIONS YREV LITTLE_ENDIAN TEMPLATE
UNDEF  -99.0
XDEF   3600 LINEAR    0.05 0.1
YDEF   1200  LINEAR -59.95 0.1
ZDEF     1 LEVELS 1013
TDEF   %d LINEAR %s 1mo
VARS   2
pr    0  99 monthly averaged rain rate [mm/hr]
count 0  99 counts
ENDVARS'''%(gsname,nt,gtime)
    

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    
def makeGsmapMonthlyGribCtl(year,ropt=''):
    

    ctlpath="pr-gsmap-%s.ctl"%(year)
    nt=12
    prdtg="%s010100"%(year)
    gtime=mf.dtg2gtime(prdtg)
    
    ctl="""dset ^pr-gsmap-%%y4.grb
index ^pr-gsmap-%s.gmp
undef 9.999E+20
options template
dtype grib
xdef 1440 linear   0.125 0.25
ydef  480 linear -59.875 0.25
zdef    1 linear 1 1
tdef %d linear %s 1mo
vars 1
pr  0 59,1,0  ** Precipitation rate [mm/h]
ENDVARS"""%(year,nt,gtime)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    cmd="gribmap -v -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)
    

def makeGrib4Dat(tdir,fdir,curdir,year):

    mf.ChangeDir(tdir)

    gzfiles=glob.glob("*.gz")
    gzfiles.sort()
    
    for gzfile in gzfiles:
        print 'ggg',gzfile
        datfile=gzfile[0:-14]+'.dat'
        print 'ddd',datfile
        tt=datfile.split('.')
        zdtg="%s%s"%(tt[1],tt[2][0:2])
        grbpath="%s/%s-%s.grb"%(fdir,gname,zdtg)
        
        gsiz=MF.getPathSiz(grbpath)
        dsiz=MF.getPathSiz(datfile)
        
        cmd="gunzip -c %s > %s/%s"%(gzfile,fdir,datfile)
        mf.runcmd(cmd,ropt)


    mf.ChangeDir(fdir)
    rc=mf.ChangeDir(fdir)
    ifile=makeGsmapMonthlyCtl(year)
    ipath="%s/%s"%(fdir,ifile)
    opath="%s/%s-%s"%(fdir,gname,year)
        
    mf.ChangeDir(curdir)
    cmd='''grads -lbc "run %s/%s %s %s"'''%(curdir,gscmd,ipath,opath)
    mf.runcmd(cmd,ropt)
    rc=mf.ChangeDir(fdir)
    rc=makeGsmapMonthlyGribCtl(year)
    cmd="rm *.dat"
    mf.runcmd(cmd,ropt)



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='GSMAP-ALL')

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(yearOpt == None):
    print 'EEE must set yearOpt -Y'
    sys.exit()
    
yy=yearOpt.split('.')

if(len(yy) == 2):
    byear=int(yy[0])
    eyear=int(yy[1])
    years=range(byear,eyear+1)
else:
    years=[
        yearOpt,
    ]
    
    
al='rainmap'
ap="""Niskur+1404"""
af='hokusai.eorc.jaxa.jp'

gscmd="w2-fld-pr-gsmap-0p1deg-monthly-lats.gs"
gname='pr-gsmap'


MF.sTimer(tag='GSMAP-ALL')

for year in years:
    
    if(doGauge):
        sbdir='/standard/v8/monthly_G'
        tbdir='/data/w22/dat/pr/gsmapV8-G/monthly'
    else:
        sbdir='/standard/v8/monthly'
        tbdir='/data/w22/dat/pr/gsmapV8/monthly'
        mf.ChkDir(tbdir,'mk')
        
    
    sdir="%s/%s"%(sbdir,year)
    tdir="%s/incoming/%s"%(tbdir,year)
    fdir="%s/final/%s"%(tbdir,year)
    mf.ChkDir(fdir,'mk')
    
    if(doWget):
        mf.ChkDir(tdir,diropt='mk')
        mf.ChangeDir(tdir)
        cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*\""%(af,sdir)
        mf.runcmd(cmd,ropt)



    # -- remake grib because .dat is either .1.dat or .0.dat
    # -- the dat file is always just .dat
    #
    rc=makeGrib4Dat(tdir, fdir, curdir, year)
    
    continue
    
    mf.ChkDir(fdir,'mk')
    
    # -- first check if processed already...
    #
    opath1st="%s/%s"%(fdir,gname)
    gpaths1st=glob.glob("%s.grb"%(opath1st))
    lgpath1st=len(gpaths1st)


    if(lgpath1st and not(override)):
        print 'III dtg: ',dtg,'already done...press...'
        continue
        
    if(doWget and (lgpath1st == 0 or override)):
        
        mf.ChkDir(tdir,diropt='mk')
        mf.ChangeDir(tdir)

        cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*\""%(af,sdir)
        mf.runcmd(cmd,ropt)

        gzfiles=glob.glob("*.gz")
        gzfiles.sort()
        
        
        if(len(gzfiles) == 0 and ropt != 'norun'):
            print 'III -- not ready at jaxa for dtg: ',dtg
            continue
        
        for gzfile in gzfiles:
            datfile=gzfile[0:-3]
            tt=datfile.split('.')
            zdtg="%s%s"%(tt[1],tt[2][0:2])
            grbpath="%s/%s-%s.grb"%(fdir,gname,zdtg)
            
            gsiz=MF.getPathSiz(grbpath)
            dsiz=MF.getPathSiz(datfile)
            
            # -- only do the gunzip if no final grbfile
            #
            if((gsiz < 0 and dsiz < 0) or override):
                cmd="gunzip -c %s > %s/%s"%(gzfile,fdir,datfile)
                mf.runcmd(cmd,ropt)
            else:
                print 'III- %s already processed...press...'%(grbpath)
                
    
    mf.ChangeDir(fdir)
    rc=mf.ChangeDir(fdir)
    ifile=makeGsmapMonthlyCtl(year)
    ipath="%s/%s"%(fdir,ifile)
    opath="%s/%s-%s"%(fdir,gname,year)
    
    mf.ChangeDir(curdir)
    cmd='''grads -lbc "run %s/%s %s %s"'''%(curdir,gscmd,ipath,opath)
    mf.runcmd(cmd,ropt)
    rc=mf.ChangeDir(fdir)
    rc=makeGsmapMonthlyGribCtl(year)
    cmd="rm *.dat"
    mf.runcmd(cmd,ropt)
    
        
MF.dTimer(tag='GSMAP-ALL')

