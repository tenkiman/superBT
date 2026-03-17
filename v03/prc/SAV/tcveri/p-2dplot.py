#!/usr/bin/env python

from tcbase import * # imports tcVM tcCL adVM adCL
from vdCL import *   # imports vdVM

class ga2DPerfPortrait(MFbase):

    def __init__(self,
                 xPP,yPP,valPP,
                 yPPtitle,
                 undef=1e20,
                 undef999=-999.,
                 gsdir='/ptmp',
                 gsname='PP',
                 colundef=85,
                 topTitle='''HWRF/ECMWF Mean Position Error %improve over GFS [%]''',
                 verb=0):

        self.colundef=colundef
        self.undef=undef
        self.undef999=undef999
        self.gsdir=gsdir
        self.gsname=gsname
        self.gspath="%s/%s.gs"%(self.gsdir,self.gsname)
        self.pngpath="%s/%s.png"%(self.gsdir,self.gsname)
        self.topTitle=topTitle
        
        self.xPP=xPP
        self.yPP=yPP
        self.yPPtitle=yPPtitle
        self.valPP=valPP
        self.ovalPP={}
        self.pcountsPP={}
        self.xPPmean={}
        self.yPPmean={}
        self.xPPmeanCounts={}
        self.yPPmeanCounts={}

        self.getPPvals()
        self.getPPcounts()

    def getPPcounts(self):
        
        for y in self.yPP:
            nmean=0
            (nx1all,nx2all)=self.yPPmeanCounts[y]
            nyears1=0
            nyears2=0
            for x in self.xPP:
                (v1,v2)=self.valPP[x,y]
                if(v1[0] != self.undef999):
                    nyears1=nyears1+1
                if(v2[0] != self.undef999):
                    nyears2=nyears2+1

            #print 'NNNNN',y,nyears1,nyears2
            if(nyears1 > 0):
                nx1all=float(nx1all)/float(nyears1)
            if(nyears2 > 0):
                nx2all=float(nx2all)/float(nyears2)
                
            if(nyears1 > nyears2):
                nx2all=nx1all
            elif(nyears2 > nyears1):
                nx1all=nx2all
            
            for x in self.xPP:
                (v1,v2)=self.valPP[x,y]
                nx1=float(v1[1])
                nx2=float(v2[1])
                
                px1=px2=-999999999999.
                
                if(nx1all > 0):
                    px1=( (nx1-nx1all)/nx1all )*100.0
                    
                if(nx2all > 0):
                    px2=( (nx2-nx2all)/nx2all)*100.0
                
                if(nx1 == 0): px1=self.undef999
                if(nx2 == 0): px2=self.undef999
                
                
                #print 'MMM',x,y,nx1,nx2,nx1all,nx2all,'ppp: ',px1,px2
                
                self.pcountsPP[x,y]=(px1,px2)
                
                
                
    def getPPvals(self):

        for x in self.xPP:
            mY1=0.0
            nY1=0
            mY2=0.0
            nY2=0.0
            for y in self.yPP:
                (v1,v2)=self.valPP[x,y]
                val1=v1[0]
                val2=v2[0]

                self.ovalPP[x,y]=(val1,val2)

                n1=v1[1]
                n2=v2[1]
                
                if(val1 != self.undef999):
                    mY1=mY1+val1*n1
                    nY1=nY1+n1

                if(val2 != self.undef999):
                    mY2=mY2+val2*n2 
                    nY2=nY2+n2

            if(nY1 > 0):
                mY1=mY1/nY1
            else:
                mY1=self.undef999

            if(nY2 > 0):
                mY2=mY2/nY2
            else:
                mY2=self.undef999

            self.xPPmean[x]=(mY1,mY2)
            self.xPPmeanCounts[x]=(nY1,nY2)

        for y in self.yPP:
            mX1=0.0
            nX1=0
            mX2=0.0
            nX2=0.0
            for x in self.xPP:
                (v1,v2)=self.valPP[x,y]

                n1=v1[1]
                n2=v2[1]

                mX1=mX1+v1[0]*n1
                mX2=mX2+v2[0]*n2

                nX1=nX1+n1
                nX2=nX2+n2

            if(nX1 > 0):
                mX1=mX1/nX1
            else:
                mX1=self.undef

            if(nX2 > 0):
                mX2=mX2/nX2
            else:
                mX2=self.undef

            self.yPPmean[y]=(mX1,mX2)
            self.yPPmeanCounts[y]=(nX1,nX2)

        return



    def pBox(self,xb,xe,yb,ye,plcol,prcol,xtitle=None,ytitle=None,
             doWholeBox=1,wholeBoxVal=0):

        lcol=1
        lthk=5
        lsty=1

        xoff=0.10

        gsbox=''


        if(doWholeBox):

            pvCol=prcol
            if(wholeBoxVal == 0):pvCol=plcol

            gsbox=gsbox+"""
    'set line %d'
    'draw polyf %f %f %f %f %f %f %f %f %f %f'
    """%(pvCol,xb,yb,xe,yb,xe,ye,xb,ye,xb,yb)

            gsbox=gsbox+"""
    'set line %d %d %d'
    """%(lcol,lsty,lthk)

            gsbox=gsbox+"""
    'draw rec %f %f %f %f'
#    'draw line %f %f %f %f'
    """%(xb,yb,xe,ye,xb,yb,xe,ye)


        else:

            smallCorner=1
            
            if(smallCorner):
                dx=xe-xb
                dy=ye-yb
                fact=0.35
                dx=dx*fact
                dy=dy*(1.0-fact)
                
                gsbox=gsbox+"""
        'set line %d'
        'draw polyf %f %f %f %f %f %f %f %f %f %f %f %f'
        """%(plcol,xb,yb,xe-dx,yb,xe,ye-dy,xe,ye,xb,ye,xb,yb)
    
                gsbox=gsbox+"""
        'set line %d'
        'draw polyf %f %f %f %f %f %f %f %f'
        """%(prcol,xe-dx,yb,xe,yb,xe,ye-dy,xe-dx,yb)
    
    
                gsbox=gsbox+"""
        'set line %d %d %d'
        """%(lcol,lsty,lthk)
    
                gsbox=gsbox+"""
        'draw rec %f %f %f %f'
        """%(xb,yb,xe,ye)
        
                if(prcol != self.colundef):
                    gsbox=gsbox+"""
        'draw line %f %f %f %f %f %f %f %f %f %f %f %f'
        """%(xb,yb,xe-dx,yb,xe,ye-dy,xe,ye,xb,ye,xb,yb)
        
            else:
        
                gsbox=gsbox+"""
        'set line %d'
        'draw polyf %f %f %f %f %f %f %f %f'
        """%(plcol,xb,yb,xe,ye,xb,ye,xb,yb)
    
                gsbox=gsbox+"""
        'set line %d'
        'draw polyf %f %f %f %f %f %f %f %f'
        """%(prcol,xb,yb,xe,yb,xe,ye,xb,yb)
    
                gsbox=gsbox+"""
        'set line %d %d %d'
        """%(lcol,lsty,lthk)
    
                gsbox=gsbox+"""
        'draw rec %f %f %f %f'
        'draw line %f %f %f %f'
        """%(xb,yb,xe,ye,xb,yb,xe,ye)
                

        if(xtitle != None):
            xs=xb-xoff
            ys=(yb+ye)*0.5
            gstitle="""
'set strsiz 0.09'
'set string 1 r 6 0'
'draw string %f %f %s'
"""%(xs,ys,xtitle)

            gsbox=gsbox+gstitle

        if(ytitle != None):
            xs=(xb+xe)*0.5 
            ys=ye + xoff
            gstitle="""
'set string 1 bl 6 45'
'draw string %f %f %s'
"""%(xs,ys,ytitle)

            gsbox=gsbox+gstitle

        return(gsbox)

    def getLcol(self,val,vals,cols):

        if(val == self.undef999):
            return(self.colundef)

        if(val < vals[0]): 
            col=cols[0]
            return(col)
        if(val >= vals[-1]):
            col=cols[-1]
            return(col)

        for i in range(0,len(vals)-1):
            if(val >= vals[i] and val < vals[i+1]):
                col=cols[i+1]
                return(col)

    def getRcol(self,val,vals,cols):

        if(val == self.undef999):
            return(self.colundef)

        if(val < vals[0]): 
            col=cols[0]
            return(col)
        if(val >= vals[-1]):
            col=cols[-1]
            return(col)

        for i in range(0,len(vals)-1):
            if(val >= vals[i] and val < vals[i+1]):
                col=cols[i+1]
                return(col)

    def putShades(self,vals,cols):

        gs=''
        ncols=len(cols)
        for n in range(0,ncols):
            i=n+1
            if(n == 0):
                ip1=i+1
                gs=gs+"""
_shdinfo.%d='Number of levels = %d'
_shdinfo.%d='%d <= %5.0f'"""%(i,ncols,i+1,cols[0],vals[0])
            elif(n == ncols-1):
                gs=gs+"""
_shdinfo.%d='%d %5.0f >'"""%(i+1,cols[n],vals[-1])
            else:
                gs=gs+"""
_shdinfo.%d='%d %5.0f %5.0f'"""%(i+1,cols[n],vals[n-1],vals[n])

        return(gs)


    def plotPP(self,doWholeBox=1,wholeBoxVal=0,doXtitle=1,
               boxwidth=None,
               xstart=2.0,doHead=1,doTail=1):


        xsize=1440
        ysize=int(xsize*(3.0/4.0))

        ystart=7.0

        nrow=len(self.yPP)
        ncol=len(self.xPP)
        
        if(boxwidth != None):
            boxwidth=boxwidth
        else:
            boxwidth=0.30
            if(ncol >= 12): boxwidth=0.24

        xstart=xstart-boxwidth

        gridctl=w2.GradsGslibDir+'/dum.ctl'

        Lvals=[   -30.0,  -20.0,  -10.0,  -5.0, -2.0, 2.0,  5.0,  10.0,   20.0,   30.0   ]
        Lcols=[29,      27,     25,     23,    21,   82,   31,   33 ,   35,     37,     39]

        Rvals=[   -100.0,  -75.0,  -50.0,  -25.0,  25.0,  50.0,   75.0,   100.0   ]
        Rcols=[45,      44,     43,     42,    41,   82,   61,   62 ,   63,     64,    65]
        Rcols=[79,      77,     75,     74,     81,    54 ,   55,     57,    59]
        
        Lgsshades=self.putShades(Lvals,Lcols)
        Rgsshades=self.putShades(Rvals,Rcols)

        if(doWholeBox):
            Rvals=Lvals
            Rcols=Lcols
            

        if(doHead):
            gshead="""
function main(args)
rc=gsfallow(on)
rc=const()
rc=jaecol2bw()
'set grads off'
'set timelab on'
'open %s'
'set cmin 1000'
'd abs(lat)'
'c'

"""%(
       gridctl,
   )
        else:
            gshead=''

        gs=gshead

        xmin=999
        xmax=-999
        ymin=999
        ymax=-999

        nJ=len(self.yPP)

        for j in range(0,nJ):

            y=self.yPP[j]

            ye=ystart-j*boxwidth
            yb=ye-boxwidth
            if(yb < ymin): ymin=yb
            if(ye > ymax): ymax=ye

            nI=len(self.xPP) # mean is at end

            for i in range(0,nI+1):

                if(i == nI):

                    xtitle=None
                    ytitle=None
                    if(j == 0): ytitle='%d-y Mn'%(nI)
                    v1=self.yPPmean[y][wholeBoxVal]
                    plcol=self.getLcol(v1,Lvals,Lcols)
                    xb=xb+boxwidth+0.25
                    xe=xb+boxwidth
                    gsbox=self.pBox(xb, xe, yb, ye, plcol, plcol,
                                    xtitle=xtitle,ytitle=ytitle,
                                    doWholeBox=1,
                                    wholeBoxVal=wholeBoxVal)
                    gs=gs+gsbox

                else:

                    x=self.xPP[i]

                    (v1,v2)=self.ovalPP[x,y]
                    (pn1,pn2)=self.pcountsPP[x,y]

                    ytitle=None
                    if(j == 0): ytitle=self.xPP[i]
                    xtitle=None
                    if(i == 0 and doXtitle): xtitle=self.yPPtitle[j]

                    xb=xstart+i*boxwidth
                    xe=xb+boxwidth   
                    if(xb < xmin): xmin=xb
                    if(xe > xmax): xmax=xe

                    if(doWholeBox):
                        plcol=self.getLcol(v1,Lvals,Lcols)
                        prcol=self.getRcol(v2,Rvals,Rcols)
                    else:
                        if(wholeBoxVal == 0):
                            plcol=self.getLcol(v1,Lvals,Lcols)
                            prcol=self.getRcol(pn1,Rvals,Rcols)
                            #prcol=self.getRcol(v1,Rvals,Rcols)

                        elif(wholeBoxVal == 1):
                            plcol=self.getLcol(v2,Lvals,Lcols)
                            prcol=self.getRcol(pn2,Rvals,Rcols)
                            #prcol=self.getRcol(v2,Rvals,Rcols)
                            
                        

                    gsbox=self.pBox(xb, xe, yb, ye, plcol, prcol,xtitle=xtitle,ytitle=ytitle,
                                    doWholeBox=doWholeBox,wholeBoxVal=wholeBoxVal)
                    gs=gs+gsbox




        for i in range(0,nI):

            ye=ystart-nJ*boxwidth-0.25
            yb=ye-boxwidth
            if(yb < ymin): ymin=yb
            if(ye > ymax): ymax=ye

            ytitle=None
            xtitle=None
            if(i == 0): xtitle='StatMn'

            xb=xstart+i*boxwidth
            xe=xb+boxwidth   
            if(xb < xmin): xmin=xb
            if(xe > xmax): xmax=xe

            x=self.xPP[i]
            v1=self.xPPmean[x][wholeBoxVal]
            plcol=self.getLcol(v1,Lvals,Lcols)

            gsbox=self.pBox(xb, xe, yb, ye, plcol, plcol,xtitle=xtitle,ytitle=ytitle,
                            doWholeBox=1,wholeBoxVal=wholeBoxVal)
            gs=gs+gsbox


        xmidR=(xmin+xmax)*0.5
        ymidR=ymin-0.75

        xmidL=xmax+0.75+boxwidth
        ymidL=(ymin+ymax)*0.5

        modelTitle=self.topTitle.split()[0].split('/')[0]
        if(wholeBoxVal == 1): modelTitle=self.topTitle.split()[0].split('/')[1]
        gs=gs+"""
'set strsiz 0.25'
'set string 1 c 6 0'
'draw string %f %f %s'
'set strsiz 0.09'

"""%(xmidR,ystart+0.75,modelTitle)

        if(doTail):
            xmidR=11.0*0.5
            gstail="""

t1='%s'
t2=''
t3=''
t3scl=1.0
rc=toptle3(t1,t2,t3,t3scl)

%s

#function cbarns (sf,vert,xmid,ymid,sfstr,force,lab,labstr,bgcolor)
rc=cbarns(0.65,0,%f,%f,'',y,y,'%% improve','')
        """%(self.topTitle,Lgsshades,xmidR,ymidR)
            
            gstail=gstail+"""
%s

rc=cbarns(0.65,1,%f,%f,'',y,y,'%% cases','')
        """%(Rgsshades,xmidL,ymidL)
            
            
            gstail=gstail+"""

'gxprint %s white x%-d y%-d'

'q pos'
'quit'
return        
        """%(self.pngpath,xsize,ysize)


        else:
            gstail=''

        gs=gs+gstail

        return(gs)

    def doGrads(self,gs):
        ropt=''
        MF.WriteString2File(gs,self.gspath)
        cmd="grads -lc %s"%(self.gspath)
        mf.runcmd(cmd,ropt)




