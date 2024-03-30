import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Monthly to Annual Conversion
def Seasonal_to_Annual_tmean(year):
    year = st.session_state.get('year', None)
    st.markdown("---")    
    
    st.info(f"Please upload seasonal mean temperature data for all seasons of the year {year}")

    # Create a file uploader for all months
    uploaded_files = st.file_uploader("Upload data for all season", type=["csv", "xlsx", "xls"], accept_multiple_files=True, key="uploader_all_seasons")

    dataframes = []

    # Read the data from the uploaded files
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        dataframes.append(data)

    # If all twelve files have been uploaded
    if len(uploaded_files) == 3:
        st.success("All files have been uploaded successfully.")
    else:
        st.warning("Please upload all three files.")

    # Create a select box to choose a file to display
    file_to_display = st.selectbox('Choose a file to display',  ["None"] + [uploaded_file.name for uploaded_file in uploaded_files], key='display_selectbox')
    if file_to_display and file_to_display != "None":
        # Find the index of the selected file in the uploaded_files list
        index = next(i for i, uploaded_file in enumerate(uploaded_files) if uploaded_file.name == file_to_display)
        # Display the data for the selected file
        st.dataframe(dataframes[index])

    if len(dataframes) == 3 and st.button('Convert'):
        all_data = pd.concat(dataframes)

        # Group by 'Gh id', 'Station Name', 'Latitude', and 'Longitude' and sum the 'Total Rainfall'
        annual_data = all_data.groupby(['Gh id', 'Station Name', 'Latitude', 'Longitude']).agg({
            'Elevation': 'first',
            'Year': 'first',
            'Mean Temperature': 'mean'
        }).reset_index()

        # Add 'No' column
        annual_data['No'] = range(1, len(annual_data) + 1)

        # Make 'No' the first column
        cols = ['No'] + [col for col in annual_data if col not in ['No', 'Mean Temperature']] + ['Mean Temperature']
        annual_data = annual_data[cols]

        # Display the annual data
        st.info(f"Annual Mean Temperature for the year {year}")
        st.write(annual_data)

        st.download_button('Download data as CSV', 
                        annual_data.to_csv(index=False),  
                        file_name=(f'tmean_annual_{year}.csv'), 
                        mime='text/csv', key=f"tmean_annual")
        
        st.session_state.annual_data = annual_data 
    
    annual_data = st.session_state.get('annual_data', None)    
    st.markdown("---")        
    st.subheader('Annual Mean Temperature Plot')  
    if st.button('Generate Map', key="generate_map_tmean_seasonal_to_annual"): 
        st.info(f"Annual mean temperature for the year {year}")
        center_coordinates = (9.5, 40.5) 
        if annual_data is not None:
            annual_data = round(annual_data,3)
            ann_tmean = px.scatter_mapbox(annual_data, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Year", "Mean Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            ann_tmean.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(ann_tmean, use_container_width=True)
            
    
    
    st.markdown("---")   
    st.subheader('Annual Mean Temperature Summary Statistics') 
    if st.button('Generate statistics', key="generate_statistics_tmean_seasonal_to_annual"):
        tmean_ann_stat = annual_data['Mean Temperature'].describe(include='all') 
        st.info(f"Annual mean temperature summary statistics for the year {year}")
        st.write(round(tmean_ann_stat,2)) 

        st.download_button('Download data as CSV', 
                        tmean_ann_stat.to_csv(index=False),  
                        file_name=f'annual_mean_tmean_stat_{year}.csv', 
                        mime='text/csv')
                
    #Create a box plot of the 'Annual Mean Temperature' column
    st.markdown("---") 
    st.subheader('Annual Mean Temperature Box Plot') 
    if st.button('Generate Box Plot', key="90"):
        st.info(f"Annual mean temperature box plot for the year {year}")

    # Create a box plot of the 'Annual Total Rainfall' column
        fig_tmean_ann = go.Figure()

        fig_tmean_ann.add_trace(go.Box(
            y=annual_data['Mean Temperature'],
            name='Mean Temperature',
            marker_color='blue',
            boxmean=True, # show mean of the data
            #boxpoints='all', # show all points
        ))

        fig_tmean_ann.update_layout(
            title='Box Plot of Annual Mean Temperature',
            title_x = 0.4,
            title_y = 0.9,
            yaxis_title='Mean Temperature',
            #xaxis_title=f'Month',
            boxmode='group', # group together boxes of the different traces for each value of x
            plot_bgcolor='rgba(0,0,0,0)', # set background color to transparent
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            ),
        )
        
        st.plotly_chart(fig_tmean_ann, use_container_width=True)
    


if __name__ == "__main__":
    Seasonal_to_Annual_tmean()