#!/usr/bin/env python
# coding: utf-8

# ## code to preprocess ERA5 data to use as initial conditions for pangu-weather

import xarray as xr
import numpy as np
import pandas as pd
import sys

from ecmwf.opendata import Client

# ### set desired time

### this is the original time provided with pangu
#ectime = pd.Timestamp(2018,9,27,12)
####

ectime_in = sys.argv[1]
#ectime = pd.Timestamp(2022,12,20,0)

ectime = pd.to_datetime(ectime_in, format="%Y%m%d%H")

print(ectime)

# ### get upper-level vars
client = Client(source="azure")  ### source can also be 'azure'

client.retrieve(
        date=ectime.strftime("%Y-%m-%d"),
        time=ectime.strftime("%H"),
        step="0",
        stream="oper",
        levtype="pl",
        param=['gh','q','t','u','v'],
        levelist = [
        '1000','925','850','700','600','500',
        '400','300','250','200','150','100','50',
    ],
        target="ecmwf/ecmwf_hres_upper_"+ectime.strftime("%Y%m%d%H")+".grib"
    )

# ### and surface vars
client = Client("azure")

client.retrieve(
        date=ectime.strftime("%Y-%m-%d"),
        time=ectime.strftime("%H"),
        step="0",
        stream="oper",
        levtype="sfc",
        param=['msl','10u','10v','2t'],
        target="ecmwf/ecmwf_hres_sfc_"+ectime.strftime("%Y%m%d%H")+".grib"
    )


# ### now read in
ec_10m = xr.open_dataset("ecmwf/ecmwf_hres_sfc_"+ectime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='', 
                              filter_by_keys={'typeOfLevel': 'heightAboveGround', 'level':10})

### HRES lon order is -180 to 180; needs to be 0 to 360
### change lon order, doing the reverse of this: https://stackoverflow.com/questions/53345442/about-changing-longitude-array-from-0-360-to-180-to-180-with-python-xarray
ec_10m.coords['longitude'] = np.where(ec_10m.coords['longitude'] < 0, 
                                          ec_10m.coords['longitude']+360,
                                          ec_10m.coords['longitude'])
ec_10m = ec_10m.sortby(ec_10m.longitude)

### need to open separately bc of cfgrib
ec_t2m = xr.open_dataset("ecmwf/ecmwf_hres_sfc_"+ectime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='', 
                              filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '2t'})
ec_t2m.coords['longitude'] = np.where(ec_t2m.coords['longitude'] < 0, 
                                          ec_t2m.coords['longitude']+360,
                                          ec_t2m.coords['longitude'])
ec_t2m = ec_t2m.sortby(ec_t2m.longitude)

ec_msl = xr.open_dataset("ecmwf/ecmwf_hres_sfc_"+ectime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='',
                              filter_by_keys={'typeOfLevel': 'meanSea'})
ec_msl.coords['longitude'] = np.where(ec_msl.coords['longitude'] < 0, 
                                          ec_msl.coords['longitude']+360,
                                          ec_msl.coords['longitude'])
ec_msl = ec_msl.sortby(ec_msl.longitude)

### upper works normally
ec_upper = xr.open_dataset("ecmwf/ecmwf_hres_upper_"+ectime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='')
ec_upper.coords['longitude'] = np.where(ec_upper.coords['longitude'] < 0, 
                                          ec_upper.coords['longitude']+360,
                                          ec_upper.coords['longitude'])
ec_upper = ec_upper.sortby(ec_upper.longitude)


# ### stack the variables into the proper shape

sfc_npy = np.stack((ec_msl.msl.to_numpy(),
               ec_10m.u10.to_numpy(),
               ec_10m.v10.to_numpy(),
               ec_t2m.t2m.to_numpy()), axis=0)

np.save("input_data_rt/input_surface_ecmwf_hres_"+ectime.strftime("%Y%m%d%H")+".npy", sfc_npy)

upper_npy = np.stack(((ec_upper.gh*9.80665).to_numpy(),  ### hres comes as height, convert to geopotential
                      ec_upper.q.to_numpy(),
                      ec_upper.t.to_numpy(),
                      ec_upper.u.to_numpy(),
                      ec_upper.v.to_numpy()), axis=0)

np.save("input_data_rt/input_upper_ecmwf_hres_"+ectime.strftime("%Y%m%d%H")+".npy", upper_npy)


