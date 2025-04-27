function main(args)
rc=gsfallow('on')
rc=const()

byear=2019
eyear=2022

year=byear
while(year <= eyear)
  'reinit'
  gfile='prg_a06h-'year'.ctl'
  fc=ofile(gfile)
  print 'yyy 'gfile' fc 'fc
  'set x 1'
  'set y 1'
  'set t 1 last'
  '!date'
  'pg=aave(pr,g)'
  '!date'
  'set gxout stat'
  'd pg'
  print result
  year=year+1

endwhile




return
