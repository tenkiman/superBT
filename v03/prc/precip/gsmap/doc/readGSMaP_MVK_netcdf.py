import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

# in case of netCDF
import netCDF4
nc=netCDF4.Dataset('gsmap_mvk.19980101.0000.v8.0000.0.nc','r')
Lon=nc.variables['Longitude'][:]
Lat=nc.variables['Latitude'][:]
hprecipRateGC=nc.variables['hourlyPrecipRateGC'][0,:,:]
nc.close()

#plot with Matplotlib
fig=plt.figure(figsize=(20,20))
# set the color interval
interval=list(np.arange(1,30,1)) 
interval.insert(0,0.1)
#set colormap
cmap=cm.jet
cmap.set_under('w', alpha=0)

#set map
m=Basemap(projection='cyl',
         resolution='c',
         llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
m.drawcoastlines(color='black')
m.drawmeridians(np.arange(0,360,30))
m.drawparallels(np.arange(-90,90,30))
x,y=m(Lon, Lat) #compute map projection
im=plt.contourf(x,y,hprecipRateGC, interval, cmap=cmap, latlon=True) 
# set colorbar
cb=m.colorbar(im, "right", size="2.5%")

plt.show()
plt.close()
