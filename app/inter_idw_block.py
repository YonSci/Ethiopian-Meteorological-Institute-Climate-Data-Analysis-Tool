import streamlit as st
from datetime import datetime
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import time
import geopandas as gpd
import regionmask
from scipy.interpolate import interp2d


def inter_idw_block():
    
    from idw_basic import idw_rblock
    
    data_final = st.session_state.get('data_final', 'None')
    df2 = st.session_state.get('df2', 'None')
    variable = st.session_state.get('variable', 'None')
    lats = st.session_state.get('lats', 'None')
    lons = st.session_state.get('lons', 'None')
    
    

    
    
    lat = data_final["Latitude"]
    lon = data_final["Longitude"]
    
    var_name = data_final[variable].name
    zvalue = data_final[var_name]
    
    
    
    col1, col2 = st.columns(2)
    
    with col1:

        p = st.slider("Enter the power parameter", min_value=1.0, max_value=5.0, value = 1.5, key="p")
        st.info(f'You selected the power parameter: {p}')
    
    with col2:
        search_radius = st.number_input("Enter the search radius", min_value=5, max_value=100000, value=10, step=10, key="search_radius")
        st.info(f'You selected the search radius: {search_radius}')
    
    start_time = time.time()
    x_idw_list1, y_idw_list1, z_head1 = idw_rblock(x=lon.astype(float).values.tolist(),
                                               y=lat.astype(float).values.tolist(),
                                               z=zvalue.values.tolist(),
                                               search_radius=search_radius,
                                               grid_side_length = 100,
                                               p=p)
    
    # Create an interpolator function
    f1 = interp2d(x_idw_list1, y_idw_list1, z_head1, kind='cubic')  
    # 'linear', 'cubic', 'quintic'.
    z1_interpolated = f1(lons, lats)
    end_time = time.time()
    time_taken = end_time - start_time
    st.success(f"The block IDW process has completed successfully. It took {round(time_taken, 2)} seconds.")
   
    
    var_name = data_final[variable].name
    if data_final[variable].name == 'Total Rainfall':
        unit = 'mm'
    elif data_final[variable].name == 'Mean Maximum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Minimum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Temperature':
        unit = '°C'
        
    # convert to netCDF
    ds_idw_block = xr.Dataset( data_vars= {var_name:(('Latitude', 'Longitude'),
                                                z1_interpolated), },
    coords={'Latitude':lats, 'Longitude':lons})
    ds_idw_block[var_name].attrs = {'units':unit, 'long_name':var_name}
    
    ds_idw_block.Latitude.attrs['units'] = 'degrees_north'
    ds_idw_block.Latitude.attrs['long_name'] = 'latitude'
    ds_idw_block.Latitude.attrs['axis'] = 'Y'
    ds_idw_block.Longitude.attrs['units'] = 'degrees_east'
    ds_idw_block.Longitude.attrs['long_name'] = 'longitude'
    ds_idw_block.Longitude.attrs['axis'] = 'X'
    ds_idw_block.attrs = {'creation_date':datetime.now(), 
                'author':'Ethiopian Meteorology Institute (EMI)', 
                'email':'address@email.com', 
                'source':'observation', 
                'conventions':'CF-1.6', 
                'platform':'observation',
                'institution':'EMI'}
    
        
    if st.checkbox("Show the interpolated data", key="_interpolated"):    
            fig, ax = plt.subplots(figsize=(14, 8), subplot_kw=dict(projection=ccrs.PlateCarree()))

            # Add country borders
            ax.add_feature(cfeature.BORDERS, edgecolor='black')
            # Add coastlines
            ax.add_feature(cfeature.COASTLINE, edgecolor='black')
            # Add oceans
            ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
            
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

            # Create meshgrid of latitude and longitude coordinates
            lon_grid, lat_grid = np.meshgrid(lons, lats)
            ax.scatter(lon_grid, lat_grid, color='blue', marker='.', s=28,  alpha=1)
            img = ds_idw_block[var_name].plot(ax=ax, 
                                    cmap='viridis',
                                    cbar_kwargs={"shrink": 0.8},
                                    transform=ccrs.PlateCarree(), 
                                    extend='both', 
                                    alpha=1.0, 
                                    #    edgecolors='black',
                                    linewidths=0.5, 
                                    antialiased=True, 
                                    zorder=1,
                                    vmin=ds_idw_block[var_name].min(), vmax=ds_idw_block[var_name].max(),
                                    levels=15,
                                    )
        
            
            # cbar = plt.colorbar(img, ax=ax, shrink=0.7)  # Adjust the shrink value as needed
            # Add x and y labels with increased font size
            ax.set_xlabel('Longitude', fontsize=14)
            ax.set_ylabel('Latitude', fontsize=14)
                
            # Add a title
            ax.set_title(f'Interpolated {var_name} on Regular Grid Points', fontsize=18, y = 1.01)
        
            st.pyplot(fig)
            
            
            
    st.markdown("#### :blue[3) Extract into Ethiopian Domain]" )
            
    if ds_idw_block is None:
        st.error("Please perform interpolation first!")
    
    else:

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        # convert the geometry column to a list
        ethiopia_geometry_list = ethiopia.geometry.tolist()
        # Create the regionmask.Regions object using the list
        et_poly = regionmask.Regions(ethiopia_geometry_list)
        
        # Mask the data using the regionmask object
        et_mask = et_poly.mask(ds_idw_block.Longitude, ds_idw_block.Latitude)
        
        et_idwmaskb =  ds_idw_block.where(et_mask == 0)
        
        min_value = et_idwmaskb[var_name].min().values
        max_value = et_idwmaskb[var_name].max().values
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
        
        longitude_min = int(lons.min())
        longitude_max = int(lons.max())
        latitude_min = int(lats.min())
        latitude_max = int(lats.max())
        
        ax.coastlines()


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

        c1= et_idwmaskb[var_name].plot(ax=ax, 
                                cmap='viridis',
                                cbar_kwargs={"shrink": 0.8},
                                transform=ccrs.PlateCarree(), 
                                extend='both', 
                                alpha=1.0, 
                                #    edgecolors='black',
                                linewidths=0.5, 
                                antialiased=True, 
                                zorder=1, 
                                vmin=et_idwmaskb[var_name].min(), 
                                vmax=et_idwmaskb[var_name].max(),
                                levels=12)
                                
    
        ax.set_xlabel('Longitude', fontsize=14)
        ax.set_ylabel('Latitude', fontsize=14)
            
        # Add a title
        ax.set_title(f'Interpolated {var_name} on Regular Grid Points over Ethiopian Domain', fontsize=16, y = 1.01)
    
        st.pyplot(fig)   
        
        
    st.markdown("#### :blue[4) Convet to NetcDF format]" )
    clicked = st.button("Convert to netCDF", key="nc1") 
    
    
    if clicked:  
        et_idwmaskb.attrs['creation_date'] = et_idwmaskb.attrs['creation_date'].isoformat()
        et_idwmaskb.to_netcdf(f'ds_{variable}_masked_idw_block.nc', engine='h5netcdf')

        with open(f"ds_{variable}_masked_idw_block.nc", "rb") as fp:
            btn = st.download_button(
                label="Download netCDF file",
                data=fp,
                file_name=f"ds_{variable}_masked_idw_block.nc",
            )




if __name__ == "__main__":
    inter_idw_block()