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

# -- get the ib3 stmids
#

stmids=MakeStmList(stmopt,tcnamesAll,verb=0)
nstmids=len(stmids)

if(nstmids == 0):
    print('WWW no ib3 stms for stmopt %s ... press ...'%(stmopt))
    sys.exit()

# -- get md3 stmids
#
(domd3,basin,year,tstmid)=getBasinYearsFromStmopt(stmopt)
print(domd3,basin,year,'tstmid:',tstmid)

if(domd3):
    
    (oyearOpt,doBdeck2)=getYears4Opts(stmopt,dtgopt,yearOpt)        

    doBT = 0
    if(doBdeck2): doBT=1

    if(verb): MF.sTimer('md3-load')
    md3=Mdeck3(oyearOpt=oyearOpt,doBT=doBT,verb=verb)
    if(verb): MF.dTimer('md3-load')
    tstmids=md3.getMd3Stmids(stmopt,dobt=1)

    years=getIntYears4oyearOpt(oyearOpt)
    
else:
    tstmids=None
    md3=None
    years=[year]

print ('oooo',years)
year=years[0]
tcnames=GetTCnamesHash(year)

#print ('ttt---nnn',tcnames)
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
    tcbasin=stmid[2:3]
    tcname=tc.name
    md3name=''
    md3key=(tcname,tcbasin)
    try:
        md3stmid=otcnames[md3key]
        #print('ffff---',md3key,md3stmid)
    except:
        md3stmid=None
    
    if(md3stmid != None):
        otcs[md3stmid]=tc
    else:
        otcs[stmid]=tc
        
okk=list(otcs.keys())
okk.sort()
for ok in okk:
    inmd3='---'
    if(ok in tstmids):
        inmd3='md3'
    print ('33333-------',inmd3,ok,otcs[ok])
    itc=otcs[ok]
    rc=getITCvars(itc,ok,verb=verb)
    
sys.exit()
    
