#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:07:43 2024

@author: ennisk
"""

import os
import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
import xarray as xr
import netCDF4 as nc


# Init date/ time of initialization
init_time = "2000-01-01T00"
init = pd.to_datetime(init_time, format="%Y-%m-%dT%H")
# ------------------------------------------

# The directory of your input and output data
input_data_dir = "/home/ennisk/AI_Models/Pangu/input_data/"
output_data_dir = "/home/ennisk/AI_Models/Pangu/output_data/"
model_24 = onnx.load("pangu_weather_24.onnx")
model_6 = onnx.load("pangu_weather_6.onnx")

# Set the behavier of onnxruntime
options = ort.SessionOptions()
options.enable_cpu_mem_arena = False
options.enable_mem_pattern = False
options.enable_mem_reuse = False
# Increase the number for faster inference and more memory consumption
options.intra_op_num_threads = 1

# Set the behavier of cuda provider
cuda_provider_options = {
    "arena_extend_strategy": "kSameAsRequested",
}

# Initialize onnxruntime session for Pangu-Weather Models
ort_session_24 = ort.InferenceSession(
    "pangu_weather_24.onnx",
    sess_options=options,
    providers=[("CUDAExecutionProvider", cuda_provider_options)],
)
print("ONNX Model Inputs:")
for input_meta in ort_session_24.get_inputs():
    print(f"Expected shape for 'input_surface': {input_meta.shape}")

ort_session_6 = ort.InferenceSession(
    "pangu_weather_6.onnx",
    sess_options=options,
    providers=[("CUDAExecutionProvider", cuda_provider_options)],
)

# Load the upper-air numpy arrays
input = np.load(input_data_dir + "input_upper_" + init.strftime("%Y%m%d%H") + ".npy").astype(np.float32)
# Load the surface numpy arrays
input_surface = np.load(input_data_dir + "input_surface_" + init.strftime("%Y%m%d%H") + ".npy").astype(np.float32)

def save_netcdf(output_data_dir, init, data, i):
    latitudes = np.linspace(90, -90, data.shape[0])
    longitudes = np.linspace(0, 359.75, data.shape[1])
    surface_da = xr.DataArray(
        data,
       dims=["lat", "lon"],
       coords={
           "lat": latitudes,
           "lon": longitudes,
       },
       name="2m_temperature",
   )
    # Convert DataArray to Dataset
    ds = xr.Dataset({"2m_temperature": surface_da})
    # Save as NetCDF
    ds.to_netcdf(
        os.path.join(output_data_dir, f"output_2m_temp_{i}.nc"))
    
save_steps = [1,2,3,4,5, 6, 7, 8, 10, 9, 11, 12, 13, 14,15, 16, 17, 18, 19,20]

# Run the inference session for 24-hour increments
input_24, input_surface_24 = input, input_surface

for i in range(21):
    # saving steps in different files for easier usage of the files/ averaging them
    #also makes it easier to make sure i have the appropriate files/dates/times for averaging
    
    #First is 24-h
    if i in save_steps:
        output, output_surface = ort_session_24.run(None, {'input':input_24, 'input_surface':input_surface_24})
        input_24, input_surface_24 = output, output_surface
    #Next is 6-h
    #We run the 6-h mainly in this project. 
    else:
        output, output_surface = ort_session_6.run(None, {'input':input, 'input_surface':input_surface})
        input, input_surface = output, output_surface

    temperature = output_surface[3,:,:] #saving only 2m-temperature not all sfc variables

    save_netcdf(output_data_dir, init, temperature, f"output_data{i}")
        
    #