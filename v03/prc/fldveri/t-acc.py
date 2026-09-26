#!/usr/bin/env python

from sBT import *

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatch
import matplotlib.lines as mlines
import matplotlib as mpl

import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters('agg')

import numpy as np
#from pylab import array,arange
#import pylab as P


def smooth(x,window_len=10,window='hanning'):
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

def makeMaskYs(ys):
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

def readAccMo(hemi,bymd,eymd):
    
    byy=int(bymd[0:4])
    eyy=int(eymd[0:4])
    
    accs=[]
    sdir='./stats/mo'
    smask="%s/*%s*"%(sdir,hemi)
    spaths=glob.glob(smask)
    spaths.sort()
    for spath in spaths:
        sdir,sfile=os.path.split(spath)
        ss=sfile.split('-')
        cards=open(spath).readlines()
        for card in cards:
            tt=card.split(',')
            acc=float(tt[-1][0:-1])
            yy=int(tt[0])
            mm=tt[1]
            print 'card',yy,byy,eyy,acc
            if(yy >= byy and yy <= eyy):
                print 'yy mm acc: ',yy,mm,acc
                accs.append(acc)
            
    
    oaccs=makeMaskYs(accs)
    return(oaccs)
    
    #cards=open(accpath).readlines()
    
def drawCritline(ax,critvalue,lcol='b'):
    minx, maxx = ax.get_xlim()
    print 'mm--mm',minx,maxx
    x=np.arange(minx,maxx+1.0,1.0)
    y=x*0.0 + critvalue
    ax.plot(x,y,color=lcol,linewidth=2.00)




nplot=2

doshow=0
doX=1
ropt=''

C2hex=w2Colors().chex

lgndloc=2

lstyle=[]
lstyle.append('-')
lstyle.append('-')

lmarker=[]
lmarker.append(' ')
lmarker.append(' ')

lcolor=[]
lcolor.append('blue')
lcolor.append('green')

lwidth=[]
lwidth.append('1.0')
lwidth.append('1.0')

llabel=[]
llabel.append('NHEM')
llabel.append('SHEM')

leghandles=[]
for n in range(0,nplot):
    leghand = mlines.Line2D([], [], color=lcolor[n], marker=lmarker[n], ls=lstyle[n], label=llabel[n])
    leghandles.append(leghand)


# 1. Create a date range for 80 years (monthly frequency)
# 1945 to 2024 inclusive (960 months)


bymdAll='1945-01-01'
bymd='1984-01-01'
bymd=bymdAll
eymd='2024-12-01'
byy=int(bymd[0:4])
eyy=int(eymd[0:4])
dyy=eyy-byy
incyy=4
if(dyy > 40):
    incyy=5


pngpath='./plt/acc-nhem-shem-%-%s.png'%
    
smthinc=24

dates = pd.date_range(start=bymd, end=eymd, freq='MS')


# -- get accs
#
nhaccs=readAccMo('nhem',bymd,eymd)
shaccs=readAccMo('shem',bymd,eymd)
nhaccsA=readAccMo('nhem',bymdAll,eymd)
shaccsA=readAccMo('shem',bymdAll,eymd)


# 2. Generate dummy data (e.g., random walk for demonstration)
#np.random.seed(42)
#values = np.random.randn(len(dates)).cumsum()


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
#ax2 = ax.twinx()
ylmin=0.5
ylmax=1.0

ax.set_ylim(ylmin,ylmax)
shvalsA=smooth(shaccsA,window_len=smthinc)
nhvalsA=smooth(nhaccsA,window_len=smthinc)
nnhA=len(nhvalsA)
nnh=len(nhaccs)
bndx=nnhA-nnh

alphaMo=0.5
nhslice=nhvalsA[bndx:]
shslice=shvalsA[bndx:]
print 'nn',nnhA,nnh,bndx,len(nhslice),len(shslice)

ax.plot(dates, nhslice,linewidth=1.5,color='blue')
ax.plot(dates, shslice,linewidth=1.5,color='green')
ax.plot(dates, nhaccs,linewidth=0.5,color='blue',alpha=alphaMo)
ax.plot(dates, shaccs,linewidth=0.5,color='green',alpha=alphaMo)
rc=drawCritline(ax,0.9,lcol='black')

# 4. Customizing the X-Axis Ticks
# Create a list of years every 5 years starting from 1945
tick_years = list(range(byy, eyy, incyy)) 

# Ensure 2024 is explicitly included as the final label
#if 2024 not in tick_years:
#    tick_years.append(2024)

# Convert year integers to actual Timestamps for the axis
tick_dates = [pd.Timestamp(year=y, month=1, day=1) for y in tick_years]

ax.set_xticks(tick_dates)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Formatting the visual
#ax.set_title('Monthly Time Series (1945 - 2024)', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
t1='5-day 500-hPa z AnomCorrCoeff (ACC) NHEM v SHEM'
t2='%s-%s'%(byy,eyy)
ylab='ACC'

fig.suptitle(t1,fontsize=13)
ax.set_title(t2,size=13)

ax.set_ylabel(ylab, fontsize=12)
ax.grid(True, linestyle='--', alpha=0.8)
ax.set_xlim(pd.Timestamp(bymd), pd.Timestamp(eymd))

#plt.xticks(rotation=45)
#plt.tight_layout()

ax.legend(loc=lgndloc,handles=leghandles)

fig.savefig(pngpath)

if(doX):
    cmd="xv %s"%(pngpath)
    mf.runcmd(cmd,ropt)
    
if(doshow): plt.show()	