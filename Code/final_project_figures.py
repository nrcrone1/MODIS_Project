# ADVANCED ENVIRONMENTAL DATA SCIENCE PROJECT - FINAL FIGURES
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / 'Data'

#%% STUDY SITE (FINAL FIGURE)
latlim = [17, 32]
lonlim = [-85.5, -70.5]
gshhs_path = r'C:\Users\noahr\Downloads\MATLAB\AdvEnvDatSci\GSHHS_shp\f\GSHHS_f_L1.shp'
S = gpd.read_file(gshhs_path, bbox=(lonlim[0], latlim[0], lonlim[1], latlim[1]))

fig, ax = plt.subplots(figsize=(7, 7))
#plot coastlines
h = S.plot(ax=ax, facecolor=[0.85, 0.85, 0.85], edgecolor=[0.6, 0.6, 0.6])

ax.set_xlim(lonlim)
ax.set_ylim(latlim)
ax.set_xlabel('Longitude', fontweight='bold', color='k')
ax.set_ylabel('Latitude', fontweight='bold', color='k')

ax.tick_params(
    axis='both',
    direction='in',
    length=6,
    width=1.2,
    colors='k',
    labelsize=12
)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

for spine in ax.spines.values():
    spine.set_linewidth(1.2)
    spine.set_color('k')

ax.set_axisbelow(False)
ax.set_frame_on(True)

plt.show()



#%% STORM TRACKS FROM 2002 TO 2020 WITHIN 100KM OF CAICOS (FINAL FIGURE)
import numpy as np
import scipy.io
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pyproj import Geod

storm_mat = scipy.io.loadmat(
    data_dir / 'ibtracs_storms_2002_to_2020.mat',
    simplify_cells=True
)

storm_data = storm_mat['storm_data']

latlim = [20.5, 23.0]
lonlim = [-73.5, -70.0]
gshhs_path = data_dir / 'GSHHS_shp' / 'f' / 'GSHHS_f_L1.shp'
S = gpd.read_file(gshhs_path, bbox=(lonlim[0], latlim[0], lonlim[1], latlim[1]))

target_names = ['MARIA', 'IRMA', 'IRENE', 'IKE', 'HANNA', 'FRANCES']
target_years = [2017, 2017, 2011, 2008, 2008, 2004]
colors = np.array([
    [1.00, 0.00, 0.00],  # Red
    [1.00, 0.75, 0.80],  # Pink
    [1.00, 0.65, 0.00],  # Orange
    [0.50, 0.00, 0.50],  # Purple
    [1.00, 1.00, 0.00],  # Yellow
    [0.50, 0.00, 0.50]   # Purple
])

fig, ax = plt.subplots()
#plot coastlines
h = S.plot(ax=ax, facecolor=[0.85, 0.85, 0.85], edgecolor=[0.6, 0.6, 0.6])

if isinstance(storm_data, dict):
    storm_data = [storm_data]
else:
    storm_data = np.atleast_1d(storm_data)

def get_field(storm, field):
    if isinstance(storm, dict):
        return storm[field]
    return getattr(storm, field)

for s in range(len(target_names)):
    # Find matching storm
    idx = [
        j for j, storm in enumerate(storm_data)
        if str(get_field(storm, 'name')).strip() == target_names[s]
        and int(get_field(storm, 'year')) == target_years[s]
    ]

    # Skip if no matching storm
    if len(idx) == 0:
        print(f"Warning: Storm {target_names[s]} ({target_years[s]}) not found")
        continue

    # Extract coordinates
    storm_lat = np.asarray(get_field(storm_data[idx[0]], 'lat')).flatten()
    storm_lon = np.asarray(get_field(storm_data[idx[0]], 'lon')).flatten()

    # Plot storm track
    ax.plot(storm_lon, storm_lat, color=colors[s, :], linewidth=1.5, zorder=3)

    # Calculate direction
    dx = np.diff(storm_lon)
    dy = np.diff(storm_lat)
    theta = np.arctan2(dy, dx)
    L = 0.04

    for i in range(len(theta)):
        x_tri = L * np.array([1, -0.5, -0.5])
        y_tri = L * np.array([0, np.sqrt(3)/2, -np.sqrt(3)/2])

        R = np.array([
            [np.cos(theta[i]), -np.sin(theta[i])],
            [np.sin(theta[i]),  np.cos(theta[i])]
        ])

        coords = R @ np.array([x_tri, y_tri])

        #plot triangles
        triangle = np.column_stack((
            storm_lon[i] + coords[0, :],
            storm_lat[i] + coords[1, :]
        ))

        ax.add_patch(Polygon(
            triangle,
            closed=True,
            facecolor=colors[s, :],
            edgecolor='none',
            zorder=3
        ))

