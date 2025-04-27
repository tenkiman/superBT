README.first (GSMaP_MVK & GSMaP_Gauge Ver.8)


********************************************************************************
* Documents
********************************************************************************
Readme (this file):     /standard/v8/README.first.txt
Version up history:     /standard/v8/GSMaP_MVK_RNL_HISTORY.txt
Caveat for algorithm:   /standard/v8/doc/CaveatForUseOfGPM-GSMaP_Ver.8.pdf
Data Format Document:   /standard/v8/doc/DataFormatDescription_MVK_RNL_v8.0000.pdf
User's Guide:           /standard/v8/doc/USERS_GUIDE_MVK_RNL_v8.0000.pdf


********************************************************************************
* Archive Period and Products
********************************************************************************
Since January 1, 1998
    Global Satellite Mapping of Precipitation Microwave-IR Combined Product (GSMaP_MVK) 
    Gauge-calibrated Rainfall Product (GSMaP_Gauge)


********************************************************************************
* Data Directory (ver.8) and File Naming Rule
********************************************************************************
Hourly Rain Rate data;
    Directory:  /standard/v8/hourly/YYYY/MM/DD/
    File Name:  gsmap_mvk.YYYYMMDD.HHNN.vP.RSKI.J.dat.gz (GSMaP_MVK)

Hourly Gauge-calibrated Rain Rate data;
    File Name:  gsmap_gauge.YYYYMMDD.HHNN.vP.RSKI.J.dat.gz (GSMaP_Gauge)
	
Satellite Information Flag;
    Directory:  /standard/v8/sateinfo/YYYY/MM/DD/
    File Name:  gsmap_mvk.YYYYMMDD.HHNN.vP.RSKI.J.sateinfo.dat.gz (GSMaP_MVK)

Observation Time Flag;
    Directory:  /standard/v8/timeinfo/YYYY/MM/DD/
    File Name:  gsmap_mvk.YYYYMMDD.HHNN.vP.RSKI.J.timeinfo.dat.gz (GSMaP_MVK)

Reliability Flag;
    Directory:  /standard/v8/reliability/YYYY/MM/DD/
    File Name:  gsmap_mvk.YYYYMMDD.HHNN.vP.RSKI.J.reliability.dat.gz (GSMaP_MVK)

Hourly Rain Rate & major flag in NetCDF;
    Directory:  /standard/v8/netcdf/YYYY/MM/DD/
    File Name:  gsmap_mvk.YYYYMMDD.HHNN.vP.RSKI.J.nc

Hourly Rain Rate & major flag in HDF;
    Directory:  /HDF/standard/v8/Hourly/YYYY/MM/DD/
    File Name:  GPMMRG_MAP_YYMMDDHHNN_H_L3S_MCH_VVV.h5

Daily Averaged Rain Data (00Z-23Z averaged); 
    Directory:  /standard/v8/daily/00Z-23Z/YYYYMM/
    File Name:  gsmap_mvk.YYYYMMDD.0.1d.daily.00Z-23Z.vP.RSKI.J.dat.gz (GSMaP_MVK)

Daily Averaged Rain Data (p12Z-11Z averaged); 
    Directory:  /standard/v8/daily/p12Z-11Z/YYYYMM/
    File Name:  gsmap_mvk.YYYYMMDD.0.1d.daily.p12Z-11Z.vP.RSKI.J.dat.gz (GSMaP_MVK)

Daily Averaged Gauge-calibrated Rain Data (00Z-23Z averaged);
    Directory:  /standard/v8/daily_G/00Z-23Z/YYYYMM/
    File Name:  gsmap_gauge.YYYYMMDD.0.1d.daily.00Z-23Z.vP.RSKI.J.dat.gz (GSMaP_Gauge)

Daily Averaged Gauge-calibrated Rain Data (p12Z-11Z averaged); 
    Directory:  /standard/v8/daily_G/p12Z-11Z/YYYYMM/
    File Name:  gsmap_gauge.YYYYMMDD.0.1d.daily.p12Z-11Z.vP.RSKI.J.dat.gz (GSMaP_Gauge)

