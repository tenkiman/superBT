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
            'basinOpt':       ['B:',None,'a','basin opt'],
            'yearOpt':        ['Y:',None,'a','yearOpt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'doRedo':         ['R',0,1,'start from -SAV file'],
            'bspdmax':        ['m:',30.0,'f',' max 6-h speed'],
            'doGenChk':       ['G',1,0,'do NOT make sure genesis dtg aligns with end of dev 9X'],
            'passNumber':     ['P:',None,'a',' passNumber'],
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


if(basinOpt != None and basinOpt != 'all'):
    basins=[basinOpt]
else:
    basinOpt='all'
    basins=['wpac','lant','epac','io','shem']

years=[]
if(yearOpt != None):
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=mf.yyyyrange(byear, eyear)

    elif(len(tt) == 1):
        years=[yearOpt]
    else:
        print 'EEE -- invalid yearopt: ',yearOpt



if(stmopt != None):
    
    md3=Mdeck3(doBT=0,doSumOnly=1)
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,verb=verb)
        
    if(len(stmids) == 0):
        print 'stmopt: ',stmopt,' not in current md3 for years: %s-%s'%(bm3year,em3year)
        print 'use -Y yyyy  -B bbbb option...'
        sys.exit()
        
elif(len(years) > 0):
    
    (stmids,sdirs)=getStmidsDirs(years,basins)

    
if(stmopt != None):
    ostmopt=stmopt
    ostmopt=ostmopt.replace(',','-')
    invPath="../qcinv/qcspd-%i-%s.txt"%(int(bspdmax),ostmopt)
    
elif(yearOpt != None):
    oyearOpt=yearOpt.replace('.','-')
    invPath="../qcinv/qcspd-%i-YEAR-%s-BASIN-%s.txt"%(int(bspdmax),oyearOpt,basinOpt)
    
if(passNumber != None):
    invPath=invPath.replace('.txt','-pass-%s.txt'%(passNumber))
    
qccards=[]
for stmid in stmids:
    
    qc2paths=0
    if(doRedo or override): qc2paths=1
    rc=doMd2Md3Mrg(stmid,doRedo=doRedo,qc2paths=qc2paths,doGenChk=doGenChk,override=override,verb=verb)
    (opath3,mpath,mpathBT,savPath,savPathBT)=rc
    if(opath3 == None):
        print 'OOO-SSS override=0 for stmid: ',stmid,'press...'
        continue
    
    # -- QC
    #
    (rcc,qcpath)=chkSpdDirMd3Mrg(opath3,mpath,mpathBT,bspdmax=bspdmax,verb=verb)
    if(rcc == 0):
        qccards.append('qc-fail: %s'%(stmid))
    elif(rcc == 2):
        print 'SSSSSSSSingleton for: ',stmid
        continue
    
        
#rc=MF.WriteList2Path(qccards,invPath,verb=1)
sys.exit()
    
    
