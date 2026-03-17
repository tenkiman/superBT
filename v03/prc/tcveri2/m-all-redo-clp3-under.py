#!/usr/bin/env python

from sBT import *

# -- before running...
#
# c.2002  72         85.0 N:   20  Nfc:     17
# c.2019  72          0.0 N:    2  Nfc:      0
# e.1997  72         98.3 N:  121  Nfc:    119
# e.2002  72         89.5 N:   86  Nfc:     77
# e.2019  72         96.6 N:   89  Nfc:     86
# h.1972  72         99.6 N:  252  Nfc:    251
# h.1986  72         91.0 N:  145  Nfc:    132
# h.2015  72         96.0 N:  100  Nfc:     96
# i.1965  72         97.8 N:   45  Nfc:     44
# i.1966  72         98.6 N:   69  Nfc:     68
# l.1954  72         92.2 N:   64  Nfc:     59
# l.1955  72         99.2 N:  120  Nfc:    119
# l.1958  72         98.8 N:   80  Nfc:     79
# l.1961  72         95.7 N:   46  Nfc:     44
# l.1964  72         95.4 N:  131  Nfc:    125
# l.1986  72         89.2 N:   37  Nfc:     33
# l.1991  72         91.9 N:   37  Nfc:     34
# l.1996  72         97.6 N:  165  Nfc:    161
# l.1998  72         99.3 N:  148  Nfc:    147
# l.2002  72         84.0 N:   94  Nfc:     79
# l.2004  72         94.8 N:  155  Nfc:    147
# l.2005  72         89.8 N:  215  Nfc:    193
# l.2006  72         96.6 N:  116  Nfc:    112
# l.2012  72         99.5 N:  183  Nfc:    182
# l.2015  72         94.4 N:   71  Nfc:     67
# l.2019  72         98.3 N:   59  Nfc:     58
# l.2020  72         90.9 N:  198  Nfc:    180
# l.2021  72         95.4 N:  109  Nfc:    104
# l.2022  72         99.2 N:  118  Nfc:    117
# l.2023  72         97.1 N:  210  Nfc:    204
# w.1960  72         99.5 N:  191  Nfc:    190
# w.1962  72         99.3 N:  145  Nfc:    144
# w.1967  72         99.5 N:  193  Nfc:    192
# w.1972  72         99.4 N:  312  Nfc:    310
# w.1997  72         99.6 N:  275  Nfc:    274

cases=[

#'c.2002',
#'c.2019',
'e.1997',
'e.2002',
'e.2019',
'h.1972',
'h.1986',
'h.2015',
'i.1965',
'i.1966',
'l.1954',
'l.1955',
'l.1958',
'l.1961',
'l.1964',
'l.1986',
'l.1991',
'l.1996',
'l.1998',
'l.2002',
'l.2004',
'l.2005',
'l.2006',
'l.2012',
'l.2015',
'l.2019',
'l.2020',
'l.2021',
'l.2022',
'l.2023',
'w.1960',
'w.1962',
#'w.1967',
#'w.1972',
#'w.1997',
	
]

# -- redo because ... doing noloads in clp3 with speed and lon check in the lant
# -- and for lant storms crossing the basin year
#
casesLANT=[

#'l.1954',
'l.1955',
'l.1958',
'l.1961',
'l.1964',
'l.1986',
'l.1991',
'l.1996',
'l.1998',
'l.2002',
'l.2004',
'l.2005',
'l.2006',
'l.2012',
'l.2015',
'l.2019',
'l.2020',
'l.2021',
'l.2022',
'l.2023',
	
]
ropt='norun'
ropt=''

MF.sTimer('ALL-redo')
for case in casesLANT:
    MF.sTimer('case-%s'%(case))
    cmd='m-redo-clp3-under.py -S %s'%(case)
    mf.runcmd(cmd,ropt)
    MF.dTimer('case-%s'%(case))
    
cmd='clp3-under.sh'
mf.runcmd(cmd,ropt)
MF.dTimer('ALL-redo')