#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Vd2a2DplotCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
        }

        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'basinOpt':            ['b:','nhem','a','basins'],
            'modelOpt':            ['T:','hwrf,tecmt,avno','a','aids to plot'],
            'otauOpt':             ['o:','all','a',"""output taus:
            
'all'   - 12,24,48,72,96,120
'sr'    - 12,24
'net'   - 'SR','MR,'LR'
""" ],
            'phrOpt':              ['p:','','a',""" ['']  no BC | 0 - 0-h BC | 6 - 6-h BC"""],
            'veriOptHomo':         ['h',0,1,"""" 1 for homogeneous; [0] for heterogeneous """],
            'veriStat':            ['s:','gainxype','a',"""['gainxype'] for gain """],
            'yearOpt':             ['y:','2007.2017','a',"""byear.eyear for a range of years"""],
            'toptitle1':           ['1:','generic1','a','toplabel1'],
            'toptitle2':           ['2:','','a','toplabel2'],
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

CL=Vd2a2DplotCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

setOpt='ncep'
#setOpt='navy'

if(setOpt == 'navy'):
    baseModels=[
        'cotc','gnav','avno',
        'clip5',
    ]
    topTitle='''COTC/GNAV Mean Position Error %improve over GFS [%]'''
    
    
    baseModels=[
        'cotc','avno','gnav',
        'clip5',
    ]
    topTitle='''COTC/GFS Mean Position Error %improve over GNAV [%]'''

    #baseModels=[
        #'cotc','gnav','tecmt',
        #'clip5',
    #]
    #topTitle='''COTC/GNAV Mean Position Error %improve over ECMWF [%]'''
    
