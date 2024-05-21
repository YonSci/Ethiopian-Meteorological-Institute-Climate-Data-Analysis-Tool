
import streamlit as st

from app.daily_indices_calculator_rf import daily_indices_calculator_rf
from app.daily_indices_calculator_tmax import daily_indices_calculator_tmax
from app.daily_indices_calculator_tmin import daily_indices_calculator_tmin
from app.daily_indices_calculator_tmean import daily_indices_calculator_tmean
from app.monthly_indices_calculator_rf import monthly_indices_calculator_rf
from app.monthly_indices_calculator_tmax import monthly_indices_calculator_tmax 
from app.monthly_indices_calculator_tmin import monthly_indices_calculator_tmin
from app.seasonal_indices_calculator_rf import seasonal_indices_calculator_rf
from app.seasonal_indices_calculator_tmax import seasonal_indices_calculator_tmax
from app.seasonal_indices_calculator_tmin import seasonal_indices_calculator_tmin
from app.annual_indices_calculator_rf import annual_indices_calculator_rf
from app.annual_indices_calculator_tmax import annual_indices_calculator_tmax
from app.annual_indices_calculator_tmin import annual_indices_calculator_tmin



def Indices_Calculator():
    # blue, green, orange, red, violet, gray/grey, rainbow.
    st.title(':blue[Indices Calculator Module] ')
    
    info = """
    <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
   
    This module offers an intuitive and interactive platform for exploring rainfall, maximum, minimum, and average temperature data. The output includes a table showing each station, a downloadable CSV file of the data, and a map showing the locations of the stations.
    
    **Rainfall Threshold**: This analysis identifies and visualizes rainfall stations that recorded rainfall above a user-selected threshold. 
    
    **Number of Rainy Days**: This analysis calculates and visualizes the number of rainy days in a selected month. 
    
    **Maximum temperature**: This analysis identifies and visualizes temperature stations that recorded maximum temperature above a user-selected threshold.
    
    **Minimum temperature**: This analysis identifies and visualizes temperature stations that recorded minimum temperature below a user-selected threshold. 
    
    **Mean temperature**: This analysis identifies and visualizes temperature stations that recorded mean temperature below a user-selected threshold.   
     </div>
    """
    
    st.markdown(info, unsafe_allow_html=True)
    st.markdown("---")
    
    variable_type = st.session_state.get('variable_type', None)
    timestep_analysis = st.session_state.get('timestep_analysis', None)
    
    # Access the shared DataFrame from session state daily 
    daily_rf = st.session_state.get('daily_rf', None)
    daily_max = st.session_state.get('daily_max', None)
    daily_min = st.session_state.get('daily_min', None)
    
    # Access the shared DataFrame from session state monthly 
    mon_rf = st.session_state.get('mon_rf', None)
    mon_max = st.session_state.get('mon_max', None)
    mon_min = st.session_state.get('mon_min', None)
    mon_mean = st.session_state.get('mon_mean', None)
    
    seas_rf = st.session_state.get('seas_rf', None)
    seas_max = st.session_state.get('seas_max', None)
    seas_min = st.session_state.get('seas_min', None)
    seas_mean = st.session_state.get('seas_mean', None)

    an_rf = st.session_state.get('an_rf', None)
    an_max = st.session_state.get('an_max', None)
    an_min = st.session_state.get('an_min', None)
    an_mean = st.session_state.get('an_mean', None)
    
    
    # Daily Data   
    if timestep_analysis == 'Daily' and variable_type == 'Rainfall':
        daily_indices_calculator_rf(variable_type, daily_rf)
    
    elif timestep_analysis == 'Daily' and variable_type == 'Maximum Temperature':
        daily_indices_calculator_tmax(variable_type, daily_max)
    
    elif timestep_analysis == 'Daily' and variable_type == 'Minimum Temperature':
        daily_indices_calculator_tmin(variable_type, daily_min)
        
    elif timestep_analysis == 'Daily' and variable_type == 'Mean Temperature':
        daily_indices_calculator_tmean(variable_type, daily_min)
        
        
    # Monthly Data
    elif timestep_analysis == 'Monthly' and variable_type == 'Rainfall':
        monthly_indices_calculator_rf(variable_type, mon_rf)
    elif timestep_analysis == 'Monthly' and variable_type == 'Maximum Temperature':
        monthly_indices_calculator_tmax(variable_type, mon_max)
    elif timestep_analysis == 'Monthly' and variable_type == 'Minimum Temperature':
        monthly_indices_calculator_tmin(variable_type, mon_min)
        
    # Seasonal Data
    elif timestep_analysis == 'Seasonal' and variable_type == 'Rainfall':
        seasonal_indices_calculator_rf(variable_type, seas_rf)
    elif timestep_analysis == 'Seasonal' and variable_type == 'Maximum Temperature':
        seasonal_indices_calculator_tmax(variable_type, seas_max)
    elif timestep_analysis == 'Seasonal' and variable_type == 'Minimum Temperature':
        seasonal_indices_calculator_tmin(variable_type, seas_min)
        
    # Annual Data
    elif timestep_analysis == 'Annual' and variable_type == 'Rainfall':
        annual_indices_calculator_rf(variable_type, an_rf)
    elif timestep_analysis == 'Annual' and variable_type == 'Maximum Temperature':
        annual_indices_calculator_tmax(variable_type, an_max)
    elif timestep_analysis == 'Annual' and variable_type == 'Minimum Temperature':
        annual_indices_calculator_tmin(variable_type, an_min)
 
        
if __name__ == "__main__":
    Indices_Calculator()
    
    
    
    
    
    
   