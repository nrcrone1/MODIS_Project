# MODIS Project
## Project title: Using MODIS imagery to improve understanding of storm-induced sediment processes on carbonate platforms

Project description: Shallow carbonate platforms, such as Turks and Caicos 
and the Great Bahamas Bank, serve as large carbon sinks and produce ~50% of 
Earth's marine carbonate sediment. Tropical cyclones and winter storms have 
the potential to transport large amounts of carbonate sediment off of the 
platform and into blue holes and the deep sea. However, it is notoriously 
difficult to gather in-situ observations during such storm events.

MODIS satellite imagery provides daily, high resolution (1 x 1 km) ocean 
color data which can be used to quantify total suspended solids (TSS) over 
shallow carbonate platforms. 

Intense storm can transport coarse-grained sands from the shallow carbonate
platform and deposit them in blue holes. Sediment cores collected from blue 
holes across the GBB have been widely used to reconstruct annual storm 
frequency over the past several hundred years.

The goal of this project is to quantify TSS using MODIS before and after 
storm events passing GBB and hopefully correlate storms which drive large 
suspension events with coarse-grained sand layers identified in blue hole 
sediment cores. 

## Central Question / Objective
The objective of this project is to characterize TCs that pass the Caicos 
platform based on their capacity to resuspend and transport sediment around the 
platform. In doing so, I aim to answer the following question:
1. What characteristics of tropical cyclones promote sediment suspension on
    the Caicos carbonate platform?
   
I hypothesize that since tropical cyclones have counterclockwise winds, storms
that pass on the south of the platform will generate onshore-directed winds
which promote sediment resuspension.


## Repository structure

```text
MODIS_Project/
├── README.md
├── Data/
│   ├── Caicos_Rrs667_2004_ASO.mat
│   ├── Caicos_Rrs667_2008_ASO.mat
│   ├── Caicos_Rrs667_2011_ASO.mat
│   ├── Caicos_Rrs667_2017_ASO.mat
│   ├── ibtracs_storms_2002_to_2020.mat
│   └── Caicos.gpkg
└── Code/
    └── final_project_figures.py
```

## How to run

1. Download the Data and Code folders from this repository
2. The file structure must remain unchanged. The python script uses relative paths to find the Data folder
3. Install the required Python libraries. All of the needed can be install using the following:
```text
conda install geopandas matplotlib scipy shapely pyproj numpy
```
4. Open the `Code` folder and run `final_project_figures.py`

