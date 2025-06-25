function main(args)

rc=gsfallow(on)
rc=const()

dov8only=0
doimergonly=0
dosbtonly=1


byear=2024 ; eyear=2024
byear=1998 ; eyear=2024
byear=1998 ; eyear=1998
byear=2022 ; eyear=2024


bdir='/data/w22'
odir='/sbt/superBT-V04/v03/prc/precip/dat/mo'
odir='../dat/mo'

# -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm main loop
#

year=byear
while(year <= eyear)
  'reinit'

if(dosbtonly)

  nave.1='gsmapV8-G'
  nave.2='imerg'

  gfile8g='prg_a06h-'year'.ctl'
  ifile='pri_a06h-'year'.ctl'

  gpath8g=bdir'/dat/pr/pr_gsmapV8-G/'gfile8g
  ipath=bdir'/dat/pr/pr_imerg/'ifile

  fg8g=ofile(gpath8g)
  fi=ofile(ipath)

  print 'fg8g 'fg8g' 'gpath8g
  print 'fi   'fi  ' 'ipath

  bfi=1
  efi=2

else

  nave.1='gsmapV6'
  nave.2='gsmapV8'
  nave.3='gsmapV8-G'
  nave.4='imerg'
  
  gfile6='prg_a06h-'year'.ctl'
  gfile8='prg_a06h-'year'.ctl'
  gfile8g='prg_a06h-'year'.ctl'
  ifile='pri_a06h-'year'.ctl'
  
  gpath6=bdir'/dat/pr/pr_gsmapV6-Grev/'gfile6
  gpath8=bdir'/dat/pr/pr_gsmapV8/'gfile8
  gpath8g=bdir'/dat/pr/pr_gsmapV8-G/'gfile8g
  ipath=bdir'/dat/pr/pr_imerg/'ifile
  
  fg6=ofile(gpath6)
  fg8=ofile(gpath8)
  fg8g=ofile(gpath8g)
  fi=ofile(ipath)
  
  print 'fg6  'fg6 ' 'gpath6
  print 'fg8  'fg8 ' 'gpath8
  print 'fg8g 'fg8g' 'gpath8g
  print 'fi   'fi  ' 'ipath

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

# - just do v8
  if(dov8only = 1)
    bfi=2
    efi=2
  endif

  if(doimergonly = 1)
    bfi=fi
    efi=fi
  endif

endif

print 'bfi 'bfi' efi 'efi

# -- outdoor path
#
ogpath=odir

# -- pppppppppppppppppppppppppppp processing loop for each 12 months
#

# -- fffffff file loop
#
ff=bfi
while(ff<=efi)

  bmo=1 ; emo=12
#  emo=1
  mo=bmo
 
# -- mmmmmmm month loop
#
  while(mo <= emo)
    
    print 'lllllll 'ff' mo: 'mo
    'set dfile 'ff
    rc=getbounds(year,mo)
    n=1
    omo1=subwrd(rc,n) ; n=n+1
    t1=subwrd(rc,n)   ; n=n+1
    t2=subwrd(rc,n)   ; n=n+1
    xl=subwrd(rc,n)   ; n=n+1
    yl=subwrd(rc,n)   
    
    print 'bounds omo1 'omo1' 't1' t2 't2' xl 'xl' yl 'yl
    opath=odir'/'nave.ff'-moave-'year'-'omo1'.dat'
    print 'opath 'opath
    'set fwrite 'opath
        
    'set x 1 'xl
    'set y 1 'yl
    'set lon  0 360'
    'set t 1'
    
'!date'

    'pm=ave(pr,t='t1',t='t2')'
    'set gxout fwrite '
    'd re(pm,0.25)'
    print result
    'disable fwrite'
    
'!date'

    mo=mo+1
  
  endwhile

  ff=ff+1

endwhile

year=year+1

endwhile
'quit'

return

# -- ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
function getbounds(year,mo)

# -- get x/y bounds

  'q ctlinfo'
  xdef=sublin(result,4)
  xl=subwrd(xdef,2)
  ydef=sublin(result,5)
  yl=subwrd(ydef,2)

# -- get time bounds

  omo1=mo
  if(mo <= 9); omo1='0'%mo ; endif

  mo2=mo+1
  omo2=mo2
  if(mo2 <= 9); omo2='0'%mo2 ; endif
  year2=year
  if(omo2 > 12) ; omo2=01 ; year2=year+1 ; endif
    
  dtg1=year%omo1'0100'
  dtg2=year2%omo2'0100'
    
  time1=dtg2gtime(dtg1)
  time2=dtg2gtime(dtg2)
    
  'set time 'time1
  'q dims'
  t1=sublin(result,5)
  t1=subwrd(t1,9)

  'set time 'time2
  'q dims'
  print 'rrr 'result
  t2=sublin(result,5)
  t2=subwrd(t2,9)
  t2=t2-1
  rc=omo1' 't1' 't2' 'xl' 'yl
  
return(rc)
    



