import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from app.inter_nn import inter_nn
from app.inter_idw import inter_idw
from app.inter_idw_block import inter_idw_block
from app.inter_idw_knn import inter_idw_knn
from app.inter_ok import inter_ok
from app.inter_uk import inter_uk
from app.inter_spline import inter_spline
from app.inter_gpr import inter_gpr

def inter_pol(variable_type, df_data):
    
    data_final = None
    df_colname = None
    
    variable = st.session_state.get('variable', 'None')
    data_tran = st.session_state.get('data_tran', 'None' )
    df2 = st.session_state.get('df2', 'None')
    lats = st.session_state.get('lats', 'None')
    lons = st.session_state.get('lons', 'None')
        
    #     if not df_data.empty:
    #         df_data = df_data.rename(columns={df_data.columns[-1]: variable})
            

    st.subheader("Spatial Interpolation")
    
    st.markdown("#### :blue[1) Select Data Type]" )
    
    user_selection = st.radio("Select data type", ["Original Data", "Transformed Data"])
    
    #if 'df_data' in locals() and 'df2' in locals() and df_data is not None and df2 is not None:
    
    if user_selection == "Original Data":
        if df_data is not None:
          data_final = df_data.copy()
        
    else: 
        if df2 is not None:
            data_final = df2.copy()
        else:
            st.error("Please select a transformation method before proceeding")
         
        # if 'df2' in locals() or 'df2' in globals():
        #     if df2 is not None:
        #         data_final = df2.copy()
        #         #st.write(data_final)
        #     else:
        #         st.write("Please select a transformation method before proceeding")
        # else:
        #     st.write("Please select a transformation method before proceeding") 
           
        
    st.session_state.data_final = data_final
 
                            
    st.markdown("#### :blue[2) Select Interpolation Method]" )
    

    interpolation_method = st.selectbox("Select interpolation method",
                                        ["None",   
                                            "Nearest Neighbor (NN)", 
                                            "Inverse Distance Weighting (IDW)",
                                            "IDW Based on Radius",
                                            "IDW Based on KNN",
                                            "Ordinary Kriging (OK)",       
                                            "Universal Kriging (UK)", 
                                            "Spline Interpolation",
                                            "Gaussian Process Regressor",],
                                                                    
                                        key="interpolation", index=0)
    # st.info("The selected interpolation method is: " + interpolation_method)
    
        
    if data_final is not None:
        df_colname = data_final[variable]
        df_colname = df_colname.name
    
     
    if interpolation_method == "Nearest Neighbor (NN)":
        inter_nn()
        
    elif interpolation_method == "Inverse Distance Weighting (IDW)":
        inter_idw()
        
    elif interpolation_method == "IDW Based on Radius":
        inter_idw_block()
        
    elif interpolation_method == "IDW Based on KNN":
        inter_idw_knn()
        
    elif interpolation_method == "Ordinary Kriging (OK)":
        inter_ok()
        
    elif interpolation_method == "Universal Kriging (UK)": 
        inter_uk()
        
    elif interpolation_method == "Spline Interpolation":
        inter_spline()
        
    elif interpolation_method == "Gaussian Process Regressor":
        inter_gpr()
    
    else:
        st.stop()
        # st.info("No interpolation method selected")
    
         
    
            
        
        
                
    st.markdown("---")
            
if __name__ == "__main__":
    inter_pol()