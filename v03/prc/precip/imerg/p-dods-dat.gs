function main(args)

rc=gsfallow(on)
rc=const()

n=1
gtime=subwrd(args,n) ; n=n+1
ofile=subwrd(args,n) ; n=n+1

dpath='https://gpm1.gesdisc.eosdis.nasa.gov:443/dods/GPM_3IMERGHH_07'

verb=1
docomp=0

'sdfopen 'dpath

'set lon -180.0 179.75'
'set lat -59.875 59.875'
'set time 'gtime
'q dims'
if(verb) ; print result ; endif

print 'making ofile: 'ofile

'set gxout fwrite'
'set fwrite 'ofile
'prd=re(precip,1440,linear,-180.0,0.25,480,linear,-59.875,0.25,ba)'
'd prd'
'disable fwrite'
'quit'

return


function getofile(gtime)

  lg=strlen(gtime)
#  print 'ggg 'gtime' ll 'lg
  dtg=gtime2dtg(gtime)
#  print 'ddd 'dtg

  min='00'
  if(lg = 15)
    min='30'
  endif

  yyyy=substr(dtg,1,4)
  mm=substr(dtg,5,2)
  dd=substr(dtg,7,2)
  hh=substr(dtg,9,2)

  otime=yyyy'-'mm'-'dd'-'hh'-'min'.dat'
  ofile=yyyy'/imerg-v7-'otime
#  print 'oooo 'ofile
  return(ofile)

function gettndx(ntime)

'set time 'ntime
'q dims'
tcard=sublin(result,5)
tndx=subwrd(tcard,9)
return(tndx)

end

function comp(args)

  'open t.ctl'
  'set dfile 2'
  'pr=pr'
  
  'set gxout stat'
  'd pr'
  print 'dods file'
  print
  print result
  
  'd prd'
  print 're ba'
  print
  print result
  
  'd prdn'
  print 're no ba'
  print
  print result

  'd precip.1'
  print '0.1 input data'
  print
  print result
  
#'d re2(precip.1,0.25,0.25,ba)'
#print 'ppp'result
return(0)
  
