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
            1:['yearOpt', 'bYYYY.eYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'ropt':             ['N','','norun',' norun is norun'],
            'bd2Update':        ['2',0,1,'update using -BT2.txt vice BT.txt'],
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

tt=yearOpt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=yyyyrange(byear, eyear)
    
elif(len(tt) == 1):
    years=[yearOpt]
    
else:
    print 'EEE -- invalid yearopt: ',yearopt

invpath="../../inv/diff-time9x-time2gen-2007-2022.txt"
invpath="../../inv/diff-time9x-time2gen-2007-2022-pass2.txt"
invpath="../../inv/diff-time9x-time2gen-2007-2022-pass3.txt"
invpath="inv/diff-time9x-time2gen-2023.txt"
invpath="gendiff-lant-2023.txt"
invpath="gendiff-wpac-2023.txt"
cards=open(invpath).readlines()

# -- work in the current version
#
sbtSrcDir=sbtSrcDir

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['w','l','e','a','b','s','p','c']

MF.sTimer('sum-md3-ALL')

for year in years:

    print 'bbb',basins

    for basin in basins:
    
        for card in cards:
            #print card[0:-1]
            #if(find(card,'WWW999') and find(card,"%s.%s"%(basin,year)) ):
            #if(find(card,'genDiff') and find(card,"%s.%s"%(basin,year)) ):
            if(find(card,'genDiff')):
                tt=card.split()
                genDiff=int(tt[-1])
                stmNN=tt[-4]
                stm9X=tt[1]
                b1idNN=stmNN[-1].lower()
                ibasin=sbtB1id2Basin[b1idNN]
                
                stmid='%s.%s'%(stmNN.lower(),year)

                if(not(b1idNN in basins)): continue
                if(genDiff == -6): continue


                pNNs=glob.glob("%s/%s/%s/%s*/%s?-sum.txt"%(sbtSrcDir,year,ibasin,stmNN[0:2],stmNN[0:2]))
                pNN=pNNs[0]
                pNNSav="%s-SAV"%(pNN)
                npNNSav=MF.getPathSiz(pNNSav)
                
            
                pNNBTs=glob.glob("%s/%s/%s/%s*/%s?-sum-BT.txt"%(sbtSrcDir,year,ibasin,stmNN[0:2],stmNN[0:2]))
                pNNBT=pNNBTs[0]
                pNNBTSav="%s-SAV"%(pNNBT)
                npNNBTSav=MF.getPathSiz(pNNBTSav)

                p9Xs=glob.glob("%s/%s/%s/%s*/%s?-sum.txt"%(sbtSrcDir,year,ibasin,stm9X[0:2],stm9X[0:2]))
                p9X=p9Xs[0]
                p9XSav="%s-SAV"%(p9X)
                np9XSav=MF.getPathSiz(p9XSav)

                print '  stmid: ',stmid
                print '  stmNN: ',stmNN
                print 'genDiff: ',genDiff
                print '     NN: ',pNN
                print '     9X: ',p9X
                print '   NNBT: ',pNNBT
                print '  NNSav: ',npNNSav,pNNSav
                print '  9XSav: ',np9XSav,p9XSav
                print 'NNBTSav: ',npNNBTSav,pNNBTSav
                print
                
                if(npNNSav > 0 and npNNBTSav > 0 and np9XSav > 0):
                    print 'All SAV files there...proceed...'
                else:
                    print 'SAV file missing...'
                    sys.exit()
                
                rc=doMd2Md3MrgGenChk(stmid,doGenChk=1,bd2Update=bd2Update,override=override,verb=1)
                
                print 'RRRCCC ',stmid,'rc: ',rc
                
               
sys.exit()
    