import streamlit as st
import bcrypt
import pickle

page_icon = "images\logo4.jpg"

st.set_page_config(
    page_title="Main Page",
    page_icon=page_icon,
    layout="centered"  # wide, centered
    )

# Function to authenticate users
def authenticate(username, password):
    stored_credentials = load_user_credentials()

    # Check if the entered username exists in the credentials
    if username in stored_credentials:
        stored_hashed_password = stored_credentials[username]["hashed_password"]
        # Check if the entered password matches the stored hashed password
        return bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password("utf-8"))

    return False

# Function to load user credentials from the pickle file
def load_user_credentials(filename="user_credentials.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

# Function to create session state
def create_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        

# Function to reset the authentication status and rerun the script
def logout():
    st.session_state.authenticated = False
    st.rerun()

# Login page
def login_page():
    st.title(':blue[Login Page] 🔒')

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate(username, password):
            st.success("Login successful!")
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    
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
        
        

    
if __name__ == "__main__":
    # Create session state
    create_session_state()

    # Check if user is authenticated
    if not st.session_state.authenticated:
        # If not authenticated, show login page
        login_page()
    else:
        # If authenticated, show landing page
        main()
