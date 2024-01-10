function main(args)
rc=gsfallow(on)
rc=const()

dpath='/dat3/dat/sbt-v03/dat/tcdiag/2017/2017090706/era5/era5.2017090706.nhem.ctl'
fo=ofile(dpath)
print 'fo 'fo

rc=metadata(fo,y,1)

n=1
nt=_nt.fo
'set x 1 '_nx.fo
'set y 1 '_ny.fo
'set z 1'


'set fwrite g.dat'
'set gxout fwrite'

while (n<=nt)
  'set t 'n
  'd uas'
  'd vas'
  'd psl'
  'd pr'
  'd prc'

  print 'nnnn 'n
  n=n+1
endwhile

'disable fwrite'


return
