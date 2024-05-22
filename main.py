import pickle
from pathlib import Path

import streamlit as st  
import streamlit_authenticator as stauth  # pip install streamlit-authenticator


# --- USER AUTHENTICATION ---
names = ["Yonas Mersha", "Teferi Demissie"]
usernames = ["yonas", "teferi"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    
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
        
        
        authenticator.logout("Logout", "sidebar")
        st.sidebar.subheader(f"Welcome {name}")
        
    if __name__ == "__main__":
        main()
        
        

        
