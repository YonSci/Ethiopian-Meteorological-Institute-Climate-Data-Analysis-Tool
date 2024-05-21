import streamlit as st
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import geopandas as gpd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from PIL import Image
import base64
import io
from matplotlib.ticker import FixedLocator


from app.monthly_rainfall import monthly_rainfall
from app.monthly_maximum_temperature import monthly_maximum_temperature
from app.monthly_minimum_temperature import monthly_minimum_temperature
from app.monthly_average_temperature import monthly_average_temperature

from app.seasonal_rainfall import seasonal_rainfall
from app.seasonal_maximum_temperature import seasonal_maximum_temperature
from app.seasonal_minimum_temperature import seasonal_minimum_temperature
from app.seasonal_average_temperature import seasonal_average_temperature

from app.annual_rainfall import annual_rainfall
from app.annual_maximum_temperature import annual_maximum_temperature
from app.annual_minimum_temperature import annual_minimum_temperature
from app.annual_average_temperature import annual_average_temperature





def Mapping_module():
    # blue, green, orange, red, violet, gray/grey, rainbow.
    st.title(':blue[Mapping Module]  🌍')
    
    info = """ 
    
        <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
        
        <p>This module is designed to seamlessly generate vital maps for EMI climate bulletins (monthly, seasonal, or annual). Users have the flexibility to choose from a range of climate variables, including rainfall, minimum temperature, maximum temperature, and average temperature, and specify their desired time period. 
        
        Utilizing these selections, the module can produce comprehensive maps for **total rainfall**, **minimum temperature**, **maximum temperature**, **percent of normal rainfall**, **rainfall departure**, and **average temperature departure** maps. 
        
        It enables to customize maps by adjusting a variety of plotting parameters, encompassing plot type, colormap, color bar options (such as padding, orientation, shrink, and aspect ratio), select region, grid settings, background color, and fonts. Users need to upload the climate data in the NetCDF file format from the previous analysis. After the maps are generated, they can be effortlessly saved to a local drive.</p>

        
        </div> 
    
    
    """
    
    st.markdown(info, unsafe_allow_html=True)
    
    
    
    
    
    
    st.markdown("---")

    st.markdown("#### :blue[Select variable and plot type]" )

    col1, col2 = st.columns(2)
    with col1:
        variable_type = st.selectbox('Select variable type', ('None',
                                                              'Rainfall', 
                                                          'Maximum Temperature', 
                                                          'Minimum Temperature',
                                                          'Average temperature'))
        st.info("You selected: " + variable_type)
        st.session_state.variable_type = variable_type
        
    with col2:
        time_step = st.selectbox('Select time step', ('None',
                                                      'Monthly', 
                                                      'Seasonal', 
                                                      'Annual'), key='time_step', index=0)
        st.info("You selected: " + time_step)
        
        
    # Monthly   
    
    if variable_type == 'Rainfall'and time_step == 'Monthly':
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.month = st.selectbox("Choose a month",
            ("January", "February", "March", "April", "May", "June", 
             "July", "August", "September", "October", "November", "December"),
            key="list_month_d1")
            
            st.info("You selected: " + st.session_state.month)
            
          
            
        with col2:    
            plot_type =  st.selectbox('Select plot type', (
                'None',
                'Monthly Total Rainfall',
                'Percent of Normal Rainfall',
                'Departure of Monthly Total Rainfall'), 
                                    key='plot_type1', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        monthly_rainfall()
        
        
        
    elif variable_type == 'Maximum Temperature'and time_step == 'Monthly':
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.month = st.selectbox("Choose a month",
            ("January", "February", "March", "April", "May", "June", 
             "July", "August", "September", "October", "November", "December"),
            key="list_month_d2")
            
            st.info("You selected: " + st.session_state.month)
            
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean maximum temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        monthly_maximum_temperature()
        
        
        
        
    elif variable_type == 'Minimum Temperature'and time_step == 'Monthly':
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.month = st.selectbox("Choose a month",
            ("January", "February", "March", "April", "May", "June", 
             "July", "August", "September", "October", "November", "December"),
            key="list_month_d3")
            
            st.info("You selected: " + st.session_state.month)
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean minimum temperature',), 
                                    key='plot_type3', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        monthly_minimum_temperature()
        
        
    elif variable_type == 'Average temperature'and time_step == 'Monthly':
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.month = st.selectbox("Choose a month",
            ("January", "February", "March", "April", "May", "June", 
             "July", "August", "September", "October", "November", "December"),
            key="list_month_d4")
            
            st.info("You selected: " + st.session_state.month)
            
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Departure of monthly average temperature',), 
                                    key='plot_type4', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        monthly_average_temperature()
        
        
    # Seasonal
            
    elif variable_type == 'Rainfall'and time_step == 'Seasonal':
        
        col1, col2 = st.columns(2)
        
        with col1:
            season = st.selectbox(
                        "Choose a Seasons",
                        ("None", "Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            st.session_state.season = season
            
            st.info("You selected: " + season)
        
        with col2:
            plot_type = st.selectbox('Select plot type', ('Seasonal Total Rainfall',
                                            'Seasonal Percent of Normal Rainfall',
                                            'Departure of Seasonal Total Rainfall'))
            
            st.session_state.plot_type = plot_type
            
            st.info("You selected: " + plot_type)
        seasonal_rainfall()
        
    
    elif variable_type == 'Maximum Temperature'and time_step == 'Seasonal':
        col1, col2 = st.columns(2)
        
        with col1:
            season = st.selectbox(
                        "Choose a Seasons",
                        ("None", "Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            st.session_state.season = season
            
            st.info("You selected: " + season)
        
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean maximum temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        seasonal_maximum_temperature()
        
        
    elif variable_type == 'Minimum Temperature'and time_step == 'Seasonal':
        col1, col2 = st.columns(2)
        
        with col1:
            season = st.selectbox(
                        "Choose a Seasons",
                        ("None", "Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            st.session_state.season = season
            
            st.info("You selected: " + season)
        
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean minimum temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        seasonal_minimum_temperature()
        
        
    elif variable_type == 'Average temperature'and time_step == 'Seasonal':
        col1, col2 = st.columns(2)
        
        with col1:
            season = st.selectbox(
                        "Choose a Seasons",
                        ("None", "Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            st.session_state.season = season
            
            st.info("You selected: " + season)
        
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Departure of seasonal average temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        seasonal_average_temperature()        
    
    # Annual        
    elif  variable_type == 'Rainfall'and time_step == 'Annual':
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_d")
            st.session_state.year = year
            st.success(f'You selected: {year}')
            
        with col2:
            plot_type = st.selectbox('Select plot type', ('Annual Total Rainfall',
                                            'Annual Percent of Normal Rainfall',
                                            'Departure of Annual Total Rainfall'))
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
            
        annual_rainfall()
        

    elif variable_type == 'Maximum Temperature'and time_step == 'Annual':
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_d")
            st.session_state.year = year
            st.success(f'You selected: {year}')
            
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean maximum temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        annual_maximum_temperature()
        
        
        
  
    elif variable_type == 'Minimum Temperature'and time_step == 'Annual':
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_d")
            st.session_state.year = year
            st.success(f'You selected: {year}')
            
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Mean minimum temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        annual_minimum_temperature()
        
        
    
    
    elif variable_type == 'Average temperature'and time_step == 'Annual':
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_d")
            st.session_state.year = year
            st.success(f'You selected: {year}')
            
        with col2:
            plot_type =  st.selectbox('Select plot type', (
            'None',
            'Departure of anuual average temperature',), 
                                    key='plot_type2', index=0)
            st.session_state.plot_type = plot_type
            st.info("You selected: " + plot_type)
        annual_average_temperature()  
    
            
            
  
if __name__ == "__main__":
    Mapping_module()    