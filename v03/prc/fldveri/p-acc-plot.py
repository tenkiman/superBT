#!/usr/bin/env python

from sBT import *

 
class AccStatsPlot(MFbase):


    def __init__(self,models,vstmids,
                 pcase,
                 ptype,
                 doland=1,
                 pdir='/tmp',
                 doMetric=0,
                 ):

        # -- 20190905 -- handle pcase with a directory
        #
        (ppdir,pfile)=os.path.split(pcase)
        
        if(len(ppdir) > 0): 
            pdir=ppdir
            pname="%s.%s"%(ptype,pfile)
        else:
            pname='%s.%s'%(ptype,pcase)
            
        self.models=models
        self.vstmids=vstmids
        self.pcase=pcase
        self.ptype=ptype
        self.doMetric=doMetric
        
        if(doland == 0):
            pname="%s-noland"%(pname)
            
        self.ppaths=[
            '%s/%s.png'%(pdir,pname),
            '%s/%s.eps'%(pdir,pname),
            '%s/%s.txt'%(pdir,pname),
            ]


        self.pvartagopt=None


    def reducestmids(self,stmids,filter9x=1):

        ostmids=[]
        for stmid in stmids:
            tt=stmid.split('.')
            stm3id=tt[0]
            stmnum=int(stm3id[0:2])
            if(filter9x and stmnum >= 90): continue
            stmyear=tt[1]
            ostmid="%s.%s"%(stm3id,stmyear[2:4])
            ostmids.append(ostmid)
            
        return(ostmids)


    def setPlottitles(self,
                      toptitle1=None,
                      toptitle2=None,
                      xlab=None,
                      ):

        models=self.models

        #
        # main title
        #
        if(toptitle1 == None):
            t1='please add using -1 command line option....'
        else:
            t1=toptitle1

        if(toptitle2 != None):
            t1=t1+'\n'+toptitle2

        self.ptitles=(t1,t2,ylab)
        self.xlab='xlab'
        self.ylab='ylab'



    def isundef(self,val,undef=None):

        if(val == None):
            return(1)

        if(undef != None):
            undefs=[undef]
        else:
            undefs=[-999.,999.]
        rc=0
        for undef in undefs:
            if(val == undef): rc=1
        return(rc)


    def iszero(self,val):
        rc=0
        if(fabs(val) == 0): rc=1
        return(rc)


    def smooth(self,x,window_len=10,window='hanning'):
        """smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal 
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.

        input:
            x: the input signal 
            window_len: the dimension of the smoothing window
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.

        output:
            the smoothed signal

        example:

        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

        see also: 

        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter

        TODO: the window parameter could be the window itself if an array instead of a string   
        """

        import numpy

        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."

        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."


        if window_len<3:
            return x


        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


        s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w=numpy.ones(window_len,'d')
        else:
            w=eval('numpy.'+window+'(window_len)')

        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len-1:-window_len+1]



    def setControls(self,controlsVar=None):
        
        if(self.ptype == 'pe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'pe-line'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,300.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'fe-line'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,200.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'pe-frac'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-pcnt'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-imp'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'pe-imps'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-imp'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'fe-imps'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-norm'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'fe'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'te'):
            ptype1='te'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,1000.0,100],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'fe0'):
            ptype1='fe0'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'pe-fe'):
            ptype1='pe'
            ptype2='fe'
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)
            
        elif(self.ptype == 'spe'):
            ptype1='spe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,110.0,10],lgndloc)

        elif(self.ptype == 'rmspe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)

        elif(self.ptype == 'vme'):
            ptype1='amvme'
            ptype2='mvme'
            lgndloc=0
            controls=([-50.0,50.0,10.0],lgndloc)

        elif(self.ptype == 'vbias'):
            ptype1='mvme'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)
            if(self.doMetric): controls=([-25.0,35.0,10.0],lgndloc)

        elif(self.ptype == 'nice'):
            ptype1='nice'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pbias'):
            ptype1='pmin'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pod'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)
            
        elif(self.ptype == 'pod-line'):
            ptype1='pods'
            ptype2='pods'
            lgndloc=2
            controls=([0.0,125.0,25],lgndloc)
        

        elif(self.ptype == 'pof'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)

        elif(self.ptype == 'gainxype'):
            ptype1='gainxype'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)

        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe0'):
            ptype1='gainxyfe0'
            ptype2=ptype1
            lgndloc=0
            controls=([-10.0,30.0,5.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
            
        elif(self.ptype == 'pbetter'):
            ptype1=self.ptype
            ptype2=ptype1
            lgndloc=0
            controls=([0.0,110.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvmax'):
            ptype1='gainxyvmax'
            ptype2=ptype1
            lgndloc=2
            controls=([-70.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvbias'):
            ptype1='gainxyvbias'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,120.0,10.0],lgndloc)

        elif(self.ptype == 'ct-ate'):
            ptype1='mcte'
            ptype2='mate'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'at-cte'):
            ptype1='mate'
            ptype2='mcte'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'r34e'):
            ptype1='r34e'
            ptype2='r34bt'
            lgndloc=0
            controls=([-200.0,200.0,25.0],lgndloc)

        else:
            print 'EEE invalid plot ptype in PlotsumStat: ',self.ptype
            sys.exit()

        if(controlsVar != None): controls=controlsVar
        self.controls=controls

    def setbarlineprops(self,n,np,pvartagopt=None):

        lstyle='-'
        wline=2.0

        if(pvartagopt == '00_12zv06_18z'):
            if(n%2 == 0):
                alphabar=alphaline=0.75
                lstyle='-'
            else:
                alphabar=alphaline=1.0
                lstyle=':'

        if(np >= 4):
            if(n%2 == 0):
                alphabar=alphaline=0.5
                lstyle=':'
            else:
                alphabar=alphaline=1.0
                lstyle='-'

        if(np == 4 and pvartagopt == '00_06_12_18z'):
            if(n == 3):
                alphabar=alphaline=0.25
                lstyle='-'
            elif(n == 2):
                alphabar=alphaline=0.5
                lstyle=':'
            elif(n == 1):
                alphabar=alphaline=0.75
                lstyle='-'
            elif(n == 0):
                alphabar=alphaline=1.0
                lstyle=':'

        if(pvartagopt == '00_12z'):
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphabar=0.5
                alphaline=1.0
                lstyle=':'

        else:
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphaline=1.0
                alphabar=1.0
                alphabar=0.85
                lstyle=':'
                lstyle='-'
                lstyle='--'


        return(lstyle,wline,alphabar,alphaline)



    def simpleplot2axis(self,
                        models,
                        dicts,
                        cnts,
                        labels,
                        irowc=None,
                        irowt=None,
                        irowl=None,
                        irowll=None,
                        do1stplot=1,
                        do2ndplot=0,
                        doBarplot=0,
                        ilstyle=None,
                        ilwidth=None,
                        ilmarker=None,
                        ialphaline=None,
                        ialphabar=None,
                        reversedirection=0,
                        dopng=0,doeps=0,doxv=0,dopdf=0,
                        useroverride=0,
                        doshow=0,
                        verb=0,
                        dotable=1,
                        countonly=0,
                        docp=0,
                        domodelrename=0,
                        do2ndval=0,
                        doline=0,
                        doErrBar=1,
                        undef=-999,
                        maxcounts=2000,
                        dosmooth=0,
                        ):
        
        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()

        from numpy import array
        import matplotlib.lines as mlines
        
        self.do2ndval=do2ndval
        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        from pylab import array,arange
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        from natsort import natsorted
        import matplotlib.patches as mpatch

        C2hex=w2Colors().chex

        # setup input
        #

        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        cnts0=cnts[0]
        #print 'cc00',cnts0
        try:
            cnts1=cnts[1]
            #print 'cc11',cnts1
        except:
            None

        taus=cnts0.keys()
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0' and nrows > 1):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1


        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        xaxisTs=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts0
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]
            xaxisT=[]

            nxpts=nts
            #if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]
                
                if(self.isundef(val1)):
                    val1=None
                if(self.isundef(val2)):
                    val2=None
                    
                if(verb): print 'nnn',nt,tau,val1,val2

                if(len(dict1[tau]) > 2 and len(dict1[tau]) != 3):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=None
                    cval1=''
                    row1.append(val1)
                else:
                    row1.append(val1)
                    xval1=0.5+(nt-1)
                    xaxis.append(xval1)
                    xaxisT.append(int(tau))

                if(self.isundef(val2) or nc == 0):
                    val2=None
                    row2.append(val2)
                else:
                    row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            if(n == 0):
                vals1.append(row1)
                #print '0000-111',n,row1
                #print '0000-222',n,row2
            elif(n == 1):
                #print '1111-111',n,row1
                #print '1111-222',n,row2
                vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)
            xaxisTs.append(xaxisT)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        xydim=(10.5,8.25)
        fig, ax = plt.subplots(figsize = xydim)
        
        mpl.rcParams.update(params)
        ax2 = ax.twinx()
        
        lgndc=[]

        xtaus0=[]
        xtaus1=[]
        ycnts0=[]
        ycnts1=[]
        ycnts=[]
        
        if(doBarplot): np=np+1

        for tau in taus:
            if(mf.find(tau,'all')):  
                continue
            else:                    
                itau=int(tau)
                ycnt0=cnts0[tau]
                ycnts0.append(ycnt0)
                xtaus0.append(itau)
                if(nrows > 1):
                    ycnt1=cnts1[tau]
                    ycnts1.append(ycnt1)
                    xtaus1.append(itau)

        if(verb):
            print 'XXXTTT--0000',n,xtaus0
            print 'CCCCCC--0000',n,ycnts0
            print 'XXXTTT--1111',n,xtaus1
            print 'CCCCCC--1111',n,ycnts1

        # -- !!!!!! force two plots !!!!!!!!!!!!!!!!!!!
        #
        np=2
        if(nrows == 1): np=1
            

        # -- first plot the two time series
        #
        for n in range(0,np):

            
            # -- key to doing multiple plots
            if(n == 0): ys=vals1[n]
            elif(n == 1): ys=vals2[0]
            
            #try:
                #print 'vvvvvyyyyyy---0000',n,vals1[0],vals2[0]
            #except:
                #None
            #try:
                #print 'vvvvvyyyyyy---nnnn',n,vals2[n]
            #except:

            #print '---yyyysssss',n,ys
            
            xaxisT=copy.copy(xaxisTs[0])
            xaxisT=copy.copy(xtaus0)
            
            if(verb):
                print 'xxxx',n,xaxisT
                print 'yyyy',n,ys
                 
            ys=self.makeMaskYs(ys)
            nxy=n
            rc=ax.plot(xaxisT,ys,
                       color=rowc[nxy],
                       linestyle=lstyle[nxy],
                       marker=lmarker[nxy],
                       linewidth=lwidth[nxy],
                       alpha=alphaline[nxy]
                       )

        if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or
           self.ptype == 'pod' or self.ptype == 'pod-line'):
            ax.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)
            

        # -- now do the smoothed time series if dosmooth=1
        #
        for n in range(0,np):

            if(n == 0): ys=vals1[n]
            elif(n == 1): ys=vals2[0]
            xaxisT=copy.copy(xtaus0)
            
            if(verb):
                print 'xxxx',n,xaxisT
                print 'yyyy',n,ys
                 
            ys=self.makeMaskYs(ys)
            
            if(dosmooth):
                ys=array(ys)
                yss=smooth(ys,window_len=7)
                rc=ax.plot(xaxisT,yss,
                           #color='black',
                           color=rowc[n],
                           linestyle='-',
                           marker='',
                           linewidth=lwidth[n],
                           alpha=1.0
                           )
                
        # -- now the count bars
        #
        rc=ax2.bar(xtaus0,ycnts0,
                   width=0.9,
                   color=rowc[0],
                   alpha=0.7,
                   #color='grey',
                   )
        
        if(nrows > 1):
            
            rc=ax2.bar(xtaus0,ycnts1,
                       width=0.5,
                       color=rowc[1],
                       alpha=0.9,
                       #color='black',
                       )
        
        ax2.set_ylabel('N',fontsize=15)
        ax2.set_ylim(0,maxcounts)
        if(maxcounts <= 2000):
            ax2.set_yticks([0,50,100,200])
        else:
            ax2.set_yticks([0,250,500])
            
            
        
        ax2.grid()
        

        # -- set the xticks
        #
        xtbeg=xtaus0[0]
        xtend=xtaus0[-1]
        nxpts=len(xtaus0)

        if(nxpts >= 40):
            xtinc=5
        elif(nxpts >=30 and nxpts < 40):
            xtinc=4
        elif(nxpts >= 20 and nxpts < 30):
            xtinc=3
        elif(nxpts >= 10 and nxpts < 20):
            xtinc=2
        elif(nxpts < 10):
            xtinc=1

        xts=arange(xtbeg,xtend,xtinc)
        
        ax.set_xlim(xtaus0[0]-0.7,xtaus0[-1]+0.7)
        ax.set_xticks(xts)
        ax.set_ylim(yb,ye)
        ax.set_yticks(yts)

        fig.suptitle(t1,fontsize=13)
        ax.set_title(t2,size=8)

        ax.set_ylabel(ylab,fontsize=15)
        if(xlab != None): ax.set_xlabel(xlab,fontsize=15)
        
        
        ax.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            fig.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            fig.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)


    def cformatVal(self,val1,val2,nc,diffv1v2=0,countonly=0):

        cval1=''
        if(val1 == None):
            return(cval1)
        
        if(val1 != ''):
            if(countonly):
                cval1="%d"%(nc)
            else:
                cval1="%4.0f[%d]"%(val1,nc)
                
        if(val1 != '' and val2 != '' and self.do2ndval != 0):
            if(countonly):
                cval1="%d"%(nc)
            else:
                if(self.do2ndval == -1):
                    cval1="%4.0f;%4.0f[%d]"%(val2,val1,nc)
                else:
                    cval1="%4.0f;%4.0f[%d]"%(val1,val2,nc)

        return(cval1)
    
    
    def makeMaskYs(self,ys):
        from numpy import empty,ma
        
        nys=empty([len(ys)])
        maskys=[]
        for i in range(0,len(ys)):
            y=ys[i]
            if(y == None):
                maskys.append(1)
            else:
                maskys.append(0)
                nys[i]=y
            
        # -- make the masked array
        #
        nys=ma.array(nys,mask=maskys)
        
        # -- set undef points to None
        #
        for i in range(0,len(nys)):
            my=maskys[i]
            if(my == 1):
               nys[i]=None            
        return(nys)
    

    def simpleplot(self,
                   models,
                   dicts,
                   cnts,
                   labels,
                   irowc=None,
                   irowt=None,
                   irowl=None,
                   irowll=None,
                   do1stplot=1,
                   do2ndplot=0,
                   ilstyle=None,
                   ilwidth=None,
                   ilmarker=None,
                   ialphaline=None,
                   ialphabar=None,
                   reversedirection=0,
                   dopng=0,doeps=0,doxv=0,dopdf=0,
                   useroverride=0,
                   doshow=0,
                   verb=0,
                   dotable=1,
                   countonly=0,
                   docp=0,
                   domodelrename=0,
                   do2ndval=0,
                   doline=0,
                   doErrBar=1,
                   undef=-999,
                   dosmooth=0,  # -- 20240704 used for plotting era5 pe
                   ):

        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()
        
        from numpy import array,ma,empty
        import matplotlib.lines as mlines

        self.do2ndval=do2ndval

        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        
        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        import numpy
        
        from pylab import arange
        import pylab as P
        from natsort import natsorted
        
        import matplotlib.patches as mpatch
        
        # -- moved to w2base.py from VT.py
        #
        C2hex=w2Colors().chex

        # -- setup output
        #
        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        taus=cnts[0]
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0' and nrows != 1):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1

        
        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]
        
        #print 'nnnnnnnnnnnnnnnnnnnn',nrows
        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            #print 'ddd111',dict1
            #print 'ddd222',dict2
            
            cnt=cnts[n]
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]

            nxpts=nts
            
            # -- ????
            #if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]

                if(len(dict1[tau]) > 2 and len(dict1[tau]) != 3):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=None
                    cval1=''
                
                row1.append(val1)
                xval1=0.5+(nt-1)
                xaxis.append(xval1)

                if(self.isundef(val2) or nc == 0):
                    val2=None
                    cval2=''
                    
                row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            vals1.append(row1)
            vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        np=len(vals1)

        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        P.rcParams.update(params)


        xydim=(10.5,8.25)
        F=P.figure(figsize=xydim)

        leftsubplot=0.10
        bottomsubplot=0.15
        if(np > 6):
            bottomsubplot=0.20

        F.subplots_adjust(top=0.9,bottom=bottomsubplot,left=leftsubplot,right=0.95,wspace=0.0,hspace=0.0)

        FP=F.add_subplot(111)

        lgndc=[]

        #
        # setup bars
        #

        dxofffraction=1.0
        dxofffraction=1.25

        barscale=0.8

        if(np == 1):
            dxofffraction=1.0


        barwidth=barscale/np
        pbarwidth=barwidth*dxofffraction
        xshift=(1.0-barscale)*0.5
        boxbarwidth=pbarwidth*0.50
        errbarwidth=boxbarwidth*0.75
        errcapsize=errbarwidth*25

        if(dxofffraction >= 1.5):
            alphabar=0.75

        leghandles=[]

        for n in range(0,np):

            ys=vals1[n]
            ys=self.makeMaskYs(ys)

            ymedian=v1medians[n]
                
            xaxisl=copy.copy(xaxiss[n])
            xaxisb=copy.copy(xaxiss[n])
            if(verb): print 'XXXLLL',n,xaxisl,ys
            
            leghand = mlines.Line2D([], [], color=rowc[n], marker='', ls=lstyle[n], label=olabels[n])
            leghandles.append(leghand)

            # ---------------11111111111111111111111111111111111111111111111111111111111
            #
            if(do1stplot):
                #adjustxaxis(n,xaxisl,barwidth,dxofffraction,center=1)
                rc=FP.plot(xaxisl,ys,
                           color=rowc[n],
                           linestyle=lstyle[n],
                           marker=lmarker[n],
                           linewidth=lwidth[n],
                           alpha=alphaline[n]
                           )

                # -- add smooth

                if(dosmooth):

                    # -- set the mask and make numpy empty array
                    #
                    
                    smoothys=numpy.empty([len(ys)])
                    maskys=[]
                    for i in range(0,len(ys)):
                        y=ys[i]
                        if(y == None):
                            maskys.append(1)
                            smoothys[i]=0.0
                        else:
                            maskys.append(0)
                            smoothys[i]=y

                    # -- make the masked array
                    #
                    nys=numpy.ma.array(smoothys,mask=maskys)

                    # -- smooth
                    #
                    win_len=7
                    if(len(xaxisl) < 7): win_len=4
                    yss=smooth(smoothys,window_len=win_len)
                    
                    # -- set undef points to None
                    #
                    for i in range(0,len(ys)):
                        my=maskys[i]
                        if(my == 1):
                           yss[i]=None
                           
                    # -- do the smooth plot
                    #
                    rc=FP.plot(xaxisl,yss,
                               color=rowc[n],
                               #color='black',
                               linestyle='-',
                               marker='',
                               linewidth=lwidth[n],
                               alpha=1.0
                               )

                if(n == np-1):
                    if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or self.ptype == 'pod-line'):
                        #FP.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)
                        FP.legend(loc=lgndloc,handles=leghandles)
                        

            # ---------------2222222222222222222222222222222222222222222222222222222222222222
            #
            if(do2ndplot > 0):

                if(do2ndplot == 2):
                    doline=1

                ys=vals2[n]
                ys=self.makeMaskYs(ys)
                
                for j in range(0,len(ymedian)):
                    ymedian[j]=v1medians[n][j]

                if(doline):
                    rc=FP.plot(xaxisl,ys,
                               color=rowc[n],
                               linestyle='--',
                               marker=lmarker[n],
                               linewidth=lwidth[n],
                               alpha=1.0
                               )
                    
                else:

                    rcBB=None
                    
                    if(len(ys) != len(xaxisl)): doErrBar=0
                    adjustxaxis(n,xaxisb,barwidth,dxofffraction)
                    
                    if(doErrBar):

                        yBBbot=v2ptl25s[n]
                        yBBtop=v2ptl75s[n]
                        ymax=v2maxs[n]
                        ymin=v2mins[n]
                        ymed=v2medians[n]
                        
                        ysBBrange=[]
                        
                        yBoxMedian=[]
                        
                        yerrMM=[]
                        yerrCenter=[]

                        yboxCenter=[]
                        yboxMM=[]
                        
                        yerrLowCenter=[]
                        yerrLowMM=[]
                        
                        yerrUpCenter=[]
                        yerrUpMM=[]

                        xaxisBB=copy.copy(xaxisb)
                        xaxisEB=copy.copy(xaxisb)
                        xaxisBBrange=[]
                        
                        lenX=len(xaxisBB)
                        for j in range(0,lenX):
                            xBB=xaxisBB[j]
                            x0BB=xBB+(pbarwidth-boxbarwidth)*0.5
                            x1BB=boxbarwidth
                            xaxisBBrange.append((x0BB,x1BB))
                            xaxisEB[j]=xaxisEB[j]+pbarwidth*0.5
                            #print 'xBB',j,xBB,xaxisBBrange[j],xaxisEB[j]
                            
                        lenY=len(row1median)
                        
                        for j in range(0,lenY):
                            
                            if(ymin[j] != undef):
                                
                                y0BB=yBBbot[j]
                                y1BB=yBBtop[j]-yBBbot[j]   
                                
                                if(ymed[j] == -999):
                                    y0BB=undef
                                    y1BB=undef
                                
                                ysBBrange.append((y0BB,y1BB))
    
                                yboxL=y1BB*0.5
                                yboxC=y0BB+yboxL
                                
                                if(ymed[j] == -999):
                                    yboxC=undef
                                    yboxL=undef
                                
                                yboxCenter.append(yboxC)
                                yboxMM.append(yboxL)
                                
                                yerrL=(ymax[j]-ymin[j])*0.5
                                yerrC=ymin[j]+yerrL
                                
                                if(ymed[j] == -999):
                                    yerrC=undef
                                    yerrL=undef
                                
                                yerrCenter.append(yerrC)
                                yerrMM.append(yerrL)
    
                                yerrLowL=(y0BB-ymin[j])*0.5
                                yerrLowC=ymin[j]+yerrLowL

                                if(ymed[j] == -999):
                                    yerrLowC=undef
                                    yerrLowL=undef

                                yerrLowCenter.append(yerrLowC)
                                yerrLowMM.append(yerrLowL)
                                
                                yerrUpL=(ymax[j]-yBBtop[j])*0.5
                                yerrUpC=yBBtop[j]+yerrUpL
                                
                                if(ymed[j] == -999):
                                    yerrUpC=undef
                                    yerrUpL=undef
                                    
                                yerrUpCenter.append(yerrUpC)
                                yerrUpMM.append(yerrUpL)
                                
                                yBoxMedian.append(ymed[j])
                                
                        nBB=len(xaxisBBrange)
                        
                        for j in range(0,nBB):
                            xBBs=[xaxisBBrange[j]]
                            xBBs1=[(xaxisb[j],pbarwidth)]
                            yBB=ysBBrange[j]
                            rcBB=FP.broken_barh(xBBs1,(0,ys[j]),facecolor=rowc[n],alpha=alphabar[n])
                            rcBB2576=FP.broken_barh(xBBs,yBB,alpha=0.5,facecolor=rowc[n],edgecolor='black',linewidth=1.0)

                        #rc=FP.errorbar(xaxisEB,yerrCenter,yerr=yerrMM,linestyle='None',capthick=2,capsize=errcapsize,
                        #               elinewidth=0.5,alpha=0.75,
                        #               ecolor=rowc[n])
                        
                        rcEB=FP.errorbar(xaxisEB,yBoxMedian,xerr=boxbarwidth*0.5,linestyle='None',capthick=0,capsize=errcapsize,
                                       elinewidth=2,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrLowCenter,yerr=yerrLowMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrUpCenter,yerr=yerrUpMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,alpha=0.5,
                                       ecolor='black')

                        #rc=FP.errorbar(xaxisEB,yboxCenter,yerr=yboxMM,linestyle='None',capthick=0,capsize=errcapsize,
                        #               elinewidth=1,alpha=1.0,
                        #               ecolor=rowc[n])
                            
                        
                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
               
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

                    #----------------2222222 bbbbbb aaaaaaa rrrrrrrrrrrrrr
                    #
                    else:

                        rc=FP.bar(xaxisb,ys,
                                  align='edge',
                                  color=rowc[n],
                                  width=pbarwidth,
                                  alpha=alphabar[n])

                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
                        
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

        # -- table
        #
        if(dotable):

            if(verb):
                print 'rowl: ',rowl
                print 'rowc: ',rowc
                for  i in range(0,len(cvals)):
                    print 'cvals',i,cvals[i]

            TT=P.table(cellText=cvals,loc='bottom',
                       cellLoc='center',
                       rowLabels=rowll,rowColours=rowt,
                       colLabels=ctaus)

            TT.set_fontsize(8)

            P.xticks(xaxis,ctausblank)


        # -- lineplot labels
        else:

            xaxisp=[]
            ctausp=[]
            
            nxpts=len(xaxis)
            if(nxpts >= 40):
                xtinc=5
            elif(nxpts >=30 and nxpts < 40):
                xtinc=4
            elif(nxpts >= 20 and nxpts < 30):
                xtinc=3
            elif(nxpts >= 10 and nxpts < 20):
                xtinc=2
            elif(nxpts < 10):
                xtinc=1

            for i in range(0,nxpts,xtinc):
                xaxisp.append(xaxis[i])
                
                # -- the last point is 'allyears' set to penultimate point
                #
                #if(i == nxpts-1):
                #    i=nxpts-2
                ctausp.append(ctaus[i])
                
            P.xticks(xaxisp,ctausp)

        if(self.ptype == 'vme' or self.ptype == 'ct-ate' or self.ptype == 'at-cte' or \
           self.ptype == 'vbias' or self.ptype == 'pbias' or mf.find(self.ptype,'gainxy')):
            draw0line(lcol='k')

        if(self.ptype == 'pod' or self.ptype == 'pof'):
            drawCritline(100.0,lcol='k')

        elif(self.ptype == 'pbetter'):
            drawCritline(50.0,lcol='k')

        elif(self.ptype == 'pod-line'):
            None
            #drawCritline(100.0,lcol='k')
            #drawCritline(95.0,lcol='k')


        #P.xlim(-1.0,len(taus)-1)
        P.xlim(-1.0,nxpts-1)
        P.ylim(yb,ye)
        P.yticks(yts)

        P.suptitle(t1,fontsize=13)
        P.title(t2,size=8)

        P.ylabel(ylab,fontsize=15)
        if(xlab != None): P.xlabel(xlab,fontsize=15)

        P.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            P.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            P.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            P.savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)





