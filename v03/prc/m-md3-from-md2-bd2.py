#!/usr/bin/env pythonw

from tcbase import TcData

from sBT import *

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
            'doTrk':          ['T',0,1,'make the md3 trk from the -sum.txt files'],
            'doBdeck2':       ['2',1,0,'this version does bdeck by default'],
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

# -- storms
#
if(stmopt != None):

    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt=None,yearOpt=None)
    
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=0,doMd3Only=1)
    
    tcD=TcData(stmopt=stmopt,doWorkingBT=doWorkingBT,doBdeck2=doBdeck2,verb=verb)
    stmids=tcD.makeStmListMdeck(stmopt,dobt=dobt,cnvSubbasin=0,verb=verb)
    
    for stmid in stmids:
          
        dobt=0      
        print 'stmid: ',stmid
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        
        dds=tcD.getDSsFullStm(stmid, dobt=dobt, doprint=0, set9xfirst=0, dowarn=0)
        scard=tcD.lsDSsStmSummary(dds,stmid,doprint=0)
        
        # -- bypass active storms
        #
        ss=scard.split()
        snumSum=ss[1]
        if(mf.find(snumSum,'*')):
            print 'WWW--stmid: ',stmid,"""is still active...don't make tdir yet...press..."""
            continue
        
        #dds.ls()
        sname=dds.sname
        # -- replace ' ' with '_'
        sname=sname.replace(' ','_')
        
        try:
            stmid9x=dds.stmid9x.upper()
        except:
            stmid9x=None
            
        try:
            stmidNN=dds.stmidNN.upper()
        except:
            stmidNN=None
            
        try:
            stm1id=dds.stm1id
        except:
            stm1id=None
            
        if(IsNN(stmid)):
            tname=stmid.replace('.','-').upper()
            osname=sname.upper()
            ostmid9x=stmid9x[0:3].upper()
            # -- handle case of shem using two subbasins
            #
            if(osname[0:2] == 'TC'):
                osname=osname[0:2]+tname[0:3]
            if(ostmid9x[0:2] == 'XX'):
                ostmid9x=ostmid9x[0:2]+tname[2]
            #print 'tttnnn---',osname,'9x: ',ostmid9x
            tname="%s-%s-%s"%(tname,osname,ostmid9x)
        elif(stmidNN != None):
            tname=stmid9x.replace('.','-').upper()
            tname="%s-DEV-%s"%(tname,stmidNN[0:3].upper())
        elif(stm1id != None):
            tname=stm1id.replace('.','-').upper()
            tname="%s-NONdev"%(tname)

        basin=md3.getBasin4b1id(b1id)
        tdir="%s/%s/%s"%(sbtSrcDir,year,basin)
        
        # -- look for existing tdir
        #
        b3id="%s%s"%(snum,b1id.upper())
        bd1mask="%s/%s*"%(tdir,b3id)
        bd1s=glob.glob(bd1mask)

        #print 'adsfasdf',stmid,bd1s
        #continue
        if(len(bd1s) == 1):
            tdirNew="%s/%s"%(tdir,tname)
            tdir=bd1s[0]
            if(tdir != tdirNew):
                print 'WWW-existing-tdir != current...'
                print 'WWW-tdirNew:   ',tdirNew
                if(doBdeck2):
                    print 'WWW-tdir(old): ',tdir,' rm -r'
                    cmd="rm -r %s"%(tdir)
                else:
                    print 'WWW-tdir(old): ',tdir,' rm -r -i'
                    cmd="rm -r -i %s"%(tdir)
                    
                mf.runcmd(cmd,ropt)
                tdir=tdirNew
            else:
                print 'III-tdir for: ',stmid,'already there: ',tdir
        else:
            tdir="%s/%s"%(tdir,tname)
            print 'WWW-tdir for: ',stmid,'...making target dir: ',tdir
            MF.ChkDir(tdir,'mk')
            
            

        oPath="%s/%s-sum.txt"%(tdir,b3id)
        oPathBT="%s/%s-sum-BT.txt"%(tdir,b3id)
        
        ocards=[]
        trk=dds.trk
        dtgs=dds.dtgs
        ktrk=trk.keys()
        ktrk.sort()

        for kt in ktrk:
            ocard=parseDssTrk(kt,trk[kt])
            if(verb): print ocard
            ocards.append(ocard)

        # -- write to oPath != None
        #
        if(oPath != None):
            MF.WriteList2Path(ocards,oPath,verb=verb)
        
        if(IsNN(stmid)): 
            dobt=1
            ocards=[]
            dds=tcD.getDSsFullStm(stmid, dobt=dobt, doprint=0, set9xfirst=0, dowarn=0)
            trk=dds.trk
            dtgs=dds.dtgs
            ktrk=trk.keys()
            ktrk.sort()
    
            for kt in ktrk:
                ocard=parseDssTrk(kt,trk[kt])
                if(verb): print ocard
                ocards.append(ocard)
        
            if(oPathBT != None):
                MF.WriteList2Path(ocards,oPathBT,verb=verb)
                


        if(doCarq): getCarq(dds)
        


