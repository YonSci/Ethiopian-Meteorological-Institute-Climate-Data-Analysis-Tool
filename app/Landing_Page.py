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
        <strong style="color: #007BFF;">EMI-CDAT</strong> is designed to streamline the data workflow within the <strong style="color: #007BFF;">Meteorological Data and Climatology Directorate</strong> of the <strong style="color: #007BFF;">Ethiopian Meteorological Institute</strong>.
        
        It automates the generation of charts, graphs, maps, and tabular outputs, thereby facilitating the production of informative bulletins. 
        
        The application is constructed and deployed using the <strong style="color: #007BFF;">Python-based Streamlit</strong> application development tool. 
        
        Furthermore, it incorporates various data analysis and visualization tools, such as <strong style="color: #007BFF;">Plotly Graphing Libraries</strong>, <strong style="color: #007BFF;">SciPy</strong>, <strong style="color: #007BFF;">NCAR PyNGL</strong>, and <strong style="color: #007BFF;">PyNIO</strong> packages, to enhance its statistical visualization and mapping capabilities.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
      
    st.markdown(
        """
        <div style="text-align: justify; font-family: Arial, sans-serif; color: #333;">
        <strong style="color: #007BFF;">Features of EMI-CDAT app include:</strong>

        <ul style="list-style-type: square;">
            <li>Reading input data in tabular formats such as Microsoft Excel spreadsheet (.xlsx) and comma-separated value (.csv).</li>
            <li>Handling input data related to daily rainfall, maximum, and minimum temperature.</li>
            <li>Generating a summary report on the missing data.</li>
            <li>Producing basic summary and indices in tabular formats.</li>
            <li>Creating maps required for monthly, seasonal (e.g., Bega, Belg, Kiremt), and annual climate bulletins.</li>
        </ul>
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