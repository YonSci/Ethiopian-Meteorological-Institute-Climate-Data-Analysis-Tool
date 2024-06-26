import streamlit as st
from passlib.context import CryptContext
import pickle

page_icon = "images/logo4.jpg"

st.set_page_config(
    page_title="Main Page",
    page_icon=page_icon,
    layout="centered"
)

# Initialize passlib context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate(username, password):
    stored_credentials = load_user_credentials()

    if username in stored_credentials:
        stored_hashed_password = stored_credentials[username]["hashed_password"]
        return pwd_context.verify(password, stored_hashed_password)

    return False

def load_user_credentials(filename="user_credentials.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def create_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def logout():
    st.session_state.authenticated = False
    st.rerun()

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

    selected_page = pages[choice]()
    
    if st.sidebar.button("Logout"):
        logout()

if __name__ == "__main__":
    create_session_state()

    if not st.session_state.authenticated:
        login_page()
    else:
        main()
