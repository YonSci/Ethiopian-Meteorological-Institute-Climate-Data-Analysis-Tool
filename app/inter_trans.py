import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats



def inter_trans(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')
    data_tran = None  
    df2 = None
    

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
                
    st.subheader("Spatial Data Transformations")
    
    
    transformation = st.selectbox("Select Transformation Method", ["None","Box-Cox Transformation", 
                                                                   "Log Transformation",
                                                                   "Arcsine Transformation",
                                                                   "Normal Scores Transformation"],
                                  index=0 , key="transformation")
   
        
    if transformation == "None":
        st.info("No transformation selected")
       
        
    elif transformation == "Box-Cox Transformation":
        st.info("Box-Cox Transformation: $y(\lambda) = (y^\lambda - 1) / \lambda$, where $\lambda$ is the transformation parameter")
        data_tran = df_data.copy()
        fitted_data, fitted_lambda = stats.boxcox(data_tran[variable])   
        data_tran['Transformed_Data'] = fitted_data   
        st.write(data_tran)
        df1 = data_tran.drop(columns=[variable])
        df2 = df1.rename(columns={'Transformed_Data': variable})  
        #st.write(df2)
  
        

        st.info(f'The optimal lambda value is: {fitted_lambda.round(2)}')

        fig, axes = plt.subplots(1,2,figsize=(8,4))

        # Plot the Distribution of Data Values
        sns.histplot(data_tran[variable], kde=True, ax=axes[0]) 
        axes[0].set_title("Before Transformation")
        axes[0].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[0].set_facecolor('lightyellow')
        
        # Plot the Distribution of the Transformed Data Values
        sns.histplot(df2[variable], kde=True, ax=axes[1]) 
        axes[1].set_title("After Transformation")
        axes[1].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[1].set_facecolor('lightyellow')

        fig.tight_layout()
        st.pyplot(fig)
    
        
    elif transformation == "Log Transformation":
        st.info("Log Transformation: $y = log(y)$")
        data_tran = df_data.copy()
        fitted_data = np.log(data_tran[variable])
        data_tran["Transformed_Data"] = fitted_data
        st.write(data_tran)
        df1 = data_tran.drop(columns=[variable])
        df2 = df1.rename(columns={'Transformed_Data': variable})  
        
        fig, axes = plt.subplots(1,2,figsize=(8,4))

        # # Plot the Distribution of Data Values
        sns.histplot(data_tran[variable], kde=True, ax=axes[0]) 
        axes[0].set_title("Before Transformation")
        axes[0].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[0].set_facecolor('lightyellow')
        
        # # Plot the Distribution of the Transformed Data Values
        sns.histplot(df2[variable], kde=True, ax=axes[1]) 
        axes[1].set_title("After Transformation")
        axes[1].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[1].set_facecolor('lightyellow')

        fig.tight_layout()
        st.pyplot(fig)
    

        
    elif transformation == "Arcsine Transformation":
        st.info("Arcsine Transformation: $y = arcsin(\sqrt{y})$")    
        data_tran = df_data.copy()    
        df_transform  = data_tran[variable]/ max(data_tran[variable]) 
        fitted_data = np.arcsin(np.sqrt(df_transform))
        data_tran["Transformed_Data"] = fitted_data
        st.write(data_tran)
        df1 = data_tran.drop(columns=[variable])
        df2 = df1.rename(columns={'Transformed_Data': variable})  
      
        
        fig, axes = plt.subplots(1,2,figsize=(8,4))

        sns.histplot(data_tran[variable], kde=True, ax=axes[0]) 
        axes[0].set_title("Before Transformation")
        axes[0].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[0].set_facecolor('lightyellow')
        
        # # Plot the Distribution of the Transformed Data Values
        sns.histplot(df2[variable], kde=True, ax=axes[1]) 
        axes[1].set_title("After Transformation")
        axes[1].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[1].set_facecolor('lightyellow')

        fig.tight_layout()
        st.pyplot(fig)
        
        
    elif transformation == "Normal Scores Transformation":
        # write blom transformation in latex
        st.info("Normal Scores Transformation: $G^{-1}\\left(\\frac{R_i - 0.375}{n + 0.25}\\right)$")
        data_tran = df_data.copy()
        def blom_transform(data):
            ranks = stats.rankdata(data)
            n = len(data)
            quantiles = (ranks - 0.375) / (n + 0.25)
            transformed_data = stats.norm.ppf(quantiles)
            return transformed_data
        
        
        # Perform normal scores transformation
        df_transform = blom_transform(data_tran[variable])
        data_tran["Transformed_Data"] = df_transform
        st.write(data_tran)
        df1 = data_tran.drop(columns=[variable])
        df2 = df1.rename(columns={'Transformed_Data': variable})  
        
        
        
        fig, axes = plt.subplots(1,2,figsize=(8,4))

        # # Plot the Distribution of Data Values
        sns.histplot(data_tran[variable], kde=True, ax=axes[0]) 
        axes[0].set_title("Before Transformation")
        axes[0].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[0].set_facecolor('lightyellow')
        
        # # Plot the Distribution of the Transformed Data Values
        sns.histplot(df2[variable], kde=True, ax=axes[1]) 
        axes[1].set_title("After Transformation")
        axes[1].grid(True, linestyle='--', linewidth=0.5, color='gray')
        axes[1].set_facecolor('lightyellow')

        fig.tight_layout()
        st.pyplot(fig)
        
        
        #st.write(data_tran)
        
        
        
        st.markdown("---")
    st.session_state.data_tran = data_tran
    st.session_state.df2 = df2
    
    
                
if __name__ == "__main__":
    inter_trans()