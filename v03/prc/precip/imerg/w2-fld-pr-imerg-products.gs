function main(args)

rc=gsfallow(on)
rc=const()

i=1

dtg=subwrd(args,i)     ; i=i+1
dpath=subwrd(args,i)   ; i=i+1
opath=subwrd(args,i)   ; i=i+1
ltable=subwrd(args,i)  ; i=i+1

outconv='grads_grib'
outconv='grib_only'

minpgood=75.0

# -- 20221224
# -- the chkvar test fails for some dtgs, but the ave still works...
# -- a grads problem in finding the correct file?
# -- grads problem definitely dealing with 30 min data...
# -- keep the minpgood requirement -- now calculated more accurately
#
#minpgood=0.0

dvar='maskout(pr,pr)'
dvarchk06='(sum('dvar',t-6*2,t+0))'
dvarchk12='(sum('dvar',t-12*2,t+0))'

lvar.1='pr'
lvrts.1='accum'
#lvrts.1='instant'


lvar.3='pr'
lvrts.3='accum'

lvar.6='pr'
lvrts.6='accum'

lvar.12='pr'
lvrts.12='accum'

lcenter='gsfc'
lmodel='imerg'
print 'qqqqq 'dpath
print 'ooooo 'opath
fd=ofile (dpath)
if(fd<=0) ; say 'no data file' ; 'quit' ; endif

rc=metadata(fd,'y')

'set_lats parmtab 'ltable

'set_lats convention 'outconv
'set_lats calendar standard'
'set_lats frequency hourly'
'set_lats model "'lmodel'"'
'set_lats center 'lcenter
'set_lats comment "IMERG pr"'

'set_lats gridtype linear'
'set x 1 '_nx.fd
'set y 1 '_ny.fd

'set_lats timeoption dim_env'
'set t 1'

#'set gxout latsgrid'
'lats_grid 'dvar
id_grid=subwrd(result,5)
if(id_grid = 0) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

gtime=dtg2gtime(dtg)
'set time 'gtime
dtg6=dtginc(dtg,-6)
gtime6=dtg2gtime(dtg6)
dtg12=dtginc(dtg,-12)
gtime12=dtg2gtime(dtg12)


# -- get time from the index bounds t-12 t-1
#
getndx=0

if(getndx = 1)
  'q dims'
  card5=sublin(result,5)
  tcur=subwrd(card5,9)
  etndx=tcur-1
  btndx6=tcur-11
  btndx12=tcur-23
  'set t 'btndx6
  'q dims'
  card5=sublin(result,5)
  bgtime6=subwrd(card5,6)

  'set t 'btndx12
  'q dims'
  card5=sublin(result,5)
  bgtime12=subwrd(card5,6)

  'set t 'etndx
  'q dims'
  card5=sublin(result,5)
  egtime=subwrd(card5,6)

  print ' tttt 12 'bgtime12' 6 'bgtime6' e 'egtime
endif

# -- only do 06h
#
do12hour=0

ngood06=chkvar(pr,6*2,dtg)
ngood12=chkvar(pr,12*2,dtg)
pgood06=(ngood06/(6*2))*100.0

pgood12=(ngood12/(12*2))*100.0
pgood06=math_nint(pgood06)
pgood12=math_nint(pgood12)

print 'RRRRRRRCCCCCCC 06h -- 'ngood06' 12: 'ngood12' pgood06: 'pgood06' pgood12: 'pgood12

rc=getdimenv()

if(pgood06 >= minpgood)
  lopath=praccum(6,gtime6,gtime,btndx6,etndx,lvar.6,lvrts.6,id_grid,opath,dtg)
  print 'YYYYYYYYYYYYYY 06h -- pgood06: 'pgood06' making: 'lopath'.grb'
else
  print 'NNNNNNNNNNNNNN 06h -- pgood06: 'pgood06
endif

if(do12hour = 1)
  if(pgood12 >= minpgood)
    lopath=praccum(12,gtime12,  gtime,btndx12,etndx,lvar.12,lvrts.12,id_grid,opath,dtg)
    print 'YYYYYYYYYYYYYY 12h -- pgood12: 'pgood12' making: 'lopath'.grb'
  else
    print 'NNNNNNNNNNNNNN 12h -- pgood12: 'pgood12
  endif
