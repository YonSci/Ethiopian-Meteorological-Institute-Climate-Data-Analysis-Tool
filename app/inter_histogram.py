import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def inter_histogram(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
        
    st.markdown("#### :blue[3) Histogram]" )
    
    bin_size = st.slider('Select Bin Size', min_value=1, max_value=50, value=10)
    st.write(f'Bin size: {bin_size}')
    
    if st.checkbox("Show Histogram", key="_histogram"):
                
        fig, ax1 = plt.subplots(figsize=(10, 8))
        
        # Plot histogram
        hist_values, bins, _ = ax1.hist(df_data[variable], bins=bin_size, color='skyblue', edgecolor='black', alpha=0.7, label='Histogram')
        ax1.set_title(f'Histogram Plot of {variable}', fontsize=20, color='blue')  # Set title
        ax1.set_xlabel(f'{variable}', fontsize=18, color='green')  # Set x-axis label
        ax1.set_ylabel('Frequency', fontsize=18, color='blue')  # Set y-axis label for histogram
        ax1.grid(True, linestyle='--', linewidth=0.5, color='gray')  # Add grid
        
        # Calculate mean and standard deviation for normal distribution
        mu, sigma = np.mean(df_data[variable]), np.std(df_data[variable])
        
        # Create secondary y-axis for normal distribution density
        ax2 = ax1.twinx()
        
        # Plot normal distribution curve
        xmin, xmax = min(df_data[variable]), max(df_data[variable])
        x = np.linspace(xmin, xmax, 100)
        y = stats.norm.pdf(x, mu, sigma)
        ax2.plot(x, y, 'r--', label='Normal Distribution')
        ax2.set_ylabel('Density', fontsize=18, color='red')  # Set y-axis label for normal distribution
        
        # Add legend for both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='best')
        
        # Set background color
        ax1.set_facecolor('lightyellow')
        ax2.set_facecolor('lightyellow')
        
        # Display Matplotlib figure using st.pyplot() with explicit argument
        st.pyplot(fig)  # Pass the current Matplotlib figure explicitly
    
            
    st.markdown("---")
            
if __name__ == "__main__":
    inter_histogram()