else:
    baseModels=[
        'hwrf','tecmt','avno',
        'clip5',
    ]
    topTitle='''HWRF/ECMWF Mean Position Error %improve over GFS [%]'''

if(modelOpt != None):
    baseModels=modelOpt.split(',')
    
if(mf.find(modelOpt,'ecmt') and mf.find(modelOpt,'hwrf') ):
    topTitle='''HWRF/ECMWF Mean Position Error %improve over GFS [%]'''
    pmodel='hwrf-ecmwf'
elif(mf.find(modelOpt,'era5') and mf.find(modelOpt,'hwrf')):
    topTitle='''HWRF/ERA5 Mean Position Error %improve over GFS [%]'''
    pmodel='hwrf-era5'

elif(mf.find(modelOpt,'era5') and mf.find(modelOpt,'ecmt')):
    topTitle='''ECMWF/ERA5 Mean Position Error %improve over GFS [%]'''
    pmodel='ecmwf-era5'
    
    


allBasinsNhem=['w','e','l']
allBasins=['w','e','l','h']
basinTitle={'w':'WPAC',
            'e':'C+EPAC',
            'l':'LANT',
            'h':'SHEM',
            }

veriStatRead=veriStat
if(veriStat == 'gainxyfe'): veriStatRead='fe'
if(veriStat == 'gainxype'): veriStatRead='pe'