endif

'quit'
return

# -- only for data processing
#
function chkvar(var,nb,dtg)

verb=0

'q dims'
card5=sublin(result,5)
curt=subwrd(card5,9)
if(verb); print 'curt: 'curt; endif

goodmaxv=1000.0
ngood=0
'set gxout stat'
ct=nb-1

while (ct >= 0)
  vct=(ct+1)*-1
#sett=curt+vct
#'set t 'sett
#'q time'
#if(verb);  print 'sssss 'sett' vct: 'cvt' 'subwrd(result,3); endif
#'d 'var
  'd 'var'(t+'vct')'
  card=sublin(result,7)
  card8=sublin(result,8)
  nvalid=subwrd(card,8)
  maxv=subwrd(card8,5)
  
if(verb)
  card9=sublin(result,9)
  card10=sublin(result,10)
  meanv=subwrd(card10,2)
  print 'qqq dtg: 'dtg' vct: 'vct' nvalid: 'nvalid' maxv: 'maxv' meanv: 'meanv' goodmaxv: 'goodmaxv
endif
  if(nvalid > 0 & maxv < goodmaxv)
    ngood=ngood+1
  endif
  ct=ct-1
endwhile

#'set t 'curt

nbm1=nb-1
#print 'pra=ave(maskout(pr,pr),t-'nbm1',t-1)*24'
#'pra=ave(maskout(pr,pr),t-'nbm1',t-1)*24'
#'d aave(pra,g)'
#print result
#print 'rrrrrrrrrrrrrrrr'

'set gxout contour'
return(ngood)


# -- function to do accumulation
# -- gsmap V6 has negative values... use maskout

function praccum(acp,bgtime,egtime,btndx,etndx,lvar,lvrts,id_grid,opath,dtg)

'set_lats deltat '0

if(acp < 10)              ;  lopath=opath'_a0'acp'h_'dtg ; endif
if(acp > 10 & acp < 100)  ;  lopath=opath'_a'acp'h_'dtg ; endif


'set_lats create 'lopath

id_file=subwrd(result,5)
if(id_file<=0) ; say 'unable to create LATS output file 'opath' sayoonara, baby ' ; 'quit' ; endif
'set_lats var 'id_file' 'lvar' 'lvrts' 'id_grid' 0'
id_var=subwrd(result,5)
if(!id_var) ; print 'unable to define the LATS VAR 'acp'; sayoonara, baby' ; 'quit' ; endif

naccum=acp*2-1
naccum=acp*2
#
# convert to mm/day .. units is mm/h hence divide by my # h (acp) vice # time steps
#

sfact=24.0
print 'pra=ave(maskout(pr,pr),t-'naccum',t-'1')*'sfact
'pra=ave(maskout(pr,pr),t-'naccum',t-'1')*'sfact

#print 'pra=ave(pr,t-'naccum',t-'1')*'sfact
#'pra=ave(pr,t-'naccum',t-'1')*'sfact

# -- as sum .. get same # as ave of rates
#
sfact=2.0
#print 'pra=sum(pr,t-'naccum',t-'1')*'sfact
#'pra=sum(pr,t-'naccum',t-'1')*'sfact

#print 'pra=sum(maskout(pr,pr),t-'naccum',t-'0')*'sfact
#'pra=sum(maskout(pr,pr),t-'naccum',t-'0')*'sfact

#print 'pra=ave(pr,time='bgtime',time='egtime')*'sfact
#'pra=ave(pr,time='bgtime',time='egtime')*'sfact
'd aave(pra,g)'
print 'ttttttttttttt 'sublin(result,1)

#print 'pra=ave(pr,t='btndx',t='etndx')*'sfact
#'pra=ave(pr,t='btndx',t='etndx')*'sfact
#'d aave(pra,g)'
#print 'nnnnnnnnnnnnn 'result

'set_lats write 'id_file' 'id_var
id_write=subwrd(result,5)
if(id_write >0) 
#  'd pra'
  'lats_data pra'
  id_output=subwrd(result,5)
else
  print 'unable to set up write for VAR 'acp'; sayoonara, baby'
 'quit'
endif
'set_lats close 'id_file

return(lopath)

