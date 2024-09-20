#!/usr/bin/env python
# coding: utf-8

# ## code to take pangu-weather output, process it, and put it into zarr

# In[1]:


import xarray as xr
import numpy as np
import pandas as pd

from metpy.units import units
import metpy.calc as mpcalc

import os
import sys


### model init time
#init = pd.Timestamp(2022,12,20,0)
init_in = sys.argv[1]
#init_in = "2024071812"

init = pd.to_datetime(init_in, format="%Y%m%d%H")
print(init)

output_data_dir = sys.argv[2]
output_zarr_dir = sys.argv[3]

step = int(sys.argv[4])
n_steps = int(sys.argv[5])
#step = 6  ### timestep in hours used for pangu forecast
#n_steps = 29  ### number of timesteps in forecast

### define lats and lons
lats = np.arange(90,-90.25,-0.25)
lons = np.arange(0,360,0.25)

levs = [1000,925,850,700,600,500,400,300,250,200,150,100,50]  ### pressure levels in hPa


# ### read surface data
for tt in range(0,n_steps):

    print("time: "+str(tt))

 #### original pangu code writes out the first forward timestep as index 0 which is confusing. I modified the inference code to write out the initial condition as index 0, then first forward step is 1.
    vtime = init + pd.Timedelta(hours=tt*step)
    vtime = pd.date_range(start=vtime,end=vtime,freq='h')  ### this needs to be in an array rather than a single value

    pangu_sfc_arr = np.load(output_data_dir+"/"+init.strftime("%Y%m%d%H")+"/output_surface_"+str(tt)+".npy")

    mslp = pangu_sfc_arr[0,:,:]
    u10 = pangu_sfc_arr[1,:,:]
    v10 = pangu_sfc_arr[2,:,:]
    t2m = pangu_sfc_arr[3,:,:]
    
    ### establish an xarray dataset 
    ds = xr.Dataset(data_vars=dict(
                mslp=(["valid_time","lat","lon"], np.expand_dims(mslp, axis=0)),
                u10=(["valid_time","lat","lon"], np.expand_dims(u10, axis=0)),
                v10=(["valid_time","lat","lon"], np.expand_dims(v10, axis=0)),
                t2m=(["valid_time","lat","lon"], np.expand_dims(t2m, axis=0)),
            ),
            coords=dict(
                valid_time=("valid_time",vtime),
                lon=("lon", lons),
                lat=("lat", lats),
                init=init,
            ),
        )

### add some attributes
    ### set a few attributes
    ds.attrs['description'] = "Pangu-Weather forecast model output"
    ds.attrs['source'] = "Russ Schumacher, Colorado State University. Original Pangu-Weather code described in Bi et al. (2023, Nature) and obtained from https://github.com/198808xc/Pangu-Weather"
    ds.t2m.attrs['long_name'] = "temperature at 2m AGL"
    ds.t2m.attrs['units'] = "K"
    ds.u10.attrs['long_name'] = "u-wind component"
    ds.u10.attrs['units'] = "m/s"
    ds.v10.attrs['long_name'] = "v-wind component"
    ds.v10.attrs['units'] = "m/s"
    ds.mslp.attrs['long_name'] = "mean sea level pressure"
    ds.mslp.attrs['units'] = "Pa"
    ds.lon.attrs['long_name'] = "longitude"
    ds.lon.attrs['standard_name'] = "longitude"
    ds.lon.attrs['units'] = "degrees_east"
    ds.lat.attrs['long_name'] = "latitude"
    ds.lat.attrs['standard_name'] = "latitude"
    ds.lat.attrs['units'] = "degrees_north"
    ds.valid_time.encoding['dtype'] = 'float64'
    
    ### put these into a zarr... 
    os.system("mkdir -p "+output_zarr_dir+"/"+init.strftime("%Y%m%d%H"))
    if tt==0:   ## start the zarr at first time, otherwise append
        ds.to_zarr(output_zarr_dir+"/"+init.strftime("%Y%m%d%H")+"/pangu_sfc.zarr",
                       mode='w')
    else:  
        ds.to_zarr(output_zarr_dir+"/"+init.strftime("%Y%m%d%H")+"/pangu_sfc.zarr",
                       append_dim='valid_time')