# -- basins
#
if(basinOpt == 'nhem' or basinOpt == None): basins=allBasinsNhem


# -- otau
#
otau=otauOpt
if(otauOpt.isdigit()): otau=int(otauOpt)
else:                  otau=otauOpt.upper()
if(otau == 'ALL'): otau='all'

# -- years
#
pyear=None
if(mf.find(yearOpt,'.')): 
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=int(tt[0])    
        eyear=int(tt[1])    
        pyear="%d-%d"%(byear,eyear)
    else:
        print 'EEE bad yearOpt, must be byear.eyear of byear'
        sys.exit()
else:
    try:
        byear=eyear=int(yearOpt)
    except:
        print 'EEE bad yearOpt -- for single year must be YYYY'
        sys.exit()

if(phrOpt != '' and phrOpt.isdigit() ): phrOpt=int(phrOpt)
else: phrOpt=''

veriOpt='-H'
if(veriOptHomo): veriOpt=''

if(veriStat == 'pod'): veriOpt='-H'

# -- defaults DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#
ilstyle=ilwidth=None	
doland=1

ptype=veriStat
pltcntvar=None
pdir='./plt'
dopng=1
doline=0
doxv=1
docp=1
verb=verb
doshow=0

if(otauOpt == 'all'):
    otaus=[12,24,48,72,96,120]        ; oname="taus-std"
