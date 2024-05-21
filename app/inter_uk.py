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
import pykrige.uk as uk
import plotly.graph_objs as go
import pandas as pd


def inter_uk():
    data_final = st.session_state.get('data_final', 'None')
    variable = st.session_state.get('variable', 'None')
    lats = st.session_state.get('lats', 'None')
    lons = st.session_state.get('lons', 'None')
    
    lon_k = np.array(data_final['Longitude']) 
    lat_k = np.array(data_final['Latitude']) 
    zdata = np.array(data_final[variable])
    
    col1, col2 = st.columns(2)    
    model = None
    with col1:
        model = st.selectbox("Select semivariogram model", ["spherical", "exponential", "gaussian", "hole-effect", "power"], key="model")
        st.latex({
            "spherical": r'\gamma(d) = p \cdot (\frac{3d}{2r} - \frac{d^3}{2r^3}) + n',
            "exponential": r'\gamma(d) = p \cdot (1 - e^{ - \frac{d}{r/3}}) + n',
            "gaussian": r'\gamma(d) = p \cdot (1 - e^{ - \frac{d^2}{(\frac{4}{7} r)^2}}) + n',
            "hole-effect": r'\gamma(d) = p \cdot (1 - (1 - \frac{d}{r / 3}) * e^{ - \frac{d}{r / 3}}) + n',
            "power": r'\gamma(d) = s \cdot d^e + n'
        }.get(model, ""))
            
    with col2:
        lag = st.number_input("Enter the lag distance", value=10, key="lag")
    
    start_time = time.time()
    UK = uk.UniversalKriging(lon_k, lat_k, zdata, variogram_model=model, verbose=False, enable_plotting=False, nlags=lag, drift_terms="regional_linear", exact_values=True)
    Uk_z, UK_ss = UK.execute('grid', lons, lats)
    

    lags = UK.lags
    semivariance = UK.semivariance
    theoretical = UK.variogram_function(UK.variogram_model_parameters, lags)          
    
    sill, range_, nugget = UK.variogram_model_parameters
    
    end_time = time.time()
    time_taken = end_time - start_time
    st.success(f"The ordinary kriging process has completed successfully. It took {round(time_taken, 2)} seconds.")
    
    if st.checkbox("Show the variogram plot", key="_variogram"):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=lags, y=semivariance, mode='markers', name='Empirical/Experimental', hovertemplate='Lag: %{x}<br>Empirical/Experimental Semivariance: %{y}<extra></extra>', marker=dict(size=10, color='LightSkyBlue')))
        fig.add_trace(go.Scatter(x=lags, y=theoretical, mode='lines', name='Theoretical', hovertemplate='Lag: %{x}<br>Theoretical Semivariance: %{y}<extra></extra>', line=dict(color='MediumPurple', width=2)))
        fig.update_layout(xaxis=dict(range=[0, max(lags) + 0.2], gridcolor='LightGray'), yaxis=dict(range=[0, max(max(semivariance) + 1000, max(theoretical))], tickformat=',.0f'), plot_bgcolor='lightyellow')
        fig.update_layout(xaxis_title='Lag', yaxis_title='Semivariance', font=dict(family='Arial', size=14, color='black'))
        fig.update_layout(title='Variogram: Empirical vs Theoretical', title_x=0.1, font=dict(family='Arial', size=14, color='black'))
        fig.add_shape(type="rect", xref="paper", x0=0, x1=0.02, y0=0, y1=nugget, fillcolor="Red", opacity=0.5, layer="below", line_width=0)
        fig.add_shape(type="rect", xref="paper", x0=0, x1=0.02, y0=nugget, y1=sill, fillcolor="Blue", opacity=0.5, layer="below", line_width=0)
        fig.add_shape(type="rect", xref="x", x0=0, x1=range_, yref="paper", y0=0, y1=0.02, fillcolor="Green", opacity=0.5, layer="below", line_width=0)
        fig.update_layout(annotations=[
            dict(x=-0.09, y=nugget/2, xref="paper", yref="y", text="Nugget", showarrow=False, align="left", font=dict(color="Red")),
            dict(x=range_/2, y=0.02, xref="x", yref="paper", text="Range", showarrow=False, align="left", font=dict(color="Green")),
            dict(x=-0.04, y=sill - ((sill-nugget)/2), xref="paper", yref="y", text="Sill", showarrow=False, align="left", font=dict(color="Blue"))
        ])
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        fig.update_layout(width=800, height=700)
        st.plotly_chart(fig) 
        
        df = pd.DataFrame({'Parameter': ['Sill', 'Range', 'Nugget'], 'Value': [sill, range_, nugget]})
        st.table(df)
        
    
        # Write to the netcdf file 
    
    var_name = data_final[variable].name

    if data_final[variable].name == 'Total Rainfall':
        unit = 'mm'
    elif data_final[variable].name == 'Mean Maximum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Minimum Temperature':
        unit = '°C'
    elif data_final[variable].name == 'Mean Temperature':
        unit = '°C'
        
        
         
    ds_uk = xr.Dataset( data_vars= {var_name:(('Latitude', 'Longitude'), Uk_z), },
    coords={'Latitude':lats, 'Longitude':lons})
    
    if var_name == 'Total Rainfall':
        ds_uk[var_name] = ds_uk[var_name].clip(min=0)
    
    ds_uk[var_name].attrs = {'units':unit, 'long_name':var_name}
    
    ds_uk.Latitude.attrs['units'] = 'degrees_north'
    ds_uk.Latitude.attrs['long_name'] = 'latitude'
    ds_uk.Latitude.attrs['axis'] = 'Y'
    ds_uk.Longitude.attrs['units'] = 'degrees_east'
    ds_uk.Longitude.attrs['long_name'] = 'longitude'
    ds_uk.Longitude.attrs['axis'] = 'X'
    ds_uk.attrs = {'creation_date':datetime.now(), 
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
        
        c1= ds_uk[var_name].plot(ax=ax, 
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
                                vmin=ds_uk[var_name].min(), 
                                vmax=ds_uk[var_name].max()
                                )
        


        ax.set_xlabel('Longitude', fontsize=14)
        ax.set_ylabel('Latitude', fontsize=14)
            
        # Add a title
        ax.set_title(f'Interpolated {var_name} on Regular Grid Points', fontsize=18, y = 1.01)
    
        st.pyplot(fig)
        
        
    st.markdown("#### :blue[3) Extract into Ethiopian Domain]" )
                
    if ds_uk is None:
        st.error("Please perform interpolation first!")

    else:

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        # convert the geometry column to a list
        ethiopia_geometry_list = ethiopia.geometry.tolist()
        # Create the regionmask.Regions object using the list
        et_poly = regionmask.Regions(ethiopia_geometry_list)
        
        # Mask the data using the regionmask object
        et_mask = et_poly.mask(ds_uk.Longitude, ds_uk.Latitude)
        
        et_dsuk =  ds_uk.where(et_mask == 0)
        
        min_value = et_dsuk[var_name].min().values
        max_value = et_dsuk[var_name].max().values
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

        c1= et_dsuk[var_name].plot(ax=ax, 
                                cmap='viridis',
                                cbar_kwargs={"shrink": 0.8},
                                transform=ccrs.PlateCarree(), 
                                extend='both', 
                                alpha=1.0, 
                                #    edgecolors='black',
                                linewidths=0.5, 
                                antialiased=True, 
                                zorder=1, 
                                vmin=et_dsuk[var_name].min(), 
                                vmax=et_dsuk[var_name].max(),
                                levels=10)
                                

        ax.set_xlabel('Longitude', fontsize=14)
        ax.set_ylabel('Latitude', fontsize=14)
            
        # Add a title
        ax.set_title(f'Interpolated {var_name} on Regular Grid Points over Ethiopian Domain', fontsize=16, y = 1.01)

        st.pyplot(fig)
        
        
        
        
    st.markdown("#### :blue[4) Convet to NetcDF format]" )
    clicked = st.button("Convert to netCDF", key="nc1") 


    if clicked:  
        et_dsuk.attrs['creation_date'] = et_dsuk.attrs['creation_date'].isoformat()
        et_dsuk.to_netcdf(f'ds_{variable}_masked_uk.nc', engine='h5netcdf')
        #et_nnmask.to_netcdf(f'ds_{variable}_masked.nc')

        # Download the netCDF file
        with open(f"ds_{variable}_masked_uk.nc", "rb") as fp:
            btn = st.download_button(
                label="Download netCDF file",
                data=fp,
                file_name=f"ds_{variable}_masked_uk.nc",
            )
    
     
if __name__ == "__main__":
    inter_uk()