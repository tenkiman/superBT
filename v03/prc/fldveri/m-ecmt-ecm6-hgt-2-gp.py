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

def replaceZwithGP(gpath,dtg,ropt='',verb=0):

    nozPath="/tmp/noz-%s.grb2"%(dtg)
    gpPath="/tmp/gp-%s.grb2"%(dtg)
    wpath="/tmp/wl-%s.wgrib2.txt"%(dtg)
    wgribout='/tmp/wgrib-out-%s.txt'%(dtg)

    gdir,gfile=os.path.split(gpath)
    ogpath="/tmp/%s"%(gfile)
    
    # -- first check of HGT...
    #
    gothgt=0
    cmd0='''wgrib2 %s > %s'''%(gpath,wpath)
    ropt='quiet'
    mf.runcmd(cmd0,ropt)
    wlcards=open(wpath).readlines()
    for wlcard in wlcards:
        if(mf.find(wlcard,':HGT:')):
            gothgt=1
            break

    if(not(gothgt)):
        if(verb): print 'III-already has GP in %s ...press...'%(gpath)
        os.unlink(wpath)
        rc=0
        return(rc)

    cmd1='''wgrib2 %s   -not ":HGT:"                              -grib_out %s >> %s'''%(gpath,nozPath,wgribout)
    mf.runcmd(cmd1,ropt)
    
    cmd2='''wgrib2 %s -match ":HGT:" -rpn "9.80665:*" -set_var GP -grib_out %s >> %s'''%(gpath,gpPath,wgribout)
    mf.runcmd(cmd2,ropt)
    
    cmd3="cat %s > %s"%(nozPath,ogpath)
    mf.runcmd(cmd3,ropt)

    cmd4="cat %s >> %s"%(gpPath,ogpath)
    mf.runcmd(cmd4,ropt)
    
    os.unlink(nozPath)
    os.unlink(gpPath)
    
    cmd5="mv %s %s.SAV"%(gpath,gpath)
    mf.runcmd(cmd5,ropt)
    
    cmd6="mv %s %s"%(ogpath,gpath)
    mf.runcmd(cmd6,ropt)
    
    #cmd='cat %s'%(wgribout)
    #mf.runcmd(cmd,ropt)
    os.unlink(wgribout)
    rc=1
    return(rc)

# -- mmmmmmmmmmmmmmmmmmmmmmmmaaaaaaaaaaiiiiiiiiiinnnnnnnnnnnnnnnnnnn
#
    
btau=0
etau=240
dtau=12
otaus=range(btau,etau+1,dtau)

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=dtg_dtgopt_prc(dtgopt)

if(diag): MF.sTimer('ALL-z-to-gp-%s'%(dtgopt))
for dtg in dtgs:
    
    year=dtg[0:4]

    if(model == 'ecmt'):
        tbdir=ecopWmoDatDir
        ogrbbase='ecop-w2flds-%s-ua'%(dtg)
    elif(model == 'ecm6'):
        tbdir=ecopWmoDatDir
        ogrbbase='ecop-w2flds-%s-ua'%(dtg)
    else:
        print 'invalid model'
        sys.exit()
    
    tdir="%s/%s/%s"%(tbdir,year,dtg)
    if(verb):
        print 'sdir: ',sdir
        print 'tdir: ',tdir
        
    MF.sTimer('hgt-gp-%s'%(dtg))
    rcfinal=0
    for otau in otaus:
        gpath="%s/%s-f%03d.grb2"%(tdir,ogrbbase,otau)
        savpath="%s.SAV"%(gpath)
        savsiz=MF.getPathSiz(savpath)
        gsiz=MF.getPathSiz(gpath)
        if(savsiz > 0 and not(override)):
            if(verb): print 'III hgt-gp model: %s  dtg: %s tau: %03d ...ALLREADY done...press...'%(model,dtg,otau)
            continue
        if(gsiz <= 0):
            print 'WWW hgt-gp not fields for dtg: ',dtg,' otau: ',otau
            if(model != 'ecm6'): 
                break
            else:
                continue
        
        rc=replaceZwithGP(gpath,dtg,ropt)
        if(rc):
             rcfinal=1
             
    if(rcfinal == 0):
        print 'HGT-GP already done for: ',dtg
    elif(rcfinal == 1):
        print 'Did the HGT-GP process for: ',dtg
        MF.dTimer('hgt-gp-%s'%(dtg))
        
if(diag): MF.dTimer('ALL-z-to-gp-%s'%(dtgopt))