elif(otauOpt == 'sr'):
    otaus=[12,24]                     ; oname="taus-short-range"
elif(otauOpt == 'net+72'):
    otaus=[12,72,120,'SR','MR','LR']  ; oname='taus-big-range'
elif(otauOpt == 'net'):
    otaus=['SR','MR','LR']            ; oname='taus-range'
else:
    print 'EEE-invalid otauOpt: ',otauOpt
    sys.exit()

if(pyear == None):
    print 'EEE-- error  in settingn yearOpt: ',yearOpt
    sys.exit()
    
pname="PP-%s-%s-%s-%s"%(basinOpt,pyear,pmodel,oname)

# -- make SSMs by basin -- contains all the stats
#
MF.sTimer('maksSMSs')
oStats={}
xYears=[]
yStats=[]
yStatsTitle=[]

for ibasin in basins:
    for otau in otaus:
        SSM=SumStatMultiYear(byear,eyear,ibasin,setOpt,
                             baseModels,veriOpt,phrOpt,veriStat,veriStatRead,otau)

        print 'SSS ibasin,otau:',ibasin,SSM.otau,SSM.otauStats.keys()
        print
        print 'YYY',SSM.years,SSM.models
        omodels=SSM.models
        if(veriStat == 'gainxyfe'): omodels=SSM.models[0:-1]
        if(veriStat == 'gainxype'): omodels=SSM.models[0:-1]

        y="%s-%s"%(ibasin,SSM.otau)

        ytitle="%s-%s"%(basinTitle[ibasin],SSM.otau.split('-')[0])
        yStats.append(y)
        yStatsTitle.append(ytitle)
        for year in SSM.years:
            x=year
            for model in omodels:
                key=(year,model,SSM.otau)
                val=SSM.otauStats[key]
                MF.append2TupleKeyDictList(oStats, x, y, val)

xYears=SSM.years        

for x in xYears:
    for y in yStats:
        print 'kkk----',x,y,oStats[x,y]

MF.dTimer('maksSMSs')

MF.sTimer('makePlot')

doWholeBox=0

gaPP=ga2DPerfPortrait(xYears,yStats,oStats,yStatsTitle,
                      topTitle=topTitle,
                      gsdir=pdir,gsname=pname, verb=0)

gsall=gaPP.plotPP(doWholeBox=doWholeBox,wholeBoxVal=0,doXtitle=1,doHead=1,doTail=0)
gsall=gsall+gaPP.plotPP(doWholeBox=doWholeBox,wholeBoxVal=1,xstart=6.0,doXtitle=0,doHead=0,doTail=1)

gaPP.doGrads(gsall)

MF.dTimer('makePlot')
