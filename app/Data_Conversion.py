import streamlit as st

from app.daily_mon_con_sum_rf import daily_mon_con_sum_rf
from app.daily_mon_con_sum_tmax import daily_mon_con_sum_tmax
from app.daily_mon_con_sum_tmin import daily_mon_con_sum_tmin
from app.daily_mon_con_sum_tmean import daily_mon_con_sum_tmean

from app.Monthly_to_Seasonal_rf import Monthly_to_Seasonal_rf
from app.Monthly_to_Seasonal_tmax import Monthly_to_Seasonal_tmax
from app.Monthly_to_Seasonal_tmin import Monthly_to_Seasonal_tmin
from app.Monthly_to_Seasonal_tmean import Monthly_to_Seasonal_tmean

from app.Monthly_to_Annual_rf import Monthly_to_Annual_rf
from app.Monthly_to_Annual_tmax import Monthly_to_Annual_tmax
from app.Monthly_to_Annual_tmin import Monthly_to_Annual_tmin
from app.Monthly_to_Annual_tmean import Monthly_to_Annual_tmean

from app.Seasonal_to_Annual_rf import Seasonal_to_Annual_rf
from app.Seasonal_to_Annual_tmax import Seasonal_to_Annual_tmax
from app.Seasonal_to_Annual_tmin import Seasonal_to_Annual_tmin
from app.Seasonal_to_Annual_tmean import Seasonal_to_Annual_tmean


