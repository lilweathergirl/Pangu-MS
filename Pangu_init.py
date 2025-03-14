#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:18:34 2024

@author: ennisk
"""

import xarray as xr
import numpy as np
import pandas as pd


# ---------------Init date/ time of initialization---------------------------
init_time = "2000-01-01T00"
init = pd.to_datetime(init_time, format="%Y-%m-%dT%H")


# ------------------Read in ARCO Cloud data set----------------------

ds = xr.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
    chunks=None,
    storage_options=dict(token="anon"),
)

plev0 = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]

# ========= Pangu surface variables =========#
vname_srf = [
    "mean_sea_level_pressure",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_temperature",
]


v_srf = ds[vname_srf].sel(time=init_time).to_array().to_numpy()
print(v_srf.shape)
# fname = "input_data/input_surface.npy"
fname = "input_data/input_surface_" + init.strftime("%Y%m%d%H") + ".npy"
print(f"Shape of v_srf before saving: {v_srf.shape}")
np.save(fname, v_srf)


# ========= Pangu variables on pressure levels ===========#
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