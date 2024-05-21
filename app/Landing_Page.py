import streamlit as st
from PIL import Image

def Landing_Page():
   #  blue, green, orange, red, violet, gray/grey, rainbow.
    st.markdown(
    """
    <style>
    .title {
        background-color: lightblue;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    <div class="title">
        <h1>Home Page 🏠</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    # Open the image
    display = Image.open('images/emi_logo.jpg')

    col1, col2 = st.columns((3, 7))
    with col1:
        st.image(display, width=200)
    with col2:
        st.markdown("<h2 style='text-align: left; color: blue; font-family: Arial, sans-serif;'>Ethiopian Meteorological Institute Climate Data Analysis Tool (EMI-CDAT)</h2>", unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown(
        """
        <div style="text-align: justify; font-family: Arial, sans-serif; color: #333;">
        <p><strong style="color: #007BFF;">EMI-CDAT</strong> is designed to streamline the data workflow within the <strong style="color: #007BFF;">Meteorological Data and Climatology Directorate</strong> of the <strong style="color: #007BFF;">Ethiopian Meteorological Institute</strong> to facilitate the production of climate bulletins (monthly, seasonal, and annual). It automates the generation of charts, graphs, maps, and tabular outputs needed to prepare climate bulletins.</p> 
        
        
        <p>The application is constructed and deployed using the <strong style="color: #007BFF;">Streamlit</strong> application development framework. The tool integrates a range of data analysis and visualization libraries, including <strong style="color: #007BFF;">Plotly</strong>, <strong style="color: #007BFF;">SciPy</strong>, <strong style="color: #007BFF;">Cartopy</strong>, <strong style="color: #007BFF;">Geopandas</strong>, <strong style="color: #007BFF;">Xarray</strong>, <strong style="color: #007BFF;">Verde</strong>, <strong style="color: #007BFF;">Sklearn</strong>, <strong style="color: #007BFF;">Shapely</strong>, <strong style="color: #007BFF;">Regionmask</strong>, <strong style="color: #007BFF;">Pykrige</strong>, and <strong style="color: #007BFF;">Seaborn</strong>, to enhance its data analysis, visualization, and mapping capabilities.</p>
        
        <p>EMI-CDAT is built upon a <strong style="color: #007BFF;">modularized system</strong>, This approach promotes code reusability, simplifies maintenance, and enhances code readability. Well-defined modules enable independent development and testing, leading to faster development cycles and more robust applications making the application well-structured and efficient.</p>
        
        <p>The application has wide or narrow page layouts, and switch between light and dark modes to suit your preference. you can personalize the application theme by editing colors and fonts.</p>
        
      </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown(
        """    
        <div style="text-align: justify; font-family: Arial, sans-serif; color: #333;">
        <p> EMI-CDAT offers six user-friendly modules to streamline climate data analysis. Each module can be accessed from the sidebar using the navigation bar. Each module tackles a specific task: </p>

        - **Data Importing**:  Interactive and user-friendly interface to configure the input settings, upload data, and display the loaded data for further analysis (CSV or Excel format).
                
        - **Missing Data Review**: Exploring missing data patterns in the dataset (Rainfall, Maximum and Minimum Temperature), offering both tabular reports and graphical visualizations. 
                     
        - **Data Conversion**: Provides seamlessly data conversion between different time scales (Daily to Monthly, Monthly to Seasonal, Monthly to Annual, Seasonal to Annual).
             
        - **Summary and Indices Calculator**: Generate informative summaries and calculate essential indices (Rainfall Threshold, Number of Rainy Days, Maximum Temperature and Minimum Temperature Thresholds) that can be used in climate bulletins.
                
        - **Interpolation**: Transform irregularly spaced station data into regularly spaced fields using a variety of spatial interpolation techniques (10) such as Nearest Neighbor, Inverse Distance Weighting, Radial basis, Simple Kriging, Ordinary Kriging, Universal Kriging, Splines, and Gaussian Process Regressor. 
                
        - **Mapping Module**: Seamlessly generate vital maps for EMI climate bulletins (monthly(6), seasonal(6), or annual(6)). 

        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
      
                  
    st.markdown('<h3 style="text-align: left; color: blue; font-family: Arial, sans-serif;">Our Partners</h3>', unsafe_allow_html=True)
    display1 = Image.open('images/AICCRA.png')

    col1, col2, col3 = st.columns(3)
    col1.image(display1, width = 300)
    
    
    
    st.markdown("---")
        
    st.markdown('<p style="text-align: center; color: gray;">Copyright @2024 EMI-CDAT</p>', unsafe_allow_html=True)
 
    st.markdown("---")  
        
 
        
if __name__ == "__main__":
    Landing_Page()