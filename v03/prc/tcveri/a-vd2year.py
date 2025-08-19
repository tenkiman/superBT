#!/usr/bin/env python

from ad2vm import *

def getBasins4Stmopt(stmopt):

    basins=[]
    bopt=stmopt.split('.')[0]
    bb=bopt.split(',')
    if(len(bb) > 1):
        basins=bb
    elif(bopt == 'all'):
        basins=['h','i','w','e','l']
    else:
        basins=[bopt]
        
    return(basins)

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

    
basins=getBasins4Stmopt(istmopt)


MF.sTimer('a-vd2-ALL')

# -- load aids-storms
#
stmopts=getStmopts(stmopt)
years=range(1945,2024+1)
aidStms=loadAd2Inv(years)
aidsStmOpt={}

# -- load vd2 yearly output
#
MF.sTimer('loadVd2Stats')
vd2Stats=loadVd2Stats(pstat)
MF.dTimer('loadVd2Stats')

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
    
 
# -- mmmaaaiiinnn processing loop by stmopts
#

MF.sTimer('VD-anl-All')              

years=[]
logpaths=[]
MF.sTimer('get-logpaths')
for stmopt in stmopts:
    
    (aidstrs,tstmids)=getAidstrs(stmopt,aidStms,verb=verb,warn=0)
    nstms=len(tstmids)
    year=stmopt.split('.')[-1]
    years.append(year)
    
    print 'Nstms %2d for stmopt: %s year: %s' %(nstms,stmopt,year)
    

kk=vd2Stats.keys()
kk.sort()
otau=0
for k in kk:
    kbasin=k[0]
    kyear=k[1]
    kmodel=k[2]
    ktau=k[3]
    kstat=k[4]
    
    if( (kbasin in basins) and (kyear in years) and ktau == otau and kstat == pstat and mf.find(kmodel,'era5')):
        print 'kkk',k,vd2Stats[k]
    
    


MF.dTimer('a-vd2-ALL')
        
sys.exit()
