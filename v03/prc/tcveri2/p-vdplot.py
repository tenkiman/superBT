#!/usr/bin/env python

from ad2vm import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class MyearVd2aCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'basinOpt':            ['b:','w','a','basins'],
            'modelOpt':            ['T:',None,'a','aids to plot'],
            'otauOpt':             ['o:','72','a',"""output Tau; 'all' for a single year""" ],
            'phrOpt':              ['h:','','a',""" ['']  no BC | 0 - 0-h BC | 6 - 6-h BC"""],
            'pfilt':               ['f:','','a',"""filter: 'z0012' | 'z0618'..."""],
            'veriOptHomo':         ['H',0,1,"""" 1 for homogeneous; [0] for heterogeneous """],
            'doxv':                ['X',0,1,"""" 1 -> xv plot """],
            'veriStat':            ['p:','pe-line','a',"""['pe'] for position error | 'pod' | gainxype """],
            'yearOpt':             ['y:','2007.2018','a',"""byear.eyear for a range of years"""],
            'toptitle1':           ['1:',None,'a','toplabel1'],
            'toptitle2':           ['2:','','a','toplabel2'],
            'veriLabel':           ['l:',None,'a','veriLabel for zip file'],
            'doAllYears':          ['a',0,1,'do summary of allyears'],
            'dotable':             ['t',0,1,'do summary of allyears'],
            'pcase':               ['c:',None,'a','set pcase for pngpath'],
            'do2axis':             ['A',0,1,"""" use 2 axis plot"""],
            'verirule':            ['3:','std','a',"""set verirule: 'std' :: NHC rule  or 'td':: any posit >= 20kt or 'ts' :: initial posit is >=35 kts"""],
            }

        self.defaults={
            }

        self.purpose='''
purpose -- multi-year veristat processing'''

        self.examples='''
%s -y 2015 -t SR -b l -s fe -v h # homogeneous, Short-Range 
'''



#--MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM main
#

CL=MyearVd2aCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

setOpt='ncep'
#setOpt='navy'

MF.ChangeDir(CL.pydir)

if(setOpt == 'navy'):
    baseModels=[
        'hwrf','avno',
        'cotc','gnav',
        'tecmt',
        'clip5',
    ]
else:
    baseModels=[
        'hwrf','avno',
        'tecmt',
        'clip5',
    ]

if(modelOpt != None):
    baseModels=modelOpt.split(',')
    
allBasins=['w','e','l']

veriStatRead=veriStat
if(veriStat == 'gainxype'): 
    veriStat='gainxype'
    veriStatRead='pe'

elif(veriStat == 'pe-line'): 
    veriStat='pe-line'
    veriStatRead='pe'

elif(veriStat == 'pod-line'): 
    veriStat='pod-line'
    veriStatRead='pod'

# -- basins
#
basins=[basinOpt]
if(basinOpt == 'n'): basins=allBasins

# -- otaus
#

iotaus=otauOpt.split(',')
if(len(iotaus) > 1):
    otaus=[]
    for iotau in iotaus:
        otaus.append(int(iotau))
        
else:
    if(otauOpt.isdigit()): otaus=[int(otauOpt)]
    else:                  
        otau=otauOpt.upper()
        if(otau == 'ALL'): 
            otaus=['all']
        else:
            otaus=[otau]


# -- years
#
if(mf.find(yearOpt,'.')): 
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=int(tt[0])    
        eyear=int(tt[1])    
    else:
        print 'EEE bad yearOpt, must be byear.eyear of byear'
        sys.exit()
else:
    try:
        byear=eyear=int(yearOpt)
    except:
        print 'EEE bad yearOpt -- for single year must be YYYY'
        sys.exit()
        
if(phrOpt != '' and phrOpt.isdigit() ): phrOpt=int(phrOpt)
else: phrOpt=''

veriOpt='-H'
if(veriOptHomo): veriOpt=''

if(mf.find(veriStat,'pod')): veriOpt='-H'

# -- defaults DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#
ilstyle=ilwidth=None	
doland=1

ptype=veriStat
pltcntvar=None
pdir='%s/plt'%(CL.curdir)
dopng=1
doline=0

xlab=None
if(veriStat == 'pe-line' or veriStat == 'pod'): 
    if(dotable):
        xlab=''
        doline=1
    else:
        xlab='Year'
        doline=1
        dotable=0

    
