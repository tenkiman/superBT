#!/usr/bin/env python

from sBT import *


class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'model':            ['m:','ecop','a','model '],
            'tarea':            ['a:','nhem','a',"""tarea, e.g., 'nhem'"""],
            'tvar':             ['v:','zg','a',"""tvar = 'zg' | 'uva' | 'ua' | 'va'"""],
            'tstat':            ['s:','acc','a',"""tstat = 'acc'..."""],
            'tlev':             ['l:',500,'i',"""tlev = 850 | 500 | 200"""],
            'ttau':             ['t:',120,'i',"""ttau, e.g., 120"""],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
        }

        self.purpose="""
make mo mean of wmo stats"""

        self.examples='''
%s -Y 1945.2024 -a nhem '''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(yearOpt != None):
    
    if(mf.find(yearOpt,'-')):
        tt=yearOpt.split('-')
        byear=int(tt[0])
        eyear=int(tt[1])
    elif(mf.find(yearOpt,'.')):
        tt=yearOpt.split('.')
        byear=int(tt[0])
        eyear=int(tt[1])
    else:
        byear=int(yearOpt)
        eyear=int(yearOpt)
    
    years=mf.yyyyrange(byear,eyear)
else:
    print 'EEE you most set -Y year1[.year2]'
    sys.exit()

sStat={
    'acc':'acAnFcwmo',
}
    
kstat=sStat[tstat]

if(model == 'ecop'):
    modelFc=modelAn='ecopw'
elif(model == 'era5'):
    modelFc=modelAn='era5w'


MF.sTimer('ALL-%s-%s-%s'%(tstat,tvar,yearOpt))
for year in years:
    
    MF.sTimer('%s-%s'%(year,tstat))
    bddir='/raid05/%s-wmo/%s'%(model,year)
    pypdir="%s/veriWMO"%(bddir)

    dtgopt="%s01.%s12.12"%(year,year)
    vdtgs=dtg_dtgopt_prc(dtgopt)
    MF.sTimer('mo-wmo-veri-%s'%(year))

    omopath="./stats/mo/%s/mo-%s-%s-%s-%s-%03d-%03d.txt"%\
        (model,tstat,year,tvar,tarea,tlev,ttau)


    mostats={}
    
    for vdtg in vdtgs:
    
        pyppath="%s/wmo-veri-%s-%s-%s.pyp"%(pypdir,modelFc,modelAn,vdtg)
        
        try:
            PF=open(pyppath,'rb')
            (Stats)=pickle.load(PF)
        except:
            Stats=None
    
        vmo=vdtg[4:6]
        if(Stats != None):
            k1='%sw'%(model)
            tkey=(k1,k1,vdtg,tarea,ttau,tvar,tlev)
            try:
                ss=Stats[tkey]
            except:
                ss=None
                
            if(ss != None):
                if(hasattr(ss,kstat)):
                    if(tstat == 'acc'):
                        #odtg=MF.dtg2ISODateTime(vdtg)
                        ostat=ss.acAnFcwmo
                        card='dtg: %s %f'%(vdtg,ostat)
                        rc=appendDictList(mostats, vmo, ostat)
            else:
                ostat=1e20
                card='dtg: %s %g'%(vdtg,ostat)
        
            if(verb): print card
        
    mcards=[]
    mm=mostats.keys()
    mm.sort()
    yms=0
    for m in mm:
        nmo=len(mostats[m])
        ms=sum(mostats[m])/len(mostats[m])
        yms=yms+ms
        mcard="%s, %s, %03d, %f"%(year,m,nmo,ms)
        if(verb): print mcard
        mcards.append(mcard)
    
    yms=yms/12.0
    print 'YYYY--- mean: %s %f'%(year,yms)
    rc=MF.WriteList2Path(mcards,omopath,verb=verb)
    MF.dTimer('%s-%s'%(year,tstat))
            
        
MF.dTimer('ALL-%s-%s-%s'%(tstat,tvar,yearOpt))
sys.exit()
    
