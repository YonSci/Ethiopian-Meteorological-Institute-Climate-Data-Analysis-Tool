import streamlit as st

from app.daily_data_miss_rf import daily_data_miss_rf
from app.daily_data_miss_tmax import daily_data_miss_tmax
from app.daily_data_miss_tmin import daily_data_miss_tmin

from app.monthly_data_miss_rf import monthly_data_miss_rf 
from app.monthly_data_miss_tmax import monthly_data_miss_tmax
from app.monthly_data_miss_tmin import monthly_data_miss_tmin 
from app.monthly_data_miss_tmean import monthly_data_miss_tmean 

from app.seasonal_data_miss_rf import seasonal_data_miss_rf
from app.seasonal_data_miss_tmax import seasonal_data_miss_tmax
from app.seasonal_data_miss_tmin import seasonal_data_miss_tmin 
from app.seasonal_data_miss_tmean import seasonal_data_miss_tmean 

from app.annual_data_miss_rf import annual_data_miss_rf
from app.annual_data_miss_tmax import annual_data_miss_tmax
from app.annual_data_miss_tmin import annual_data_miss_tmin 
from app.annual_data_miss_tmean import annual_data_miss_tmean 

#from app.annual_data_miss import annual_data_miss

def Missing_Data():
    st.title(':blue[Missing Data Module] 🗓️')
    
    info = """
        <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
        <p>The Missing Data module creates an interactive and informative page for exploring missing data patterns in a meteorological dataset (Rainfall, Maximum and Minimum Temperature), offering both tabular reports and graphical visualizations.</p>
        
        <ol>
            <li><b>Access Data</b>
                <ul>
                    <li>It retrieves the uploaded data and other relevant information (time step, variable type, month, season, year, etc) from the Data Importing Module.</li>
                </ul>
            </li>
            <li><b>Analyze Missing Data</b>
               <ul>
                   <li>Calculates and displays the total missing data count and percentage from the entire data set.</li>
               </ul>
            </li>
            <li><b>Generate tabular reports and chars for each day</b>
               <ul>
                   <li>Generate a tabular report showing the missing data count for each day from all the stations and download the data as a CSV file.</li>
                   <li>Generate a bar chart report showing the missing data count for each day and download the chart as an image file.</li>
               </ul>
            </li>
            <li><b>Generate Maps and tabular reports for stations</b>
               <ul>
                   <li>Generates maps and tabular reports for stations above/below the specified threshold criteria (3/5-day rule)  and downloads the data.</li>
                   <li>Generates maps and tabular reports for  Stations Without Missing Data that satisfy the threshold criteria (3/5-day rule)  and downloads the data.</li>
               </ul>
            </li>
        </ol>
        </div>
    """
    st.markdown(info, unsafe_allow_html=True)
 
    # # Access the shared month value from session state
    
    month = st.session_state.get('month', 'Unknown Month')
    season = st.session_state.get('season', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')   
    
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
        daily_data_miss_rf(variable_type, daily_rf)
    
    elif timestep_analysis == 'Daily' and variable_type == 'Maximum Temperature':
        daily_data_miss_tmax(variable_type, daily_max)
    
    elif timestep_analysis == 'Daily' and variable_type == 'Minimum Temperature':
        daily_data_miss_tmin(variable_type, daily_min)
   
    #  Monthly Data                            
    elif timestep_analysis == 'Monthly' and variable_type == 'Rainfall':
        monthly_data_miss_rf(variable_type, mon_rf)
        
    elif timestep_analysis == 'Monthly' and variable_type == 'Maximum Temperature':
        monthly_data_miss_tmax(variable_type, mon_max)
    
    elif timestep_analysis == 'Monthly' and variable_type == 'Minimum Temperature':
        monthly_data_miss_tmin(variable_type, mon_min)
        
    elif timestep_analysis == 'Monthly' and variable_type == 'Mean Temperature':
        monthly_data_miss_tmean(variable_type, mon_mean)
        
    # Seasonal Data                            
    elif timestep_analysis == 'Seasonal' and variable_type == 'Rainfall':
        seasonal_data_miss_rf(variable_type, seas_rf)
        
    elif timestep_analysis == 'Seasonal' and variable_type == 'Maximum Temperature':
        seasonal_data_miss_tmax(variable_type, seas_max)
        
    elif timestep_analysis == 'Seasonal' and variable_type == 'Minimum Temperature':
        seasonal_data_miss_tmin(variable_type, seas_min)
        
    elif timestep_analysis == 'Seasonal' and variable_type == 'Mean Temperature':
        seasonal_data_miss_tmean(variable_type, seas_mean)
            
    #  Annual Data    
    elif timestep_analysis == 'Annual' and variable_type == 'Rainfall':
        annual_data_miss_rf(variable_type, an_rf)
        
    elif timestep_analysis == 'Annual' and variable_type == 'Maximum Temperature':
        annual_data_miss_tmax(variable_type, an_max)
    
    elif timestep_analysis == 'Annual' and variable_type == 'Minimum Temperature':
        annual_data_miss_tmin(variable_type, an_min)
        
    elif timestep_analysis == 'Annual' and variable_type == 'Mean Temperature':
        annual_data_miss_tmean(variable_type, an_mean)
        
    else:
        st.warning("No data to review, Please load data in the Data Importing Page 😔") 
                    
                     
if __name__ == "__main__":
    Missing_Data()

     

    
    
         
       
       

        
                     
   
    
    
    
    
    
    
    