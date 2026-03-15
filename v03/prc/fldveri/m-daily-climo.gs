function main(args)

rc=gsfallow(on)
rc=const()

year=subwrd(args,1)

if(year = '')
  print 'must set year at command line...'
  'quit'
endif 

_verb=1

sdir='/raid05/era5-anl/da'
tdir='/raid05/era5-anl/climo/da'
spath=sdir'/era5-da-1991-2021.ctl'

fc=ofile(spath)
if(_verb) ; print 'fffccc 'fc ; endif

# -- vars
#
var.1='z5'
var.2='u8'
var.3='v8'
var.4='u2'
var.5='v2'

nvar=5

# -- x dims
#
_nx=240
_dx=1.5
_bx=_dx/2
_ex=360.0-_bx

# -- y dims
_ny=_nx/2
_dy=_dx
_by=-90.0+_dy/2
_ey=90.0-_dy/2

cdtg0=bdtg
#edtg=dtginc(bdtg,48)

if(year = 1991)
nyear=365
endif

if(year = 1992)
nyear=366
endif

tpath=tdir'/era5-climo-da-'nyear'.dat'
if(_verb) ; print 'tttt 'tpath ; endif

'set fwrite 'tpath  

bdtg=year'010100'
edtg=year'123112'

#edtg=year'010300'


# -- main loop
#
cdtg0=bdtg
while(cdtg0 < edtg)

  n=1
  
  cdtg24=dtginc(cdtg0,24)
  ldtg24='2020'substr(cdtg0,5,10)
  ctime0=dtg2gtime(cdtg0)
  'set time 'ctime0

  if(_verb) ; print 'ccc 'cdtg0' lll 'ldtg24 ; endif

  while(n <= nvar)
     cvar=var.n
     rc=mkdailyclm(cvar,cdtg0,ldtg24,nyear)
     n=n+1
  endwhile
  
  cdtg0=cdtg24

endwhile
'disable fwrite'
'quit'

return

# -- make daily mean using ave(dtg0-dtg1)
#
function mkdailyclm(cvar,cdtg0,cdtg24,nyear)

ctime0=dtg2gtime(cdtg0)
ctime24=dtg2gtime(cdtg24)


'set lat '_by' '_ey
'set lon '_bx' '_ex

#'q dims'
#print 'oooooodiiimmmmsss'
#print result


#'set gxout fwrite'
#'d avar'
#print 'ooooooooodddddddddddd'
#print result

# -- make daily average
#
'avar=ave('cvar',time='ctime0',time='ctime24','nyear')'

if(_verb)
  'set gxout stat'
  'd avar'
  card=sublin(result,11)
  mean=subwrd(card,2)
print 'daclm for 'cvar' dtg: 'cdtg0' gtime: 'ctime0'-'ctime24' cvar: 'cvar' mean: 'mean
  
  'set gxout fwrite'
  'd avar'
else
  'set gxout fwrite'
  'd avar'
endif


return(1)


