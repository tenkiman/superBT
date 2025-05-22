function main(args)

rc=gsfallow(on)
rc=const()

n=1
print 'args 'args
tdir=subwrd(args,n); n=n+1
yyyymm=subwrd(args,n); n=n+1

mm=substr(yyyymm,5,2)
yyyy=substr(yyyymm,1,4)
nmo=subwrd(_monamel,mm)
moyear=nmo%yyyy

print 'iyyy 'tdir
print 'iyyy 'yyyymm' 'imo' 'yyyy' 'nmo' 'moyear

'sdfopen https://gpm1.gesdisc.eosdis.nasa.gov:443/dods/GPM_3IMERGM_07'
'set time 1'moyear
'set lon -180.0 179.75'
'set lat -59.875 59.875'
'q dim'
print result
'set fwrite 'tdir'/3B-MO.MS.MRG.3IMERG.'yyyymm'01-S000000-E235959.'mm'.V07B.HDF5.SUB.dat'
'set gxout fwrite'
'prd=re(precip,1440,linear,-180.0,0.25,480,linear,-59.875,0.25,ba)'
'd prd'
print result
'disable fwrite'

'set x   1 3600'
'set y 300 1500'
'q dims'
print result
'set fwrite 'tdir'/3B-MO.MS.MRG.3IMERG.'yyyymm'01-S000000-E235959.'mm'.V07B.HDF5.SUB.0p1.dat'
'set gxout fwrite'
'd precip'
print result

'quit'

return