del ds, pangu_sfc_arr


# ### and upper-level data
for tt in range(0,n_steps):

    print("time: "+str(tt))

    vtime = init + pd.Timedelta(hours=tt*step)
    vtime = pd.date_range(start=vtime,end=vtime,freq='h')  ### this needs to be in an array rather than a single value

    pangu_upper_arr = np.load(output_data_dir+"/"+init.strftime("%Y%m%d%H")+"/output_upper_"+str(tt)+".npy")

    z = pangu_upper_arr[0,:,:]
    q = pangu_upper_arr[1,:,:]
    t = pangu_upper_arr[2,:,:]
    u = pangu_upper_arr[3,:,:]
    v = pangu_upper_arr[4,:,:]
    
    ### establish an xarray dataset 
    ds = xr.Dataset(data_vars=dict(
                z=(["valid_time","lev","lat","lon"], np.expand_dims(z, axis=0)),
                q=(["valid_time","lev","lat","lon"], np.expand_dims(q, axis=0)),
                t=(["valid_time","lev","lat","lon"], np.expand_dims(t, axis=0)),
                u=(["valid_time","lev","lat","lon"], np.expand_dims(u, axis=0)),
                v=(["valid_time","lev","lat","lon"], np.expand_dims(v, axis=0)),
            ),
            coords=dict(
                valid_time=("valid_time",vtime),
                lon=("lon", lons),
                lat=("lat", lats),
                lev=("lev", levs),
                init=init,
            ),
                        )

### add some attributes
    ### set a few attributes
    ds.attrs['description'] = "Pangu-Weather forecast model output"
    ds.attrs['source'] = "Russ Schumacher, Colorado State University. Original Pangu-Weather code described in Bi et al. (2023, Nature) and obtained from https://github.com/198808xc/Pangu-Weather"
    ds.t.attrs['long_name'] = "temperature on isobaric levels"
    ds.t.attrs['units'] = "K"
    ds.u.attrs['long_name'] = "u-wind component on isobaric levels"
    ds.u.attrs['units'] = "m/s"
    ds.v.attrs['long_name'] = "v-wind component on isobaric levels"
    ds.v.attrs['units'] = "m/s"
    ds.q.attrs['long_name'] = "specific humidity on isobaric levels"
    ds.q.attrs['units'] = "kg/kg"
    ds.z.attrs['long_name'] = "geopotential"
    ds.z.attrs['units'] = 'm**2 s**-2'
    ds.lev.attrs['long_name'] = "isobaric level"
    ds.lev.attrs['units'] = "hPa"
    ds.lon.attrs['long_name'] = "longitude"
    ds.lon.attrs['standard_name'] = "longitude"
    ds.lon.attrs['units'] = "degrees_east"
    ds.lat.attrs['long_name'] = "latitude"
    ds.lat.attrs['standard_name'] = "latitude"
    ds.lat.attrs['units'] = "degrees_north"
    ds.valid_time.encoding['dtype'] = 'float64'
    
    ### put these into a zarr... 
    os.system("mkdir -p "+output_zarr_dir+"/"+init.strftime("%Y%m%d%H"))
    if tt==0:   ## start the zarr at first time, otherwise append
        ds.to_zarr(output_zarr_dir+"/"+init.strftime("%Y%m%d%H")+"/pangu_upper.zarr",
                       mode='w')
    else:  
        ds.to_zarr(output_zarr_dir+"/"+init.strftime("%Y%m%d%H")+"/pangu_upper.zarr",
                       append_dim='valid_time')


