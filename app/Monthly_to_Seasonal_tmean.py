import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Monthly to Seasonal Conversion
def Monthly_to_Seasonal_tmean(season, year):
    
    season = st.session_state.get('season', None)
    year = st.session_state.get('year', None)
    
    season_abbreviations = {
    "Belg (FMAM)": "FMAM",
    "Kiremt (JJAS)": "JJAS",
    "Bega (ONDJ)": "ONDJ"
    }
    
    st.markdown("---")        

    st.info(f"Please upload monthly mean temperature data for all months of the {season} season")

    # Create a file uploader for all months
    uploaded_files = st.file_uploader("Upload data for all months", type=["csv", "xlsx", "xls"], accept_multiple_files=True, key="uploader_all_months")

    dataframes = []

    # Read the data from the uploaded files
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        dataframes.append(data)

    # If all twelve files have been uploaded
    if len(uploaded_files) == 4:
        st.success("All files have been uploaded successfully.")
    else:
        st.warning("Please upload all four files.")

    # Create a select box to choose a file to display
    file_to_display = st.selectbox('Choose a file to display',  ["None"] + [uploaded_file.name for uploaded_file in uploaded_files], key='display_selectbox')
    if file_to_display and file_to_display != "None":
        # Find the index of the selected file in the uploaded_files list
        index = next(i for i, uploaded_file in enumerate(uploaded_files) if uploaded_file.name == file_to_display)
        # Display the data for the selected file
        st.dataframe(dataframes[index])

    if len(dataframes) == 4 and st.button('Convert'):
        all_data = pd.concat(dataframes)

        # Group by 'Gh id', 'Station Name', 'Latitude', and 'Longitude' and sum the 'Mean Temperature'
        seasonal_data = all_data.groupby(['Gh id', 'Station Name', 'Latitude', 'Longitude']).agg({
            'Elevation': 'first',
            'Year': 'first',
            'Mean Temperature': 'mean'
        }).reset_index()

        # Add 'No' column
        seasonal_data['No'] = range(1, len(seasonal_data) + 1)
        
        # Add 'Season' column with the abbreviation of the season
        seasonal_data = seasonal_data.assign(Season=season_abbreviations[season])
        
        # Make 'No' the first column
        cols = ['No'] + [col for col in seasonal_data if col not in ['No', 'Mean Temperature']] + ['Mean Temperature']
        seasonal_data = seasonal_data[cols]

        # Display the seasonal data
        st.info(f"Mean Temperature for {season} season {year}")
        st.write(seasonal_data)

        st.download_button('Download data as CSV', 
                        seasonal_data.to_csv(index=False),  
                        file_name=(f'tmean_{season}_{year}.csv'), 
                        mime='text/csv', key=f"tmean_seasonal")
        
        st.session_state.seasonal_data = seasonal_data 
        
    seasonal_data = st.session_state.get('seasonal_data', None)    
    st.markdown("---")        
    st.subheader('Seasonal Mean Temperature Plot')  
    if st.button('Generate Map', key="generate_map_tmean_monthly_to_seasonal"): 
        st.info(f"Mean Temperature for {season} season {year}")
        center_coordinates = (9.5, 40.5) 
        if seasonal_data is not None:
            seasonal_data = round(seasonal_data,3)
            sea_tmean = px.scatter_mapbox(seasonal_data, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Year", "Mean Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            sea_tmean.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(sea_tmean, use_container_width=True)
            
    
    
    st.markdown("---")   
    st.subheader('Seasonal Mean Temperature  Summary Statistics') 
    if st.button('Generate statistics', key="generate_statistics_tmean_monthly_to_seasonal"):
        tmean_sea_stat = seasonal_data['Mean Temperature'].describe(include='all') 
        st.info(f"Seasonal mean temperature summary statistics for the year {year}")
        st.write(round(tmean_sea_stat,2)) 

        st.download_button('Download data as CSV', 
                        tmean_sea_stat.to_csv(index=False),  
                        file_name=f'seasonal_tmean_stat_{year}.csv', 
                        mime='text/csv')
                
    #Create a box plot of the 'mean temperature' column
    st.markdown("---") 
    st.subheader('Seasonal Mean Temperature Box Plot') 
    if st.button('Generate Box Plot', key="90"):
        st.info(f"Seasonal mean temperature box plot for the year {year}")

    # Create a box plot of the 'Seasonal Mean Temperature' column
        fig_tmean_sea = go.Figure()

        fig_tmean_sea.add_trace(go.Box(
            y=seasonal_data['Mean Temperature'],
            name='Mean Temperature',
            marker_color='blue',
            boxmean=True, # show mean of the data
            #boxpoints='all', # show all points
        ))

        fig_tmean_sea.update_layout(
            title='Box Plot of Seasonal Mean Temperature',
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
        
        st.plotly_chart(fig_tmean_sea, use_container_width=True)
    

if __name__ == "__main__":
    Monthly_to_Seasonal_tmean()