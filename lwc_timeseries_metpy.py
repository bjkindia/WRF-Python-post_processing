#!/usr/bin/env python
# coding: utf-8

# In[1]:


from metpy.cbook import get_test_data
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import matplotlib.dates as mdates
from glob import glob
from netCDF4 import Dataset as nc
from wrf import getvar, ALL_TIMES, geo_bounds
import pandas as pd

pas  =  xr.open_dataset("YSU/wrfout_d01_2020-11-23_18:00:00")

ncfile = xr.open_mfdataset("MYNN3/wrfout_*", concat_dim='Time',combine = "nested",compat='no_conflicts',coords ="minimal") 
ncfile.XTIME


# In[3]:


ph = pas.metpy.parse_cf('PH')
phb = pas.metpy.parse_cf('PHB')
hgt = pas.metpy.parse_cf('HGT')
time = pas.metpy.parse_cf('XTIME')
z = ((ph+phb)/9.81)-hgt
z = z.isel(Time=0).isel(south_north=133).sel(west_east=168)
z=z.to_numpy()

time=pd.date_range(start='23-11-2020 18:00', end='25-11-2020 10:00',periods=81)
#vert=np.arange(16)
vert,time = np.meshgrid( z[0:16],time)

# # Get all the YSU files                                                                                                                  
# YSU_files = glob("MYNN3/wrfout_d01_**")
# ysufiles = [nc(x) for x in YSU_files]
# # LWC is the example variable and includes all times                                                                                            
# # ysu_lwc = getvar(ysufiles, "QNCLOUD", timeidx=ALL_TIMES)
ysu_lwc = ncfile.metpy.parse_cf('QCLOUD')
ysu_lwc = ysu_lwc.isel(south_north=133).sel(west_east=168)

ysu_lwc = ysu_lwc[:,0:16]
fig, ax = plt.subplots(figsize=(14, 8))


#mp1=ax.contourf(time[40:-1,:], vert[40:-1,:], ysu_lwc[40:-1,:],cmap='BuGn',levels=14)#, vmin=0, vmax=0.0004)
mp1=ax.contourf(time, vert, ysu_lwc,cmap='BuGn',levels=14)

cbar = fig.colorbar(mp1, ax=ax,shrink=0.8)
cbar.minorticks_on()
cbar.set_label('QCLOUD(kg/kg)',fontsize=12)
#plt.savefig("multi_QCLOUD.jpg",dpi=300)
fig.suptitle('Liquid Water Content (24-11-2020 06:00 UTC)',x=0.45, y=.95,fontsize=16)
# fig.suptitle('24-11-2020 06:00 UTC',x=0.75, y=.95,fontsize=10)#,loc='right')
plt.show()


#




