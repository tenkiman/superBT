function main(args)

rc=gsfallow(on)
rc=const()

byear=2007
eyear=2021
byear=2014
byear=2021
eyear=2021
byear=2020
eyear=2020

byear=2008
eyear=2008
byear=2009
eyear=2022

byear=2008 ; eyear=2008

byear=2022 ; eyear=2022
byear=2021 ; eyear=2021
byear=2020 ; eyear=2020
byear=2001 ; eyear=2001
byear=2022 ; eyear=2022

year=byear
doImerg=1

bdir='/braid1/mfiorino/w22'
bdir='/data/w22'
prmax=6.0

while(year <= eyear)

yearp1=year+1
gver=7
if(year <= 2013) ; gver=6 ; endif
gver='6'

btime='00z1jan'year
etime='00z1jun'year
etime='00z1jan'yearp1

dodef=1
#dodef=0
if(dodef)

  'reinit'

# -- special case for gsmap V6 -- bad data in 2008
#
p6mask='maskout(p6,'prmax'-p6)'
if(year = 2008 | year = 2020)
  p6mask='maskout(maskout(p6,3.3-p6),p6-1.8)'
endif

pcmask='maskout(pc,'prmax'-pc)'
if(year = 2022 | year = 2021 | year = 2020)
  pcmask='maskout(maskout(pc,3.3-pc),pc-1.8)'
endif

  #gpath=bdir'/dat/pr/pr_gsmap/prg_a06h-'year'.ctl'
  gpath6=bdir'/dat/pr/pr_gsmapV6-Grev/prg_a06h-'year'.ctl'
  if(year <= 2019)
    cpath=bdir'/dat/pr/cmorph-v10/pr_cmorph/prc_a06h-'year'.ctl'
    cver='V10'
  else
    cpath=bdir'/dat/pr/pr_cmorph/prc_a06h-'year'.ctl'
    cver='V0X'
  endif

  ipath=bdir'/dat/pr/pr_imerg/pri_a06h-'year'.ctl'
  
# -- gave.dat vice prod .ctl

  ipath='../../dat/gave/pri-gave-'year'.ctl'
  gpath6='../../dat/gave/prgv6-gave-'year'.ctl'
  cpath='../../dat/gave/prc-gave-'year'.ctl'
  
  fc=ofile(cpath)
  f6=ofile(gpath6)
  fi=ofile(ipath)
  'set x 1'
  'set y 1'

'set t 1 last'
# -- take out the 1st point
#  'set time 00z3jan'year' 00z1jan'yearp1
#  'set time 'btime' 'etime

if(doImerg)
'!date'
  'pi=aave(pr.'fi',g)'
endif
'!date'
'pc=aave(pr.'fc',g)'
'!date'
'p6=aave(pr.'f6',g)'

if(year = 2022 | year = 2021 | year = 2020)
  'set time 'btime
  'd ave('pcmask',time='btime',time='etime')'
  print result
  pcard=sublin(result,2)
  pcmean=subwrd(pcard,4)
  print 'mmmmm 'pcmean
  pcmask='const('pcmask','pcmean',-u)'
  print pcmask
  'set time 'btime' 'etime
endif

if(year = 2008 | year = 2020)
  'set time 'btime
  'd ave('p6mask',time='btime',time='etime')'
  print result
  pcard=sublin(result,2)
  p6mean=subwrd(pcard,4)
  print 'mmmmm 'p6mean
  p6mask='const('p6mask','p6mean',-u)'
  print p6mask
  'set time 'btime' 'etime
endif

endif

#2008: p6mask='const(maskout(maskout(p6,3.3-p6),p6-1.8),2.34081,-u)'
#pcmask='const(maskout(maskout(pc,3.3-pc),pc-1.8),2.62658,-u)'
#p6mask='maskout(p6,'prmax'-p6)'
p6mask=p6
pcmask=pc
pimask=pi


'c'
'set timelab on'
'set grads off'
'set parea 0.75 10.5 0.5 7.75'

'set vrange 1 4.5'
'set ylint 0.5'

'set cmark 0'
'set ccolor 2'
'd 'p6mask

'set cmark 0'
'set ccolor 3'
'd 'pcmask

if(doImerg)
  'set cmark 0'
  'set ccolor 4'
  'd maskout(pi,'prmax'-pc)'
endif

'set cmark 0'
'set cthick 10'
'set ccolor 2'
'd linreg('p6mask')'
gag=subwrd(result,4)

'set cmark 0'
'set cthick 10'
'set ccolor 3'
'd linreg('pcmask')'
gac=subwrd(result,4)

if(doImerg)
  'set cmark 0'
  'set cthick 10'
  'set ccolor 4'
  'd linreg(maskout(pi,'prmax'-pi))'
  gai=subwrd(result,4)
endif

gdiff=(gac-gag)/((gac+gag)*0.5)
gdiff=gdiff*100.0
gdiff=math_nint(gdiff)
print 'gdiff 'gdiff

if(doImerg)
  idiff=(gag-gai)/((gag+gai)*0.5)
  idiff=idiff*100.0
  idiff=math_nint(idiff)
  print 'idiff 'idiff
endif

t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) [mm/d]'
t2='mean CMOPRPH: 'gac' mean GSMaP: 'gag' C-G diff ~ 'gdiff'%'

if(year = 2008)
  t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) [mm/d]'
  t3='NB: 66 GSMaP-V'gver'bad 6-h grids'
  t2='mean CMOPRPH: 'gac' mean GSMaP: 'gag' C-G diff ~ 'gdiff'% '
endif

if(year = 2022)
  t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) [mm/d]'
  t3='NB: 41 bad CMOPRH 6-h grids'
  t2='mean CMOPRPH: 'gac' mean GSMaP: 'gag' C-G diff ~ 'gdiff'% '
endif

if(year = 2021)
  t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) [mm/d]'
  t3='NB: 62 bad CMOPRH 6-h grids'
  t2='mean CMOPRPH: 'gac' mean GSMaP: 'gag' C-G diff ~ 'gdiff'% '
endif

if(year = 2020)
  t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) [mm/d]'
  t3='NB: 72 bad CMOPRH 6-h grids and 09 bad GSMaP-V'gver' 6-h grids'
  t2='mean CMOPRPH: 'gac' mean GSMaP: 'gag' C-G diff ~ 'gdiff'% '
endif

if(doImerg)
  t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaP-V'gver' (red) v IMERG (blue) [mm/d]'
  t2='mean CMOPRPH: 'gac' GSMaP: 'gag' IMERG: 'gai' C-G diff ~ 'gdiff'% G-I diff ~ 'idiff'%'
endif

rc=toptitle(t1,t2,1.0,1,1)
if(year = 2008 | year = 2022 | year = 2021 | year = 2020)
  rc=toptle3(t1,t2,t3,1.0,1,1,2)
endif

ppath='pr-gave-c-v-g-v'gver'-'year'.png'
if(doImerg)
  ppath='pr-gave-c-v-g-v'gver'-v-i-'year'.png'
endif
'gxprint 'ppath

year=year+1

endwhile

return
