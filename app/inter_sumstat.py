import streamlit as st

def inter_sumstat(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
        
    st.subheader("Exploratory Spatial Data Analysis")

    #st.subheader("Summary Statistics")
    st.markdown("#### :blue[1) Summary Statistics]" )
    if st.button('Compute Summary Statistics', key="_summary"):
        if df_data is not None:
            summary = df_data[variable].describe().T            
            summary['skew'] = df_data[variable].skew()
            summary['kurt'] = df_data[variable].kurt()
            summary['1st_q'] = df_data[variable].quantile(0.25)
            summary['3rd_q'] = df_data[variable].quantile(0.75)
            summary['median'] = df_data[variable].median()
            
            # Transpose the summary statistics
            st.write(summary)
            
        else:
            st.write("Please first upload .csv, .xlsx, or .xls files 😔")
            
    st.markdown("---")

            
if __name__ == "__main__":
    inter_sumstat()