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
            1:['yearopt', 'bYYYY.eYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doTrk':            ['T',1,0,'do NOT make the track files'],
            'ropt':             ['N','','norun',' norun is norun'],
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

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=yyyyrange(byear, eyear)
    
elif(len(tt) == 1):
    
    years=[yearopt]
    
else:
    print 'EEE -- invalid yearopt: ',yearopt


# -- work in the current version
#
sbtSrcDir=sbtSrcDir

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']

MF.sTimer('sum-md3-ALL')

for year in years:
    tdir="%s/%s"%(sbtSrcDir,year)
    MF.ChkDir(tdir,'mk')
    for basin in basins:

        btdir="%s/%s"%(tdir,basin)
        MF.ChkDir(btdir,'mk')

        bopt="%s.%s"%(basin[0],year)
        if(basin == 'epac'):
            bopt=bopt+',c.%s'%(year)
            
        if(basin == 'shem'):
            bopt='h.%s'%(year)
            
        smask="%s/%s/*"%(tdir,basin)
        spaths=glob.glob(smask)
        spaths.sort()

        MF.sTimer('sum-md3-%s-%s'%(basin,year))

        stmNNs={}
        stm9XsDev={}
        stm9XsNon={}

        lall=len(spaths)
        
        for spath in spaths:

            ss=spath.split('/')

            sdir=ss[-1]
            ssum=sdir.split('-')
            stmid="%s.%s"%(ssum[0],ssum[1])
            if(IsNN(stmid)):
                
                if(len(ssum) != 4 and len(ssum) != 5):
                    print 'EEE: bad NN dir:',spath
                    sys.exit()
                    
                stmid9x="%s.%s"%(ssum[-1],ssum[1])
                stmNNs[stmid]=(stmid9x,sdir)
            
            elif(Is9X(stmid)):
                
                stmid9x=stmid
                if(mf.find(sdir,'DEV')):
                    if(len(ssum) != 4):
                        print 'EEE bad 9x DEV dir',spath
                        sys.exit()
                    
                    stmidNN="%s.%s"%(ssum[-1],ssum[1])
                    stm9XsDev[stmid9x]=(stmidNN,sdir)
                    
                elif(find(sdir,'NON')):
                    stm9XsNon[stmid]=(stmid,sdir)
                    
                    
        nns=stmNNs.keys()
        nns.sort()
        lnns=len(nns)
        
        n9ds=stm9XsDev.keys()
        n9ds.sort()
        ln9ds=len(n9ds)
        
        n9ns=stm9XsNon.keys()
        n9ns.sort()
        ln9ns=len(n9ns)
        
        lallNN=lnns+ln9ds+ln9ns
        if(lallNN != lall):
            print 'EEE total number of storms not adding up'
            sys.exit

        nnn=float(lnns)
        n9x=float(ln9ds+ln9ns)
        
        rdev=-99.
        if(n9x != 0.0):
            rdev=(nnn/n9x)*100.0
            if(rdev > 100.0): rdev=-99.
        
        ncard='%s #s NNs: %4d  n9Devs: %4d  n9Nons: %4d  nall: %4d = nallnns: %4d rdev: %3.0f'%(year,lnns,ln9ds,ln9ns,lall,lallNN,rdev)
        
        if(lnns != ln9ds):
            
            if(ln9ds < lnns):
                ncard=ncard+' <--- WWW # dev 9X < # NN'
            else:
                badStmid=None
                for n in n9ns:
                    print n
                    if(n != None and IsNN(n)): badStmid=n
                
                print 'EEE -- NN dev mislabelled... badStmid: ',badStmid
                sys.exit()
            
        print ncard
        if(verb):
            odict={}
            for nd in n9ds:
                stmid=stm9XsDev[nd][0]
                stmdir=stm9XsDev[nd][1]
                odict[stmid]=nd
                
            kk=odict.keys()
            kk.sort()
            for k in kk:
                if(not(k in nns)):
                    print 'EEE NN-9X this NN storm not in 9XsDev: ',k
                    sys.exit()
                print 'NN-9X: ',k,odict[k]
        
        continue
        
        
        for nn in nns:
            
            stm9x=stmNNs[nn]
            
            if(not(stm9x in n9s)):
                print 'EEEE ',nn,' NOT with an associated 9X: ',stm9x
            if(verb): print 'nn',nn,stm9x,(stm9x in n9s)
        
            
        
MF.dTimer('sum-md3-ALL')
                         
sys.exit()
    