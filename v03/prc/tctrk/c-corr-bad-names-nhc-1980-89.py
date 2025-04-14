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

print 'yyy',year

tadDtg=abdirDtg
tdStm=abdirStm
tstd=tmtrkbdir

ladDtg=abdirDtgL
ldStm=abdirStmL
lstd=tmtrkbdirL

tads={
    'adt':(tadDtg,ladDtg),
    'ast':(tdStm,ldStm),
    'std':(tstd,lstd),
}


kk=tads.keys()
kk.sort()

(tdir,ldir)=tads['adt']

tdir="%s/%s"%(tdir,year)
ldir="%s/%s"%(ldir,year)

# -- adeck-dtg
ldtgs=glob.glob("%s/%s??????"%(ldir,year))

ldtgs.sort()

for ldtg in ldtgs:
    cdtg=ldtg.split('/')[-1]
    lmask="%s/%s/tctrk.*"%(ldir,cdtg)
    tmask="%s/%s/tctrk.*"%(tdir,cdtg)
    lpaths=glob.glob(lmask)
    tpaths=glob.glob(tmask)
    #print 'lll: ',cdtg,lmask,lpaths
    #print 'ttt: ',cdtg,tmask,tpaths
    #for tpath in tpaths:
        #(dd,tfile)=os.path.split(tpath)
        #rc=MF.PathModifyTime(tpath)
        #tdtg=rc[-1]
        #tsiz=MF.GetPathSiz(tpath)
        #opath="%s-orig"%(tpath)
        #print tdtg,tsiz,tfile
        
    for lpath in lpaths:
        (dd,lfile)=os.path.split(lpath)
        rc=MF.PathModifyTime(lpath)
        ldtg=rc[-1]
        lsiz=MF.GetPathSiz(lpath)
        tpath="%s/%s/%s"%(tdir,cdtg,lfile)
        (dd,tfile)=os.path.split(tpath)
        rc=MF.PathModifyTime(tpath)
        tdtg=rc[-1]
        tsiz=MF.GetPathSiz(tpath)
        
        #print 'lll',ldtg,lsiz,lpath
        #print 'ttt',tdtg,tsiz,tpath
        rc=MF.runcmdLog('diff %s %s'%(lpath,tpath),quiet=1)
        if(len(rc) > 1):
            #print 'lll',lpath
            #print 'ttt',tpath
            l1=rc[0].split('c')
            l2=rc[0].split('a')
            #print len(l1),len(l2)
            if(len(l1) == 1 and len(l2) > 1):
                l1=l2
            lc1=l1[0].split(',')[0]
            lc2=l1[0].split(',')[-1]
            tc1=l1[1].split(',')[0]
            tc2=l1[1].split(',')[-1]
            #print 'rc0',rc[0],l1,'ll',lc1,lc2,tc1,tc2
            #print 'rc: '
            #for r in rc:
            #    print r
            print
            print 'ddddd',cdtg,lsiz,tsiz,lfile
            print 'lll',lpath
            print 'ttt',tpath

            tce=int(tc2)-int(tc1)
            print 'ttt---',int(tc1),int(tc2),'tce: ',tce,len(rc)
            
            print rc[1]
            
            tcn=int(tce)*-1 -2
            print rc[tcn]
                
            
        else:
            print 'same...'
            
print 'tdir: ',tdir,' ldir: ',ldir





sys.exit()