Hourly Rain & Gauge-calibrated Rain Data in Text Format; 
    Directory:  /standard/v8/txt/hourly/XX_ZZZZZZ/YYYY/MM/DD/
    File Name:  gsmap_mvk_vPRSKIJ_YYYYMMDD_HH00_XX_ZZZZZZ.csv.zip (GSMaP_MVK & GSMaP_Gauge)

Daily Averaged Rain & Gauge-calibrated Rain Data in Text Format (00Z-23Z averaged); 
    Directory:  /standard/v8/txt/daily/00Z-23Z/XX_ZZZZZZ/YYYY/MM/
    File Name:  gsmap_mvk_vPRSKIJ_YYYYMMDD_daily_00Z-23Z_XX_ZZZZZZ.csv.zip (GSMaP_MVK & GSMaP_Gauge)

Daily Averaged Rain & Gauge-calibrated Rain Data in Text Format (p12Z-11Z averaged); 
    Directory:  /standard/v8/txt/daily/p12Z-11Z/XX_ZZZZZZ/YYYY/MM/
    File Name:  gsmap_mvk_vPRSKIJ_YYYYMMDD_daily_p12Z-11Z_XX_ZZZZZZ.csv.zip (GSMaP_MVK & GSMaP_Gauge)

Daily Averaged Rain & major flag in HDF;
    Directory:  /HDF/standard/v8/Daily/YYYY/MM
    File Name:  GPMMRG_MAP_YYMMDD_D_L3S_MCD_VVV.h5

Monthly Averaged Rain Data;
    Directory:  /standard/v8/monthly/YYYY/
    File Name:  gsmap_mvk.YYYYMM.0.1d.monthly.vP.RSKI.J.dat.gz (GSMaP_MVK)

Monthly Averaged Gauge-calibrated Rain Data;
    Directory:  /standard/v8/monthly_G/YYYY/
    File Name:  gsmap_gauge.YYYYMM.0.1d.monthly.vP.RSKI.J.dat.gz (GSMaP_Gauge)

Monthly Averaged Rain & Gauge-calibrated Rain Data in Text Format; 
    Directory:  /standard/v8/txt/monthly/XX_ZZZZZZ/YYYY/
    File Name:  gsmap_mvk_vPRSKIJ_YYYYMM_monthly_XX_ZZZZZZ.csv.zip (GSMaP_MVK & GSMaP_Gauge)

Monthly Averaged Rain & major flag in HDF;
    Directory:  /HDF/standard/v8/Monthly/YYYY
    File Name:  GPMMRG_MAP_YYMM_M_L3S_MCM_VVV.h5


where,

YYYY:   4-digit year
YY:     2-digit year
MM:     2-digit month
DD:     2-digit day
HH:     2-digit hour
NN:     2-digit minute (currently fixed as 00)
P:      Algorithm version
R:      Version of microwave imager algorithm (reset when P is updated)
S:      Version of microwave sounder algorithm (reset when P is updated)
K:      Version of microwave imager/sounder algorithm (reset when P is updated)
I:      Version of microwave-IR combined algorithm
J:      Inclement number of reprocessing
XX_ZZZZZZ: 	9-digit area name
VVV:    3-digit product version.

********************************************************************************
* Sample code
********************************************************************************

Directory:              /standard/v8/sample/

Fortran Sample Code:    read_GSMaP_MVK_0.1deg.v8.f

IDL Sample Code:        GSMaP_MVK_sample.v8.pro

Python sample code:     readGSMaP_MVK_netcdf.py

GrADS Control File:
    Hourly Rainfall Data            GSMaP_MVK.hourly.rain.v8.ctl
    Satellite Information Flag      GSMaP_MVK.hourly.sat.v8.ctl
    Observation Time Flag           GSMaP_MVK.hourly.time.v8.ctl
    Reliability Flag                GSMaP_MVK.hourly.reliability.v8.ctl
    Daily (00Z-23Z avaraged)        GSMaP_MVK.daily.00Z-23Z.v8.ctl
    Daily (p12Z-11Z averaged)       GSMaP_MVK.daily.p12Z-11Z.v8.ctl
    Monthly                         GSMaP_MVK.monthly.v8.ctl

********************************************************************************

