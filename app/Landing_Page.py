import streamlit as st
from PIL import Image

def Landing_Page():
    #  blue, green, orange, red, violet, gray/grey, rainbow.
    st.title(':blue[Home Page] 🏠')
    
    st.markdown("---")
     
    # Open the image
    display = Image.open('images/emi_logo.jpg')

    col1, col2 = st.columns((3, 7))
    col1.image(display, width=200)
    col2.markdown("<h2 style='text-align: left; color: blue;'>Ethiopian Meteorological Institute Climate Data Analysis Tool (EMI-CDAT)</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(
    """
    <div style="text-align: justify">
    <strong>EMI-CDAT</strong> is designed to streamline the data workflow within the <strong>Meteorological Data and Climatology Directorate</strong> of the <strong>Ethiopian Meteorological Institute</strong>.
    
    It automates the generation of charts, graphs, maps, and tabular outputs, thereby facilitating the production of informative bulletins. 
    
    The application is constructed and deployed using the <strong>Python-based Streamlit</strong> application development tool. 
    
    Furthermore, it incorporates various data analysis and visualization tools, such as <strong>Plotly Graphing Libraries</strong>, <strong>SciPy</strong>, <strong>NCAR PyNGL</strong>, and <strong>PyNIO</strong> packages, to enhance its statistical visualization and mapping capabilities.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
      
    st.markdown(
    """
    <div style="text-align: justify">
    <strong>Features of EMI-CDAT app include:</strong>

    - Reading input data in tabular formats such as Microsoft Excel spreadsheet (.xlsx) and comma-separated value (.csv).
    - Handling input data related to daily rainfall, maximum, and minimum temperature.
    - Generating a summary report on the missing data.
    - Producing basic summary and indices in tabular formats.
    - Creating maps required for monthly, seasonal (e.g., Bega, Belg, Kiremt), and annual climate bulletins.
    </div>
    """, unsafe_allow_html=True)
            
    st.markdown("---")
    
    st.markdown('<h3 style="text-align: left; color: blue;">Our Partners</h3>', unsafe_allow_html=True)
    display1 = Image.open('images/AICCRA.png')
        
    col1, col2, col3 = st.columns(3)
    col1.image(display1, width = 300)
    
    st.markdown("---")
        
    st.markdown('<p style="text-align: center; color: gray;">Copyright @2024 EMI-CDAT</p>', unsafe_allow_html=True)
 
    st.markdown("---")    
        
if __name__ == "__main__":
    Landing_Page()