docp=0
verb=verb
doshow=0
dosmooth=1

# -- make SSMs by basin -- contains all the stats
#
MF.sTimer('maksSMSs')
SSMs={}

# -- make SSM for multiple taus
#
for otau in otaus:
    for ibasin in basins:
        SSM=SumStatMultiYear(byear,eyear,ibasin,setOpt,
                             baseModels,veriOpt,phrOpt,
                             veriStat,veriStatRead,
                             otau,pfilt,
                             veriLabel=veriLabel,
                             verirule=verirule,
                             verb=verb)
        SSMs[ibasin,otau]=SSM


MF.dTimer('maksSMSs')

if(len(basins) == 1): basin=basins[0]
else:                 basin=basins[0]

# -- get basic info from the first
#
SSM=SSMs[basin,otaus[0]]

# -- set up SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#
models=SSM.models
times=SSM.years
if(otau == 'all'): times=SSM.taus
if(veriStat == 'gainxype'):
    stype=veriStat
else:
    stype=veriStatRead

#if(basin == 'w'): doAllYears=1
if(otau == 'all' and byear == eyear): 
    times=SSM.taus
    doAllYears=0
    
# -- top title
#

itoptitle1=toptitle1
itoptitle2=toptitle2

if(itoptitle1 == None):

    yeartitle="%d-%d"%(byear,eyear)
    if(byear == eyear): yeartitle="%d"%(byear)
    if(basinOpt == 'w'):
        toptitle1="WPAC %s tau: %s"%(yeartitle,str(otau))
    elif(basinOpt == 'e'):
        toptitle1="C+EPAC %s tau: %s"%(yeartitle,str(otau))
    elif(basinOpt == 'l'):
        toptitle1="LANT %s tau: %s"%(yeartitle,str(otau))
    elif(basinOpt == 'n'):
        toptitle1="NHEM %s tau: %s"%(yeartitle,str(otau))
    elif(basinOpt == 'h'):
        toptitle1="SHEM %s tau: %s"%(yeartitle,str(otau))


    # -- name of png file
    #
    omodels=modelOpt.replace(',','-')
    oyears=yearOpt.replace('.','-')
    oplotopt=''
    if(do2axis):oplotopt='cnts_'
        
    pcase="%s%s_%s_%s_%s_%s"%(oplotopt,basin,otau,omodels,oyears,SSM.veriLabel)
        
    # -- top title
    #
    toptitle1="%s pcase: %s"%(toptitle1,pcase)
    
# -- axis setting
#
plotcontrolVar=None
if(veriStat == 'gainxyfe' or veriStat == 'gainxype'):
    
    if(baseModels[-1] == 'clip5'):
        plotcontrolVar=([-40.0,100.0,10],2) # gainxyfe for hfip
    else:
        plotcontrolVar=([-40.0,80.0,10],2) # gainxyfe for hfip
        plotcontrolVar=([-20.0,40.0,5],2) # gainxyfe for era5

if(veriStat == 'fe' and otau == 'SR'):
    plotcontrolVar=([0.0,150.0,25],2) # gainxyfe for hfip
elif(veriStat == 'fe' and otau == 'MR'):
    plotcontrolVar=([0.0,300.0,50],2) # gainxyfe for hfip
elif(veriStat == 'fe' and otau == 'LR'):
    plotcontrolVar=([0.0,600.0,50],2) # gainxyfe for hfip

if(veriStat == 'pe' and otau == 'SR'):
    plotcontrolVar=([0.0,150.0,25],2) # gainxyfe for hfip
elif(veriStat == 'pe' and otau == 'MR'):
    plotcontrolVar=([0.0,300.0,50],2) # gainxyfe for hfip
elif(veriStat == 'pe' and otau == 'LR'):
    plotcontrolVar=([0.0,600.0,50],2) # gainxyfe for hfip

# -- initial position/intensity error
#
if(veriStat == 'pe' and otau == 0):
    plotcontrolVar=([0.0,150.0,25],2)

if((veriStat == 'pe-line' or veriStat == 'pe') and otau == 72):
    plotcontrolVar=([0.0,500.0,50],2)

if((veriStat == 'pod-line' or veriStat == 'pod')):
    plotcontrolVar=([0,50,60,70,75,80,85,90,95,100,120],2)
    
