function main(args)

rc=gsfallow('on')
rc=const()
rc=jaecol2()
basin=subwrd(args,1)
ivar=subwrd(args,2)

ddir='/data/w22/dat/tc/sbt/v01/gadat'


if(ivar = mvmax)
  var='mvmax' ; ylo=0 ; yhi=45 ; yd=5 ;  ylab='ERA5 Vmax[kts]'
endif

if(ivar = shr)
  var='shr' ; ylo=0; yhi=40 ; yd=5 ;  ylab='ERA5 850-200 hPa Shear[kts]'
endif

if(ivar = tpw)
  var='tpw' ; ylo=40; yhi=80 ; yd=5 ;  ylab='ERA5 TotPrecipWater [mm]'
endif

if(ivar = rh700)
  var='rh700' ; ylo=45; yhi= 85 ; yd=5 ;  ylab='ERA5 700 hPa RH [%]'
endif

if(ivar = cpshi)
  var='cpshi' ; ylo=-60; yhi= 80 ; yd=20;  ylab='ERA5 CPS High [m]'
endif

if(ivar = cpslo)
  var='cpslo' ; ylo=-60; yhi= 80 ; yd=20;  ylab='ERA5 CPS Low [m]'
endif

if(ivar = prg5)
  var='prg5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 500-km precip [mm/d]'
endif

if(ivar = pri5)
  var='pri5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 500-km precip [mm/d]'
endif

if(ivar = prc5)
  var='prc5' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='CMORPH 500-km precip [mm/d]'
endif

if(ivar = prg3)
  var='prg3' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 300-km precip [mm/d]'
endif

if(ivar = pri3)
  var='pri3' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 300-km precip [mm/d]'
endif

if(ivar = prc3)
  var='prc3' ; ylo=20; yhi= 100 ; yd=10 ;  ylab='CMORPH 300-km precip [mm/d]'
endif

if(ivar = prg8)
  var='prg8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='GSMaP 800-km precip [mm/d]'
endif

if(ivar = pri8)
  var='pri8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='IMERG 800-km precip [mm/d]'
endif

if(ivar = prc8)
  var='prc8' ; ylo=0; yhi= 80 ; yd=10 ;  ylab='CMORPH 800-km precip [mm/d]'
endif

if(basin = 'l') ; t1=ylab' LANT 2007-2021' ; endif
if(basin = 'w') ; t1=ylab' WPAC 2007-2021' ; endif
if(basin = 'e') ; t1=ylab' EPAC 2007-2021' ; endif
if(basin = 'h') ; t1=ylab' SHEM 2007-2021' ; endif


pngpath='plt/dev-non/'var'-'basin'-07-21.png'

ncol=23 ; ncola=29 ; nsty=3
dcol=33 ; dcola=39 ; dsty=3
xlab='Time to Genesis(dev) v Dissipation(nondev) [h] '
npath=ddir'/ts-non-'basin'.07-21.ctl'
nf=ofile(npath)

dpath=ddir'/ts-dev-'basin'.07-21.ctl'
df=ofile(dpath)

rc=metadata(nf,y, 0)
rc=metadata(df,y, 0)

nyn=_ny.nf
nyd=_ny.df

print 'ddd 'nyd' nn 'nyn

if(nyd >= nyn) ; nyall=nyn ; endif
if(nyn > nyd)  ; nyall=nyd ; endif
# -- weird problem when nyd>nyn and using npvalid.gsf...
#
if(basin = 'l')
nyn=nyall
nyd=nyall
endif

print 'nnnn 'nyn' 'nyd' 'nyall
'set grads off'
'set timelab on'
'set missconn on'
'set mproj off'
'set parea 1 10.5 0.75 7.5'
'set lon -120 0'
'set y 1'
nave='ave('var'.'nf',y=1,y='nyn')'
dave='ave('var'.'df',y=1,y='nyd')'

#'d 'nave
#'d 'dave
#'q pos'
'set xlint 24'
'set vrange 'ylo' 'yhi
'set ylint 'yd
yy=1
while(yy <= nyn)

# -- non dev
#
nv=var'.'nf'(y='yy')'
nnp=npvalid(nv)

#print 'nnnnnpppp 'nnp
'set cmark 0'
'set ccolor 'ncol
'set cthick 1'
'set cstyle 'nsty

if(nnp != 999)
  'd 'nv
endif
yy=yy+1
endwhile  
 
# -- dev
#
yy=1
while(yy <= nyd)
dv=var'.'df'(y='yy')'
nnd=npvalid(dv)

'set cmark 0'
'set ccolor 'dcol
'set cthick 1'
'set cstyle 'dsty

if(nnd != 999)
  'd 'dv
endif

yy=yy+1

endwhile
'set y 1'
'set cmark 0'
'set ccolor 0'
'set cthick 10'
'd 'nave

'set cmark 0'
'set ccolor 'ncola
'set cthick 8'
'd 'nave

'set cmark 0'
'set ccolor 0'
'set cthick 10'
'd 'dave

'set cmark 0'
'set ccolor 'dcola
'set cthick 8'
'd 'dave

if(var = 'shr')
'set cmark 0'
'set ccolor 1'
'set cthick 15'
'd const('dave',15,-a)'
endif

'draw xlab 'xlab
'draw ylab 'ylab

t2='#Dev(green): '_ny.df' #NonDev(red): '_ny.nf
rc=toptitle(t1,t2,1.25)

'gxprint 'pngpath' x1024  y768'

'q pos'
'quit'

return
