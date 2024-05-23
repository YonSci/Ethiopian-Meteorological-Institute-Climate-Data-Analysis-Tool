import streamlit as st
import streamlit_authenticator as stauth

page_icon = "images\logo4.jpg"

st.set_page_config(
    page_title="Main Page",
    page_icon=page_icon,
    layout="centered"  # wide, centered
    )

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login(main)


    
from app.Landing_Page import Landing_Page
from app.Data_Importing_Module import Data_Importing_Module
from app.Missing_Data import Missing_Data
from app.Data_Conversion import Data_Conversion
from app.Indices_Calculator import Indices_Calculator
from app.Interpolation_netCDF_convector import Interpolation_netCDF_convector
from app.Mapping_module import Mapping_module

def main():
    st.sidebar.title("Navigation Bar")
    
    pages = {
        "Landing Page": Landing_Page,
        "Data Importing Module": Data_Importing_Module,
        "Data Review Module": Missing_Data, 
        "Data Conversion & Summary Statistics": Data_Conversion,
        "Indices Calculator Module": Indices_Calculator, 
        "Interpolation & netCDF Convector Module": Interpolation_netCDF_convector, 
        "Mapping Module": Mapping_module
    }
    
    choice = st.sidebar.selectbox("Go to", list(pages.keys()))
    

    # Instantiate the chosen class
    selected_page = pages[choice]()
    
    
    # Add logout button to the sidebar
    if st.sidebar.button("Logout"):
        logout()
        
        