center_lat = 21.72
center_lon = -71.81
radius_km = 100

# Generate bearings around the circle
azimuth = np.arange(0, 361, 1)

# Calculate circle coordinates
geod = Geod(ellps='WGS84')
circle_lon, circle_lat, _ = geod.fwd(
    np.full(len(azimuth), center_lon),
    np.full(len(azimuth), center_lat),
    azimuth,
    np.full(len(azimuth), radius_km * 1000)
)

#plot star on blue hole location
ax.plot(center_lon, center_lat, 'k*',
        markersize=10, linewidth=1.5, zorder=4)

#plot circle
ax.fill(
    circle_lon, circle_lat,
    color=[0.8, 0.8, 0.8],
    alpha=0.25,
    edgecolor='none',
    zorder=2
)

#formatting
ax.set_xlim([-73.5, -70])
ax.set_ylim([20.5, 23])
ax.set_xlabel('Longitude', fontweight='bold', color='k')
ax.set_ylabel('Latitude', fontweight='bold', color='k')

ax.tick_params(
    axis='both',
    direction='in',
    length=6,
    width=1.2,
    colors='k',
    labelsize=12
)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

for spine in ax.spines.values():
    spine.set_linewidth(1.2)
    spine.set_color('k')

#formatting
ax.set_frame_on(True)
ax.set_axisbelow(False)

plt.show()




#%% LOAD 2004 DATA (FINAL 2004 DATA)
import numpy as np
import scipy.io
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import shapely
from pyproj import Transformer

filepath = data_dir / 'Caicos_Rrs667_2004_ASO.mat'
data = scipy.io.loadmat(filepath, simplify_cells=True)

lon = data['lon']
lat = data['lat']
rrs667 = data['rrs667']


#%% LOAD OFFSHORE SEGMENTS (FINAL SEGMENTS)
#only have to do this once

gpkg = data_dir / 'Caicos.gpkg'

north = gpd.read_file(gpkg, layer="10km_offshore_north")
west = gpd.read_file(gpkg, layer="10km_offshore_west")
southwest = gpd.read_file(gpkg, layer="10km_offshore_southwest")
south = gpd.read_file(gpkg, layer="10km_offshore_south")
east = gpd.read_file(gpkg, layer="10km_offshore_east")


# Project MODIS longitude/latitude into UTM
LON, LAT = np.meshgrid(lon, lat)

crs = north.crs
transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
modis_x, modis_y = transformer.transform(LON, LAT)


#north mask
north_shape = north.geometry
north_mask = np.zeros(modis_x.shape, dtype=bool)
for i in range(len(north_shape)):
    north_mask = north_mask | shapely.contains_xy(
        north_shape.iloc[i], modis_x, modis_y
    )

#west mask
west_shape = west.geometry
west_mask = np.zeros(modis_x.shape, dtype=bool)
for i in range(len(west_shape)):
    west_mask = west_mask | shapely.contains_xy(
        west_shape.iloc[i], modis_x, modis_y
    )

#southwest mask
southwest_shape = southwest.geometry
southwest_mask = np.zeros(modis_x.shape, dtype=bool)
for i in range(len(southwest_shape)):
    southwest_mask = southwest_mask | shapely.contains_xy(
        southwest_shape.iloc[i], modis_x, modis_y
    )

#south mask
south_shape = south.geometry
south_mask = np.zeros(modis_x.shape, dtype=bool)
for i in range(len(south_shape)):
    south_mask = south_mask | shapely.contains_xy(
        south_shape.iloc[i], modis_x, modis_y
    )