if(veriStat == 'vbias' and otau == 0):
    plotcontrolVar=([-40.0,20.0,10],2) 

#if(veriStat == 'pod'):
    #try: cotau=int(otau)
    #except: cotau=otau 
    #if(cotau == 'MR'):
        #plotcontrolVar=([0.0,250.0,25],2)
    #elif(otau == 'LR'):
        #plotcontrolVar=([0.0,350.0,50],2)
    #elif(otau == 'SR'):
        #plotcontrolVar=([0.0,150.0,25],2)
    #elif(otau == 'all'):
        #plotcontrolVar=([0.0,200.0,25],2)
    #elif( (cotau >= 72 and cotau <= 96) ):
        #plotcontrolVar=([0.0,700.0,25],2)
    #elif( (cotau >= 120) ):
        #plotcontrolVar=([0.0,350.0,50],2)
    #elif( (cotau >= 24 and cotau <= 60) ):
        #plotcontrolVar=([0.0,150.0,25],2)
    #else:
        #plotcontrolVar=([0.0,150.0,25],2)

sAlldicts={}
nAlldicts={}
MF.sTimer('makesDicts')
stype=veriStatRead
if(veriStat == 'gainxype'): stype=veriStat
for otau in otaus:
    (sdicts,ndicts)=setDicts(SSMs, models, basins, times, otau, otaus, stype, doAllYears,verb=verb)
    sAlldicts[otau]=sdicts
    nAlldicts[otau]=ndicts
    
sdicts=sAlldicts[otaus[0]]
ndicts=nAlldicts[otaus[0]]
if(verb): 
    print '00000',sdicts[0][0]
    print 'NNNNN',ndicts[0]

# -- combine into one sdicts
#
if(len(otaus) == 2):
    sdicts=combineSdicts(sAlldicts,otaus)
    if(verb): print 'CCCCC',sdicts
    

MF.dTimer('makesDicts')

MF.sTimer('makePlot')

taids=SSM.models
tstmids=[]

ostats={}
cases={}
casedtgs={}

verivars=getVerivars(veriStat)                                # from vdVM.py

ss=SumStats(taids,tstmids,                                    # a class() from vdCL.py
            verivars,ostats,
            cases,casedtgs)

rc=getPvarivars(ptype,pcase,toptitle1)                        # vdVM.py


(pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,toptitle1,toptitle2)=rc

if(itoptitle2 != None):
    toptitle2=itoptitle2


pss=SumStatsPlot(ss.models,ss.vstmids,pcase,ptype,pdir=pdir,doland=doland)
#if(verb): pss.ls()

pss.setPlottitles(toptitle1,toptitle2,SSM.taus,xlab=xlab)

if(pltcntvar != None):
    tt=pltcntvar.split(',')
    plotcontrolVar=([float(tt[0]),float(tt[1]),float(tt[2])],2)

pss.setControls(controlsVar=plotcontrolVar)

#if(baseModels[-1] == 'clip5' and not(mf.find(veriStat,'gainxy'))): pss.controls[0][1]=pss.controls[0][1]*2.0

if(len(otaus) == 2): do2ndplot=1

if(do2axis):
    
    #do2ndplot=1
    pss.simpleplot2axis(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,  # a class() from vdCL.py
                        ilmarker=ss.markaids,
                        do1stplot=do1stplot,
                        do2ndplot=do2ndplot,
                        dopng=1,
                        ilstyle=ilstyle,
                        ilwidth=ilwidth,
                        do2ndval=do2ndval,
                        doline=doline,
                        doxv=doxv,
                        docp=1,
                        verb=verb,
                        doErrBar=doErrBar,
                        dotable=dotable,
                        dosmooth=dosmooth,
                        maxcounts=4000,
                        doshow=doshow)
    
    
else:

    pss.simpleplot(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,  # a class() from vdCL.py
                   ilmarker=ss.markaids,
                   do1stplot=do1stplot,
                   do2ndplot=do2ndplot,
                   dopng=1,
                   ilstyle=ilstyle,
                   ilwidth=ilwidth,
                   do2ndval=do2ndval,
                   doline=doline,
                   doxv=doxv,
                   docp=1,
                   verb=verb,
                   doErrBar=doErrBar,
                   dotable=dotable,
                   dosmooth=dosmooth,
                   doshow=doshow)

MF.dTimer('makePlot')
