import xarray as xr
import numpy as np
import pandas as pd

# ------------------------------------------
init_time = "2020-01-01T18"
init = pd.to_datetime(init_time, format="%Y-%m-%dT%H")
# ------------------------------------------

ds = xr.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
    chunks=None,
    storage_options=dict(token="anon"),
)

plev0 = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]

# ========= surface =========#
vname_srf = [
    "mean_sea_level_pressure",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_temperature",
]

v_srf = ds[vname_srf].sel(time=init_time).to_array().to_numpy()

# fname = "input_data/input_surface.npy"
fname = "input_data/input_surface_" + init.strftime("%Y%m%d%H") + ".npy"
np.save(fname, v_srf)

# ========= upper ===========#
vname_upper = [
    "geopotential",
    "specific_humidity",
    "temperature",
    "u_component_of_wind",
    "v_component_of_wind",
]

v_upper = ds[vname_upper].sel(time=init_time, level=plev0).to_array().to_numpy()

fname = "input_data/input_upper_" + init.strftime("%Y%m%d%H") + ".npy"
np.save(fname, v_upper)
