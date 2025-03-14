#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:01:06 2025

@author: ennisk
"""

import matplotlib.pyplot as plt
import numpy as np

save_directory = '/Users/ennisk/anaconda3/Data Driven Figures/case study sept 2019/'


## Case Study PCNW September 2019 Pangu 6-hour model vs Pangu 24-hr model
## These values were done both in python & saved and read in by a netcdf file 
## But these values were also calculated by hand to make sure the code  saving 
## the averages to one netcdf was working properly

## This code I am posting is this is the by hand calculations of the values for transparency
## The other way to do it is just by reading in a file and doing the calculations through a loop
## on python and saving that daily average
## Both of these methods worked and yielded the same result which was great!

## This code features data that is in the supplemental part of the Journal paper.

pangu_data = {
    "Pangu 6-h 06z": [
        20.96, 15.73, 19.56, 17.87, 22.67, 17.23, 17.28, 19.78, 24.66, 20.78,
        20.59, 15.67, 18.81, 19.79, 16.78, 13.51, 18.21, 18.81, 22.54, 16.28
    ],
    "Pangu 6-h 12z": [
        21.46, 17.87, 20.78, 18.04, 24.08, 21.66, 19.76, 21.44, 25.01, 23.20,
        21.12, 17.39, 19.60, 20.50, 19.21, 14.01, 19.25, 19.66, 23.06, 17.79
    ],
    "Pangu 6-h 18z": [
        21.13, 19.16, 20.99, 20.51, 26.88, 24.22, 24.99, 25.66, 27.34, 23.83,
        21.61, 23.40, 22.91, 23.08, 19.06, 14.80, 20.44, 22.18, 22.75, 20.14
    ],
    "Pangu 6-h 00z": [
        19.87, 18.93, 17.22, 19.82, 25.41, 20.98, 22.16, 22.71, 26.79, 22.90,
        20.01, 22.75, 21.11, 20.94, 17.62, 13.74, 19.78, 21.47, 22.17, 19.97
    ],
    "Pangu 24-h 06z": [
        9.33, 21.63, 27.49, 16.88, 12.04, 24.76, 28.76, 18.30, 13.85, 23.55,
        26.07, 18.04, 14.14, 23.10, 26.52, 17.40, 13.23, 24.15, 28.24, 18.15
        ],
    "Pangu 24-h 12z": [
        21.14, 27.20, 16.74, 11.90, 24.66, 28.71, 18.38, 14.04, 23.33, 25.47,
        17.77, 14.04, 22.68, 25.92, 16.93, 12.75, 23.92, 28.13, 17.91, 13.58
        ],
    "Pangu 24-h 18z": [
        25.29, 20.80, 19.90, 20.63, 24.78, 19.39, 18.97, 23.33, 25.41, 19.73,
        19.01, 20.62, 22.91, 19.95, 12.79, 16.86, 20.07, 17.94, 15.58, 21.60
        ],
    "Pangu 24-h 00z": [
        19.31, 20.56, 19.77, 20.22, 23.01, 20.67, 19.19, 22.91, 21.13, 20.89,
        21.52, 22.43, 22.51, 20.00, 19.80, 17.41, 16.19, 19.04, 19.79, 20.28
        ],
    "ERA5": [
        20.96, 23.78, 22.54, 21.29, 22.40, 22.87, 22.35, 22.52, 22.37, 22.96,
        19.55, 18.90, 14.89, 13.54, 13.19, 14.12, 16.83, 17.31, 18.03, 19.06
    ]
}

#Plotting the models in different colours with markers on each line except ERA5

colors = {"Pangu 6-h 06z": "magenta", "Pangu 6-h 12z": "hotpink", "Pangu 6-h 18z": "darkviolet", "Pangu 6-h 00z": "mediumvioletred", 
          "Pangu 24-h 00z": "crimson", "Pangu 24-h 06z": "palevioletred", "ERA5": "black", "ERA5 06z": "black"}

colors = {"Pangu 24-h 06z": "magenta", "Pangu 24-h 12z": "hotpink", "Pangu 24-h 18z": "darkviolet", 
          "Pangu 24-h 00z": "crimson", "ERA5": "black"}

markers = { "Pangu 6-h 06z": "o", "Pangu 6-h 12z": "o", "Pangu 6-h 18z": "o", "Pangu 6-h 00z": "o", "Pangu 24-h 00z": "o", 
            "Pangu 24-h 06z": "o", "ERA5": "none", "ERA5 06z": "none"}

markers = { "Pangu 24-h 06z": "o", "Pangu 24-h 12z": "o", "Pangu 24-h 18z": "o", "Pangu 24-h 00z": "o", 
            "ERA5": "none"}

#Lead times 1-20
lead_times = np.arange(1, 21)
ticks = np.arange(0,36,5)

#Plotting every other dy
dates = [f'8/{28 + i}' if (28 + i) <= 31 else f'9/{(i - 3)}' for i in range(20)]
odd_lead_times = lead_times[0::2]  
odd_dates = dates[0::2]    

# Plot each forecast model
plt.figure(figsize=(16, 9.5))

for model, temperatures in pangu_data.items():
    plt.plot(
        lead_times,
        temperatures,
        label=model,
        color=colors[model],
        marker=markers[model],
        linestyle='-' if model == "ERA5" else '--', 
        linewidth=5,
        markersize=8
    )

    # Heatwave highlight
y_bottom, y_top = 0, 0.3
x_heatwave = np.linspace(5, 12, 100)
plt.fill_between(
    x_heatwave, y_bottom, y_top, color='black', alpha=0.7, 
    label='Heatwave Period', edgecolor='black', linestyle='-', linewidth=4
    )
plt.fill_between(
    x_heatwave, y_bottom, y_top, color='black', hatch='//', 
    edgecolor='grey', alpha=0.9
)

    # Plot settings
plt.xlabel('Lead Time (Days)', fontsize=25, labelpad=10)
plt.ylabel('Temperature (°C)', fontsize=26, labelpad=10)
plt.xticks(odd_lead_times, [f"{lt}\n{date}" for lt, date in zip(odd_lead_times, odd_dates)], fontsize=19, rotation=0)
plt.yticks(ticks, fontsize=21)
plt.legend(loc='lower right', fontsize=15)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#plt.savefig(save_directory + 'pangu_NW2019_24hr_data.png', dpi=850)
plt.tight_layout()
plt.show()
