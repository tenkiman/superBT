*
* GrADS control file for GSMaP_MVK Reliability Flag
*
* Reliability flag information is assigned to 1 byte integer
* (see details in DataFormDesctiption.pdf).
*
DSET   ^gsmap_mvk.%y4%m2%d2.%h200.v8.0000.0.reliability.dat
TITLE   GSMaP_MVK 0.1deg Hourly Reliability Flag (ver.8)
UNDEF   -1.0
OPTIONS YREV LITTLE_ENDIAN TEMPLATE
XDEF   3600  LINEAR  0.05  0.1
YDEF   1200  LINEAR  -59.95 0.1
zdef   1 levels 1000
TDEF   87600 LINEAR 00Z1dec2021 1hr
VARS     1
rel        0 -1,40,1    reliability flag (1-10)
ENDVARS
