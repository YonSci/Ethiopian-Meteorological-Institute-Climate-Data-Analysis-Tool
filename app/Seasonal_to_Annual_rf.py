import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Monthly to Annual Conversion
def Seasonal_to_Annual_rf(year):
    year = st.session_state.get('year', None)
    st.markdown("---")        

    st.info(f"Please upload seasonal rainfall data for all seasons of the year {year}")

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
            'ELID': 'first',
            'Year': 'first',
            'Total Rainfall': 'sum'
        }).reset_index()

        # Add 'No' column
        annual_data['No'] = range(1, len(annual_data) + 1)

        # Make 'No' the first column
        cols = ['No'] + [col for col in annual_data if col not in ['No', 'Total Rainfall']] + ['Total Rainfall']
        annual_data = annual_data[cols]

        # Display the annual data
        st.info(f"Annual total rainfall for the year {year}")
        st.write(annual_data)

        st.download_button('Download data as CSV', 
                        annual_data.to_csv(index=False),  
                        file_name=(f'rf_annual_{year}.csv'), 
                        mime='text/csv', key=f"rf_annual")
        
        st.session_state.annual_data = annual_data 
    
    annual_data = st.session_state.get('annual_data', None)    
    st.markdown("---")        
    st.subheader('Annual Total Rainfall Plot')  
    if st.button('Generate Map', key="generate_map_rf_seasonal_to_annual"): 
        st.info(f"Annual total rainfall for the year {year}")
        center_coordinates = (9.5, 40.5) 
        if annual_data is not None:
            annual_data = round(annual_data,3)
            ann_rf = px.scatter_mapbox(annual_data, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Year", "Total Rainfall"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            ann_rf.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(ann_rf, use_container_width=True)
            
    
    
    st.markdown("---")   
    st.subheader('Annual Rainfall Summary Statistics') 
    if st.button('Generate statistics', key="generate_statistics_rf_seasonal_to_annual"):
        rainfall_ann_stat = annual_data['Total Rainfall'].describe(include='all') 
        st.info(f"Annual total rainfall summary statistics for the year {year}")
        st.write(round(rainfall_ann_stat,2)) 

        st.download_button('Download data as CSV', 
                        rainfall_ann_stat.to_csv(index=False),  
                        file_name=f'annual_total_rf_stat_{year}.csv', 
                        mime='text/csv')
                
    #Create a box plot of the 'Annual Total Rainfall' column
    st.markdown("---") 
    st.subheader('Annual Total Rainfall Box Plot') 
    if st.button('Generate Box Plot', key="90"):
        st.info(f"Annual total rainfall box plot for the year {year}")

    # Create a box plot of the 'Annual Total Rainfall' column
        fig_rf_ann = go.Figure()

        fig_rf_ann.add_trace(go.Box(
            y=annual_data['Total Rainfall'],
            name='Total Rainfall',
            marker_color='blue',
            boxmean=True, # show mean of the data
            #boxpoints='all', # show all points
        ))

        fig_rf_ann.update_layout(
            title='Box Plot of Annual Total Rainfall ',
            title_x = 0.4,
            title_y = 0.9,
            yaxis_title='Rainfall',
            #xaxis_title=f'Month',
            boxmode='group', # group together boxes of the different traces for each value of x
            plot_bgcolor='rgba(0,0,0,0)', # set background color to transparent
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            ),
        )
        
        st.plotly_chart(fig_rf_ann, use_container_width=True)
        
if __name__ == "__main__":
    Seasonal_to_Annual_rf()