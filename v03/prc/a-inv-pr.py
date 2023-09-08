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
#            1:['yearOpt',  'years to run'],
#            2:['basinOpt',  'basins'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is noru'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'doInv':            ['I',0,1,' run inv from here'],
        }

        self.purpose="""
calc R34 using tcprop"""

        self.examples='''
%s cur12 ukm2 tukm2'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(stmopt == None):
    print 'EEE must set -S stmopt in %s',CL.pyfile
    sys.exit()
    
ipath="inv/pr/inv-pr-%s.txt"%(stmopt)
isiz=MF.getPathSiz(ipath)

if(isiz <= 0 or override):
    cmd='p-pr.py -S %s -I'%(stmopt)
    mf.runcmd(cmd,ropt)
    if(ropt == 'norun'): 
        print 'need to run p-pr.py -I'
        sys.exit()

    ipath="inv/pr/inv-pr-%s.txt"%(stmopt)
    isiz=MF.getPathSiz(ipath)
    

if(isiz > 0):
    cards=open(ipath).readlines()
    rc=MF.PathCreateTime(ipath)
    print 'create time: ',rc[0]
else:
    print 'no pr inv for stmopt: ',stmopt
    sys.exit()
    
prFails=[]
prAge=-999
for card in cards:
    #print card[0:-1]
    tt=card.split()
    stmid=tt[0]
    status=int(tt[-3])
    prhour=int(tt[-1])
    if(verb): print 'stmid: ',stmid,' prStatus: ',status,' prhour: ',prhour
    if(prhour > prAge): prAge=prhour
    if(status == 0):
        prFails.append(stmid)
        
if(len(prFails) == 0):
    print 'pr all good for stmopt: ',stmopt,' prAge: ',prAge
else:
    for stmid in prFails:
        print 'FFF for stmid:',stmid
    
sys.exit()