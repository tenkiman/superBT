*
* GrADS control file for GSMaP_MVK Satellite Info Flag (ver.8)
*
* Satellite/Sensor information is assigned to each bit in the 32-bit
* integer (see details in DataFormatDesctiption_MVK_v7.0000.pdf).
*
DSET   ^gsmap_mvk.%y4%m2%d2.%h200.v8.0000.0.sateinfo.dat
TITLE  GSMaP_MVK 0.1deg Hourly Satellite Information Flag (ver.8)
OPTIONS YREV LITTLE_ENDIAN TEMPLATE
UNDEF  -999
XDEF    3600 LINEAR  0.05 0.1
YDEF    1200 LINEAR -59.95 0.1
ZDEF       1 LEVELS 1013
TDEF   87600 LINEAR 00Z1dec2021 1hr
VARS    1
sat    0  -1,40,4   satellite information flag
ENDVARS
