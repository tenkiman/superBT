#!/usr/bin/env python

from sBT import *
from tcbase import TcData

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

def setTmtrkNDir(dtg):

    stcgbdir=adeckSdir
    year=dtg[0:4]
    ttcgbdir="%s/%s"%(tcgenbdir,year)
    MF.ChkDir(ttcgbdir,'mk')
        
    return(ttcgbdir,stcgbdir)

def getPrecip(tcG,prB,gentau,override):
    

    # -- get precip
    #
    pr=prB.getPrsTau(gentau)
    
    # -- processing tests -- dopr for either PRoverride | override  
    #
    if(pr == None): 
        prall1=0
    else:
        prall1=(pr[0] == 1 and pr[1] == 1 and pr[2] == 1)
        
    dopr=( pr == None or (len(pr) == 2) or ( len(pr) == 3 and pr[2] == -999. ) or prall1 or override)

    # -- if not done, look at the fields and get...TcPrBasin is only a container
    #
    if(dopr):
        pr=tcG.fldDiagTcGen(basin,gentau,dogendtg,quiet=quiet,verb=verb)

        try:
            prB.prs[gentau]=pr
        except:
            prB.prs={}
            prB.prs[gentau]=pr
        
    # -- put precip
    #
    if(dopr or override):
        MF.sTimer('putPrs')
        prB.putPrs()
        MF.dTimer('putPrs')
        
    return(pr)
    
    
    

class TcgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            #2:['modelopt',    'model|model1,model2|all|allgen'],            
        }

        self.defaults={
            'modelopt','era5',
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'ropt':             ['N',0,1,' run | no run q'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doBT':             ['B',0,1,'only display best track info, if bd2 then set to 1'],
            'doBdeck2':         ['2',0,1,'use bdeck2'],
            'yearOpt':          ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            'doNNand9X':        ['D',1,0,'do NOT list 9X that developed into NN'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'dogendtg':         ['T',0,1,' dogendtg -- set bdtg, gentau back from dtgopt'],
            'gentauOpt':        ['t:','all','a',"""gentauOpt -- fc tau opt for genesis: 'all'|'allgen'|'all24h'"""],
            'quiet':            ['q',1,0,' run GA in NOT quiet mode'],
            'overrideGA':       ['0',0,1,'overrideGA -- just track anl'],
            'lsInv':            ['l',0,1,' ls from inv'],
            
            
        }

        self.purpose="""
an 'ls' or listing app for 'mdeck3' data two filter options are available:
-S by storm"""

        self.examples='''
%s 1944121500 
%s 1945090700
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TcgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)

if(verb):
    print 'sss---',stmopt
    print 'ddd---',dtgopt
    print 'yyy---',yearOpt
    
    print 'ooo---yyy',oyearOpt
    print 'ooo---BBB',doBdeck2
    
if(doBdeck2):
    doBT=1
    
MF.sTimer('ALL')

if(verb): MF.sTimer('md3-load')
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
if(verb): MF.dTimer('md3-load')

dtgs=dtg_dtgopt_prc(dtgopt)
basins=['wpac']
basins=['lant']
model='era5'
diag=0
doclean=0
gentaus=[24,48,72,96,120]
gentaus=getGentaus(gentauOpt)

# -- LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
#
if(lsInv):
    for dtg in dtgs:
        (ttcgbdir,stcgbdir)=setTmtrkNDir(dtg)
        if(diag): MF.sTimer(tag='inV.ls')
        iV=InvHash(dsname='invTcgen.%s'%(dtg),
                   tbdir=ttcgbdir,
                   diag=diag,
                   verb=verb,
                   #override=doclean,unlink=doclean, -- no cleaing if doing ls...
                   )
        iV.lsInv([model],basins,[dtg],gentaus,dogendtg,oneline=1)
        if(diag): MF.dTimer(tag='inV.ls')
    sys.exit()


# -- make gaP object
#
xgrads=setXgrads(useStandard=0,useX11=0,returnBoth=0)

tcGP=TcgenGA(gaQuiet=quiet,overrideGA=overrideGA,xgrads=xgrads)

didPrc=0

for dtg in dtgs:

    (dtgstms,m3trks)=md3.getMd3tracks4dtg(dtg,dobt=dobt,doBdeck2=doBdeck2, 
                                          verb=verb)

    tcD=TcData(dtgopt=dtg)
    for stmid in dtgstms:
        card=printMd3Trk(m3trks[stmid],dtg)
        print card

        
    (ttcgbdir,stcgbdir)=setTmtrkNDir(dtg)

    if(diag): MF.sTimer(tag='inV')
    iV=InvHash(dsname='invTcgen.%s'%(dtg),
               tbdir=ttcgbdir,
               diag=diag,
               verb=verb,
               override=doclean,
               unlink=doclean)
    rc=iV.lsInv([model],basins,[dtg],gentaus,dogendtg,mode='chk')

        
    for basin in basins:

        # -- get basin obj
        #
        tcB=TcBasin(basin)
        
        # -- get precip state obj
        #
        prB=TcPrBasin(model,basin,dtg)

        for gentau in gentaus:

            bdtg=dtg
            if(dogendtg):
                bdtg=mf.dtginc(dtg,-gentau)
                prB=TcPrBasin(model,basin,bdtg,verb=1)

            # -- make tcG object -- put in the dtg, bdtg will be calc inside the obj
            #
            omodelPlot=None

            tcG=Tcgen(tcGP,tcD,iV,tcB,prB,model,basin,dtg,gentau,dogendtg,stcgbdir,
                      omodelPlot=omodelPlot,
                      verb=verb,
                      override=override,
                      overrideGA=overrideGA)

            pr=getPrecip(tcG,prB,gentau,override)
            
            tcG.setTCgenProps(gentau,dogendtg,verb=verb)


            # -- if tcG.done == -999 => no trackers available
            if(tcG.done != -999):
                tcG.compMtoO(dtg,gentau,dogendtg,verb=verb) 
            

            MF.sTimer('doInv-loop')
            tcG.doInv(iV,pr,overrideInv=1,verb=verb)
            MF.dTimer('doInv-loop')	

            # -- PPPLLLOOOTTT - prp
            #
            BMoverride=0
            doland=1
            dowindow=0
            doxv=0
            
            tcG.w2PlotTcGenFld(field='prp',dostdd=1,doxv=doxv,
                               dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                               verb=verb,override=override,quiet=quiet)
            
            if(not(tcG.allreadyDone)): didPrc=didPrc+1
            # -- PPPLLLOOOTTT - n850
            #
            tcG.w2PlotTcGenFld(field='n850',dostdd=1,doxv=doxv,
                               dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                               verb=verb,override=override,quiet=quiet)
            if(not(tcG.allreadyDone)): didPrc=didPrc+1

            # -- PPPLLLOOOTTT - uas
            #
            tcG.w2PlotTcGenFld(field='uas',dostdd=1,doxv=doxv,
                               dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                               verb=verb,override=override,quiet=quiet)
            if(not(tcG.allreadyDone)): didPrc=didPrc+1
            
        # -- put prs for basin
        #
        if(not(overrideGA)):
            prB.putPrs()    


    # -- iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    #    invoverride default is 1, set to 0 if doing a single model ot single gentau-- do inventory for tcgen.php
    #
    if(ropt != 'norun'):
        MF.sTimer('doInv-putPyp')
        iV.putPyp()
        MF.dTimer('doInv-putPyp')
            

MF.dTimer('ALL')



sys.exit()


