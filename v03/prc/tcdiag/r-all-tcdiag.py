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
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'dtgopt':           ['d:',None,'a','dtgopt'],
            'stmopt':           ['S:',None,'a','stmopt'],
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

m3=Mdeck3()

if(dtgopt != None and stmopt == None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
elif(stmopt != None and dtgopt == None):
    #dtgs=m3.getMd3StmDtgs4Stmopt(stmopt,syear='2006')
    dtgs=m3.getMd3StmDtgs4Stmopt(stmopt)
else:
    print 'EEE--(%s) must set either dtgopt or stmopt alone...sayounara'%(CL.pyfile)
    sys.exit()

if(dtgopt != None): MF.sTimer('AAA-TCDIAG-%s'%(dtgopt))
if(stmopt != None): MF.sTimer('AAA-TCDIAG-%s'%(stmopt))

endEra5Dtg='2023050100'
oopt=''
if(override): oopt='-O'
for dtg in dtgs:
    dEnd=mf.dtgdiff(dtg,endEra5Dtg)
    if(dEnd <= 0.0):
        print 'no ERA5 fields for: ',dtg,' press...'
        continue
    else:
        cmd="s-sbt-tcdiag.py %s %s"%(dtg,oopt)
        mf.runcmd(cmd,ropt)
    
if(dtgopt != None): MF.dTimer('AAA-TCDIAG-%s'%(dtgopt))
if(stmopt != None): MF.dTimer('AAA-TCDIAG-%s'%(stmopt))

sys.exit()


