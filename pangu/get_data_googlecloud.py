import xarray as xr
import numpy as np

ds = xr.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
    chunks=None,
    storage_options=dict(token="anon"),
)

time0 = "2020-01-01T18:00:00"  # hourly data
plev0 = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]

# ========= surface =========#
vname_srf = [
    "mean_sea_level_pressure",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_temperature",
]

v_srf = ds[vname_srf].sel(time=time0).to_array().to_numpy()

fname = "input_data/input_surface.npy"
np.save(fname, v_srf)
# ========= upper ===========#
vname_upper = [
    "geopotential",
    "specific_humidity",
    "temperature",
    "u_component_of_wind",
    "v_component_of_wind",
]

v_upper = ds[vname_upper].sel(time=time0, level=plev0).to_array().to_numpy()

fname = "input_data/input_upper.npy"
np.save(fname, v_upper)
