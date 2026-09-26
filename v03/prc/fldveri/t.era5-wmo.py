#!/usr/bin/env python

from sBT import *
from M2 import setModel2

m2=setModel2('era5w')
dtg='1945090700'
m2.setDbase(dtg)

model='era5w'
maxtau=240
verb=1

rc=getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau,verb=verb)
print rc
