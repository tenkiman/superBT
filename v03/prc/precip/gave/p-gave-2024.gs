function main(args)

rc=gsfallow(on)
rc=const()

byear=2020 ; eyear=2020
byear=2008 ; eyear=2008
byear=2022 ; eyear=2022
byear=2007 ; eyear=2022
byear=2020 ; eyear=2022
byear=2007 ; eyear=2019
byear=2020 ; eyear=2022
byear=2001 ; eyear=2006
byear=2003 ; eyear=2007
byear=2020 ; eyear=2022
byear=2015 ; eyear=2015
byear=2019 ; eyear=2019
byear=2022 ; eyear=2022
byear=2023 ; eyear=2024
byear=2001 ; eyear=2021
byear=1998 ; eyear=2000
# -- correct 2000
byear=2000 ; eyear=2000
byear=2024 ; eyear=2024

# -- no V* 2012-14

dov8only=1
byear=2012 ; eyear=2014

# -- after redo of products V8 and V8-G
dov8only=0
byear=1998 ; eyear=2014
byear=2015 ; eyear=2024

nave.1='gsmapV6'
nave.2='gsmapV8'
nave.3='gsmapV8-G'
nave.4='imerg'

bdir='/data/w22'
odir='/sbt/superBT-V04/v03/prc/precip/dat'
year=byear
while(year <= eyear)
  'reinit'

  gfile6='prg_a06h-'year'.ctl'
  gfile8='prg_a06h-'year'.ctl'
  gfile8g='prg_a06h-'year'.ctl'
  ifile='pri_a06h-'year'.ctl'

#  gpath6=bdir'/dat/pr/pr_gsmapV6-Grev/'gfile6
#  gpath8=bdir'/dat/pr/pr_gsmapV8/'gfile8
  gpath8g=bdir'/dat/pr/pr_gsmapV8-G/'gfile8g
  ipath=bdir'/dat/pr/pr_imerg/'ifile
  
#  fg6=ofile(gpath6)
#  fg8=ofile(gpath8)
  fg8g=ofile(gpath8g)
  fi=ofile(ipath)
  
#print 'fg6  'fg6 ' 'gpath6
#print 'fg8  'fg8 ' 'gpath8
print 'fg8g 'fg8g' 'gpath8g
print 'fi   'fi  ' 'ipath

ogpath=odir

bfi=1
efi=4

# -- case with no gsmapV6
#
if( fg6 = 0)
  efi=3
  nave.1='gsmapV8'
  nave.2='gsmapV8-G'
  nave.3='imerg'
else
  nave.1='gsmapV6'
  nave.2='gsmapV8'
  nave.3='gsmapV8-G'
  nave.4='imerg'
endif

nave.1='gsmapV8-G'
nave.2='imerg'

# - just do v8
if(dov8only = 1)
  bfi=2
  efi=2
endif

# -- just do the two we're going to use
#
nave.1='gsmapV8-G'
nave.2='imerg'
bfi=1
efi=2

print 'bfi 'bfi' efi 'efi

fi=bfi
while(fi<=efi)
  'set dfile 'fi
  'set x 1'
  'set y 1'
  'set t 1 last'
  'q dims'
  tset=sublin(result,5)
  print 'fi 'fi' dims 'tset
  'q ctlinfo'
  dset=sublin(result,1)
  tdef=sublin(result,7)
  print 'fi 'fi'  dset 'dset
  print 'fi 'fi'  tdef 'tdef

'!date'

  'pg=aave(pr,g)'
  'set fwrite 'odir'/gave-'nave.fi'-'year'.dat'
  'set gxout fwrite '
  'd pg'
  print result
  'disable fwrite'

'!date'

  fi=fi+1
endwhile

year=year+1

endwhile
return
