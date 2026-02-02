#!/usr/bin/env python

from ad2vm import *


def getDsbdir(dssDir):
    
    if(dssDir != None):
        dsbdir=dssDir
        
    else:
        # -- local for DSs or DSs-local in .
        #
        dsbdir="%s/DSs"%(TcDataBdir)
        localDSs=os.path.abspath('./DSs')
        localDSsLocal=os.path.abspath('./DSs-local')
        
        if(os.path.exists(localDSs) and dolocalDSs):
            print 'llllllllllll',localDSs
            dsbdir=localDSs
            
        elif(os.path.exists(localDSsLocal) and dolocalDSs):
            print 'llllllllllll--------lllllllllll',localDSsLocal
            dsbdir=localDSsLocal
    
        else:
            dsbdir="%s/DSs"%(TcDataBdir)
            
    return(dsbdir)
        

def getBd2Years(tstmids,dsbdir,override=0,rmInteractive=0):
    
    byears=[]
    for tstmid in tstmids:
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        byears.append(byear)
        
    byears=mf.uniq(byears)
    print 'bd2year     bd2siz     bdpath'
    for byear in byears:
        bd2path="%s/bd2-%s.pypdb"%(dsbdir,byear)
        bsiz=MF.getPathSiz(bd2path)
        bsiz=float(bsiz)/(1024)
        print '%s        %5dK     %s'%(byear,mf.nint(bsiz),bd2path)
        if(override):
            rmopt=''
            if(rmInteractive): rmopt='-i'
                 
            mf.runcmd("rm %s %s"%(rmopt,bd2path))
            bsiz=MF.getPathSiz(bd2path)
            bsiz=float(bsiz)/(1024)
            print 'override=1  new bd2path...'
            print '%s        %5dK     %s'%(byear,mf.nint(bsiz),bd2path)
            
    
    return(byears)
    
def makeBdeck2s(fstmids,md3,domiss=0,
                warn=0,verb=0):
    
    bd2s={}
    
    m3stmids={}
    
    for fstmid in fstmids:
        (tstmid,m2stmid)=fstmid
        m3stmids[tstmid]=m2stmid

    tstmids=m3stmids.keys()
    tstmids.sort()
    
    for tstmid in tstmids:
        
        # -- get ATCF adeck cards
        #
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        
        # -- get stmcards
        #
        (rc,m3cards)=md3.getMd3Cards(tstmid)
        #print 'stmcards',len(m3cards)
        (smeta,smetacard)=md3.getMd3StmMeta(tstmid)
        ss9=smeta[-2]
        stmDev=None
        ss=ss9.split( )
        stm9xid="%s.%s"%(ss[-1],byear)
        sname=smeta[4]
        basin=sbtB1id2Basin[b1id]
        useVmax4TcCode=1
        m3trk=MD3trk(m3cards,stm1id,stm9xid,dom3=1,isBD2=1,sname=sname,basin=basin,stmDev=stmDev,
                     useVmax4TcCode=useVmax4TcCode,
                     verb=verb)        
    
        utstmid=tstmid.upper()
        MF.sTimer('bds-%s'%(utstmid))
        bd2s[utstmid]=Bdeck2(m3trk,tstmid,verb=0)
        MF.dTimer('bds-%s'%(utstmid))

        # -- look for alternate stmid
        #
        m3stmid=m3stmids[tstmid].upper()
        if(m3stmid != utstmid):
            MF.sTimer('bds-%s'%(m3stmid))
            print 'WWW add md2 stmid ',m3stmid,' bd2 -- the same bd2 as md3 stmid ',utstmid
            bd2s[m3stmid]=Bdeck2(m3trk,tstmid,verb=0)
            MF.dTimer('bds-%s'%(m3stmid))
                    
        continue
        
    return(bd2s)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'dssDir':              ['D:',None,'a','set base dir for DSs'],
            'verb':                ['V',0,1,'verb is verbose'],
            'override':            ['O',0,1,'override and delete previous bd2'],
            'quiet':               ['q',0,1,'1 - turn off all diag messages'],
            'ropt':                ['N','','norun',' norun is norun'],
            'doBT':                ['B',0,1,'only display best track info, if bd2 then set to 1'],
            'doBdeck2':            ['2',0,1,'use bdeck2'],
            'yearOpt':             ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'dobt':                ['b',1,0,'dobt=1 UNLESS set...do ALL TCs and pTCs'],
            'stmopt':              ['S:',None,'a','stmopt'],
            'dtgopt':              ['d:',None,'a','dtgopt to get tstmids'],
            'doput':               ['P',1,0,'do NOT put bd2'],
            'dols':                ['l',0,1,'1 - list'],
            'dolslong':            ['L',0,1,'1 - long list'],
            'dolsfull':            ['F',0,1,'1 - full list'],
            'strictChkIfRunning':  ['s',1,0,'do NOT do strict check if running -- any instance'],
            'corrTauDisCont':      ['C',0,1,'correct tau discontinuity by interp -- mainly for ecmwf trackers'],
            'dolocalDSs':          ['x',1,0,'do NOT use local DSs dir'],
            'warn':                ['W',1,0,'do NOT use bdeck2 (ln -s for 2024->)'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- bd2 from sBT vice mD2 %s'''
        self.examples='''
%s -S w.15
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' for errAD option: ',option
    elif(option == 'stmopt'):
        print 'EEE must set -S stmopt OR -d dtgopt'
    elif(option == 'source'):
        print 'EEE must set source for no plain args and NOT doing -l -L'
    else:
        print 'Stopping in errAD: ',option
    sys.exit()
        

def warnAD(option,opt=None):

    if(option == 'taids'):
        print 'WWW # of taids = 0 :: no stms to verify...stmopt: ',stmopt
    else:
        print 'continuing in warnAD: ',option



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    
# -- get inventory of aids 1945-2024
#
years=range(1945,2024+1)
aidStms=loadAd2Inv(years)

MF.sTimer('all-AD2')

(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)

if(doBdeck2): doBT=1

# -- get Mdeck3 with tc best track
#
md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

# -- set the dsbdir
#
dsbdir=getDsbdir(dssDir)

# -- get stmids
#
if(stmopt == None and dtgopt == None): errAD('stmopt')

if(stmopt != None):
      
    # -- specific for making bd2 .. always best track posits only
    #
    dobt=1
    dofilt9x=0
    doNNand9X=0
    
    tstmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        tstmids=tstmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

    # -- get bd2 years and paths and optionally rm -i to start with fresh files
    #
    byears=getBd2Years(tstmids,dsbdir,override=override)
        
    # -- get the md3 and md2 stmids
    #
    fstmids=getFstmids4Tstmids(tstmids,aidStms)

    # -- make the bd2
    #
    bd2s=makeBdeck2s(fstmids,md3,warn=warn,verb=verb)

    # -- PPPPBBBB - put Bdeck2
    #
    if(doput):

        MF.sTimer('bds-put')
        bDSs=putBdeck2sDataSets(bd2s,dsbdir=dsbdir,verb=verb)
        MF.dTimer('bds-put')
    
        for byear in byears:
            bsiz=MF.getPathSiz(bDSs[byear].path)
            bsiz=float(bsiz)/(1024)
            MF.sTimer('bds-put-%-5.0f Kb'%(bsiz))
            MF.dTimer('bds-put-%-5.0f Kb'%(bsiz))

else:
    print 'EEE must set the stmopt to make md3 bd2s...'
    
MF.dTimer('all-AD2')
sys.exit()
    
