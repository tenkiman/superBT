#!/usr/bin/env pythonw

from sBT import *

sMdesc=lsSbtVars()
    
class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'doCarq':         ['q',0,1,'parse the cq0/12/24 and of12/24 objects on dds'],
            'doWorkingBT':    ['W',0,1,'using working/b*.dat for bdecks vice ./b*.dat'],
            'oPath':          ['o:',None,'a','write output to oPath'],
            'sumPath':        ['r:',None,'a','read path to generate summary card'],
            'doTrk':          ['T',1,0,'make the md3 trk by default'],
            'doBdeck2':       ['2',1,0,'this version does bdeck2 by default'],
            }

        self.purpose='''
make mdeck3'''
        
        self.examples='''
%s -S 30w.19'''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

md3=Mdeck3(doBT=0,doMd3Only=1)

if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,verb=verb)

    for stmid in stmids:
        (mpath,mpathBT,mpath9X,stmid9X)=getSrcSumTxt(stmid,verb=verb)

        if(verb == 0):
            print 'mpath:   ',mpath
            print 'mpathBT: ',mpathBT
            if(mpath9X != None): print 'mpath9X: ',mpath9X

    sys.exit()
    

# -- mmmmmmmmmmmmmmmmmmmmmmmmm main
#
isBT=0
isMRG=0
isDEV=0
isBD2=0
if(doBdeck2): isBD2=1

if(sumPath != None):
    
    if(mf.find(sumPath, '-BT.txt')):  isBT=1
    if(mf.find(sumPath, '-MRG.txt')): isMRG=1

    rc=getStmids4SumPath(sumPath)
    (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
    rc=getStmParams(ostm1id)
    b1id=rc[1]
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(isBD2 and mf.find(ostm9xid,'xx')): 
        stm9xid='%s%s.%s'%(b1id,stm1id[0:2],stm1id[-4:])
        #print 'stm9xid-XNN:',stm9xid,b1id

    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()
        isDEV=1
        
    try:
        icards=open(sumPath).readlines()
    except:
        print """EEE can't read sumPath: %s -- sayounara"""%(sumPath)
        sys.exit()
    
    (sdir,sfile)=os.path.split(sumPath)

    if(verb):
        print 'spath: ',sumPath
    ostm1id=stm1id.replace('.','-')

    ofile="%s-md3.txt"%(ostm1id.upper())
    if(mf.find(sfile,'BT')):
        ofile="%s-md3-BT.txt"%(ostm1id.upper())
        
    ofileS=ofile.replace('md3','sum-md3')

    if(mf.find(sfile,'MRG')):
        ofileS=ofile.replace('md3','sum-md3-MRG')
    
    opathS="%s/%s"%(sdir,ofileS)
    opath="%s/%s"%(sdir,ofile)

    opathSTmp="/tmp/%s"%(ofileS)
    opathTmp="/tmp/%s"%(ofile)

    if(verb):
        print 'stm1id: ',stm1id	
        print 'stm9xid: ',stm9xid

        print 'sname:  ',sname
        print 'stmDev: ',stmDev

        print 'sdir:   ',sdir
        print 'sfile:  ',sfile

        print 'ofile:  ',ofile
        print 'ofileS: ',ofileS
        
        print 'opath:  ',opath
        print 'opathS: ',opathS

    if(verb):    
        for icard in icards:
            print 'iii',icard[0:-1]
        
    useVmax4TcCode=1
    ocards=[]
    dom3=0
    if(isMRG): dom3=0
    md3=MD3trk(icards,stm1id,stm9xid,isBD2=isBD2,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,
               useVmax4TcCode=useVmax4TcCode,verb=verb)
    dtgs=md3.dtgs
    trk=md3.trk
    basin=md3.basin
    
    # -- analyze the stm to make summary card
    #
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    print '222-M2SUM: ',m3sum[0:-1]
    if(isMRG):
        print '333-MMM',rcsum,m3sum[0:-1],opathS
        rc=MF.WriteString2Path(m3sum, opathS)
    else:
        if(isBT):
            print '222-BBB',rcsum,m3sum[0:-1]
        else:
            print '222-999',rcsum,m3sum[0:-1]

    # -- now do trk
    #

    if(doTrk):

        ktrk=trk.keys()
        ktrk.sort()
        ocards=[]
        
        for kt in ktrk:
            ocard=parseDssTrkMD3(kt,trk[kt],stm1id,stm9xid,basin,rcsum=rcsum,sname=sname)
            ocard=ocard.replace(' ','')
            if(verb): print 'ooo---iii',ocard,len(ocard.split(','))
            ocards.append(ocard)

        rc=MF.WriteList2Path(ocards, opathTmp,verb=verb)
        (m3trk,m3info)=getMd3trackSpath(opathTmp,verb=verb)
        m3trki=setMd3track(m3trk,stm1id,verb=verb)
        dtgs=m3trki.keys()
        dtgs.sort()
        
        m3cards=[]
        for dtg in dtgs:
            try:
                m3i=m3info[dtg]
                m2trk=trk[dtg]
            except:
                None
                #m3i=['','']
            im3trk=m3trki[dtg]
            #print im3trk[0:5],m3i,len(m3trk),len(m3i)
            #m2trk.ls()
            m3card=makeMd3Card(dtg,im3trk, m3i,m2trk,useM3Iname=1,verb=verb)
            m3cards.append(m3card)
        #md3.m3tri=m3trki
        print 'all path: ',opath
        rc=MF.WriteList2Path(m3cards, opath,verb=verb)

        md3=MD3trk(m3cards,stm1id,stm9xid,dom3=1,isBD2=1,sname=sname,basin=basin,stmDev=stmDev,
                   useVmax4TcCode=useVmax4TcCode,
                   verb=verb)
        print 'sum path: ',opathS
        (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
        m3sum=m3sum.replace(' ','')
        m3sum=m3sum+',\n'
        print '333-M3SUM: ',m3sum[0:-1]
        rc=MF.WriteString2Path(m3sum, opathS)
        if(isBT):
            print '333-NNN',rcsum,m3sum[0:-1]
        else:
            print '333-999',rcsum,m3sum[0:-1]
        

