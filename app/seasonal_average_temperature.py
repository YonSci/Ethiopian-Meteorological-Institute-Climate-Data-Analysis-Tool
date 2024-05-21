import streamlit as st
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.colors as mcolors
import io


def seasonal_average_temperature():
    
    variable_type = st.session_state.get('variable_type', 'None')
    plot_type = st.session_state.get('plot_type', 'None')
    time_step = st.session_state.get('time_step', 'None')
    season = st.session_state.get('season', 'None')
    
    if plot_type == 'Departure of seasonal average temperature':
        
        if variable_type == 'Average temperature':
            variable = 'Mean Temperature'
            
            
        # Load the shapefile
        ethiopia = gpd.read_file('ethiopia/gadm36_ETH_0.shp')
        ethiopia_reg = gpd.read_file('ethiopia/gadm36_ETH_1.shp')
        
        
        st.markdown("#### :blue[Upload seasonal average temperature NetCDF File]" )
        uploaded_file = st.file_uploader("Choose a NetCDF file", 
                                        type=["nc"], key='uploaded_file2')
        if uploaded_file is not None:
        # Read the uploaded file
            f = xr.open_dataset(io.BytesIO(uploaded_file.read()))
            
            
        st.markdown("#### :blue[Upload LTM average temperature NetCDF File]" )
        uploaded_file = st.file_uploader("Choose a NetCDF file", 
                                        type=["nc"], key='uploaded_file3')
        if uploaded_file is not None:
        # Read the uploaded file
            z = xr.open_dataset(io.BytesIO(uploaded_file.read()))
            
             # Extract the variables
            var1 = f['t2m']
            var2 = z['t2m']
    
         
            # temp11 = var1.isel(time=0)
            # temp22 = var2.isel(time=0)
            
            var3  = var1 - var2
            
            lon = f['longitude'].values
            lat = f['latitude'].values
            
            
            
      
            data_min = var3.min()
            data_max = var3.max()
            
            # st.write(data_min.values)
            # st.write(data_max.values)
            
            

            # lon = f['Longitude'][:]
            # lat = f['Latitude'][:]
            
            # st.write(var2.shape)
            
 
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
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                bg_color = st.selectbox('Pick a background color', 
                                    ['white', 'lightgrey', 'lightblue', 'lightyellow', 'lightgreen', 'lightcoral'],
                                    index=0)
            
            with col2:
                title_font = st.selectbox('Enter a title font', 
                                        ['Arial', 
                                        'Times New Roman',
                                        'Courier New', 'Comic Sans MS', 'Impact'], index=0)
            with col3:
                dep = st.number_input("Enter value to classify as postive/negative departure:", value=-0.00)
         
            # Create custom colormap with user's selection
            cmap = plt.get_cmap(selected_colormap)

            # Define bins based on thresholds
            
            bins = [data_min, dep, data_max]
            
            


            st.markdown("---")

            st.markdown("#### :blue[Display seasonal departure average temperature from normal]" )  
            if f is not None:
                if st.checkbox("Plot seasonal departure average temperature from normal", key="_display"):
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

                    # Choose plotting method
                    if plot_type == "Contour":
                        contour = ax.contourf(lon, lat, var3, 
                                              levels=bins, 
                                              cmap=cmap, 
                                              extend=colorbar_extend.lower())

                        cbar = plt.colorbar(contour, 
                                            orientation=colorbar_orientation.lower(), 
                                            pad=colorbar_pad, 
                                            shrink=colorbar_shrink,
                                            aspect=aspect)
                        
                        cbar.set_label('Average temperature difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)
                        
                        cbar.set_ticks([-0.8, 0.5])
                        cbar.set_ticklabels(['Negative Departure', 'Postive Departure'],
                                            rotation=0)

               
        
                    elif plot_type == "Pcolormesh":
                        pcolormesh = ax.pcolormesh(lon, lat, var3,
                                                   cmap=cmap)
                        cbar = plt.colorbar(pcolormesh, 
                                            orientation=colorbar_orientation.lower(),
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        cbar.set_label('Average temperature difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)
                        

                    elif plot_type == "Scatter":
                        lon, lat = np.meshgrid(lon, lat)
                        scatter = ax.scatter(lon, lat, c=var3,
                                             cmap=cmap)
                        cbar = plt.colorbar(scatter, orientation=colorbar_orientation.lower(),
                                            pad=colorbar_pad, 
                                            aspect=aspect, 
                                            shrink=colorbar_shrink)
                        
                        cbar.set_label('Average temperature difference [-]', fontsize=12)
                        cbar.ax.xaxis.set_ticks_position('bottom')
                        cbar.ax.xaxis.set_label_position('bottom')
                        cbar.ax.tick_params(labelsize=10)
                        
                        #cbar.set_ticks([-0.8, 0.5])
                        #cbar.set_ticklabels(['Negative Departure', 'Postive Departure'],
                        #                    rotation=0)

                        

                    
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
                    ax.set_title(f' Departure of {season} average temperature from normal', fontsize=20, y=1.01, fontname=title_font)

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
            
    
    
    
    
    
if __name__ == '__main__':
    seasonal_average_temperature()