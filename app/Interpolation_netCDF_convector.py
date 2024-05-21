import streamlit as st
import pandas as pd


from app.inter_sumstat import inter_sumstat
from app.inter_visual import inter_visual
from app.inter_histogram import inter_histogram
from app.inter_qqplot import inter_qqplot
from app.inter_trans import inter_trans
from app.inter_grid import inter_grid
from app.inter_pol import inter_pol
# from app.inter_nn import inter_nn


def Interpolation_netCDF_convector():
    # blue, green, orange, red, violet, gray/grey, rainbow.
    st.title(':blue[Interpolation and Visualization] ')
        
    info = """
    <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    
    <p>This module designed to transform irregularly spaced station data into regularly spaced fields using a variety of spatial interpolation methods enabling a seamless analysis of spatial phenomena. The interpolation module offers a comprehensive toolkit for spatial analysis and interpolation of EMI weather data. 
    
    Users can select their variable of interest and upload the corresponding dataset. You can upload monthly, seasonal, or annual data files in csv or excel format. The data should at least contain the following columns: Longitude, Latitude, and the variable of interest.

    Through **exploratory spatial data analysis (ESDA)**, users can delve into the dataset's characteristics, including **summary statistics**, **visualizations**, **histograms**, and **normal QQ plots**. 
    
    Spatial data transformations such as **Box-Cox, Log**, **Arcsine**, or **Normal Scores** are available to normalize variables if needed. Following data preparation, users define a **regular grid** over the study area to facilitate spatial interpolation. 
    
    Various interpolation methods (**Nearest Neighbor**, **Inverse Distance Weighting**, **IDW Based on Radius**, **IDW Based on K-Nearest Neighbors**, **Radial basis**, **Simple Kriging**, **Ordinary Kriging**, **Universal Kriging**, **Splines**, and **Gaussian Process Regressor**) enable estimation of values at unsampled locations. 
    
    Post-interpolation, users can extract and analyze interpolated surfaces within the Ethiopian domain, defining the **region of interest**. Finally, the module facilitates conversion of extracted data into **NetCDF** format for further analysis or sharing, providing a robust framework tailored to Ethiopian contexts.</p>
        
    </div>
    """
    
    df_data = None
    variable = None
    LAT = None
    LON = None
    ds_nn = None
    ds_ok = None
    ds_uk = None
    
    
    st.markdown(info, unsafe_allow_html=True)
    st.markdown("---")
    
    
    st.subheader("Select the variable of interest")
    variable_type = st.selectbox('Select variable type', ('None','Rainfall', 
                                                          'Maximum Temperature', 
                                                          'Minimum Temperature',
                                                          'Average temperature'))
    st.info("You selected: " + variable_type)
    st.session_state.variable_type = variable_type
    
    if variable_type == 'Rainfall':
        variable = 'Total Rainfall'
    elif variable_type == 'Maximum Temperature':
        variable = 'Mean Maximum Temperature'
    elif variable_type == 'Minimum Temperature':
        variable = 'Mean Minimum Temperature'
    elif variable_type == 'Average temperature':
        variable = 'Mean Temperature'
        
    st.session_state.variable = variable
        
    st.markdown("---")
    
    st.subheader("Upload data")
    
    upload_data = st.file_uploader(f"Please upload data in CSV or Excel file formats", type={"csv", "xlsx", "xls"}, key="loader1")
    if upload_data is not None:
        try:
            df_data = pd.read_csv(upload_data)
        except Exception as e:
            df_data = pd.read_excel(upload_data)
            
        if st.button('Load the data', key="_display"):
            if df_data is not None:
                st.success(f'You uploaded data with {df_data.shape[0]} rows and {df_data.shape[1]} columns.')
                st.write(df_data)
            else:
                st.write("Please first upload .csv, .xlsx, or .xls files 😔")
                
                
    st.session_state.df_data = df_data

                
    st.markdown("---")
    
    # Summary statistics
    if variable_type == 'Rainfall':
        inter_sumstat(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_sumstat(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_sumstat(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_sumstat(variable_type, df_data)
        
    # Visualizations 
    if variable_type == 'Rainfall':
        inter_visual(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_visual(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_visual(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_visual(variable_type, df_data)
        
    # Histogram
    if variable_type == 'Rainfall':
        inter_histogram(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_histogram(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_histogram(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_histogram(variable_type, df_data)
        
    # QQ plot
    if variable_type == 'Rainfall':
        inter_qqplot(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_qqplot(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_qqplot(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_qqplot(variable_type, df_data)
        
    # Data transformation
    if variable_type == 'Rainfall':
        inter_trans(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_trans(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_trans(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_trans(variable_type, df_data)    
        
    # Grid
    if variable_type == 'Rainfall':
        inter_grid(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_grid(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_grid(variable_type, df_data)   
    elif variable_type == 'Average temperature':
        inter_grid(variable_type, df_data) 
        
    # Interpolation
    if variable_type == 'Rainfall':
        inter_pol(variable_type, df_data)
    elif variable_type == 'Maximum Temperature':
        inter_pol(variable_type, df_data)
    elif variable_type == 'Minimum Temperature':
        inter_pol(variable_type, df_data)
    elif variable_type == 'Average temperature':
        inter_pol(variable_type, df_data)
        
            
if __name__ == "__main__":
    Interpolation_netCDF_convector()