#!/usr/bin/env python
# coding: utf-8

# ## code to preprocess ERA5 data to use as initial conditions for pangu-weather

import xarray as xr
import numpy as np
import pandas as pd
import cdsapi
import sys

# ### set desired time

### this is the original time provided with pangu
#eratime = pd.Timestamp(2018,9,27,12)
####

eratime_in = sys.argv[1]

eratime = pd.to_datetime(eratime_in, format="%Y%m%d%H")

print(eratime)


# ### get upper-level vars

URL = 'https://cds-beta.climate.copernicus.eu/api'
KEY = 'your-key-here'

client = cdsapi.Client(url=URL, key=KEY)

dataset = 'reanalysis-era5-pressure-levels'
request = {
  'product_type': ['reanalysis'],
    'variable': [
        'geopotential', 'specific_humidity', 'temperature',
        'u_component_of_wind', 'v_component_of_wind',
    ],
  'year': [eratime.strftime("%Y")],
  'month': [eratime.strftime("%m")],
  'day': [eratime.strftime("%d")],
  'time': [eratime.strftime("%H:%M")],
    'pressure_level': [
        '1000','925','850','700','600','500',
        '400','300','250','200','150','100','50',
    ],
  'data_format': 'grib',
}
target = "era5/era5_upper_"+eratime.strftime("%Y%m%d%H")+".grib"

client.retrieve(dataset, request, target)


# ### and surface vars

client = cdsapi.Client(url=URL, key=KEY)

dataset = "reanalysis-era5-single-levels"
request = {
  'product_type': ['reanalysis'],
    'variable': ['mean_sea_level_pressure',
                 '10m_u_component_of_wind', '10m_v_component_of_wind', 
                 '2m_temperature', ],
  'year': [eratime.strftime("%Y")],
  'month': [eratime.strftime("%m")],
  'day': [eratime.strftime("%d")],
  'time': [eratime.strftime("%H:%M")],
  'data_format': 'grib',
}
target = "era5/era5_sfc_"+eratime.strftime("%Y%m%d%H")+".grib"

client.retrieve(dataset, request, target)


# ### now read one of these in

era5_sfc = xr.open_dataset("era5/era5_sfc_"+eratime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='')

era5_upper = xr.open_dataset("era5/era5_upper_"+eratime.strftime("%Y%m%d%H")+".grib", engine='cfgrib',
                              indexpath='')


# ### stack the variables into the proper shape

sfc_npy = np.stack((era5_sfc.msl.to_numpy(),
               era5_sfc.u10.to_numpy(),
               era5_sfc.v10.to_numpy(),
               era5_sfc.t2m.to_numpy()), axis=0)

np.save("input_data/input_surface_era5_"+eratime.strftime("%Y%m%d%H")+".npy", sfc_npy)

upper_npy = np.stack((era5_upper.z.to_numpy(),
                      era5_upper.q.to_numpy(),
                      era5_upper.t.to_numpy(),
                      era5_upper.u.to_numpy(),
                      era5_upper.v.to_numpy()), axis=0)

np.save("input_data/input_upper_era5_"+eratime.strftime("%Y%m%d%H")+".npy", upper_npy)


