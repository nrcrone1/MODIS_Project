# EXPLORATORY DATA ANALYSIS 

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Project title: Integrating MODIS imagery with blue hole sediment cores to 
# improve understanding of storm-induced sediment processes on carbonate 
# platforms

# Project description: Shallow carbonate platforms, such as the Great Bahamas 
# Bank (GBB), serve a large carbon sinks and produce ~50% of Earth's marine 
# carbonate sediment. Tropical cyclones and winter storms have the potential 
# to transport large amounts of carbonate sediment off of the platform and 
# into blue holes and the deep sea. However, it is notoriously difficult to 
# gather in-situ observations during such storm events.

# MODIS satellite imagery provides daily, high resolution (1 x 1 km) ocean 
# color data which can be used to quantify total suspended solids (TSS) over 
# shallow carbonate platforms. 

# Intense storm can transport coarse-grained sands from the shallow carbonate
# platform and deposit them in blue holes. Sediment cores collected from blue 
# holes across the GBB have been widely used to reconstruct annual storm 
# frequency over the past several hundred years.

# The goal of this project is to quantify TSS using MODIS before and after 
# storm events passing GBB and hopefully correlate storms which drive large 
# suspension events with coarse-grained sand layers identified in blue hole 
# sediment cores. 

#%%  DATASET 1: MODIS AQUA IMAGERY
#Description of the dataset
# - AQUA MODIS Level-2 Regional Ocean Color data
# - This dataset, provided by the National Aeronautics and Space 
#   Administration (NASA), Ocean Biology Processing Group, provides calibrated, 
#   atmospherically corrected ocean color measurements of particular interested
#   for my project are remote sensing reflectance values

#Spatial and temporal domains and resolution
# - Daily MODIS imagery atop Long Island, Bahamas (22.50N to 24.00N, -74.40W to -75.80W) was acquired for Jan 1 to Dec 31, 2011 
# - Daily MODIS imagery atop Turks and Caicos (20.82N to 22.62N, -70.84W to -72.78W) was acquired for Jan 1 to Dec 31, 2017 
# - These data has a spatial resolution of 1km x 1km 
# - These data were gridded to an equidistant cylindrical projection while
#   maintaining the 1km x 1km spatial resolution using the NASA OCSSW software

#Instructions for data acquisition
#- The AQUA MODIS Level-2 Regional Ocean Color data was accessed and downloaded from the
#  NASA Common Metadata Repository using the NASA earthaccess python library

#Links to datasets and software used
# - NASA AQUA MODIS Level-2 Regional Ocean Color data
#   https://www.earthdata.nasa.gov/data/catalog/ob-cloud-modisa-l2-oc-2022.0#overview
# - NASA earthaccess library
#   https://earthaccess.readthedocs.io/en/stable/
# - NASA OCSSW software
#   https://oceandata.sci.gsfc.nasa.gov/ocssw

#%%  DATASET 1: FIGURES 1-3 (TSS ON TURKS AND CAICOS PLATFORM IN 2017)

# Load MATLAB file
filepath = 'Data/MiddleCaicos_Rrs667_2017_auto.mat'
data = loadmat(filepath)

rrs667 = data['rrs667']
lat = data['lat'].squeeze()
lon = data['lon'].squeeze()
total_days = data['total_days'].squeeze()

# Calculate TSS
TSS = 62.86 * ((rrs667 * np.pi) / (0.1736 - (rrs667 * np.pi)))


# The next two figures show maps of the Turks and Caicos platform before
# and after Hurricane Irma in Septempber 2017. TSS plumes are visible outlining
# the island after Hurricane Irma. One issue I am currently facing is that
# most of the platform was masked during NASA's processing procedure. A red
# dot is placed in the center of the platform (southwest of the Island) for
# spatial reference. 

# Map before Irma
plt.figure()
plt.pcolormesh(lon, lat, TSS[:, :, 242], shading='auto')
plt.scatter(
    360 - 71.9,
    21.6,
    s=50,
    color='red'
)
plt.colorbar(label='TSS (mg/L)')
plt.xlim(287.2, 289.2)
plt.ylim(20.8, 22.7)
plt.show()

# Map after Irma
plt.figure()
plt.pcolormesh(lon, lat, TSS[:, :, 251], shading='auto')
plt.scatter(
    360 - 71.9,
    21.6,
    s=50,
    color='red'
)
plt.colorbar(label='TSS (mg/L)')
plt.xlim(287.2, 289.2)
plt.ylim(20.8, 22.7)
plt.show()


# TSS time series (3 pixels chosen to represent sediment plume)
# For this timeseries, I choose 3 pixels along the edge of the platform
# which weren't masked out. 
TSS_timeseries1 = TSS[57, 80, :]
TSS_timeseries2 = TSS[59, 82, :]
TSS_timeseries3 = TSS[58, 82, :]

