*
* GrADS control file for GSMaP_NRT Observation Time Flag (ver.8)
*
* Flag indicates relative time of latest microwave radiomerter
* observation at each pixel (see details in DataFormatDesctiption_MVK_v8.0000.pdf).
* Positive value indicates microwave sensor observation during current
* one-hour period.
*
DSET   ^gsmap_mvk.%y4%m2%d2.%h200.v8.0000.0.timeinfo.dat
TITLE  GSMaP_MVK 0.1deg Hourly Observation Time Flag (ver.8)
OPTIONS YREV LITTLE_ENDIAN TEMPLATE
UNDEF  -999.0
XDEF    3600 LINEAR  0.05 0.1
YDEF    1200 LINEAR -59.95 0.1
ZDEF       1 LEVELS 1013
TDEF   87600 LINEAR 00Z1dec2021 1hr
VARS    1
time    0  99   observation time flag
ENDVARS
