import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature

def inter_grid(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
        
    st.subheader("Prepare Regular Grid")
                
    st.write("Please select the bounding box and grid interval")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        min_lat = st.number_input("Enter minimum latitude", value=3.0, key="min_lat")
    with col2:
        max_lat = st.number_input("Enter maximum latitude", value=16.0, key="max_lat")
    with col3:
        grid_interval = st.number_input("Enter latitude step", value=0.1, key="step_lat")

    col1, col2, col3 = st.columns(3)
    with col1:
        min_lon = st.number_input("Enter minimum longitude", value=33.0, key="min_lon")
    with col2:
        max_lon = st.number_input("Enter maximum longitude", value=49.0, key="max_lon")
    with col3:
        grid_interval = st.number_input("Enter longitude step", value=0.1, key="step_lon")
                    
            
    longitude_min = int(min_lon)
    longitude_max = int(max_lon)
    latitude_min = int(min_lat)
    latitude_max = int(max_lat)
  
    # LAT = np.arange(min_lat, max_lat, grid_interval)
    # LON = np.arange(min_lon, max_lon, grid_interval)
    
    lats = np.arange(min_lat, max_lat, grid_interval)
    lons = np.arange(min_lon, max_lon, grid_interval)
    
   
    st.session_state.lats = lats
    st.session_state.lons = lons
    st.session_state.grid_interval = grid_interval


    # Create meshgrid of latitude and longitude coordinates
    lon_grid, lat_grid = np.meshgrid(lons, lats)
            
    if st.checkbox("Create Regular Grid", key="_grid"): 
      
        # Create a GeoAxes object
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection=ccrs.PlateCarree()))
        # ax.set_extent([longitude_min, longitude_max, latitude_min, latitude_max])

        # Add country borders
        ax.add_feature(cfeature.BORDERS, edgecolor='black')
        # Add coastlines
        ax.add_feature(cfeature.COASTLINE, edgecolor='black')
        # Add oceans
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')


        # Add gridlines and labels
        gl = ax.gridlines(draw_labels=False)
        gl.xlocator = mticker.FixedLocator(range(longitude_min, longitude_max, 2)) 
        gl.ylocator = mticker.FixedLocator(range(latitude_min, latitude_max, 2))  

        # Manually set x and y labels
        ax.set_xticks(range(longitude_min, longitude_max, 2), crs=ccrs.PlateCarree())  
        ax.set_yticks(range(latitude_min, latitude_max, 2), crs=ccrs.PlateCarree())  
        ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
        ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)

        # Create meshgrid of latitude and longitude coordinates
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        ax.scatter(lon_grid, lat_grid, color='blue', marker='.', s=28,  alpha=1)

        # Add a title
        ax.set_title('Regular Grid Points', fontsize=12, y=1.01)
        ax.set_xlabel('Longitude', fontsize=10)
        ax.set_ylabel('Latitude', fontsize=10)

        st.pyplot(fig)
        
        

    
            
    st.markdown("---")
            
if __name__ == "__main__":
    inter_grid()