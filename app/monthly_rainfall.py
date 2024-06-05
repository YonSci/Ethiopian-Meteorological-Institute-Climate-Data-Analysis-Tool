import streamlit as st
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.colors as mcolors
import netCDF4 as nc
import io


def monthly_rainfall():
    
    if 'month' not in st.session_state:
        st.session_state['month'] = 'None'
    
    variable_type = st.session_state.get('variable_type', 'None')
    plot_type = st.session_state.get('plot_type', 'None')
    time_step = st.session_state.get('time_step', 'None')
    month = st.session_state.get('month', 'None')
    
        
    
    
    
        
    if plot_type == 'Monthly Total Rainfall':
            
        if variable_type == 'Rainfall':
            variable = 'Total Rainfall'
        
            
        colormap_options = {
        "Viridis": "viridis",
        "Plasma": "plasma",
        "Inferno": "inferno",
        "Magma": "magma",
        "Cividis": "cividis",
        "Blues": "Blues",
        "YlGnBu": "YlGnBu",
        "PuBuGn": "PuBuGn"
        }
    
        lon = None
        lat = None
        rain = None
        ds = None
     

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        ethiopia_reg = gpd.read_file('ethiopia/gadm36_ETH_1.shp')
        
            
        st.markdown("---")
        
        st.markdown("#### :blue[Upload monthly rainfall NetCDF File]" )

        uploaded_file = st.file_uploader("Upload a NetCDF file")

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data.coords["Longitude"]
                    lat = data.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    rain = data[variable][:, :]
                   

                    # Get the min and max values of the variable
                    min_val = rain.min().values
                    max_val = rain.max().values

          

            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")



        st.markdown("---")
        
        st.markdown("#### :blue[Set Plotting Parameters]" )
            
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            plot_type = st.selectbox("Select a plot type", options=["Contour", "Pcolormesh", "Scatter"])

        with col2:
            selected_colormap = st.selectbox("Select a colormap", options=list(colormap_options.keys()))
        
        with col3:
            contour_levels = st.slider("Select contour levels", min_value=1, max_value=20, value=10)


        col1, col2, col3 = st.columns(3)
        
        with col1:
            colorbar_extend = st.selectbox("Colorbar Extension Style", options=["Both", "Neither"], index=1)

        with col2:
            colorbar_orientation = st.selectbox("Colorbar Orientation", options=["Horizontal", "Vertical"], index=1)

        with col3:
            colorbar_pad = st.slider("Colorbar Padding", min_value=0.0, max_value=1.0, value=0.01)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            colorbar_shrink = st.slider("Colorbar Shrink", min_value=0.0, max_value=1.0, value=0.8)

        with col2:
            aspect = st.number_input("Aspect Ratio", min_value=0, max_value=100, value=20)
        
        with col3:
            option = st.selectbox('Select region to plot', ('Country Boundary', 'Regional Boundary'))

        col1, col2 = st.columns(2)
        with col1:
            grid = st.checkbox('Show Grid', value=True)
        
        with col2:
            grid_interval = st.number_input('Grid Interval', min_value=0.0, max_value=5.0, value=1.0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            bg_color = st.selectbox('Pick a background color', 
                                ['white', 'lightgrey', 'lightblue', 'lightyellow', 'lightgreen', 'lightcoral'],
                                index=0)
        
        with col2:
            title_font = st.selectbox('Enter a title font', 
                                    ['Arial', 
                                    'Times New Roman',
                                    'Courier New', 'Comic Sans MS', 'Impact'], index=0)


        st.markdown("---")

        st.markdown("#### :blue[Display Monthly Rainfall]" )  
        if ds is not None:
            if st.checkbox("Plot Monthly Rainfall Data", key="_display"):
                fig, ax = plt.subplots(figsize=(12, 8), 
                                        subplot_kw={'projection': ccrs.PlateCarree()},
                                        #facecolor=bg_color,
                                        edgecolor='black')

                # Define min and max lat/lon for the plot
                min_lat, max_lat = 3.0, 15.0
                min_lon, max_lon = 33.0, 48.0

                # Set map extent
                ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

                # Add geographical features
                ax.add_feature(cfeature.COASTLINE)
                ax.add_feature(cfeature.LAND, edgecolor='black', color=bg_color)
                ax.add_feature(cfeature.OCEAN, edgecolor='black', color='lightblue')
                #ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=1.5)

                # Plot the selected region
                if option == 'Country Boundary':
                    ethiopia.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)
                elif option == 'Regional Boundary':
                    ethiopia_reg.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)

                # Contour plot with user-selected colormap
                cmap = colormap_options[selected_colormap]


                # Choose plotting method
                if plot_type == "Contour":
                    contour = ax.contourf(lon, lat, rain, 
                                            levels=np.linspace(min_val,
                                                               max_val, 
                                                               contour_levels),
                                            cmap=cmap, 
                                            extend=colorbar_extend.lower())
                    cbar = plt.colorbar(contour, orientation=colorbar_orientation.lower(), 
                                        pad=colorbar_pad, 
                                        aspect=aspect, 
                                        shrink=colorbar_shrink)
                elif plot_type == "Pcolormesh":
                    pcolormesh = ax.pcolormesh(lon, lat, rain, cmap=cmap)
                    cbar = plt.colorbar(pcolormesh, 
                                        orientation=colorbar_orientation.lower(),
                                        pad=colorbar_pad, aspect=aspect, 
                                        shrink=colorbar_shrink)
                elif plot_type == "Scatter":
                    lon, lat = np.meshgrid(lon, lat)
                    scatter = ax.scatter(lon, lat, c=rain, cmap=cmap)
                    cbar = plt.colorbar(scatter, orientation=colorbar_orientation.lower(),
                                        pad=colorbar_pad, 
                                        aspect=aspect, 
                                        shrink=colorbar_shrink)
                    
                cbar.set_label('Rainfall [mm]', fontsize=12)

                
                # Add gridlines with matched labels
                
                if grid:
                    # ax.set_xticks(np.arange(min_lon, max_lon + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                    # ax.set_yticks(np.arange(min_lat, max_lat + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                    gl = ax.gridlines(draw_labels=False, dms=False, x_inline=False, y_inline=False, linewidth=1, 
                                    color='gray', alpha=0.5, linestyle='--')
                    # gl.xlocator = plt.FixedLocator(np.arange(min_lon, max_lon + grid_interval, grid_interval))
                    # gl.ylocator = plt.FixedLocator(np.arange(min_lat, max_lat + grid_interval, grid_interval))
                    
                    xticks = np.clip(np.arange(min_lon, max_lon + grid_interval, grid_interval), min_lon, max_lon)
                    yticks = np.clip(np.arange(min_lat, max_lat + grid_interval, grid_interval), min_lat, max_lat)

                    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
                    ax.set_yticks(yticks, crs=ccrs.PlateCarree())

                    gl.xlocator = plt.FixedLocator(xticks)
                    gl.ylocator = plt.FixedLocator(yticks)
                    
                    
                    
                    
                    gl.top_labels = False
                    gl.right_labels = False
                    gl.xlabel_style = {'size': 12}
                    gl.ylabel_style = {'size': 12}

                # Add a title
                ax.set_title(f'Monthly {variable} during {month}', fontsize=20, y=1.01, fontname=title_font)

                ax.set_xlabel('Longitude', fontsize=14)
                ax.set_ylabel('Latitude', fontsize=14)

                plt.tight_layout()

                # Display the plot
                st.pyplot(fig)
                
                
                # Plotting
                def save_figure(fig):
                    # Save the figure to a bytes buffer
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    return buf

                # Save figure to buffer
                buf = save_figure(fig)

                # Download button
                st.download_button(
                    label="Download Plot as Image",
                    data=buf,
                    file_name=f"rainfall_plot_{variable_type}_{time_step}.png",
                    mime="image/png"
                )
        
            
        # elif plot_type == 'Percent of Normal Rainfall':
        #     st.write('Percent of Normal Rainfall')

        # elif plot_type == 'Departure of Monthly Total Rainfall':
        #     st.write('Departure of Monthly Total Rainfall')
      
            
    if plot_type == 'Percent of Normal Rainfall':
        st.latex(r"PoN = \frac{Rainfall - Mean}{Std Deviation} \times 100")
        
        if variable_type == 'Rainfall':
            variable = 'Total Rainfall'
        elif variable_type == 'Maximum Temperature':
            variable = 'Mean Maximum Temperature'
        elif variable_type == 'Minimum Temperature':
            variable = 'Mean Minimum Temperature'
        elif variable_type == 'Average temperature':
            variable = 'Mean Temperature'
            
            
        colormap_options = {
        "Viridis": "viridis",
        "Plasma": "plasma",
        "Inferno": "inferno",
        "Magma": "magma",
        "Cividis": "cividis",
        "Blues": "Blues",
        "YlGnBu": "YlGnBu",
        "PuBuGn": "PuBuGn"
        }
    
    

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        ethiopia_reg = gpd.read_file('ethiopia/gadm36_ETH_1.shp')


        var1 = var2 = var3 = None  # Initialize the variables

        
        st.markdown("#### :blue[Upload monthly rainfall NetCDF File]" )
        uploaded_file = st.file_uploader("Upload a NetCDF file", key='uploaded_file2')

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data_t = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data_t.coords["Longitude"]
                    lat = data_t.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    var1 = data_t[variable][:, :]

                    # st.write(var1.shape)
                   

                    # Get the min and max values of the variable
                    min_val1 = var1.min().values
                    max_val1 = var1.max().values


            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")


                    
        
        st.markdown("#### :blue[Upload monthly long term mean rainfall NetCDF File]" )

        uploaded_file = st.file_uploader("Upload a NetCDF file",  key='uploaded_file3')

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data_ltm = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data_ltm.coords["Longitude"]
                    lat = data_ltm.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    var2 = data_ltm[variable][:, :]
                   

                    # Get the min and max values of the variable
                    min_val2 = var2.min().values
                    max_val2 = var2.max().values


            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")

        
                
        st.markdown("#### :blue[Upload monthly long term Std deviation rainfall NetCDF File]" )

        uploaded_file = st.file_uploader("Upload a NetCDF file", key='uploaded_file4')

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data_std = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data_std.coords["Longitude"]
                    lat = data_std.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    var3 = data_std[variable][:, :]
                   

                    # Get the min and max values of the variable
                    min_val3 = var3.min().values
                    max_val3 = var3.max().values


            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")
            
            st.markdown("---")

    

        # Calculate departure, intermediate, and percentage normal rainfall

        if var1 is not None and var2 is not None and var3 is not None:

            var11= var1.isel(time=0)
            var22 = var2.isel(time=0)
            var33 = var3.isel(time=0)

            dep_rain = var11 - var22
            inter_rain = dep_rain / var33
            pn_rain = inter_rain * 100

            # lon = ds['lon'].values
            # lat = ds['lat'].values
            
            # Define the levels and colormap
            levels = [0, 75, 125, 300]
            
            
            st.markdown("#### :blue[Set Plotting Parameters]" )
                
            col1, col2, col3 = st.columns(3)
            
            with col1: 
                plot_type = st.selectbox("Select a plot type", options=["Contour", "Pcolormesh", "Scatter"])
                
            with col2:
                selected_colormap = st.selectbox("Select a colormap", options=list(colormap_options.keys()))

            with col3:
                colorbar_orientation = st.selectbox("Colorbar Orientation", options=["Horizontal", "Vertical"], index=1)

         
            col1, col2, col3 = st.columns(3)
            
            with col1:
                colorbar_pad = st.slider("Colorbar Padding", min_value=0.0, max_value=1.0, value=0.01)

            with col2:
                colorbar_shrink = st.slider("Colorbar Shrink", min_value=0.0, max_value=1.0, value=0.8)

            with col3:
                aspect = st.number_input("Aspect Ratio", min_value=0, max_value=100, value=20)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                option = st.selectbox('Select region to plot', ('Country Boundary', 'Regional Boundary'))

            with col2:
                grid = st.checkbox('Show Grid', value=True)
            
            with col3:
                grid_interval = st.number_input('Grid Interval', min_value=0.0, max_value=5.0, value=1.0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                bg_color = st.selectbox('Pick a background color', 
                                    ['white', 'lightgrey', 'lightblue', 'lightyellow', 'lightgreen', 'lightcoral'],
                                    index=0)
            
            with col2:
                title_font = st.selectbox('Enter a title font', 
                                        ['Arial', 
                                        'Times New Roman',
                                        'Courier New', 'Comic Sans MS', 'Impact'], index=0)
          

            cmap = colormap_options[selected_colormap]
            cmap = plt.get_cmap(cmap, len(levels) - 1)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=False)
            
            st.markdown("---")

            st.markdown("#### :blue[Display Percent of Noraml Rainfall]" )  
            if data_t and data_ltm and data_std is not None:
                if st.checkbox("Plot Percent of Normal Rainfall Data", key="_display"):
                    fig, ax = plt.subplots(figsize=(12, 8), 
                                            subplot_kw={'projection': ccrs.PlateCarree()},
                                            #facecolor=bg_color,
                                            edgecolor='black')

                    # Define min and max lat/lon for the plot
                    min_lat, max_lat = 3.0, 15.0
                    min_lon, max_lon = 33.0, 48.0

                    # Set map extent
                    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

                    # Add geographical features
                    ax.add_feature(cfeature.COASTLINE)
                    ax.add_feature(cfeature.LAND, edgecolor='black', color=bg_color)
                    ax.add_feature(cfeature.OCEAN, edgecolor='black', color='lightblue')

                    # Plot the selected region
                    if option == 'Country Boundary':
                        ethiopia.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)
                    elif option == 'Regional Boundary':
                        ethiopia_reg.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)


                    if plot_type == "Contour":
                        contour = ax.contourf(lon, lat, pn_rain, 
                                              levels=levels, 
                                              cmap=cmap, 
                                              norm=norm, 
                                              extend='both')
                        
                        
                        cbar = plt.colorbar(contour, 
                                            orientation=colorbar_orientation.lower(), 
                                        pad=colorbar_pad, 
                                        aspect=aspect, 
                                        shrink=colorbar_shrink)

                        # Custom ticks and labels
                        cbar.set_ticks([37.5, 100, 212.5])  # Midpoints of the intervals
                        cbar.set_ticklabels(['<75%', '75-125%', '>125%'])

                        # Set colorbar label
                        cbar.set_label('[%]', fontsize=12)
                        
                      
                    elif plot_type == "Pcolormesh":
                        pcolormesh = ax.pcolormesh(lon, 
                                                   lat, 
                                                   pn_rain, 
                                                   cmap=cmap,
                                                   norm=norm)   
                        cbar = plt.colorbar(pcolormesh, 
                                            orientation=colorbar_orientation.lower(), 
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        cbar.set_ticks([37.5, 100, 212.5])  # Midpoints of the intervals
                        cbar.set_ticklabels(['<75%', '75-125%', '>125%'])

                        # Set colorbar label
                        cbar.set_label('[%]', fontsize=12)
                
                    elif plot_type == "Scatter":
                        lon, lat = np.meshgrid(lon, lat)
                        scatter = ax.scatter(lon, lat, c=pn_rain, cmap=cmap, norm=norm)
                        cbar = plt.colorbar(scatter, 
                                            orientation=colorbar_orientation.lower(),
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        
                        cbar.set_ticks([37.5, 100, 212.5])  # Midpoints of the intervals
                        cbar.set_ticklabels(['<75%', '75-125%', '>125%'])

                        # Set colorbar label
                        cbar.set_label('[%]', fontsize=12)
                        
                        #cbar.set_label('[%]', fontsize=12)

                    
                    # Add gridlines with matched labels
                    
                    if grid:
                        # ax.set_xticks(np.arange(min_lon, max_lon + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                        # ax.set_yticks(np.arange(min_lat, max_lat + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                        gl = ax.gridlines(draw_labels=False, dms=False, x_inline=False, y_inline=False, linewidth=1, 
                                        color='gray', alpha=0.5, linestyle='--')
                        # gl.xlocator = plt.FixedLocator(np.arange(min_lon, max_lon + grid_interval, grid_interval))
                        # gl.ylocator = plt.FixedLocator(np.arange(min_lat, max_lat + grid_interval, grid_interval))
                        
                        xticks = np.clip(np.arange(min_lon, max_lon + grid_interval, grid_interval), min_lon, max_lon)
                        yticks = np.clip(np.arange(min_lat, max_lat + grid_interval, grid_interval), min_lat, max_lat)

                        ax.set_xticks(xticks, crs=ccrs.PlateCarree())
                        ax.set_yticks(yticks, crs=ccrs.PlateCarree())

                        gl.xlocator = plt.FixedLocator(xticks)
                        gl.ylocator = plt.FixedLocator(yticks)
                        
                        gl.top_labels = False
                        gl.right_labels = False
                        gl.xlabel_style = {'size': 12}
                        gl.ylabel_style = {'size': 12}

                    ax.set_title(f'Percent of Normal Rainfall during {month}', fontsize=20, y=1.01, fontname=title_font)

                    ax.set_xlabel('Longitude', fontsize=14)
                    ax.set_ylabel('Latitude', fontsize=14)

                    plt.tight_layout()

                    # Display the plot
                    st.pyplot(fig)
                    
                    
                               # Plotting
                    def save_figure(fig):
                        # Save the figure to a bytes buffer
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        return buf

                    # Save figure to buffer
                    buf = save_figure(fig)

                    # Download button
                    st.download_button(
                        label="Download Plot as Image",
                        data=buf,
                        file_name=f"PNR_plot_{variable_type}_{time_step}.png",
                        mime="image/png"
                    )
             
                    
    var4 = var5 = None  # Initialize the variables
          
    
    if plot_type == 'Departure of Monthly Total Rainfall':
        if variable_type == 'Rainfall':
            variable = 'Total Rainfall'

                    
        # divergent_colormaps = [
        # 'RdYlBu', 
        # 'Spectral', 
        # 'coolwarm',
        # 'bwr', 
        # 'seismic', 
        # 'PiYG',
        # 'PRGn', 
        # 'BrBG', 
        # 'RdGy', 
        # 'RdBu', 
        # 'RdYlGn'
        # ]
            
            

        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        ethiopia_reg = gpd.read_file('ethiopia/gadm36_ETH_1.shp')
        
        
        st.markdown("#### :blue[Upload monthly rainfall NetCDF File]" )

        uploaded_file = st.file_uploader("Upload a NetCDF file",  key='uploaded_file5')

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data_current = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data_current.coords["Longitude"]
                    lat = data_current.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    var4 = data_current[variable][:, :]
                   

                    # Get the min and max values of the variable
                    min_val4 = var4.min().values
                    max_val4 = var4.max().values


            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")


   
            
        st.markdown("#### :blue[Upload previous year rainfall NetCDF File]" )

        uploaded_file = st.file_uploader("Upload a NetCDF file",  key='uploaded_file6')

        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Convert the uploaded file to BytesIO
                file = io.BytesIO(uploaded_file.read())
                
                # Use netCDF4 to read the file
                with nc.Dataset('dummy', mode='r', memory=file.read()) as ds:
                    # Convert netCDF4 dataset to xarray Dataset
                    data_pre = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

                    # Get latitude and longitude variables
                    lon = data_pre.coords["Longitude"]
                    lat = data_pre.coords["Latitude"]

                    # Get the variable using netCDF4 dataset

                    var5 = data_pre[variable][:, :]
                

                    # Get the min and max values of the variable
                    min_val5 = var5.min().values
                    max_val5 = var5.max().values


            except Exception as e:
                st.error(f"Error opening dataset: {e}")
        else:
            st.info("Please upload a NetCDF file.")
            
            #  # Extract the variables
            # var1 = ds['rfe']
            # var2 = ds_pre['rfe']

        if var4 is not None and var5 is not None:

            rain44 = var4.isel(time=0)
            rain55 = var5.isel(time=0)
          

            var66  = rain44 - rain55


            # lon = ds['lon'].values
            # lat = ds['lat'].values
            
            data_min = var66.min().values
            data_max = var66.max().values
            
           
            
            
            st.markdown("---")
        
            st.markdown("#### :blue[Set Plotting Parameters]" )
                
            col1, col2, col3 = st.columns(3)
            
            with col1: 
                plot_type = st.selectbox("Select a plot type", options=["Contour", "Pcolormesh", "Scatter"])

            with col2:
                # selected_colormap  = st.selectbox("Select a colormap", divergent_colormaps)
                colormap_options = sorted(m for m in plt.colormaps() if not m.endswith("_r"))  # Avoid reversed colormaps
                selected_colormap = st.selectbox("Please select a colormap:", colormap_options)

            with col3:
                contour_levels = st.slider("Select contour levels", min_value=1, max_value=20, value=10)


            col1, col2, col3 = st.columns(3)
            
            with col1:
                colorbar_extend = st.selectbox("Colorbar Extension Style", options=["Both", "Neither"], index=1)

            with col2:
                colorbar_orientation = st.selectbox("Colorbar Orientation", options=["Horizontal", "Vertical"], index=1)

            with col3:
                colorbar_pad = st.slider("Colorbar Padding", min_value=0.0, max_value=1.0, value=0.01)

            col1, col2, col3 = st.columns(3)
            
            with col1:
                colorbar_shrink = st.slider("Colorbar Shrink", min_value=0.0, max_value=1.0, value=0.8)

            with col2:
                aspect = st.number_input("Aspect Ratio", min_value=0, max_value=100, value=20)
            
            with col3:
                option = st.selectbox('Select region to plot', ('Country Boundary', 'Regional Boundary'))

            col1, col2 = st.columns(2)
            with col1:
                grid = st.checkbox('Show Grid', value=True)
            
            with col2:
                grid_interval = st.number_input('Grid Interval', min_value=0.0, max_value=5.0, value=1.0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                bg_color = st.selectbox('Pick a background color', 
                                    ['white', 'lightgrey', 'lightblue', 'lightyellow', 'lightgreen', 'lightcoral'],
                                    index=0)
            
            with col2:
                title_font = st.selectbox('Enter a title font', 
                                        ['Arial', 
                                        'Times New Roman',
                                        'Courier New', 'Comic Sans MS', 'Impact'], index=0)
            col1, col2 = st.columns(2)
            
            with col1:
                    dry_threshold = st.number_input("Enter the value below which it is classified as Drier than last year:", value=-25)
            with col2:
                wet_threshold = st.number_input("Enter the value above which it is classified as Wetter than last year:", value=25)

                
                
            if dry_threshold >= wet_threshold:
                st.error("Dry threshold must be less than wet threshold. Please adjust the values.")

                # Create custom colormap with distinct colors
            # colors = ['royalblue', 'lightgrey', 'darkorange']  # Adjust colors as desired
            # cmap = ListedColormap(colors)

            # # Define bins based on data min/max and thresholds
            # bins = [data_min, dry_threshold, wet_threshold, data_max]
            
            
            # Create custom colormap with user's selection
            cmap = plt.get_cmap(selected_colormap)

            # Define bins based on thresholds
            bins = [data_min, dry_threshold, wet_threshold, data_max]

            st.markdown("---")

            st.markdown("#### :blue[Display Departure of Monthly Rainfall ]" )  
            if ds is not None:
                if st.checkbox("Plot Monthly Departure of Rainfall", key="_display"):
                    fig, ax = plt.subplots(figsize=(12, 8), 
                                            subplot_kw={'projection': ccrs.PlateCarree()},
                                            #facecolor=bg_color,
                                            edgecolor='black')

                    # Define min and max lat/lon for the plot
                    min_lat, max_lat = 3.0, 15.0
                    min_lon, max_lon = 33.0, 48.0

                    # Set map extent
                    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

                    # Add geographical features
                    ax.add_feature(cfeature.COASTLINE)
                    ax.add_feature(cfeature.LAND, edgecolor='black', color=bg_color)
                    ax.add_feature(cfeature.OCEAN, edgecolor='black', color='lightblue')
                    # ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=1.5)

                    # Plot the selected region
                    if option == 'Country Boundary':
                        ethiopia.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)
                    elif option == 'Regional Boundary':
                        ethiopia_reg.plot(ax=ax, color='None', edgecolor='black', linewidth=1.5, zorder=2)

                    # Choose plotting method
                    if plot_type == "Contour":
                        contour = ax.contourf(lon, lat, var66, 
                                                levels=bins, 
                                                cmap=cmap, 
                                                extend=colorbar_extend.lower())

                        cbar = plt.colorbar(contour, 
                                            orientation=colorbar_orientation.lower(), 
                                            pad=colorbar_pad, 
                                            shrink=colorbar_shrink,
                                            aspect=aspect)
                        
                        cbar.set_label('Rainfall Difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)

                        # Set colorbar ticks and labels
                        cbar.set_ticks([-75, 0, 75])
                        cbar.set_ticklabels(['Below Normal', 'Normal', 'Above Normal'])
                        
                        
                        
                    elif plot_type == "Pcolormesh":
                        pcolormesh = ax.pcolormesh(lon, lat, var66, 
                                                    cmap=cmap)
                        cbar = plt.colorbar(pcolormesh, 
                                            orientation=colorbar_orientation.lower(),
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        cbar.set_label('Rainfall Difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)

                        # Set colorbar ticks and labels
                        cbar.set_ticks([-75, 0, 75])
                        cbar.set_ticklabels(['Below Normal', 'Normal', 'Above Normal'])
                        
                        
                    elif plot_type == "Scatter":
                        lon, lat = np.meshgrid(lon, lat)
                        scatter = ax.scatter(lon, lat, c=var66,
                                                cmap=cmap)
                        cbar = plt.colorbar(scatter, orientation=colorbar_orientation.lower(),
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        cbar.set_label('Rainfall Difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)

                        # Set colorbar ticks and labels
                        cbar.set_ticks([-75, 0, 75])
                        cbar.set_ticklabels(['Below Normal', 'Normal', 'Above Normal'])
                        
                        

                    
                    # Add gridlines with matched labels
                    
                    if grid:
                        # ax.set_xticks(np.arange(min_lon, max_lon + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                        # ax.set_yticks(np.arange(min_lat, max_lat + grid_interval, grid_interval), crs=ccrs.PlateCarree())
                        gl = ax.gridlines(draw_labels=False, dms=False, x_inline=False, y_inline=False, linewidth=1, 
                                        color='gray', alpha=0.5, linestyle='--')
                        # gl.xlocator = plt.FixedLocator(np.arange(min_lon, max_lon + grid_interval, grid_interval))
                        # gl.ylocator = plt.FixedLocator(np.arange(min_lat, max_lat + grid_interval, grid_interval))
                        
                        xticks = np.clip(np.arange(min_lon, max_lon + grid_interval, grid_interval), min_lon, max_lon)
                        yticks = np.clip(np.arange(min_lat, max_lat + grid_interval, grid_interval), min_lat, max_lat)

                        ax.set_xticks(xticks, crs=ccrs.PlateCarree())
                        ax.set_yticks(yticks, crs=ccrs.PlateCarree())

                        gl.xlocator = plt.FixedLocator(xticks)
                        gl.ylocator = plt.FixedLocator(yticks)
                        
                        
                        
                        
                        gl.top_labels = False
                        gl.right_labels = False
                        gl.xlabel_style = {'size': 12}
                        gl.ylabel_style = {'size': 12}

                    # Add a title
                    ax.set_title(f'Departure of {month} rainfall from previous year', fontsize=20, y=1.01, fontname=title_font)

                    ax.set_xlabel('Longitude', fontsize=14)
                    ax.set_ylabel('Latitude', fontsize=14)

                    plt.tight_layout()

                    # Display the plot
                    st.pyplot(fig)
                    
                        # Plotting
                    def save_figure(fig):
                        # Save the figure to a bytes buffer
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        return buf

                    # Save figure to buffer
                    buf = save_figure(fig)

                    # Download button
                    st.download_button(
                        label="Download Plot as Image",
                        data=buf,
                        file_name=f"Departure_plot_{variable_type}_{time_step}.png",
                        mime="image/png"
                    )
                
                
                
        
    if __name__ == "__main__":
        monthly_rainfall()   
