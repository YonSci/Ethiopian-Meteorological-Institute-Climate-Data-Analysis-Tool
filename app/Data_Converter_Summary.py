import streamlit as st

from app.daily_mon_con_sum_rf import daily_mon_con_sum_rf
from app.daily_mon_con_sum_tmax import daily_mon_con_sum_tmax
from app.daily_mon_con_sum_tmin import daily_mon_con_sum_tmin
from app.daily_mon_con_sum_tmean import daily_mon_con_sum_tmean


def Data_Converter_Summary():
    # blue, green, orange, red, violet, gray/grey, rainbow.
    st.title(':blue[Data Converter & Summary Statistics Module] 🖩')
    
        # Access the shared month value from session state
    month = st.session_state.get('month', 'Unknown Month')
    season = st.session_state.get('season', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')   
    
    variable_type = st.session_state.get('variable_type', 'None')
    timestep_analysis = st.session_state.get('timestep_analysis', 'None')
    
    variable_type2 = st.session_state.get('variable_type2', 'None')
    

    # Access the shared DataFrame from session state
    daily_rf = st.session_state.get('daily_rf', None)
    daily_max = st.session_state.get('daily_max', None)
    daily_min = st.session_state.get('daily_min', None)
    
    mon_rf = st.session_state.get('mon_rf', 'None')
    mon_max = st.session_state.get('mon_max', 'None')
    mon_min = st.session_state.get('mon_min', 'None')
    mon_mean = st.session_state.get('mon_mean', 'None')
    
    seas_rf = st.session_state.get('seas_rf', 'None')
    seas_max = st.session_state.get('seas_max', 'None')
    seas_min = st.session_state.get('seas_min', 'None')
    seas_mean = st.session_state.get('seas_mean', 'None')
    
    an_rf = st.session_state.get('an_rf', 'None')
    an_max = st.session_state.get('an_max', 'None')
    an_min = st.session_state.get('an_min', 'None')
    an_mean = st.session_state.get('an_mean', 'None')
    
    st.markdown("---")

    # calculation_rule = """
    #     <span style="color:blue">

    #     **Calculation Rules:**

    #     1. Monthly, seasonal, and annual values are calculated only when all daily data are available.

    #     2. In case of data scarcity, exceptions are made:

    #         a. For rainfall, monthly values will be calculated even if three-day values are missing.
            
    #         b. For temperature, monthly values will be calculated even if five-day values are missing.
             
    #         c. The mean monthly temperature is computed when there is available daily data for both maximum and minimum temperatures throughout a given month, meeting the criteria of the 5-day rule.
        
    #     </span>
    #     """
    
    info = """
    <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">

    <p>The Data Converter & Summary Statistics Module seamlessly transform and summarize meteorological data (Rainfall, Maximum Temperature, and Minimum Temperature.) This module offers a user-friendly interface to effortlessly handle the conversion of meteorological data.</p>

    <ol>
    <li><b>Data Conversion: Convert meteorological data across different time scales</b>
            
    <ul>
        <li>Daily to Monthly</li>
        <li>Monthly to Seasonal</li>
        <li>Seasonal to Annual</li>
    </ul>
    </li>
   
    <li><b>  Monthly, seasonal, and annual values are calculated only when all daily data are available.</b>
    </li>

    <li><b> In case of data scarcity, exceptions are made</b>
    <ul>
      
     <li>For rainfall, monthly values will be calculated even if three-day values are missing.</li>

     <li>For temperature, monthly values will be calculated even if five-day values are missing.</li>
     </ul>
    </li>

     <li><b>Generate interactive maps and insightful summary statistics (tabular & box plot) for each meteorological variable.</b>
            
    <li><b>Calculate Monthly Mean Temperature: Calculate the monthly mean temperature when the daily maximum and minimum temperature data is available, meeting the criteria of the 5-day rule.</b></li>
    </ol>
    </div>
    """

    st.markdown(info, unsafe_allow_html=True)
    #st.markdown("---")
    
    
    # Convert the daily data in monthly data frame 
    # Input:  daliy data of a given month daily_rf, daily_max, daily_min
    
    
    # Daily Data  
    
    month_to_number = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
    }

    Rainfall_mon = None  
    rainfall_mon_stat = None  
    
    if timestep_analysis == 'Daily' and variable_type == 'Rainfall':
        daily_mon_con_sum_rf(variable_type, daily_rf)
        
    elif timestep_analysis == 'Daily' and variable_type == 'Maximum Temperature':
        daily_mon_con_sum_tmax(variable_type, daily_max)
        
    elif timestep_analysis == 'Daily' and variable_type == 'Minimum Temperature':
        daily_mon_con_sum_tmin(variable_type, daily_min)
        
    elif timestep_analysis == 'Daily' and variable_type == 'Mean Temperature':
        daily_mon_con_sum_tmean(variable_type, daily_max, daily_min)
                        
            
    # elif timestep_analysis == 'Monthly' and variable_type is not None:
    #     st.write("Monthly Data:  Monthly to Seasonal Conversion") 
    #     st.write("Monthly Data:  Monthly to Annual Conversion") 

        
    # elif timestep_analysis == 'Seasonal' and variable_type is not None:
    #     st.write("Seasonal Data:  Seasonal to Annual Conversion") 
        
    # elif timestep_analysis == 'Annual' and variable_type is not None:
    #     st.write("Annual Data:  Other Stats")
    else:
        st.warning("No data to convert, Please load data in the Data Importing Page 😔") 
    

    
 
    
if __name__ == "__main__":
    Data_Converter_Summary()
    
     
    