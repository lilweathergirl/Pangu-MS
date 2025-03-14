#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 08:29:09 2025

@author: ennisk
"""

## This code plots the spatial temperature distribution error for both models over the selected NCA regions
## in this project. The files that are read in contain all 60 heatwaves averaged for day 10 (day 1 of HW). 
## Each region has 16 heat waves with the exception of the Southeast which had 12 

import xarray as xr
import numpy as np  
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.ops import unary_union
import shapely.vectorized
import cartopy.io.shapereader as shpreader

# Defining states for each NCA region

MW_state_names = ['Ohio', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Indiana', 'Illinois', 'Missouri']
NW_state_names = ['Washington', 'Oregon', 'Idaho']
SE_state_names = ['Florida', 'Georgia', 'South Carolina', 'North Carolina', 'Alabama', 'Louisiana', 
                  'Mississippi', 'Arkansas', 'Tennessee', 'Kentucky', 'Virginia']
NE_state_names = ['Maine', 'Vermont', 'Massachusetts', 'New Hampshire', 'New York',
                  'Rhode Island', 'Connecticut', 'New Jersey', 'Delaware', 'Maryland',
                  'Pennsylvania', 'West Virginia']


all_state_names = set(MW_state_names + NW_state_names + SE_state_names + NE_state_names)

#extent over America
overall_extent = [-125, -66, 25, 50]

era5_file = '/Users/ennisk/anaconda3/ERA5/ERA5_60.nc'
ds_era5 = xr.open_dataset(era5_file)

#Select time index 10 from ERA data to ensure its subtracting the lead time 10 1avaeraged value
temp_era5 = ds_era5['2m_temperature'].isel(time=10) - 273.15

era5_lon = temp_era5.longitude.values
era5_lon_adjusted = np.where(era5_lon > 180, era5_lon - 360, era5_lon)
temp_era5 = temp_era5.assign_coords(longitude=era5_lon_adjusted)

temp_era5_region = temp_era5.where(
    (temp_era5.longitude >= overall_extent[0]) & (temp_era5.longitude <= overall_extent[1]) &
    (temp_era5.latitude  >= overall_extent[2]) & (temp_era5.latitude  <= overall_extent[3]),
    drop=True
)

#--------------------------

# Pangu forecast data: no time index because each pangu forecast file was separate so I only added all the
# lead time 10's and averaged them for each NCA region. 
pangu_file = '/Users/ennisk/anaconda3/Pangu/pangu_60.nc'
ds_pangu = xr.open_dataset(pangu_file)
temp_pangu = ds_pangu['2m_temperature'] - 273.15


pangu_lon = temp_pangu.lon.values
pangu_lon_adjusted = np.where(pangu_lon > 180, pangu_lon - 360, pangu_lon)
temp_pangu = temp_pangu.assign_coords(lon=pangu_lon_adjusted)

temp_pangu_interp = temp_pangu.interp(lon=temp_era5_region.longitude, lat=temp_era5_region.latitude)

temp_pangu_region = temp_pangu_interp.where(
    (temp_pangu_interp.lon >= overall_extent[0]) & (temp_pangu_interp.lon <= overall_extent[1]) &
    (temp_pangu_interp.lat >= overall_extent[2]) & (temp_pangu_interp.lat <= overall_extent[3]),
    drop=True
)

# Calculate error for lt 10
error_field = temp_pangu_region - temp_era5_region

## This next section ensures there are masks only over the selected NCA regions and bodies of water/ other 
## states are nulled out so that we can just focus on our chosen regions and analyze those patterns. 
shapefile_states = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
reader_states = shpreader.Reader(shapefile_states)

states_geoms = []
for record in reader_states.records():
    if record.attributes['admin'] == 'United States of America' and record.attributes['name'] in all_state_names:
        states_geoms.append(record.geometry)

if not states_geoms:
    raise ValueError("No states found for the provided state names.")

states_union = unary_union(states_geoms)

lons = error_field.lon.values
lats = error_field.lat.values
lon2d, lat2d = np.meshgrid(lons, lats)

mask_states = shapely.vectorized.contains(states_union, lon2d, lat2d)

lakes_shapefile = shpreader.natural_earth(resolution='10m', category='physical', name='lakes')
reader_lakes = shpreader.Reader(lakes_shapefile)
great_lake_names = {"Lake Superior", "Lake Michigan", "Lake Huron", "Lake Erie", "Lake Ontario"}
lakes_geoms = []
for record in reader_lakes.records():
    if record.attributes['name'] in great_lake_names:
        lakes_geoms.append(record.geometry)

if not lakes_geoms:
    raise ValueError("No Great Lakes found in the shapefile.")

great_lakes_union = unary_union(lakes_geoms)
mask_great_lakes = shapely.vectorized.contains(great_lakes_union, lon2d, lat2d)
final_mask = mask_states & (~mask_great_lakes)

error_field_masked = error_field.where(final_mask)

#Plotting the figure
plt.figure(figsize=(16, 9))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(overall_extent, crs=ccrs.PlateCarree())

ax.add_feature(cfeature.OCEAN, facecolor='lightgray')
ax.set_facecolor('lightgray')
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')
ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')

#Colour bar error 
error_min, error_max = -10, 10
error_bins = np.linspace(error_min, error_max, 50)

error_plot = error_field_masked.plot.contourf(
    ax=ax, cmap='RdBu_r', extend='both', levels=error_bins,
    add_colorbar=False, transform=ccrs.PlateCarree()
)

cbar = plt.colorbar(error_plot, ax=ax, orientation='vertical', pad=0.03, shrink=0.80)
cbar.set_ticks(np.linspace(error_min, error_max, 5))
cbar.set_label('Temperature Error (°C)', fontsize=25, labelpad=5)
cbar.ax.tick_params(labelsize=20)

ax.set_title('Pangu Forecast 2m Temperature Error: All Heat waves', fontsize=20)
#plt.savefig('/Users/ennisk/anaconda3/Data Driven Figures/Error_All_Regions_pangu60.png', dpi=850)
plt.tight_layout()
plt.show()