#east mask
east_shape = east.geometry
east_mask = np.zeros(modis_x.shape, dtype=bool)
for i in range(len(east_shape)):
    east_mask = east_mask | shapely.contains_xy(
        east_shape.iloc[i], modis_x, modis_y
    )


#%% APPLY SPATIAL MASK TO 2004 (FINAL SEGMENT MASKS)
TSS = 62.86 * ((rrs667 * np.pi) / ((0.1736) - (rrs667 * np.pi)))

north_mask_3d = np.broadcast_to(north_mask[:, :, np.newaxis], TSS.shape)
TSS_north = TSS.copy()
TSS_north[~north_mask_3d] = np.nan

west_mask_3d = np.broadcast_to(west_mask[:, :, np.newaxis], TSS.shape)
TSS_west = TSS.copy()
TSS_west[~west_mask_3d] = np.nan

southwest_mask_3d = np.broadcast_to(southwest_mask[:, :, np.newaxis], TSS.shape)
TSS_southwest = TSS.copy()
TSS_southwest[~southwest_mask_3d] = np.nan

south_mask_3d = np.broadcast_to(south_mask[:, :, np.newaxis], TSS.shape)
TSS_south = TSS.copy()
TSS_south[~south_mask_3d] = np.nan

east_mask_3d = np.broadcast_to(east_mask[:, :, np.newaxis], TSS.shape)
TSS_east = TSS.copy()
TSS_east[~east_mask_3d] = np.nan


#%% 2004 SCATTER SUBPLOTS - ALL SEGMENTS (FINAL FIGURE)

fig, axes = plt.subplots(5, 1, figsize=(4.5, 8))
fig.subplots_adjust(hspace=0.35)

page = TSS.shape[2]


