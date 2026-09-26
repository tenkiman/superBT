#!/usr/bin/env python

from ad2vm import *

def setVd2aRun(doZip,
#               pstat,
#               stmopt,pstag,ftag,htag,
#               bypassOver,modelOpt,
               override=0,
               ):
    
    if(doZip):
        
        tvdir='/tmp'
        logpath='%s/vd2inv-%s-%s-%s-%s.txt'%(tvdir,stmopt,pstag,ftag,htag)
        lsiz=MF.getPathSiz(logpath)
        
        vsiz=-999
        for vz in vzfiles:
            vpath="%s/%s"%(tvdir,vz)
            if(vpath == logpath):
                vsiz=MF.getPathSiz(vpath)
                vi=VZ.getinfo(vz)
                vdate=vi.date_time
                vsiz=vi.file_size
        
        ovopt=''
        if(vsiz > 0 and not(override)):
            print 'WWW vpath: %s already done in %s'%(vpath,zippath)
            return(ovopt,logpath)
    
        if(vsiz <= 0 or override):
            ovopt='-O'
        
        #if((pstat == 'pod' or pfilt != None) and not(override)):
        if((pstat == 'pod' or pfilt != None)):
            ovopt=''
    
        if(bypassOver or modelOpt != None):
            ovopt=''
            
    else:
        
        tvdir='./vd2out'
        logpath='%s/vd2out-%s-%s-%s-%s.txt'%(tvdir,stmopt,pstag,ftag,htag)
        lsiz=MF.getPathSiz(logpath)
        
        if(lsiz > 0 and not(override)):
            print 'WWW logpath: %s already done...'%(logpath)
            ovopt=None
            return(ovopt,logpath)
    
        if(lsiz <= 0 or override):
            ovopt='-O'
        
        #if((pstat == 'pod' or pfilt != None) and not(override)):
        if((pstat == 'pod' or pfilt != None)):
            ovopt=''
    
        if(bypassOver or modelOpt != None):
            ovopt=''
            
    return(ovopt,logpath)
        

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'bypassOver':       ['B',0,1,'bypass override'],
            'modelOpt':         ['T:',None,'a','aids to plot'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a','stmopt1:stmopt2:stmopt3...'],
            'add00':            ['0',1,0,'do NOT add 00 to aids for bias-corrected'],
            'pstat':            ['p:','pe','a',"""stat: ['pe'] | 'pod' | 'vbias'"""],
            'pfilt':            ['f:',None,'a',"""filter: 'z0012' | 'z0618'..."""],
            'ptype':            ['h',0,1,"""[0 - 'hetero'] | 1 - 'homo'"""],
            'warn':             ['w',0,1,"""print warning messages"""],
            'useTaids':         ['t',0,1,"""do NOT use taids vice vaids -- do alias in vdeck not adeck"""],
            'doZip':            ['Z',0,1,"""put to .zip file"""],
            'verirule':         ['3:','std','a',"""set verirule: 'std' :: NHC rule  or 'td':: any posit >= 20kt or 'ts' :: initial posit is >=35 kts"""],
        }

        self.purpose="""'
make atcf-form of trackers in adeck-stm"""

        self.examples='''
%s -S l.07  # dtgopt ignored'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgopt=yearOpt=None
istmopt=stmopt

stmopts=getStmopts(stmopt)
    
years=range(1945,2024+1)
aidStms=loadAd2Inv(years)

aidsStmOpt={}

prcdir='/w21/prc/tcdat'

# -- set top side options before going by stmopts
#
# options - pstat sets output
#
pstag=pstat
psopt='-p %s'%(pstat)

# options - pfilt
#
fopt=''
ftag='all'

# options - verirule
#
vropt=''
if(verirule != 'std' and verirule == 'ts'):
    vropt='-3 ts'

if(pfilt != None):
    fopt='-f %s'%(pfilt)
    ftag=pfilt

if(vropt != ''):
    ftag="%s-%s"%(ftag,verirule)
    
if(modelOpt != None):
    if(fopt != ''):
        ftag="%s-%s"%(ftag,modelOpt.replace(',','-'))
    else:
        ftag=modelOpt.replace(',','-')
    
# options - hetero | homo
#
hopt='-H'
htag='hetero'
if(ptype):
    hopt=''
    htag='homo'
    
# -- zip file
#
if(doZip):
    zippath='./vd2zip/vd2inv-%s-%s-%s.zip'%(pstag,ftag,htag)
    print 'zippath: %s'%(zippath)
    try:
        VZ=zipfile.ZipFile(zippath,'a')
    except:
        VZ=zipfile.ZipFile(zippath,'w')
    vzfiles=VZ.namelist()

MF.sTimer('VD-inv-All')              

# -- first loop by stmopts to get aidstrs and tstmids
#
for stmopt in stmopts:
    (aidstrs,tstmids,faidstr)=getAidstrs(stmopt,aidStms,verb=verb)
    aidsStmOpt[stmopt]=(aidstrs,faidstr)
 
# -- mmmaaaiiinnn processing loop by stmopts
#
for stmopt in stmopts:


    (aidstrs,faidstr)=aidsStmOpt[stmopt]
        
    rc=aidstrAnl(aidstrs,faidstr,add00=add00,verb=verb)
    (taids,vaids,aaids,taids00,vaids00,aaids00,tstmids)=rc


    nstms=len(tstmids)
    if(nstms == 0):
        if(warn): print 'WWW - no storms for stmopt: ',stmopt,' ... press ...'
        continue
        
    # options - vaopt taids
    # use taids to rename in vd2 decks
    #
    #
    if(useTaids):
        vaopt=taids
        vaopt00=taids00
    else:
        vaopt=vaids
        vaopt00=vaids00
        
    if(modelOpt != None):
        vaopt=modelOpt
        vaopt00=''
        for val in vaopt.split(','):
            vaopt00=vaopt00+"%s00,"%(val)
        vaopt00=vaopt00[0:-1]

    print
    print 'Nstms %2d for stmopt: %s aidopts: ' %(nstms,stmopt)
    print '   vaopt: ',vaopt
    print ' vaopt00: ',vaopt00
    print '  psopt: ',psopt,' fopt: ',fopt,' hopt: ',hopt,'vropt: ',vropt
    print

    (ovopt,logpath)=setVd2aRun(doZip,override=override)
    if(ovopt == None):
        continue
    
    # -- vd2a raw
    #
    MF.sTimer('vd2-%s'%(stmopt))
    vapp='w2-tc-dss-vd2-anl.py'
    cmd='''%s/%s -S %s -T %s %s %s %s %s %s | tee %s'''%\
        (prcdir,vapp,stmopt,vaopt,ovopt,hopt,fopt,vropt,psopt,logpath)
    mf.runcmd(cmd,ropt)
    
    # -- vd2a phr 00
    #
    if(add00):
        cmd='''%s/%s -S %s -T %s %s %s %s %s %s | tee -a %s'''%\
            (prcdir,vapp,stmopt,vaopt00,ovopt,hopt,fopt,vropt,psopt,logpath)
        mf.runcmd(cmd,ropt)
    MF.dTimer('vd2-%s'%(stmopt))

    # -- zip the output
    #
    if(doZip):
        (vdir,vfile)=os.path.split(logpath)
        if(ropt != 'norun'):
            VZ.write(logpath,vfile,compress_type = zipfile.ZIP_DEFLATED)
        else:
            print 'will zipfile.write logpath: ',logpath
        cmd="rm %s"%(logpath)
        mf.runcmd(cmd,ropt)
        VZ.close()

MF.dTimer('VD-inv-All')              
        
sys.exit()
