from metpy.cbook import get_test_data
import xarray as xr
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import os
import matplotlib.dates as mdates
import glob
from netCDF4 import Dataset as nc
import seaborn as sns
from wrf import getvar, ALL_TIMES, geo_bounds
import pandas as pd
time=pd.date_range(start='23-11-2020 18:00', end='25-11-2020 10:00',periods=81)
#==============================================================================================================
#Pecs station observational data
df = pd.read_excel('2020_11__Pecs.xlsx', sheet_name="wrf", header=0)#, names=None, index_col=None, usecols=None, squeeze=False, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, parse_dates=False, date_parser=None, thousands=None, comment=None, skipfooter=0, convert_float=None, mangle_dupe_cols=True, storage_options=None)
# print(df.head())
df = df.replace('nincsadat', '')
time1=pd.date_range(start='23-11-2020 18:00', end='25-11-2020 10:00',freq='min')
df['Date UTC'] = df['Date UTC'].str.extract(r'(\d+)', expand=False)
# print(time)
ta=pd.to_numeric(df['Ta'])#.astype(int)
td=pd.to_numeric(df['Td'])#.astype(int)
# print(len(td))
for i in range(len(td)):
    if td[i]<-2:
        td[i]=td[i+3]
df['Rh']=pd.to_numeric(df['Rh'])#.astype(int)
#==============================================================================================================
# ACM2 PBL
acm2 = sorted(glob.glob("ACM/wrfout_d01_*"), key=os.path.getmtime)
# acm2 = glob("ACM/wrfout_d01_*")
acm = [nc(x) for x in acm2]
acm_t2 = getvar(acm, "tc", timeidx=ALL_TIMES)
#time=getvar(ncfiles,"times")
#print(time)
acm_t2 = acm_t2.isel(south_north=168).sel(west_east=133).sel(bottom_top=1)

#==============================================================================================================
# MYJ
myj3 = sorted(glob.glob("MYJ/wrfout_d01_*"), key=os.path.getmtime)
myj = [nc(x) for x in myj3]
myj_t2 = getvar(myj, "tc", timeidx=ALL_TIMES)
#time=getvar(ncfiles,"times")
#print(time)
myj_t2 = myj_t2.isel(south_north=168).sel(west_east=133).sel(bottom_top=1)

#==============================================================================================================
# MYNN 3
myn3 = sorted(glob.glob("MYNN3/wrfout_d01_*"), key=os.path.getmtime)
myn = [nc(x) for x in myn3]
myn_t2 = getvar(myn, "tc", timeidx=ALL_TIMES)
myn_t2 = myn_t2.isel(south_north=168).sel(west_east=133).sel(bottom_top=1)

#==============================================================================================================
# YSU
YSU2 = sorted(glob.glob("YSU/wrfout_d01_*"), key=os.path.getmtime)
ysu = [nc(x) for x in YSU2]
ysu_t2 = getvar(ysu, "tc", timeidx=ALL_TIMES)
ysu_t2 = ysu_t2.isel(south_north=168).sel(west_east=133).sel(bottom_top=1)

#==============================================================================================================
# YSU
qnse2 = sorted(glob.glob("QNSE/wrfout_d01_*"), key=os.path.getmtime)
qnse = [nc(x) for x in qnse2]
qnse_t2 = getvar(qnse, "tc", timeidx=ALL_TIMES)
qnse_t2 = qnse_t2.isel(south_north=168).sel(west_east=133).sel(bottom_top=1)

sns.set_theme()

#print(t2)
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(time1,ta)#, len(z))
ax.plot(time,acm_t2)#, len(z))
ax.plot(time,ysu_t2)
ax.plot(time,myj_t2)
ax.plot(time,myn_t2)
ax.plot(time,qnse_t2)
ax.grid()
ax.set_xlabel('Time',fontsize=12)
ax.set_ylabel('Temp (k)', fontsize=12)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
xfmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(xfmt)
plt.title("Temperature at 2 meter",loc='left')
plt.title("Lon = 46.07, Lat = 18.20",loc='right')

ax.legend(["OBS","ACM2","YSU","MYNN3","MYJ","QNSE"])

# ax.fontsize=20
ax.grid()

#plt.xticks(rotation='20')
#plt.ylim(0,1000)
#plt.xlim(270, 280)
fig.savefig("Temp_timeseries_Pecs.png",dpi=240)
plt.show()