def Data_Conversion():
    st.title(':blue[Data Conversion and Summary Module] 📊')
    
    info = """
        <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
        <p>The Data Conversion and Summary module provides a user-friendly interface for converting climate data (Rainfall, Maximum Temperature, Minimum Temperature, Mean Temperature) between different time scales, visualizing the data, and downloading the results. The user can select a conversion type from a dropdown menu, and the module will perform the selected conversion on the data. The user is prompted to:</p>
        
        <ol>
            <li>Select Conversion Type: The available conversion types are:
            <ul>
                <li>Daily to Monthly: This conversion aggregates daily data into monthly data.</li>
                <li>Monthly to Seasonal: This conversion aggregates monthly data into seasonal data (Belg, Kiremt, Bega).</li>
                <li>Monthly to Annual: This conversion aggregates monthly data into annual data.</li>
                <li>Seasonal to Annual: This conversion aggregates seasonal data into annual data.</li>
            </ul>
            </li>
            <li>Select the variable type, season and year for the conversion.</li>
            <li>Upload Data: The data can be uploaded in CSV or Excel format.</li>
            <li>Data Display: After the files are uploaded, the user can select a file from a dropdown menu to display its data.</li>
            <li>Data Conversion: Once all files have been uploaded, the user can click the 'Convert' button to convert the data.</li>
            <li>Data Download: After the conversion, the user can download the annual data as a CSV file.</li>
            <li>Data Visualization: The user can generate a map showing the data for each station. The map is is interactive, allowing the user to hover over each point to see more information.</li>
            <li>Summary Statistics: The user can generate summary statistics for the data, which can also be downloaded as a CSV file.</li>
            <li>Box Plot: The user can generate a box plot of the  data. The box plot provides a visual representation of the distribution of the data.</li>
        </ol>
        </div>
    """
    st.markdown(info, unsafe_allow_html=True)
    
    
    
    
    variable_type = st.session_state.get('variable_type', 'None')
    timestep_analysis = st.session_state.get('timestep_analysis', 'None')
    
    # Access the shared DataFrame from session state
    daily_rf = st.session_state.get('daily_rf', None)
    daily_max = st.session_state.get('daily_max', None)
    daily_min = st.session_state.get('daily_min', None)
    
    conversion = st.selectbox("Choose a conversion type",
                              ("None", "Daily to Monthly", "Monthly to Seasonal", "Monthly to Annual", "Seasonal to Annual"))
    if conversion =='None':
        st.warning("Please select an appropriate conversion 😞")
        
    else:
        st.success(f'You selected: {conversion} conversion')
    
    if conversion == "Daily to Monthly":
        
        if timestep_analysis == 'Daily' and variable_type == 'Rainfall':
            daily_mon_con_sum_rf(variable_type, daily_rf)
        
        elif timestep_analysis == 'Daily' and variable_type == 'Maximum Temperature':
            daily_mon_con_sum_tmax(variable_type, daily_max)
            
        elif timestep_analysis == 'Daily' and variable_type == 'Minimum Temperature':
            daily_mon_con_sum_tmin(variable_type, daily_min)
            
        elif timestep_analysis == 'Daily' and variable_type == 'Mean Temperature':
            daily_mon_con_sum_tmean(variable_type, daily_max, daily_min)
    
    # Monthly to Seasonal Conversion
    elif conversion == "Monthly to Seasonal":
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            variable_types = st.selectbox(
                "Select variable type", 
                ('None','Rainfall', 'Maximum Temperature', 'Minimum Temperature', 'Mean Temperature'), key="list_variables_v")
            if variable_types == 'None':
                st.warning("Please select an appropriate variable type 😞")            
            else:
                st.success(f"You selected: {variable_types.lower()}")
                    
            
        with col2:
            season = st.selectbox(
                    "Choose a Seasons",
                    ("None", "Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            if season =='None':
                st.warning("Please select an appropriate season 😞")
            else:
                st.success(f'You selected: {season}')
            

        with col3:
            year = st.selectbox("Choose a year", ["None"] + list(range(2023, 2051)), key="list_year_s")
            if year == 'None':
                st.warning("Please select an appropriate year 😞")
            else:
                st.success(f'You selected: {year}')
                
        
            st.session_state.variable_types = variable_types
            st.session_state.season = season
            st.session_state.year = year
            
        if variable_types == "Rainfall" and season != "None" and year != "None":
            Monthly_to_Seasonal_rf(season, year)
            
        elif variable_types == "Maximum Temperature" and season != "None" and year != "None":
            Monthly_to_Seasonal_tmax(season, year)
            
        elif variable_types == "Minimum Temperature" and season != "None" and year != "None":
            Monthly_to_Seasonal_tmin(season, year)
            
        elif variable_types == "Mean Temperature" and season != "None" and year != "None":
            Monthly_to_Seasonal_tmean(season, year)
            
        st.markdown("---")
        
    # Monthly to Annual Conversion    
    
    elif conversion == "Monthly to Annual":
        st.markdown("---")
    
        col1, col2 = st.columns(2)
        with col1:
            
            variable_types = st.selectbox('Select variable type', ('None','Rainfall', 'Maximum Temperature', 'Minimum Temperature', 'Mean Temperature'))
            
            if variable_types == 'None':
                st.warning("Please select an appropriate variable type 😞")            
            else:
                st.success(f"You selected: {variable_types.lower()}")
                
        with col2:
            year = st.selectbox("Choose a year", ["None"] + list(range(2023, 2051)), key="list_year_s")
            if year == 'None':
                st.warning("Please select an appropriate year 😞")
            else:
                st.success(f'You selected: {year}')
   
            st.session_state.variable_types = variable_types
            st.session_state.year = year
                
        if variable_types == "Rainfall" and year != "None":
            Monthly_to_Annual_rf(year)
            
        elif variable_types == "Maximum Temperature" and year != "None":
            Monthly_to_Annual_tmax(year)
            
        elif variable_types == "Minimum Temperature" and year != "None":
            Monthly_to_Annual_tmin(year)
            
        elif variable_types == "Mean Temperature" and year != "None":
            Monthly_to_Annual_tmean(year)
                
        st.markdown("---")   
        
    # Monthly to Seasonal Annual
        
    elif conversion == "Seasonal to Annual":
        st.markdown("---")
    
        col1, col2 = st.columns(2)
        with col1:
            
            variable_types = st.selectbox('Select variable type', ('None','Rainfall', 'Maximum Temperature', 'Minimum Temperature', 'Mean Temperature'))
            
            if variable_types == 'None':
                st.warning("Please select an appropriate variable type 😞")            
            else:
                st.success(f"You selected: {variable_types.lower()}")
                
        with col2:
            year = st.selectbox("Choose a year", ["None"] + list(range(2023, 2051)), key="list_year_s")
            if year == 'None':
                st.warning("Please select an appropriate year 😞")
            else:
                st.success(f'You selected: {year}')
                
            st.session_state.variable_types = variable_types
            st.session_state.year = year
            
        if variable_types == "Rainfall" and year != "None":
            Seasonal_to_Annual_rf(year)
            
        elif variable_types == "Maximum Temperature" and year != "None":
            Seasonal_to_Annual_tmax(year)
        
        elif variable_types == "Minimum Temperature" and year != "None":
            Seasonal_to_Annual_tmin(year)
            
        elif variable_types == "Mean Temperature" and year != "None":
            Seasonal_to_Annual_tmean(year)
            
        st.markdown("---") 
        
if __name__ == "__main__":
    Data_Conversion()
    
