#!/usr/bin/env python3

from ibvm import *

        
class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'yearOpt':          ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'sumonly':          ['s',0,1,'list stmids only'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
        }

        self.purpose="""
an 'ls' or listing app for 'mdeck3' data two filter options are available:
-S by storm
-d by dtg or date-time-group or YYYYMMDDHH"""

        self.examples='''
%s -S w.19 -s       # list just the summary for ALL WPAC storms in 2019 including 9Xdev and 9Xnon and NN
%s -S w.19 -s -B    # list the summary for only numbered or NN WPAC storms in 2019 w/o summary of 9Xdev
%s -S 20w.19        # list all posits for supertyphoon HAGIBIS -- the largest TC to hit Tokyo
%s -S l.18-22 -s -B # list all atLANTic storms 2018-2022
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print(CL.estr)

byear=1940
eyear=2023

# -- get the iTCs tcnames for MakeStmList()
#
PA=open('%s/iTC-%s-%s.pyp'%(ddir,byear,eyear),'rb')
aTCs=pickle.load(PA)
PA.close()
astmids=list(aTCs.keys())

PN=open('%s/iTC-tcnamesAll.pyp'%(ddir),'rb')
tcnamesAll=pickle.load(PN)
PN.close()
astmids=list(aTCs.keys())

# -- get the jtwc bd2s 
#
byearjt=1945
eyearjt=2023
PJ=open('%s/iTC-bd2-jtwc-%s-%s.pyp'%(ddir,byearjt,eyearjt),'rb')
oBD2s=pickle.load(PJ)
PJ.close()

PMJ=open('%s/iTC-md2-jtwc-%s-%s.pyp'%(ddir,byearjt,eyearjt),'rb')
oMD2s=pickle.load(PMJ)
PMJ.close()


# -- get the ib3 stmids
#
stmids=MakeStmList(stmopt,tcnamesAll,verb=verb)
nstmids=len(stmids)

if(nstmids == 0):
    print('WWW no ib3 stms for stmopt %s ... press ...'%(stmopt))
    sys.exit()

# -- get md3 stmids
#
(domd3,basin,year,tstmid)=getBasinYearsFromStmopt(stmopt)

tcnames=GetTCnamesHash(year)

stmid2tcname={}
kk=tcnames.keys()
otcnames={}

for k in kk:
    ndat="%s.%s"%(k[1].lower(),k[0])
    nbasin=k[1][-1:].lower()
    #print(k,nbasin)
    nkey=(tcnames[k],nbasin)
    otcnames[nkey]=ndat
    
kk=otcnames.keys()

if(verb):
    for k in kk:
        print('ooo===',k,otcnames[k])

otcs={}
for stmid in stmids:
    tc=aTCs[stmid.lower()]
    tcname=tc.name
    otcs[stmid]=tc
        
okk=list(otcs.keys())
okk.sort()

aastmids=[]
mmstmids=[]
iistmids=[]

for tstmid in okk:
    itc=otcs[tstmid]
    #lsIBtrack(itc, tstmid)

    (b2trk,b2dtgs)=getB2trk(tstmid,oBD2s)
    (m2trk,m2dtgs)=getM2trk(tstmid,oMD2s)
        
    bdstat='---'
    if(len(b2trk) > 0 and len(m2trk) > 0): 
        bdstat=tstmid[0:3]
        aastmids.append(tstmid)
    else:
        
        # -- search for matching b/mdeck
        #
        m2dtgs=getM2dtgsByYear(oMD2s, tstmid)
        b2dtgs=getB2dtgsByYear(oBD2s, tstmid)
        
        rc=getBD2ForIB(itc,oBD2s,tstmid,b2dtgs)
        (mstmid,m2trk,pcmd2)=getMD2ForIB(itc,oMD2s,tstmid,m2dtgs,aTCs,verb=verb)
        if(mstmid != None):
            mmstmids.append((tstmid,mstmid,pcmd2))
            bdstat=mstmid[0:3]
            #print('MMM %s -> %s'%(tstmid,mstmid),'pcmd2: %3.0f'%(pcmd2))
        else:
            iistmids.append(tstmid)
            
    print('mmmsssbdeck3: %s md2: %s'%(tstmid,bdstat))
    rc=getITCvars(itc,tstmid,m2trk,verb=verb,doprint=0)
    
print('aaaaa',aastmids,len(aastmids))
print('mmmmm',mmstmids,len(mmstmids))
print('iiiii',iistmids,len(iistmids))

for mmstmid in mmstmids:
    nstmid=getMD2stmid(mmstmid, tcnamesAll)
    print('mm',mmstmid,'nn',nstmid)
sys.exit()
    
