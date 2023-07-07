# superBT = a super Tropical Cyclone Best Track data set

       A super Best Track for Tropical Cyclone (TC) Forecasting and Research
       
				   20230707
				 Mike Fiorino
			       mfiorino@gmu.edu


What's a superBT?
=================

A super(position) of ancillary data to the final/post-season best tracks of
the operational US TC forecast agencies:

JTWC - Joint Typhoon Warning Center, Pearl Harbor HI
---- basins: western North Pacific (WPAC), Indian Ocean (IO), and southern Hemisphere (SHEM)
  
NHC  - National Hurricane Center, Miami FL
---- basins, central and eastern North Pacific (C/EPAC), and North Atlantic (LANT)

*** The superBT is global ***


Ancillary Data Sets
====================

1) operational information on both developing and non-developing pre/potential or pTCs
2) ECMWF ERA5 reanalysis 00/12 UTC 10-d forecasts
3) three near-global high-resolution in space and time precipitation analyses:
   a) NOAA CMORPH (US)
   b) JAXA GsMAP (Japan)
   c) NASA IMERG (US)
4) Wind Structure
   a) CIRA MTCSWA (US)


Version History:
================

V03 -- beta version 3
    a) 2007-2023 (the 2023 SHEM season started 1 July 2022)
    b) ERA5 TC forecasts (both TCs and pTCs)
    c) storm & environment variables from ERA5 on the track forecasts
    d) mean precip in the r=300,500,800 km areas for both the observed and forecast tracks
    e) direct calculation of the Radius of the Outer-most Closed Isobar (ROCI/POCI) from ERA5

V10 -- first release = V03 +
    a) 1999-2023
    b) radius of 34 kt winds (R34) from ERA5 and CIRA


Files:
=====

v03/doc/ -- docs
----------------

NB: under development

sbt-full-20230115.txt            -- initial doc
sbt-tccodes-subbasin-codes.txt   -- TC and basin codes


v03/dat/ -- data
----------------

sum-md3-2007-2023-MRG.csv    -- summary of each TC
h-meta-md3-sum-csv.txt       -- description of each column in sum-md3 file

all-md3-2007-2023-MRG.csv    -- best track + extra operational information
h-meta-md3-vars-csv.txt      -- description of each column in all-md3 file

sbt-v03-2007-2023-MRG.csv    -- the superBT 
h-meta-sbt-v03-vars-csv.txt  -- description of each column in sbt-v03 file

v03/prc/ -- processing (python2 but easily converted to py3)
------------------------------------------------------------

checking code:
c-9xtime-time2gen.py
c-md3-nn-9x.py
c-stm-dir-sum.py

processing code:
p-md3-ls.py        -- a storm listing utility
p-md3-stm-anl.py
p-sbt-v03-anl.py

vars/methods/classes:
sBT.py

