import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt

def inter_qqplot(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
            
    st.markdown("#### :blue[4) Norman QQ Plot]" )
    
    if st.checkbox("Show Normal QQ Plot", key="_qqplot"):
        # Create QQ plot using SciPy
        
        _, ax = plt.subplots()  
        
        # Plot QQ plot
        stats.probplot(df_data[variable], dist="norm", plot=ax, fit=True)
        
        # Customize plot appearance
        ax.set_title(f'Normal QQ Plot of {variable}', fontsize=12, color='blue')  # Set title
        ax.set_xlabel('Theoretical Quantiles', fontsize=12, color='green')  # Set x-axis label
        ax.set_ylabel('Sample Quantiles', fontsize=12, color='purple')  # Set y-axis label
        ax.grid(True, linestyle='--', linewidth=0.5, color='gray')  # Add grid
        
        # Set background color
        ax.set_facecolor('lightyellow')
        
        # Display Matplotlib figure using st.pyplot() with explicit argument
        st.pyplot(plt.gcf())  # Pass the current Matplotlib figure explicitly
        
   
    st.markdown("---")
            
if __name__ == "__main__":
    inter_qqplot()