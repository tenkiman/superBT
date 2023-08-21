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
            1:['year',    'dtgopt'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'printAll':         ['p',0,1,'print all dtgs...'],
            'redoIt':           ['R',0,1,'check tctrk and tcdiag...'],
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

invpath="inv/chk/chk-%s.txt"%(year)
#print 'iii',invpath
ptimemin=10.0
cards=open(invpath).readlines()
print
print 'REDO tmtrkN for %s'%(year)
print
redoDtgs=[]
for card in cards:
    if(mf.find(card,'timer: all-%s'%(year))):
        tt=card.split()
        ptime=float(tt[-4])
        dtg=tt[-6][-10:]
        
        if(printAll):
            print 'alldone: %s'%(dtg)
        if(ptime > ptimemin):
            if(printAll): print
            print 'retrking: %s  %4.0f'%(dtg,ptime)
            if(printAll): print
            if(redoIt): redoDtgs.append(dtg)
            
for rdtg in redoDtgs:
    rropt='norun'
    rropt=''
    topt='-T'
    if(rdtg[8:10] == '00'): topt=''
    print 'rrr',rdtg,topt,rdtg[8:10]
    continue
    cmd="../tctrk/s-sbt-tmtrkN.py %s %s"%(rdtg,topt)
    mf.runcmd(cmd,rropt)
    
    dopt=''
    cmd="../tcdiag/s-sbt-tcdiag.py %s %s"%(rdtg,dopt)
    mf.runcmd(cmd,rropt)
    
            

sys.exit()