plt.figure()
plt.scatter(total_days,TSS_timeseries1,label='Pixel 1')
plt.scatter(total_days,TSS_timeseries2,label='Pixel 2')
plt.scatter(total_days,TSS_timeseries3,label='Pixel 3')
plt.axvline(250,linestyle='--',color='black',label='Irma') # Irma
plt.axvline(265,linestyle='--',color='red',label='Maria') # Maria
plt.xlabel('Months in 2017')
plt.ylabel('TSS (mg/L)')
plt.xlim(1, 365)
# Month positions
monthDays = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
monthLabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
plt.xticks(monthDays, monthLabels)
plt.title('Example timeseries of TSS on Turks and Caicos platform during 2017')
plt.legend()
plt.show()

# Notice the elevated TSS values following Hurricane Irma but not Hurricane
# Maria. This indicates something about Irma's track and/or intensity was
# condusive for sediment resuspension but not Maria's.

#%%  DATASET 1: FIGURE 4 (TIMESERIES OF TSS ON LONG ISLAND, BAHAMAS PLATFORM IN 2011)

# Load MATLAB file
filepath = 'Data/LongIsland_Rrs667_2011.mat'
data = loadmat(filepath)

rrs667 = data['rrs667']
lat = data['lat'].squeeze()
lon = data['lon'].squeeze()
total_days = data['total_days'].squeeze()

# Calculate TSS
TSS = 62.86 * ((rrs667 * np.pi) / (0.1736 - (rrs667 * np.pi)))

# TSS time series (2 pixels chosen to represent sediment plume)
TSS_timeseries1 = TSS[71, 10, :]
TSS_timeseries2 = TSS[72, 9, :]

plt.figure()
plt.scatter(total_days,TSS_timeseries1,label='Pixel 1')
plt.scatter(total_days,TSS_timeseries2,label='Pixel 2')
plt.axvline(235,linestyle='--',color='black',label='Irene') # Irene
plt.xlabel('Months in 2011')
plt.ylabel('TSS (mg/L)')
plt.xlim(1, 365)
# Month positions
monthDays = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
monthLabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
plt.xticks(monthDays, monthLabels)
plt.title('Example timeseries of TSS on Long Island platform during 2011')
plt.legend()
plt.show()


#%% DATASET 2: SEDIMENT CORE DATA

#Description of the dataset
# - Sediment core data from Long Island Blue Hole
# - This dataset includes grain size data and coarse-grained anomaly data from
#   sediment cores collected from Long Island Blue Hole (Cores LIBH2 and LIBH
#   surface drive from Wallace et al 2021)
# - These sediment cores were collected in 2016 from Long Island Blue Hole in
#   the Bahamas. The cores stratigraphy were matched to create an ~11m long 
#   composite core spanning the last ~1100 years.
#   For the purpose of my project, I will be focusing on data from the last 
#   20 years. 

#Spatial and temporal domains and resolution
# - Spatial domain: Long Island Blue Hole, Bahamas (23.27N, -75.12W)
# - Sampling frequency: 1cm resolution down core. Represents ~1 year per cm.

#Instructions for data acquisition
# - Data can be acquired through the dataset DOI provided below

#Citations to publications and datasets
# - Wallace et al (2021) publication
#   E.J. Wallace, J.P. Donnelly, P.J. van Hengstum, T.S. Winkler, K. McKeon, 
#   D. MacDonald, N.E. d'Entremont, R.M. Sullivan, J.D. Woodruff, A.D. Hawkes, 
#   C. Maio. 2022. 1050 years of hurricane strikes on Long Island in The 
#   Bahamas. Paleoceanography and Paleoclimatology. doi: 10.1029/2020PA004156
# - Dataset DOI
#   https://doi.org/10.25921/f8zv-xw05


#%%  DATASET 2: FIGURE 1 (TIMESERIES OF MODERN STORM EVENTS RECORDED IN LONG ISLAND BLUE HOLE SEDIMENT CORE)
# Load MATLAB file
filepath = 'Data/Long_Island_core_data.txt'
long_island_grain_size_data = np.loadtxt(filepath,skiprows=1)

depth = np.floor(long_island_grain_size_data[:, 0]) 
age_ce = long_island_grain_size_data[:, 2] 
coarse_anom = long_island_grain_size_data[:, 6]

# This figure shows the first ~160 years of the grain size anomalies 
# from Wallace et al (2021). Storm events are defined at coarse-grained 
# anomalies that exceed 5.9% and are indicated by stars on the figure.
# The overlapping timeframe between the sediment core storm record and MODIS
# imagery is highlighted in gray. 

# Plot storm event timeseries
plt.figure()
plt.plot(age_ce,coarse_anom,label='Coarse Anomalies')
plt.axhline(5.9,linestyle='--',color='black',label='Event Threshold') 
event_mask = (coarse_anom > 5.9) & (age_ce >= 1850) # Identify storm events
plt.scatter(age_ce[event_mask],coarse_anom[event_mask],s=80,color='black',marker='*',label='Storm Events')
plt.axvspan(2002,2020,color='gray',alpha=0.25,label='MODIS timeframe')
plt.xlabel('Age CE')
plt.ylabel('Coarse Anomaly')
plt.xlim(1850, 2020)
plt.legend(loc='upper left')
plt.show()

# The only other dataset that I don't have in time for this submission is 
# the equivalent sediment core data from Turks and Caicos (lizzie has this 
# somewhere but I haven't dug it up)








