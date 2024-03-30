import streamlit as st
import pandas as pd

def dataload_page():
    st.title("Data Load Page")

    # ... (Other UI elements)

    uploaded_data = st.file_uploader("Upload CSV/Excel file", type=["csv", "xlsx"])

    if uploaded_data is not None:
        # Perform actions on the uploaded data
        df = pd.read_csv(uploaded_data)  # Adjust for Excel files if needed
        st.write("Uploaded data:")
        st.write(df)

    # Store the uploaded data in session state
    st.session_state.uploaded_data = df if uploaded_data else None
