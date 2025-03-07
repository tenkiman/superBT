#!/usr/bin/env python

from sBT import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
        }


        self.options={
            'yearOpt':          ['Y:',None,'a','yearOpt for setting paths of md3'],
            'dtgopt':           ['d:',None,'a','dtgopt'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'ls9only':          ['9',0,1,'ls9only'],
            'ls1only':          ['1',0,1,'ls1only'],
            'lsAll':            ['A',0,1,'ls all'],
            'doSig':            ['G',0,1,'ls only Sig'],
            'do9Xonly':         ['X',0,1,'ls only Sig'],
            'doReRun':          ['R:',0,'i','rerun singletone'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

r9vmin=35
r9latmax=40.0
r1vmin=35
r1latmax=40.0
r999={}
r111={}
rall={}
n11=0
n99=0
n11sig=0
n99sig=0
naa=0

if(yearOpt != None and dtgopt == None):
    year=yearOpt
    iyear=str(year)
    dtgopt="%s01.%s12.6"%(iyear,iyear)
    
doInvPath=1
yearOpt=None
(oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)
doBT=0
if(doBdeck2): doBT=1

print 'oyearOpt: ',oyearOpt,' dtgopt: ',dtgopt

md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)

invpath=getInvPath4Dtgopt(dtgopt,invdir='./inv',getonly=1)

print 'iii',invpath
cards=open(invpath).readlines()
for card in cards:
    if(mf.find(card,'vmax')):
        naa=naa+1
        tt=card.split()
        stmid=tt[0]
        dtg=tt[1]
        rccode=tt[3]
        vmax=tt[5]
        nl=int(tt[7])
        
        if(vmax == "***"): 
            vmax=-999
        else:
            vmax=int(vmax)
        
        MF.appendDictList(rall,dtg,(nl,stmid,vmax))

        if(nl == -999):
            MF.appendDictList(r999,dtg,(stmid,vmax))
        elif(nl == 999):
            MF.appendDictList(r111,dtg,(stmid,vmax))
            
            
if(ls9only or lsAll):
    print
    #print '-----99999'
    
kk9=r999.keys()
kk9.sort()
for k9 in kk9:
    r9=r999[k9]
    l9=len(r9)
    r9stmids=[]
    for k in range(0,l9):
        r9stmids.append((r9[k][0],r9[k][1]))
        n99=n99+1
    for k in range(0,l9):
        tstmid=r9stmids[k][0]
        tvmax=int(r9stmids[k][1])
        tdtg=k9
        if(tvmax >= r9vmin):
            rc=getStmParams(tstmid)
            tstmid9x="%s%s.%s"%(rc[1],rc[0],rc[2])
            tstmid9x=tstmid9x
            (mrc,mtrk)=md3.getMd3track(tstmid,dobt=0,doBdeck2=doBdeck2)
            (mrc9,mtrk9)=md3.getMd3track(tstmid9x,dobt=0,doBdeck2=doBdeck2)
            dtgs9x=mtrk9.keys()
            dtgsNN=mtrk.keys()
    
            inNN=(tdtg in dtgsNN)
            in9X=(tdtg in dtgs9x)
            
            if(inNN):
                rc=mtrk[tdtg]
            elif(in9X):
                rc=mtrk9[tdtg]
            else:
                print 'no joy finding: ',tstmid,tstmid9x,'dtg: ',tdtg
                sys.exit()
            
            (mlat,mlon,mvmax,mpmin)=rc[0:4]
            mtccode=rc[8]
            mwncode=rc[9]
            tmlat=float(mlat)
            tmlat=abs(tmlat)
            isTC=(IsTc(mtccode) == 1)
            isWN=(IsWarn(mwncode) == 1)
            
            if(tmlat <= r9latmax):
                doRun=(isTC and isWN)
            
                lssig=(doSig and doRun)
                if((ls9only or lsAll)):
                    if(lssig):
                        print '999-SSS',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN
                    elif(not(doSig)):
                        if(Is9X(tstmid)):
                            print '999-SSS-999999999',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN
                        else:
                            print '999',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN
                
                if(doRun):
                    n99sig=n99sig+1
                if(doReRun == 9 and doRun):
                    cmd="s-sbt-tmtrkN.py %s -S %s -T -O"%(tdtg,tstmid)
                    mf.runcmd(cmd,ropt)
    
if(ls1only or lsAll):    
    print
    #print '-----11111'
kk1=r111.keys()
kk1.sort()
for k1 in kk1:
    r1=r111[k1]
    l1=len(r1)
    r1stmids=[]
    for k in range(0,l1):
        r1stmids.append((r1[k][0],r1[k][1]))
        n11=n11+1

    for k in range(0,l1):
        tstmid=r1stmids[k][0]
        tvmax=int(r1stmids[k][1])
        tdtg=k1
        if(tvmax >= r1vmin):
            (mrc,mtrk)=md3.getMd3track(tstmid)
            rc=mtrk[tdtg]
            (mlat,mlon,mvmax,mpmin)=rc[0:4]
            mtccode=rc[8]
            mwncode=rc[9]
            mlat=float(mlat)
            tmlat=abs(mlat)
            isTC=(IsTc(mtccode) == 1)
            isWN=(IsWarn(mwncode) == 1)
            if(tmlat <= r1latmax):
                
                doRun=(isTC and isWN)

                lssig=(doSig and doRun)

                if((ls1only or lsAll)):
                    if(lssig):
                        print '111-SSS',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN
                    elif(not(doSig)):
                        if(Is9X(tstmid)):
                            print '111-SSS-99999999',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN
                        else:
                            print '111',tdtg,tstmid,tvmax,mlat,mlon,mvmax,mpmin,mtccode,mwncode,isTC,isWN

                if(doRun):
                    n11sig=n11sig+1
                    if(doReRun == 1 and doRun):
                        cmd="s-sbt-tmtrkN.py %s -S %s -T -O"%(tdtg,tstmid)
                        mf.runcmd(cmd,ropt)



p99=(n99*1.0/naa*1.0)*100.
p11=(n11*1.0/naa*1.0)*100.
p99sig=(n99sig*1.0/naa*1.0)*100.
p11sig=(n11sig*1.0/naa*1.0)*100.

p99sigEX=((n99-n99sig)*1.0/n99*1.0)*100.
p11sigEX=((n11-n11sig)*1.0/n11*1.0)*100.

print
print 'NNN %s naa: %-5d n99: %-5d n11: %-5d   p99/p99sig/p99sigEX:  %4.1f/%-4.1f/%-4.1f  p11/p11sig/p11sigEX: %4.1f/%-4.1f/%-4.1f'%\
      (dtgopt,naa,n99,n11,p99,p99sig,p99sigEX,p11,p11sig,p11sigEX)
print
sys.exit()


