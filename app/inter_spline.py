from datetime import datetime
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import geopandas as gpd
import regionmask
import streamlit as st
import numpy as np
import time
import plotly.graph_objs as go
import pandas as pd
import verde as vd




def inter_spline():
    data_final = st.session_state.get('data_final', 'None')
    df2 = st.session_state.get('df2', 'None')
    variable = st.session_state.get('variable', 'None')
    lats = st.session_state.get('lats', 'None')
    lons = st.session_state.get('lons', 'None')
    grid_interval = st.session_state.get('grid_interval', 'None')
    
    
    lon_k=np.array(data_final['Longitude']) 
    lat_k=np.array(data_final['Latitude']) 
    zdata=np.array([data_final[variable]])
    
    col1, col2 = st.columns(2)
    
    with col1:
        damping = st.number_input('Enter damping value', min_value=0.0, max_value=1.0, value=0.05, step=0.01)
        
    with col2: 
        mindist = st.number_input('Enter mindist value', min_value=0.0, max_value=1000.0, value=100.0, step=10.0)
       
    start_time = time.time()
    coordinates = (data_final.Longitude.values, data_final.Latitude.values)
    region = vd.get_region(coordinates)
    
    longitude_min = int(lons.min())
    longitude_max = int(lons.max())
    latitude_min = int(lats.min())
    latitude_max = int(lats.max())
    
    region = (longitude_min, longitude_max, latitude_min,latitude_max)
    spacing = grid_interval
    
    grid_E = vd.grid_coordinates(region=region,spacing=spacing)[0]
    gridE_first_row = grid_E[0, :]
    
    grid_N = vd.grid_coordinates(region=region,spacing=spacing)[1]
    gridN_first_row = grid_N[:, 0]
    
    
    spline = vd.Spline()
    score_default = np.mean(
    vd.cross_val_score(spline, coordinates, data_final[variable]))
    spline.fit(coordinates, data_final[variable])
    
    # chain = vd.Chain(
    # [
    #     ("mean", vd.BlockReduce(np.mean, spacing=spacing )),
    #     ("spline", vd.Spline(damping=damping, mindist=mindist)),
    #     ("spline", vd.Spline()),

    # ]
    # )
    
    chain = vd.Chain(
    [
        ("mean", vd.BlockReduce("mean", spacing=spacing )),
        ("spline", vd.Spline(damping=damping, mindist=mindist)),
        ("spline", vd.Spline()),
    ]
    )
    
    chain.fit(coordinates, data_final[variable])


    grid = chain.grid(
        region=region,
        spacing=spacing,
        dims=["Latitude", "Longitude"],
        data_names=variable,
        )
    
    spline_inter = grid[variable]
    
    end_time = time.time()
    time_taken = end_time - start_time
    st.success(f"The spline interpolation process has completed successfully. It took {round(time_taken, 2)} seconds.")
    
    
    var_name = data_final[variable].name

    if data_final[variable].name == 'Total Rainfall':
        unit = 'mm'
    elif data_final[variable].name == 'Mean Maximum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Minimum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Temperature':
        unit = '°C'
     
    
    
    ds_spline = xr.Dataset( data_vars= {var_name:(('Latitude', 'Longitude'), spline_inter.data), },
                           coords={'Latitude':gridN_first_row, 'Longitude':gridE_first_row})
    
    if var_name == 'Total Rainfall':
        ds_spline[var_name] = ds_spline[var_name].clip(min=0)
    
    ds_spline[var_name].attrs = {'units':unit, 'long_name':var_name}
    
    ds_spline.Latitude.attrs['units'] = 'degrees_north'
    ds_spline.Latitude.attrs['long_name'] = 'latitude'
    ds_spline.Latitude.attrs['axis'] = 'Y'
    ds_spline.Longitude.attrs['units'] = 'degrees_east'
    ds_spline.Longitude.attrs['long_name'] = 'longitude'
    ds_spline.Longitude.attrs['axis'] = 'X'
    ds_spline.attrs = {'creation_date':datetime.now(), 
                'author':'Ethiopian Meteorology Institute (EMI)', 
                'email':'address@email.com', 
                'source':'observation', 
                'conventions':'CF-1.6', 
                'platform':'observation',
                'institution':'EMI'}
    
  
    if st.checkbox("Show the interpolated data", key="_interpolated2"):
            fig, ax = plt.subplots(figsize=(14, 8), subplot_kw=dict(projection=ccrs.PlateCarree()))

            # Add country borders
            ax.add_feature(cfeature.BORDERS, edgecolor='black')
            # Add coastlines
            ax.add_feature(cfeature.COASTLINE, edgecolor='black')
            # Add oceans
            ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
            
            ax.coastlines()
            
                    
            longitude_min = int(lons.min())
            longitude_max = int(lons.max())
            latitude_min = int(lats.min())
            latitude_max = int(lats.max())


            # Add gridlines and labels
            gl = ax.gridlines(draw_labels=False)
            gl.xlocator = mticker.FixedLocator(range(longitude_min, longitude_max, 2)) 
            gl.ylocator = mticker.FixedLocator(range(latitude_min, latitude_max, 2))  

            # Manually set x and y labels
            ax.set_xticks(range(longitude_min, longitude_max, 2), crs=ccrs.PlateCarree())  
            ax.set_yticks(range(latitude_min, latitude_max, 2), crs=ccrs.PlateCarree())  
            ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
            ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
            
            c1= ds_spline[var_name].plot(ax=ax, 
                                    cmap='viridis',
                                    cbar_kwargs={"shrink": 0.8},
                                    transform=ccrs.PlateCarree(), 
                                    extend='both', 
                                    alpha=1.0, 
                                    #    edgecolors='black',
                                    linewidths=0.5, 
                                    antialiased=True, 
                                    zorder=1, 
                                    levels=12,
                                    vmin=ds_spline[var_name].min(), 
                                    vmax=ds_spline[var_name].max()
                                    )
            


            ax.set_xlabel('Longitude', fontsize=14)
            ax.set_ylabel('Latitude', fontsize=14)
                
            # Add a title
            ax.set_title(f'Interpolated {var_name} on Regular Grid Points', fontsize=18, y = 1.01)
        
            st.pyplot(fig)
    
  
  
    st.markdown("#### :blue[3) Extract into Ethiopian Domain]" )
                    
    if ds_spline is None:
        st.error("Please perform interpolation first!")

    else:

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        # convert the geometry column to a list
        ethiopia_geometry_list = ethiopia.geometry.tolist()
        # Create the regionmask.Regions object using the list
        et_poly = regionmask.Regions(ethiopia_geometry_list)
        
        # Mask the data using the regionmask object
        et_mask = et_poly.mask(ds_spline.Longitude, ds_spline.Latitude)
        
        et_dsspline =  ds_spline.where(et_mask == 0)
        
        min_value = et_dsspline[var_name].min().values
        max_value = et_dsspline[var_name].max().values
        num_ticks = 5
        

    if st.checkbox("Show the extracted data", key="_extracted"):
        fig, ax = plt.subplots(figsize=(14, 8), 
                            subplot_kw=dict(projection=ccrs.PlateCarree()))

        # Add country borders
        ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=0.1)
        # Add coastlines
        ax.add_feature(cfeature.COASTLINE, edgecolor='black')
        # Add oceans
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        
        ax.coastlines()
        longitude_min = int(lons.min())
        longitude_max = int(lons.max())
        latitude_min = int(lats.min())
        latitude_max = int(lats.max())


        # Add gridlines and labels
        gl = ax.gridlines(draw_labels=False)
        gl.xlocator = mticker.FixedLocator(range(longitude_min, longitude_max, 2)) 
        gl.ylocator = mticker.FixedLocator(range(latitude_min, latitude_max, 2))  

        # Manually set x and y labels
        ax.set_xticks(range(longitude_min, longitude_max, 2), crs=ccrs.PlateCarree())  
        ax.set_yticks(range(latitude_min, latitude_max, 2), crs=ccrs.PlateCarree())  
        ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
        ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
        
        # Add the GeoPandas DataFrame
        ethiopia.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)

        c1= et_dsspline[var_name].plot(ax=ax, 
                                cmap='viridis',
                                cbar_kwargs={"shrink": 0.8},
                                transform=ccrs.PlateCarree(), 
                                extend='both', 
                                alpha=1.0, 
                                #    edgecolors='black',
                                linewidths=0.5, 
                                antialiased=True, 
                                zorder=1, 
                                vmin=et_dsspline[var_name].min(),
                                vmax=et_dsspline[var_name].max(),
                                levels=12)
                                

        ax.set_xlabel('Longitude', fontsize=14)
        ax.set_ylabel('Latitude', fontsize=14)
            
        # Add a title
        ax.set_title(f'Interpolated {var_name} on Regular Grid Points over Ethiopian Domain', fontsize=16, y = 1.01)

        st.pyplot(fig)
    

    
    
    st.markdown("#### :blue[4) Convet to NetcDF format]" )
    clicked = st.button("Convert to netCDF", key="nc1") 


    if clicked:  
        et_dsspline.attrs['creation_date'] = et_dsspline.attrs['creation_date'].isoformat()
        et_dsspline.to_netcdf(f'ds_{variable}_masked_spline.nc', engine='h5netcdf')
        #et_nnmask.to_netcdf(f'ds_{variable}_masked.nc')

        # Download the netCDF file
        with open(f"ds_{variable}_masked_spline.nc", "rb") as fp:
            btn = st.download_button(
                label="Download netCDF file",
                data=fp,
                file_name=f"ds_{variable}_masked_spline.nc",
            )
        
    
if __name__ == "__main__":
    inter_spline()