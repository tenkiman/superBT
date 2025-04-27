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

nave.1='gsmapV6'
nave.2='cmorph'
nave.3='imerg'

bdir='/data/w22'
odir='/data/w22/prj-superBT/dat/gave'
year=byear
while(year <= eyear)
  'reinit'
  gfile6='prg_a06h-'year'.ctl'
  cfile='prc_a06h-'year'.ctl'
  ifile='pri_a06h-'year'.ctl'

  gpath=bdir'/dat/pr/pr_gsmap/'gfile
  gpath6=bdir'/dat/pr/pr_gsmapV6-Grev/'gfile6
  
  if(year <= 2019)
    cpath=bdir'/dat/pr/cmorph-v10/pr_cmorph/'cfile
    cver='V10'
  else
    cpath=bdir'/dat/pr/pr_cmorph/'cfile
    cver='V0X'
  endif
  ipath=bdir'/dat/pr/pr_imerg/'ifile

  f6=ofile(gpath6)
  fc=ofile(cpath)
  fi=ofile(ipath)
  
print 'f6 'f6' 'gpath6
print 'fc 'fc' 'cpath
print 'fi 'fi' 'ipath

ogpath=odir
bfi=1
efi=3

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
  'pg=aave(pr,g)'
  'set fwrite 'odir'/gave-'nave.fi'-'year'.dat'
  'set gxout fwrite '
  'd pg'
  print result
  'disable fwrite'
  fi=fi+1
endwhile

year=year+1

endwhile
return
