#!/usr/bin/env python

from ad2vm import *

def setVd2aRun(
#               pstat,
#               stmopt,pstag,ftag,htag,
#               bypassOver,modelOpt,
warn=0,
override=0,
               
):

    svdir='./vd2out'
    logpath='%s/vd2out-%s-%s-%s-%s.txt'%(svdir,stmopt,pstag,ftag,htag)
    lsiz=MF.getPathSiz(logpath)

    
    if(lsiz > 0 and not(override)):
        if(warn): print 'WWW logpath: %s already done...'%(logpath)
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
        

def parseVdStats(pstat,pfilt,istmopt,logpaths,verb=0):

    allStats={}
    taus=[]
    years=[]
    ibasin=istmopt.split(".")[0]
    
    MF.sTimer('parseVd2Year')
    
    for logpath in logpaths:
        
        (ldir,lfile)=os.path.split(logpath)
        
        ll=lfile.split('-')
        (basin,year)=ll[1].split('.')
        #print 'lll',basin,year,logpath,lfile
        years.append(year)
        try:
            cards=open(logpath).readlines()
        except:
            cards=[]
                

        for card in cards:
            
            if(mf.find(card,'nada')):continue
            if(not(mf.find(card,'SSHH'))): continue
                
            tt=card.split()
            if(verb): print 'card:',tt
            n=1
            model=tt[n]        ; n=n+1
            tau=int(tt[n])     ; n=n+1  ; taus.append(tau)
            stype=tt[n]        ; n=n+1
            stat=float(tt[n])  ; n=n+2
            ncounts=int(tt[n]) 

            if(stype == 'pod'):
                n=n+2
                nfc=int(tt[n])

            # -- full record
            #
            if(len(tt) >= 19):
                n=n+2
                mean=float(tt[n])    ; n=n+1
                amean=float(tt[n])   ; n=n+1
                sigma=float(tt[n])   ; n=n+2
                minv=float(tt[n])    ; n=n+1
                ptl25=float(tt[n])   ; n=n+2
                median=float(tt[n])  ; n=n+1
                ptl75=float(tt[n])   ; n=n+1
                ptl90=float(tt[n])   ; n=n+1
                maxv=float(tt[n])    ; n=n+1
                
                ostat=(stat,ncounts,minv,ptl25,median,ptl75,ptl90,maxv)
                if(verb): print 'oo--ss-pe ',year,model,tau,stype,ostat
                allStats[basin,year,model,tau,stype]=ostat
                
            else:
                if(verb): print 'ss-oo-pod',year,model,tau,stype,stat,ncounts,nfc
                ostat=(stat,ncounts,nfc)
                allStats[basin,year,model,tau,stype]=ostat

    taus=mf.uniq(taus)
    years=mf.uniq(years)
    byear=years[0]
    eyear=years[-1]

    tvdir='./vd2stat'

    opstat=pstat
    if(pfilt != None): opstat='%s-%s'%(opstat,pfilt)
    
    vd2pyp='%s/vd2Stat-%s-%s-%s-%s.pyp'%(tvdir,opstat,ibasin,byear,eyear)
    print 'vvvvvv',vd2pyp
    PS=open(vd2pyp,'w')
    pyp=allStats
    pickle.dump(pyp,PS)    
    MF.dTimer('parseVd2Year')
    
    return(allStats)



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
            'useTaids':         ['t',0,1,"""use taids vice vaids"""],
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

# -- load aids-storms
#
stmopts=getStmopts(stmopt)
years=range(1945,2024+1)
aidStms=loadAd2Inv(years)
aidsStmOpt={}

# -- load vd2 yearly output
#
vd2Stats=loadVd2Stats(pstat)

print 'vvv',vd2Stats['w','1945','tera5',0,pstat]
sys.exit()


pstag=pstat
psopt='-p %s'%(pstat)

# options - pfilt
#
fopt=''
ftag='all'

if(pfilt != None):
    fopt='-f %s'%(pfilt)
    ftag=pfilt
    
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
    

# -- first loop by stmopts to get aidstrs and tstmids
#
for stmopt in stmopts:
    (aidstrs,tstmids)=getAidstrs(stmopt,aidStms,verb=verb)
    aidsStmOpt[stmopt]=aidstrs
 
# -- mmmaaaiiinnn processing loop by stmopts
#

MF.sTimer('VD-anl-All')              

logpaths=[]
MF.sTimer('get-logpaths')
for stmopt in stmopts:

    year=stmopt.split('.')[-1]
    
    aidstrs=aidsStmOpt[stmopt]
    rc=aidstrAnl(aidstrs,add00=add00,verb=verb)
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

    print 'Nstms %2d for stmopt: %s' %(nstms,stmopt)

    (ovopt,logpath)=setVd2aRun(override=override)
    logpaths.append(logpath)
    
logpaths.sort()
MF.dTimer('get-logpaths')

vdStats={}
vdStats=parseVdStats(pstat,pfilt,istmopt,logpaths)

MF.dTimer('VD-anl-All')              
sys.exit()

kk=vdStats.keys()
kk.sort()


otau=0
for k in kk:
    #print 'kk',k,vdStats[k],pstat
    kbasin=k[0]
    kyear=k[1]
    kmodel=k[2]
    ktau=k[3]
    kstat=k[4]
    
    if(ktau == otau and kstat == pstat and mf.find(kmodel,'era5')):
        print 'kkk',k,vdStats[k]
    
    


        
sys.exit()
