#!/bin/bash -i

b2='al'
b1='l'
year=2015

b2='io'
b1='i'
year=1983

b2='ep'
b1='e'
year=2012
year=2015

bopt="$b1.$year"

ropt='-N'
ropt=''

rm -i "DSs-local/ad2-$b2-$year.pypdb"

ad2 all -S "$bopt" -O1 -o "$ropt"
ad2 era5,clp3 -S "$bopt" -O1 -o "$ropt"

p-adinv.py -S "$bopt" -A -O "$ropt"
m-ad2inv.py -i -Y "$year" "$ropt"

#exit;


p-adinv.py -S "$bopt" -A -O "$ropt"

p-vdinv.py -S "$bopt" -O "$ropt"
p-vdinv.py -S "$bopt" -O -p pod "$ropt"
p-vdinv.py -S "$bopt" -O -p pod -f z0012 "$ropt"
p-vdinv.py -S "$bopt" -O -f z0012 "$ropt"