#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class MyearVd2aCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'basinOpt':            ['b:','w','a','basins'],
            'dotable':             ['t',0,1,'do summary of allyears'],
            'pcase':               ['c:',None,'a','set pcase for pngpath'],
            }

        self.defaults={
            }

        self.purpose='''
purpose -- multi-year veristat processing'''

        self.examples='''
%s -y 2015 -t SR -b l -s fe -v h # homogeneous, Short-Range 
'''



#--MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM main
#

CL=MyearVd2aCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.ChangeDir(CL.pydir)

# -- defaults DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#
ilstyle=ilwidth=None	
doland=1

ptype=veriStat
pltcntvar=None
pdir='%s/plt'%(CL.curdir)
dopng=1
doline=0

docp=0
verb=verb
doshow=0
dosmooth=1

# -- make SSMs by basin -- contains all the stats
#
plotcontrolVar=([-40.0,20.0,10],2) 


sAlldicts[otau]=sdicts
nAlldicts[otau]=ndicts
    
sdicts=sAlldicts[otaus[0]]
ndicts=nAlldicts[otaus[0]]

MF.sTimer('makePlot')

rc=getPvarivars(ptype,pcase,toptitle1)                        # vdVM.py

(pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,toptitle1,toptitle2)=rc

if(itoptitle2 != None):
    toptitle2=itoptitle2

pss=AccStatsPlot(ss.models,ss.vstmids,pcase,ptype,pdir=pdir,doland=doland)
pss.ls()

sys.exit()
#if(verb): pss.ls()

pss.setPlottitles(toptitle1,toptitle2,SSM.taus,xlab=xlab)

if(pltcntvar != None):
    tt=pltcntvar.split(',')
    plotcontrolVar=([float(tt[0]),float(tt[1]),float(tt[2])],2)

pss.setControls(controlsVar=plotcontrolVar)

#if(baseModels[-1] == 'clip5' and not(mf.find(veriStat,'gainxy'))): pss.controls[0][1]=pss.controls[0][1]*2.0

if(len(otaus) == 2): do2ndplot=1

pss.simpleplot(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,  # a class() from vdCL.py
               ilmarker=ss.markaids,
               do1stplot=do1stplot,
               do2ndplot=do2ndplot,
               dopng=1,
               ilstyle=ilstyle,
               ilwidth=ilwidth,
               do2ndval=do2ndval,
               doline=doline,
               doxv=doxv,
               docp=1,
               verb=verb,
               doErrBar=doErrBar,
               dotable=dotable,
               dosmooth=dosmooth,
               doshow=doshow)
