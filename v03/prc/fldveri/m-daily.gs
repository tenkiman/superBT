function main(args)

rc=gsfallow(on)
rc=const()

year=subwrd(args,1)

if(year = '')
  print 'must set year at command line...'
  'quit'
endif 

_verb=0
bdtg=year'010100'
edtg=year'123112'

sdir='/raid05/era5-anl'
tdir='/raid05/era5-anl/da/'year
spath=sdir'/era5-anl-'year'-ua.ctl'

fc=ofile(spath)
if(_verb) ; print 'fffccc 'fc ; endif

# -- vars
#
var.1='zg'
lev.1='500'
var.2='ua'
lev.2='850'
var.3='va'
lev.3='850'

var.4='ua'
lev.4='200'
var.5='va'
lev.5='200'

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

# -- main loop
while(cdtg0 < edtg)

  n=1
  tpath=tdir'/era5-da-'cdtg0'.dat'
  if(_verb) ; print 'tttt 'tpath ; endif
  'set fwrite 'tpath  
  
  cdtg24=dtginc(cdtg0,24)
  
  ctime0=dtg2gtime(cdtg0)
  'set time 'ctime0

  if(_verb) ; print 'ccc 'cdtg0' ccc222444 'cdtg24 ; endif

  while(n <= nvar)
     cvar=var.n
     clev=lev.n
     rc=mkdaily(cvar,clev,cdtg0,cdtg24)
     n=n+1
  endwhile
  'disable fwrite'
  
  cdtg0=cdtg24

endwhile

'quit'

return

# -- make daily mean using ave(dtg0-dtg1)
#
function mkdaily(cvar,clev,cdtg0,cdtg24)

'set lev 'clev
'set lat -90 90'
'set lon 0 360'

ctime0=dtg2gtime(cdtg0)
ctime24=dtg2gtime(cdtg24)

print 'da for 'cvar' lev: 'clev' dtg: 'cdtg0' gtime: 'ctime0' - 'ctime24

# -- make daily average
'avar=ave('cvar',time='ctime0',time='ctime24')'

#'set gxout stat'
#'d avar'
#print 'aaaaaaaaaaaaaaaaaa '
#print result

expr='re('cvar','_nx',linear,'_bx','_dx','_ny',linear,'_by','_dy',ba)'

'set lat '_by' '_ey
'set lon '_bx' '_ex
#'q dims'
#print 'oooooodiiimmmmsss'
#print result

#'d 'expr
#print 'sssssssssooooooooo'
#print result

'set gxout fwrite'
'd 'expr
#print 'ooooooooodddddddddddd'
#print result


return(expr)


