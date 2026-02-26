#!/usr/bin/env python

from ad2vm import *

def lsOgrd(ondx,ovals):
    (i,j,m,tau)=ondx
    ocard="I:J:MM:tau: %3d %3d %2d %3d |"%(i,j,m,tau)
    no=len(ovals)
    for n in range(0,no):
        oval=ovals[n]
        (blat,blon,bvmax,bdir,bspd,bstmid)=oval
        sep='::'
        if(n == no-1):
            sep=''
        ocard="%s %4.1f %5.1f %s %s"%(ocard,blat,blon,bstmid,sep)

    print ocard
    return(ocard)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['ptype',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'override':            ['O',0,1,'override and delete previous bd2'],
            'ropt':                ['N','','norun',' norun is norun'],
            'yearOpt':             ['Y:',None,'a','yearOpt -- to select byear-eyear range default is 2007-2022 in sBTvars.py'],
            'stmopt':              ['S:',None,'a','stmopt'],
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

    if(option == 'stmopt'):
        print 'EEE must set -S stmopt OR -d dtgopt OR -Y yearOpt'
    else:
        print 'Stopping in errAD: ',option
    sys.exit()
        



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    
# -- defaults

dssDir=None
dtgopt=None


# -- define the 2D grid global dx x dy
#
dx=dy=2.5
dx=dy=1.0
bgrd=W2areaGlobal(dx=dx,dy=dy)

# -- define the taus
#
btau=0
btinc=24
btaue=120
btaus=range(btau,btaue+1,btinc)

byear=1985
eyear=2024

# -- initialize output grid fro
#
pypPath='./mf-tc-climo-%s-%s.pyp'%(byear,eyear)

if(MF.getPathSiz(pypPath) > 0):
    PS=open(pypPath,'r')
    MF.sTimer('init--open')
    ogrd=pickle.load(PS)
    PS.close()
    MF.dTimer('init--open')
else:
    print 'pypPath not available: ',pypPath
    sys.exit()
    
sys.exit()
oo=ogrd.keys()
oo.sort()

for o in oo:
    if(len(ogrd[o]) > 0):
        lsOgrd(o,ogrd[o])

sys.exit()    
