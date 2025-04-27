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
byear=2019; eyear=2022
byear=2015 ; eyear=2015
byear=2019 ; eyear=2019 
byear=2022 ; eyear=2022
byear=2001 ; eyear=2022
byear=1998 ; eyear=2024
byear=2000 ; eyear=2000

# -- g6 v g8g v imerg comp
#
comp6to8=1
byear=2001; eyear=2001

# -- g8 v g8g v imerg comp
# -- using comp6to8 flag
#
comp6to8=0
byear=1998 ; eyear=2024
#byear=2023 ; eyear=2024

year=byear

bdir='/braid1/mfiorino/w22'
bdir='/data/w22'
prmax=6.0

while(year <= eyear)

gver='6Grev'

btime='00z1jan'year
etime='00z1jun'year
etime='00z1jan'yearp1

cver='V0X'
if(year <= 2019) ; cver='V10' ; endif

  
'reinit'

  
# -- gave.dat vice prod .ctl
bdir='/sbt/superBT-V04/v03/prc/precip/dat'
ipath=bdir'/pri-gave-'year'.ctl'
gpath8=bdir'/prg8-gave-'year'.ctl'
gpath8g=bdir'/prg8g-gave-'year'.ctl'
gpath6=bdir'/prgv6-gave-'year'.ctl'
  
f6=ofile(gpath6)
f8=ofile(gpath8)
f8g=ofile(gpath8g)
fi=ofile(ipath)

print 'f6: 'f6' gpath6: 'gpath6
print 'f8: 'f8' gpath8: 'gpath8
print 'f8g: 'f8g' gpath8g: 'gpath8g
print 'fi: 'fi' igpath: 'ipath


'set x 1'
'set y 1'
'set t 1 last'

p6mask='pr.'f6
p8mask='pr.'f8
p8gmask='pr.'f8g
pimask='pr.'fi


'c'
'set timelab on'
'set grads off'
'set parea 0.75 10.5 0.5 7.75'

'set vrange 1 4.5'
'set ylint 0.5'

comp6to8=0

if(year >= 2001 & comp6to8 = 1)

# -- g6 v g8 v imerg
#
  'set cmark 0'
  'set ccolor 2'
  'd 'p6mask
  
  'set cmark 0'
  'set ccolor 3'
  'd 'p8gmask
  
  'set cmark 0'
  'set ccolor 4'
  'd 'pimask
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 2'
  'd linreg('p6mask')'
  ga6=subwrd(result,4)
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 3'
  'd linreg('p8gmask')'
  ga8g=subwrd(result,4)
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 4'
  'd linreg('pimask')'
  gai=subwrd(result,4)
  
  gdiff=(ga6-ga8g)/((ga8g+ga6)*0.5)
  gdiff=gdiff*100.0
  gdiff=math_nint(gdiff)
  print 'gdiff 'gdiff
  
  print 'gai 'gai' ga6 'ga6' ga8 ' ga8
  idiff=(gai-ga8g)/((ga8g+gai)*0.5)
  idiff=idiff*100.0
  idiff=math_nint(idiff)
  
#t1=year' GlobAve PR CMORPH-'cver' (green) v GSMaPV'gver' (red) v IMERG (blue) [mm/d]'
#t2='mean CMOPRPH: 'ga8' GSMaP: 'ga6' IMERG: 'gai' C-G diff ~ 'gdiff'% I-G diff ~ 'idiff'%'
  
  pngfile='pr-gave-G6-v-G8G-v-I'
  t1=year' GlobAve PR GSMapV6 (green) v GSMaPV8G (red) v IMERG (blue) [mm/d]'
  t2='mean GSMaP6: 'ga6' GSMaP8G: 'ga8g' IMERG: 'gai' G6-G8G diff ~ 'gdiff'% I-G8G diff ~ 'idiff'%'

else

# -- g8 v g8g v imerg
#

  'set cmark 0'
  'set ccolor 2'
  'd 'p8mask

  'set cmark 0'
  'set ccolor 3'
  'd 'p8gmask
  
  'set cmark 0'
  'set ccolor 4'
  'd 'pimask
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 2'
  'd linreg('p8mask')'
  ga8=subwrd(result,4)
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 2'
  'd linreg('p8gmask')'
  ga8g=subwrd(result,4)
  
  'set cmark 0'
  'set cthick 10'
  'set ccolor 4'
  'd linreg('pimask')'
  gai=subwrd(result,4)
  
  gdiff=(ga8-ga8g)/((ga8+ga8g)*0.5)
  gdiff=gdiff*100.0
  gdiff=math_nint(gdiff)
  print 'gdiff 'gdiff
  
  print 'gai 'gai' ga8 'ga8' ga8g ' ga8g
  idiff=(gai-ga8g)/((ga8g+gai)*0.5)
  idiff=idiff*100.0
  idiff=math_nint(idiff)
  
  pngfile='pr-gave-G8-v-G8G-v-I'
  t1=year' GlobAve PR GSMapV8 (green) v GSMaPV8G (red) v IMERG (blue) [mm/d]'
  t2='mean GSMaP8: 'ga8' GSMaP8G: 'ga8g' IMERG: 'gai' G8-G8G diff ~ 'gdiff'% I-G8G diff ~ 'idiff'%'

endif


rc=toptitle(t1,t2,0.9,1,1)

pdir='plt/gave'
ppath=pdir'/'pngfile'-'year'.png'

print 'ppath: 'ppath
'gxprint 'ppath

year=year+1

'q pos'
endwhile

'quit'
return
