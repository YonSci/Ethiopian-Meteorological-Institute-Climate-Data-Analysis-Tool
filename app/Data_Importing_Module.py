import streamlit as st
import pandas as pd

def Data_Importing_Module():
    st.title(":blue[Data Importing Page] 🗃️")

    info = """
        <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">

        <h3>Welcome to the Data Importing Page!</h3>

        <p>This page provides an interactive and user-friendly interface to configure the input settings, upload data, and display the loaded data for further analysis.</p>

        <ol>
            <li><b>Configure Data Input Parameters</b>
                <ul>
                    <li>Choose the time step for data analysis (Daily, Monthly, Seasonal, or Annual).</li>
                    <li>Select the variable type for analysis (Rainfall, Maximum Temperature, Minimum Temperature, or Mean Temperature).</li>
                    <li>Specify the month and year of the data for additional analysis.</li>
                </ul>
            </li>
            <li><b>Upload Data Files</b>
                <ul>
                    <li>Depending on the chosen time step and variable type, users are guided to upload relevant data files in CSV or Excel format.</li>
                </ul>
            </li>
            <li><b>Display Data</b>
                <ul>
                    <li>Once the data is uploaded, the script showcases the loaded data on the page.</li>
                </ul>
            </li>
        </ol>
        </div>
    """
    st.markdown(info, unsafe_allow_html=True)
    

    st.markdown("---")
    st.markdown("##### Set the input timestep and variable type")
    
    col1, col2 = st.columns(2)
    with col1:
        timestep_analysis = st.selectbox("Choose time step", ("None", "Daily",  "Monthly", "Seasonal", "Annual"))
        
        if timestep_analysis == 'None':
            st.warning("Please select an appropriate time step 😞")   
            
        elif timestep_analysis == 'Daily':
            st.success("You selected daily time step")
            
        elif timestep_analysis == 'Monthly':
            st.success("You selected monthly time step")
        
        elif timestep_analysis == 'Seasonal':
            st.success("You selected seasonal time step")
            
        elif timestep_analysis == 'Annual':
            st.success("You selected annual time step")
        
    with col2:
        variable_type = st.selectbox('Select variable type', ('None','Rainfall', 'Maximum Temperature', 'Minimum Temperature', 'Mean Temperature'))
        
        if variable_type == 'None':
            st.warning("Please select an appropriate variable type 😞")            
        else:
            st.success(f"You selected {variable_type.lower()} data for analysis")
            
      # Store the variable_type in session state
    st.session_state.timestep_analysis = timestep_analysis
    st.session_state.variable_type = variable_type
    
    st.markdown("---")
    
    if timestep_analysis == 'Daily' and variable_type != 'None':
        st.markdown("##### Set the input month and year")   
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox(
                "Choose a month",
                (
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ),
                key="list_month_d"
            )
            st.success(f'You selected: {month}')
        with col2:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_d")
            st.success(f'You selected: {year}')
            
                       
        st.session_state.month = month
        st.session_state.year = year
        
        
    elif timestep_analysis == 'Monthly' and variable_type != 'None':
        st.markdown("##### Set the input month and year")
    
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox(
                "Choose a month",
                (
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ),
                key="list_month_m"
            )
            st.success(f'You selected: {month}')
        with col2:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_m")
            st.success(f'You selected: {year}')
            
        st.session_state.month = month
        st.session_state.year = year
            
            
    elif timestep_analysis == 'Seasonal' and variable_type != 'None':
        st.markdown("##### Set the Analysis Season and Year")
    
        col1, col2 = st.columns(2)
        with col1:
            season = st.selectbox(
                "Choose a Seasons",
                ("Belg (FMAM)", "Kiremt (JJAS)", "Bega (ONDJ)"), key="list_season_s" )
            st.success(f'You selected: {season}')

        with col2:
            year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_s")
            st.success(f'You selected: {year}')
            
        st.session_state.season = season
        st.session_state.year = year
            
                        
            
    elif timestep_analysis == 'Annual' and variable_type != 'None':
        st.markdown("##### Set the Analysis Year")
        year = st.selectbox("Choose a year", list(range(2023, 2051)), key="list_year_y")
        st.success(f'You selected: {year}')
                
        st.session_state.year = year

    # Daily Data   

    # Load daily data     
    st.markdown("---")
    # Initialize daily variables outside block  
    daily_rf = None  
    daily_max = None
    daily_min = None
    
    if timestep_analysis == 'Daily' and variable_type == 'Rainfall':
        #st.write(f"Please upload the {variable_type} data in CSV or Excel format")
        daily_uploadrf = st.file_uploader(f"Please upload daily rainfall data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader1")
        if daily_uploadrf is not None:
            try:
                daily_rf = pd.read_csv(daily_uploadrf)
            except Exception as e:
                daily_rf = pd.read_excel(daily_uploadrf)
                
            if st.button('Load the data', key="daily_rf_display"):
                if daily_rf is not None:
                    st.success(f'You uploaded daily rainfal data for {month} {year}')
                    st.write(daily_rf)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Daily' and variable_type == 'Maximum Temperature':
        #st.write(f"Please upload the {variable_type} data in CSV or Excel format")
        daily_uploadmx = st.file_uploader(f"Please upload daily maximum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader2")
        if daily_uploadmx is not None:
            try:
                daily_max = pd.read_csv(daily_uploadmx)
            except Exception as e:
                daily_max = pd.read_excel(daily_uploadmx)
            if st.button('Load the data', key="daily_tm_display"):
                if daily_max is not None:
                    st.success(f'You uploaded daily maximum temperature data for {month} {year}')
                    st.write(daily_max)
                    #st.success("Data Displayed!")
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Daily' and  variable_type == 'Minimum Temperature':
        #st.write(f"Please upload the {variable_type} data in CSV or Excel format")
        daily_uploadmn = st.file_uploader(f"Please upload daily minimum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader3")
        if daily_uploadmn is not None:
            try:
                daily_min = pd.read_csv(daily_uploadmn)
            except Exception as e:
                daily_min = pd.read_excel(daily_uploadmn)
            if st.button('Load the data', key="daily_tn_display"):
                if daily_min is not None:
                    st.success(f'You uploaded daily minimum temperature data for {month} {year}')
                    st.write(daily_min)
                    #st.success("Data Displayed!")
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                        
    elif timestep_analysis == 'Daily' and variable_type == 'Mean Temperature':
        st.markdown("##### Select both Maximum and Minimum temperature data")
        variable_type2 = st.multiselect('Select both data', ('Maximum Temperature', 'Minimum Temperature'), key="vt2")
        if len(variable_type2) == 0:
            st.warning("Please select an appropriate variable type 😞")
        elif len(variable_type2) == 1:
            st.warning("Please select both maximum and minimum temperature data 😞")
        else:
            st.success("You selected both maximum and minimum temperature data")
            
        st.session_state.variable_type2 = variable_type2
        
        if timestep_analysis == 'Daily' and 'Maximum Temperature' in variable_type2 and 'Minimum Temperature' in variable_type2:
            #st.write("Please upload maximum temperature data in CSV or Excel format")
            daily_uploadmx = st.file_uploader(f"Please upload daily maximum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader4")
            if daily_uploadmx is not None:
                try:
                    daily_max = pd.read_csv(daily_uploadmx)
                except Exception as e:
                    daily_max = pd.read_excel(daily_uploadmx)
                if st.button('Load the data', key="daily_tm_display"):
                    if daily_max is not None:
                        st.success(f'You uploaded daily maximum temperature data for {month} {year}')
                        st.write(daily_max)
                        #st.success("Data Displayed!")
                    else:
                        st.write("Please first upload .csv, .xlsx, or .xls files 😔")
            
            # st.write(f"Please upload minimum temperature data in CSV or Excel format")
            daily_uploadmn = st.file_uploader(f"Please upload daily minimum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader5")
            if daily_uploadmn is not None:
                try:
                    daily_min = pd.read_csv(daily_uploadmn)
                except Exception as e:
                    daily_min = pd.read_excel(daily_uploadmn)
                if st.button('Load the data', key="daily_tn_display"):
                    if daily_min is not None:
                        st.success(f'You uploaded daily minimum temperature data for {month} {year}')
                        st.write(daily_min)
                    else:
                        st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                    
                
                    
    st.session_state.daily_rf = daily_rf
    st.session_state.daily_max = daily_max
    st.session_state.daily_min = daily_min 
    
    
    # Load monthly data
    # Initialize monthly variables 
    mon_rf = None
    mon_max = None
    mon_min = None
    mon_mean = None
    
    if timestep_analysis == 'Monthly' and variable_type == 'Rainfall':
        mon_uploadrf = st.file_uploader(f"Please upload monthly rainfall data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader6")
        if mon_uploadrf is not None:
            try:
                mon_rf = pd.read_csv(mon_uploadrf)
            except Exception as e:
                mon_rf = pd.read_excel(mon_uploadrf)
            
        if st.button('Load the data', key="mon_rf_display"):
            if mon_rf is not None:
                st.success(f'You uploaded monthly rainfall data for {month} {year}')
                st.write(mon_rf)
            else:
                st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Monthly' and variable_type == 'Maximum Temperature':
        mon_uploadmx = st.file_uploader(f"Please upload monthly maximum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader7")
        if mon_uploadmx is not None:
            try:
                mon_max = pd.read_csv(mon_uploadmx)
            except Exception as e:
                mon_max = pd.read_excel(mon_uploadmx)
            if st.button('Load the data', key="mon_tm_display"):
                if mon_max is not None:
                    st.success(f'You uploaded monthly maximum temperature data for {month} {year}')
                    st.write(mon_max)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Monthly' and  variable_type == 'Minimum Temperature':
        mon_uploadmn = st.file_uploader(f"Please upload monthly minimum temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader8")
        if mon_uploadmn is not None:
            try:
                mon_min = pd.read_csv(mon_uploadmn)
            except Exception as e:
                mon_min = pd.read_excel(mon_uploadmn)
            if st.button('Load the data', key="mon_tn_display"):
                if mon_min is not None:
                    st.success(f'You uploaded monthly minimum temperature data for {month} {year}')
                    st.write(mon_min)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                    
    elif timestep_analysis == 'Monthly' and  variable_type == 'Mean Temperature':
        mon_uploadmean = st.file_uploader(f"Please upload monthly mean temperature data in CSV or Excel file formats for {month} {year}", type={"csv", "xlsx", "xls"}, key="loader9")
        if mon_uploadmean is not None:
            try:
                mon_mean = pd.read_csv(mon_uploadmean)
            except Exception as e:
                mon_mean = pd.read_excel(mon_uploadmean)
            if st.button('Load the data', key="mon_tmean_display"):
                if mon_mean is not None:
                    st.success(f'You uploaded monthly mean temperature data for {month} {year}')
                    st.write(mon_mean)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
    
    st.session_state.mon_rf = mon_rf
    st.session_state.mon_max = mon_max
    st.session_state.mon_min = mon_min
    st.session_state.mon_mean = mon_mean
    
    # Load seasonal data
    # Initialize Seasonal variables  
    seas_rf = None
    seas_max = None
    seas_min = None
    seas_mean = None

    
    if timestep_analysis == 'Seasonal' and variable_type == 'Rainfall':
        seas_uploadrf = st.file_uploader(f"Please upload seasonal rainfall data in CSV or Excel file formats for {season} {year}", type={"csv", "xlsx", "xls"}, key="loader10")
        if seas_uploadrf is not None:
            try:
                seas_rf = pd.read_csv(seas_uploadrf)
            except Exception as e:
                seas_rf = pd.read_excel(seas_uploadrf)
            
        if st.button('Load the data', key="seas_rf_display"):
            if seas_rf is not None:
                st.success(f'You uploaded seasonal rainfall data for {season} {year}')
                st.write(seas_rf)
            else:
                st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Seasonal' and variable_type == 'Maximum Temperature':
        seas_uploadmx = st.file_uploader(f"Please upload seasonal maximum temperature data in CSV or Excel file formats for {season} {year}", type={"csv", "xlsx", "xls"}, key="loader11")
        if seas_uploadmx is not None:
            try:
                seas_max = pd.read_csv(seas_uploadmx)
            except Exception as e:
                seas_max = pd.read_excel(seas_uploadmx)
            if st.button('Load the data', key="sea_tm_display"):
                if seas_max is not None:
                    st.success(f'You uploaded seasonal maximum temperature data for {season} {year}')
                    st.write(seas_max)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Seasonal' and  variable_type == 'Minimum Temperature':
        seas_uploadmn = st.file_uploader(f"Please upload seasonal minimum temperature data in CSV or Excel file formats for {season} {year}", type={"csv", "xlsx", "xls"}, key="loader12")
        if seas_uploadmn is not None:
            try:
                seas_min = pd.read_csv(seas_uploadmn)
            except Exception as e:
                seas_min = pd.read_excel(seas_uploadmn)
            if st.button('Load the data', key="seas_tn_display"):
                if seas_min is not None:
                    st.success(f'You uploaded seasonal minimum temperature data for {season} {year}')
                    st.write(seas_min)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                    
    elif timestep_analysis == 'Seasonal' and  variable_type == 'Mean Temperature':
        seas_uploadmean = st.file_uploader(f"Please upload seasonal mean temperature data in CSV or Excel file formats for {season} {year}", type={"csv", "xlsx", "xls"}, key="loader13")
        if seas_uploadmean is not None:
            try:
                seas_mean = pd.read_csv(seas_uploadmean)
            except Exception as e:
                seas_mean = pd.read_excel(seas_uploadmean)
            if st.button('Load the data', key="sea_tmean_display"):
                if seas_mean is not None:
                    st.success(f'You uploaded seasonal mean temperature data for {season} {year}')
                    st.write(seas_mean)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                    
                    
    st.session_state.seas_rf = seas_rf
    st.session_state.seas_max = seas_max
    st.session_state.seas_min = seas_min
    st.session_state.seas_mean = seas_mean 
    
                    
                    
    # Load annual data                
    # Initialize annual variables outside block  
    an_rf = None
    an_max = None
    an_min = None
    an_mean = None
    
    
    if timestep_analysis == 'Annual' and variable_type == 'Rainfall':
        an_uploadrf = st.file_uploader(f"Please upload annual rainfall data in CSV or Excel file formats for {year}", type={"csv", "xlsx", "xls"}, key="loader14")
        if an_uploadrf is not None:
            try:
                an_rf = pd.read_csv(an_uploadrf)
            except Exception as e:
                an_rf = pd.read_excel(an_uploadrf)
            
        if st.button('Load the data', key="an_rf_display"):
            if an_rf is not None:
                st.success(f'You uploaded annual rainfall data for {year}')
                st.write(an_rf)
            else:
                st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Annual' and variable_type == 'Maximum Temperature':
        an_uploadmx = st.file_uploader(f"Please upload annual maximum temperature data in CSV or Excel file formats for {year}", type={"csv", "xlsx", "xls"}, key="loader15")
        if an_uploadmx is not None:
            try:
                an_max = pd.read_csv(an_uploadmx)
            except Exception as e:
                an_max = pd.read_excel(an_uploadmx)
            if st.button('Load the data', key="an_tm_display"):
                if an_max is not None:
                    st.success(f'You uploaded annual maximum temperature data for {year}')
                    st.write(an_max)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")

    elif timestep_analysis == 'Annual' and  variable_type == 'Minimum Temperature':
        an_uploadmn = st.file_uploader(f"Please upload annual minimum temperature data in CSV or Excel file formats for {year}", type={"csv", "xlsx", "xls"}, key="loader16")
        if an_uploadmn is not None:
            try:
                an_min = pd.read_csv(an_uploadmn)
            except Exception as e:
                an_min = pd.read_excel(an_uploadmn)
            if st.button('Load the data', key="an_tn_display"):
                if an_min is not None:
                    st.success(f'You uploaded annual minimum temperature data for {year}')
                    st.write(an_min)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                    
    elif timestep_analysis == 'Annual' and  variable_type == 'Mean Temperature':
        an_uploadmean = st.file_uploader(f"Please upload annual mean temperature data in CSV or Excel file formats for {year}", type={"csv", "xlsx", "xls"}, key="loader17")
        if an_uploadmean is not None:
            try:
                an_mean = pd.read_csv(an_uploadmean)
            except Exception as e:
                an_mean = pd.read_excel(an_uploadmean)
            if st.button('Load the data', key="an_tmean_display"):
                if an_mean is not None:
                    st.success(f'You uploaded annual mean temperature data for {year}')
                    st.write(an_mean)
                else:
                    st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                
    st.session_state.an_rf = an_rf
    st.session_state.an_max = an_max
    st.session_state.an_min = an_min
    st.session_state.an_mean = an_mean

        

    st.markdown("---")
        

        
if __name__ == "__main__":
    Data_Importing_Module()