# Plot north
ax = axes[0]
Y = TSS_north.reshape((-1, page), order='F')
idx = np.flatnonzero(~np.isnan(Y.ravel(order='F')))
row_idx, time_idx = np.unravel_index(idx, Y.shape, order='F')
ax.scatter(time_idx + 1, Y.ravel(order='F')[idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.8275, 0.8510])
# Mark storms
ax.axvline(244, linestyle='--', linewidth=2)
ax.scatter(239, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none')
ax.scatter(248, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot west
ax = axes[1]
Y = TSS_west.reshape((-1, page), order='F')
idx = np.flatnonzero(~np.isnan(Y.ravel(order='F')))
row_idx, time_idx = np.unravel_index(idx, Y.shape, order='F')
ax.scatter(time_idx + 1, Y.ravel(order='F')[idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.6980, 0.5922])
# Mark storms
ax.axvline(244, linestyle='--', linewidth=2)
ax.scatter(239, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none')
ax.scatter(248, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot southwest
ax = axes[2]
Y = TSS_southwest.reshape((-1, page), order='F')
idx = np.flatnonzero(~np.isnan(Y.ravel(order='F')))
row_idx, time_idx = np.unravel_index(idx, Y.shape, order='F')
ax.scatter(time_idx + 1, Y.ravel(order='F')[idx], 15,
           facecolors='none', edgecolors=[0.5020, 0.3922, 0.6353])
# Mark storms
ax.axvline(244, linestyle='--', linewidth=2)
ax.scatter(239, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none')
ax.scatter(248, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot south
ax = axes[3]
Y = TSS_south.reshape((-1, page), order='F')
idx = np.flatnonzero(~np.isnan(Y.ravel(order='F')))
row_idx, time_idx = np.unravel_index(idx, Y.shape, order='F')
ax.scatter(time_idx + 1, Y.ravel(order='F')[idx], 15,
           facecolors='none', edgecolors=[0.1569, 0.4706, 0.6471])
# Mark storms
ax.axvline(244, linestyle='--', linewidth=2)
ax.scatter(239, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none')
ax.scatter(248, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after%formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot east
ax = axes[4]
Y = TSS_east.reshape((-1, page), order='F')
idx = np.flatnonzero(~np.isnan(Y.ravel(order='F')))
row_idx, time_idx = np.unravel_index(idx, Y.shape, order='F')
ax.scatter(time_idx + 1, Y.ravel(order='F')[idx], 15,
           facecolors='none', edgecolors=[0.3176, 0.5529, 0.2824])
# Mark storms
ax.axvline(244, linestyle='--', linewidth=2)
ax.scatter(239, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none')
ax.scatter(248, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after%formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# FORMATTING ALL TILES
for k in range(len(axes)):
    axes[k].set_xlim([213, 305])
    axes[k].set_ylim([0, 4])

    axes[k].xaxis.set_minor_locator(ticker.FixedLocator(np.arange(214, 305, 1)))
    axes[k].yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 4.5, 0.5)))

    axes[k].tick_params(
        axis='both',
        which='both',
        colors='k',
        width=1
    )

    axes[k].tick_params(axis='both', which='major', labelsize=9)
    axes[k].tick_params(axis='both', which='minor', length=3)

    for label in axes[k].get_xticklabels() + axes[k].get_yticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(9)

    for spine in axes[k].spines.values():
        spine.set_linewidth(1)
        spine.set_color('k')

# Major x-axis ticks
for k in range(len(axes)):
    axes[k].set_xticks([213, 227, 244, 258, 274, 288])
    axes[k].set_xticklabels(['Aug 1', 'Aug 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15'])
# Legend
#legend(ax(end), h, 'Frances', 'Location', 'best')

plt.show()







#%% LOAD 2008 DATA (FINAL DATA)
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

filepath = data_dir / 'Caicos_Rrs667_2008_ASO.mat'
data = scipy.io.loadmat(filepath, simplify_cells=True)
rrs667 = data['rrs667']


#%% APPLY SPATIAL MASK TO 2008 (FINAL SEGMENT MASKS)
TSS = 62.86 * ((rrs667 * np.pi) / ((0.1736) - (rrs667 * np.pi)))

north_mask_3d = np.broadcast_to(north_mask[:, :, np.newaxis], TSS.shape)
TSS_north = TSS.copy()
TSS_north[~north_mask_3d] = np.nan

west_mask_3d = np.broadcast_to(west_mask[:, :, np.newaxis], TSS.shape)
TSS_west = TSS.copy()
TSS_west[~west_mask_3d] = np.nan

southwest_mask_3d = np.broadcast_to(southwest_mask[:, :, np.newaxis], TSS.shape)
TSS_southwest = TSS.copy()
TSS_southwest[~southwest_mask_3d] = np.nan

south_mask_3d = np.broadcast_to(south_mask[:, :, np.newaxis], TSS.shape)
TSS_south = TSS.copy()
TSS_south[~south_mask_3d] = np.nan

east_mask_3d = np.broadcast_to(east_mask[:, :, np.newaxis], TSS.shape)
TSS_east = TSS.copy()
TSS_east[~east_mask_3d] = np.nan


#%% 2008 SCATTER SUBPLOTS - ALL SEGMENTS (FINAL FIGURE)

fig, axes = plt.subplots(5, 1, figsize=(4.5, 8))
fig.subplots_adjust(hspace=0.35)
page = TSS.shape[2]


# Plot north
ax = axes[0]
Y = TSS_north.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.8275, 0.8510])
# Mark storms
h1 = ax.axvline(246, linestyle='--', linewidth=2, color='k') #hanna
h2 = ax.axvline(251, linestyle='--', linewidth=2, color='r') #ike
ax.scatter(242, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before hanna
ax.scatter(249, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after hanna
ax.scatter(254, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after ike
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot west
ax = axes[1]
Y = TSS_west.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.6980, 0.5922])
# Mark storms
h1 = ax.axvline(246, linestyle='--', linewidth=2, color='k') #hanna
h2 = ax.axvline(251, linestyle='--', linewidth=2, color='r') #ike
ax.scatter(242, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before hanna
ax.scatter(249, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after hanna
ax.scatter(254, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after ike
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot southwest
ax = axes[2]
Y = TSS_southwest.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.5020, 0.3922, 0.6353])
# Mark storms
h1 = ax.axvline(246, linestyle='--', linewidth=2, color='k') #hanna
h2 = ax.axvline(251, linestyle='--', linewidth=2, color='r') #ike
ax.scatter(242, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before hanna
ax.scatter(249, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after hanna
ax.scatter(254, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after ike
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot south
ax = axes[3]
Y = TSS_south.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.1569, 0.4706, 0.6471])
# Mark storms
h1 = ax.axvline(246, linestyle='--', linewidth=2, color='k') #hanna
h2 = ax.axvline(251, linestyle='--', linewidth=2, color='r') #ike
ax.scatter(242, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before hanna
ax.scatter(249, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after hanna
ax.scatter(254, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after ike
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot east
ax = axes[4]
Y = TSS_east.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.3176, 0.5529, 0.2824])
# Mark storms
h1 = ax.axvline(246, linestyle='--', linewidth=2, color='k') #hanna
h2 = ax.axvline(251, linestyle='--', linewidth=2, color='r') #ike
ax.scatter(242, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before hanna
ax.scatter(249, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after hanna
ax.scatter(254, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after ike
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# FORMATTING ALL TILES
for k in range(len(axes)):
    axes[k].set_xlim([213, 305])
    axes[k].set_ylim([0, 4])

    axes[k].xaxis.set_minor_locator(ticker.FixedLocator(np.arange(214, 305, 1)))
    axes[k].yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 4.5, 0.5)))

    axes[k].tick_params(axis='both', which='both', colors='k', width=1)
    axes[k].tick_params(axis='both', which='major', labelsize=9)
    axes[k].tick_params(axis='both', which='minor', length=3)

    for label in axes[k].get_xticklabels() + axes[k].get_yticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(9)

    for spine in axes[k].spines.values():
        spine.set_linewidth(1)
        spine.set_color('k')

# Major x-axis ticks
for k in range(len(axes)):
    axes[k].set_xticks([213, 227, 244, 258, 274, 288])
    axes[k].set_xticklabels(['Aug 1', 'Aug 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15'])
# Legend
#legend(ax(end), [h1 h2], {'Ike', 'Hanna'}, 'Location', 'best')


#%% LOAD 2011 DATA (FINAL DATA)
filepath = data_dir / 'Caicos_Rrs667_2011_ASO.mat'
data = scipy.io.loadmat(filepath, simplify_cells=True)
rrs667 = data['rrs667']


#%% APPLY SPATIAL MASK TO 2011 (FINAL SEGMENT MASKS)
TSS = 62.86 * ((rrs667 * np.pi) / ((0.1736) - (rrs667 * np.pi)))

north_mask_3d = np.broadcast_to(north_mask[:, :, np.newaxis], TSS.shape)
TSS_north = TSS.copy()
TSS_north[~north_mask_3d] = np.nan

west_mask_3d = np.broadcast_to(west_mask[:, :, np.newaxis], TSS.shape)
TSS_west = TSS.copy()
TSS_west[~west_mask_3d] = np.nan

southwest_mask_3d = np.broadcast_to(southwest_mask[:, :, np.newaxis], TSS.shape)
TSS_southwest = TSS.copy()
TSS_southwest[~southwest_mask_3d] = np.nan

south_mask_3d = np.broadcast_to(south_mask[:, :, np.newaxis], TSS.shape)
TSS_south = TSS.copy()
TSS_south[~south_mask_3d] = np.nan

east_mask_3d = np.broadcast_to(east_mask[:, :, np.newaxis], TSS.shape)
TSS_east = TSS.copy()
TSS_east[~east_mask_3d] = np.nan


#%% 2011 SCATTER SUBPLOTS - ALL SEGMENTS (FINAL FIGURE)

fig, axes = plt.subplots(5, 1, figsize=(4.5, 8))
fig.subplots_adjust(hspace=0.35)
page = TSS.shape[2]


# Plot north
ax = axes[0]
Y = TSS_north.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.8275, 0.8510])
# Mark storms
h1 = ax.axvline(235, linestyle='--', linewidth=2, color='k') #irene
ax.scatter(233, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before 
ax.scatter(243, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after 
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot west
ax = axes[1]
Y = TSS_west.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.6980, 0.5922])
# Mark storms
h1 = ax.axvline(235, linestyle='--', linewidth=2, color='k') #irene
ax.scatter(233, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before 
ax.scatter(243, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after 
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot southwest
ax = axes[2]
Y = TSS_southwest.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.5020, 0.3922, 0.6353])
# Mark storms
h1 = ax.axvline(235, linestyle='--', linewidth=2, color='k') #irene
ax.scatter(233, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before 
ax.scatter(243, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after 
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot south
ax = axes[3]
Y = TSS_south.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.1569, 0.4706, 0.6471])
# Mark storms
h1 = ax.axvline(235, linestyle='--', linewidth=2, color='k') #irene
ax.scatter(233, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before 
ax.scatter(243, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after 
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot east
ax = axes[4]
Y = TSS_east.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.3176, 0.5529, 0.2824])
# Mark storms
h1 = ax.axvline(235, linestyle='--', linewidth=2, color='k') #irene
ax.scatter(233, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before 
ax.scatter(243, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after 
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# FORMATTING ALL TILES
for k in range(len(axes)):
    axes[k].set_xlim([213, 305])
    axes[k].set_ylim([0, 4])

    axes[k].xaxis.set_minor_locator(ticker.FixedLocator(np.arange(214, 305, 1)))
    axes[k].yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 4.5, 0.5)))

    axes[k].tick_params(axis='both', which='both', colors='k', width=1)
    axes[k].tick_params(axis='both', which='major', labelsize=9)
    axes[k].tick_params(axis='both', which='minor', length=3)

    for label in axes[k].get_xticklabels() + axes[k].get_yticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(9)

    for spine in axes[k].spines.values():
        spine.set_linewidth(1)
        spine.set_color('k')

# Major x-axis ticks
for k in range(len(axes)):
    axes[k].set_xticks([213, 227, 244, 258, 274, 288])
    axes[k].set_xticklabels(['Aug 1', 'Aug 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15'])


#%% LOAD 2017 DATA (FINAL DATA)
filepath = data_dir / 'Caicos_Rrs667_2017_ASO.mat'
data = scipy.io.loadmat(filepath, simplify_cells=True)
rrs667 = data['rrs667']


#%% APPLY SPATIAL MASK TO 2017 (FINAL SEGMENT MASKS)
TSS = 62.86 * ((rrs667 * np.pi) / ((0.1736) - (rrs667 * np.pi)))

north_mask_3d = np.broadcast_to(north_mask[:, :, np.newaxis], TSS.shape)
TSS_north = TSS.copy()
TSS_north[~north_mask_3d] = np.nan

west_mask_3d = np.broadcast_to(west_mask[:, :, np.newaxis], TSS.shape)
TSS_west = TSS.copy()
TSS_west[~west_mask_3d] = np.nan

southwest_mask_3d = np.broadcast_to(southwest_mask[:, :, np.newaxis], TSS.shape)
TSS_southwest = TSS.copy()
TSS_southwest[~southwest_mask_3d] = np.nan

south_mask_3d = np.broadcast_to(south_mask[:, :, np.newaxis], TSS.shape)
TSS_south = TSS.copy()
TSS_south[~south_mask_3d] = np.nan

east_mask_3d = np.broadcast_to(east_mask[:, :, np.newaxis], TSS.shape)
TSS_east = TSS.copy()
TSS_east[~east_mask_3d] = np.nan


#%% 2017 SCATTER SUBPLOTS - ALL SEGMENTS (FINAL FIGURE)

fig, axes = plt.subplots(5, 1, figsize=(4.5, 8))
fig.subplots_adjust(hspace=0.15)
page = TSS.shape[2]


# Plot north
ax = axes[0]
Y = TSS_north.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.8275, 0.8510])
# Mark storms
h1 = ax.axvline(250, linestyle='--', linewidth=2, color='k') #irma
h2 = ax.axvline(265, linestyle='--', linewidth=2, color='r') #maria
ax.scatter(249, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before irma
ax.scatter(252, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after irma
ax.scatter(261, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after maria
ax.scatter(267, 4, 60, marker='v', facecolors=[1.0, 0.5, 0.0], edgecolors='none') # Image after maria
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot west
ax = axes[1]
Y = TSS_west.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.7451, 0.6980, 0.5922])
# Mark storms
h1 = ax.axvline(250, linestyle='--', linewidth=2, color='k') #irma
h2 = ax.axvline(265, linestyle='--', linewidth=2, color='r') #maria
ax.scatter(249, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before irma
ax.scatter(252, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after irma
ax.scatter(261, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after maria
ax.scatter(267, 4, 60, marker='v', facecolors=[1.0, 0.5, 0.0], edgecolors='none') # Image after maria
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot southwest
ax = axes[2]
Y = TSS_southwest.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.5020, 0.3922, 0.6353])
# Mark storms
h1 = ax.axvline(250, linestyle='--', linewidth=2, color='k') #irma
h2 = ax.axvline(265, linestyle='--', linewidth=2, color='r') #maria
ax.scatter(249, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before irma
ax.scatter(252, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after irma
ax.scatter(261, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after maria
ax.scatter(267, 4, 60, marker='v', facecolors=[1.0, 0.5, 0.0], edgecolors='none') # Image after maria
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot south
ax = axes[3]
Y = TSS_south.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.1569, 0.4706, 0.6471])
# Mark storms
h1 = ax.axvline(250, linestyle='--', linewidth=2, color='k') #irma
h2 = ax.axvline(265, linestyle='--', linewidth=2, color='r') #maria
ax.scatter(249, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before irma
ax.scatter(252, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after irma
ax.scatter(261, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after maria
ax.scatter(267, 4, 60, marker='v', facecolors=[1.0, 0.5, 0.0], edgecolors='none') # Image after maria
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# Plot east
ax = axes[4]
Y = TSS_east.reshape((-1, page), order='F')
row_idx, time_idx = np.where(~np.isnan(Y))
ax.scatter(time_idx + 1, Y[row_idx, time_idx], 15,
           facecolors='none', edgecolors=[0.3176, 0.5529, 0.2824])
# Mark storms
h1 = ax.axvline(250, linestyle='--', linewidth=2, color='k') #irma
h2 = ax.axvline(265, linestyle='--', linewidth=2, color='r') #maria
ax.scatter(249, 4, 60, marker='v', facecolors=[0.55, 0.75, 0.40], edgecolors='none') # Image before irma
ax.scatter(252, 4, 60, marker='v', facecolors=[0.6, 0.0, 0.0], edgecolors='none') # Image after irma
ax.scatter(261, 4, 60, marker='v', facecolors=[0.0, 0.0, 1.0], edgecolors='none') # Image after maria
ax.scatter(267, 4, 60, marker='v', facecolors=[1.0, 0.5, 0.0], edgecolors='none') # Image after maria
#formatting
ax.set_ylabel('TSS (mg/L)', fontweight='bold', color='k')


# FORMATTING ALL TILES
for k in range(len(axes)):
    axes[k].set_xlim([213, 305])
    axes[k].set_ylim([0, 4])

    axes[k].xaxis.set_minor_locator(ticker.FixedLocator(np.arange(214, 305, 1)))
    axes[k].yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 4.5, 0.5)))

    axes[k].tick_params(axis='both', which='both', colors='k', width=1)
    axes[k].tick_params(axis='both', which='major', labelsize=9)
    axes[k].tick_params(axis='both', which='minor', length=3)

    for label in axes[k].get_xticklabels() + axes[k].get_yticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(9)

    for spine in axes[k].spines.values():
        spine.set_linewidth(1)
        spine.set_color('k')

# Major x-axis ticks
for k in range(len(axes)):
    axes[k].set_xticks([213, 227, 244, 258, 274, 288])
    axes[k].set_xticklabels(['Aug 1', 'Aug 15', 'Sep 1', 'Sep 15', 'Oct 1', 'Oct 15'])
# Legend
#legend(ax(end), [h1 h2], {'Ike', 'Hanna'}, 'Location', 'best')

plt.show()





