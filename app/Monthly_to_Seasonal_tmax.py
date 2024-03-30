import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Monthly to Seasonal Conversion
def Monthly_to_Seasonal_tmax(season, year):
    
    season = st.session_state.get('season', None)
    year = st.session_state.get('year', None)
    
    season_abbreviations = {
    "Belg (FMAM)": "FMAM",
    "Kiremt (JJAS)": "JJAS",
    "Bega (ONDJ)": "ONDJ"
    }
    
    st.markdown("---")        

    st.info(f"Please upload monthly maximum temperature data for all months of the {season} season")

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

        # Group by 'Gh id', 'Station Name', 'Latitude', and 'Longitude' and sum the 'Mean Maximum Temperature'
        seasonal_data = all_data.groupby(['Gh id', 'Station Name', 'Latitude', 'Longitude']).agg({
            'Elevation': 'first',
            'ELID': 'first',
            'Year': 'first',
            'Mean Maximum Temperature': 'mean'
        }).reset_index()

        # Add 'No' column
        seasonal_data['No'] = range(1, len(seasonal_data) + 1)
        
        # Add 'Season' column with the abbreviation of the season
        seasonal_data = seasonal_data.assign(Season=season_abbreviations[season])
        
        # Make 'No' the first column
        cols = ['No'] + [col for col in seasonal_data if col not in ['No', 'Mean Maximum Temperature']] + ['Mean Maximum Temperature']
        seasonal_data = seasonal_data[cols]

        # Display the seasonal data
        st.info(f"Mean Maximum Temperature for {season} season {year}")
        st.write(seasonal_data)

        st.download_button('Download data as CSV', 
                        seasonal_data.to_csv(index=False),  
                        file_name=(f'tmax_{season}_{year}.csv'), 
                        mime='text/csv', key=f"tmax_seasonal")
        
        st.session_state.seasonal_data = seasonal_data 
        
    seasonal_data = st.session_state.get('seasonal_data', None)    
    st.markdown("---")        
    st.subheader('Seasonal Mean Maximum Temperature Plot')  
    if st.button('Generate Map', key="generate_map_tmax_monthly_to_seasonal"): 
        st.info(f"Mean Maximum Temperature for {season} season {year}")
        center_coordinates = (9.5, 40.5) 
        if seasonal_data is not None:
            seasonal_data = round(seasonal_data,3)
            sea_tmax = px.scatter_mapbox(seasonal_data, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Year", "Mean Maximum Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            sea_tmax.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(sea_tmax, use_container_width=True)
            
    
    
    st.markdown("---")   
    st.subheader('Seasonal Mean Maximum Temperature  Summary Statistics') 
    if st.button('Generate statistics', key="generate_statistics_tmax_monthly_to_seasonal"):
        tmax_sea_stat = seasonal_data['Mean Maximum Temperature'].describe(include='all') 
        st.info(f"Seasonal mean maximum temperature summary statistics for the year {year}")
        st.write(round(tmax_sea_stat,2)) 

        st.download_button('Download data as CSV', 
                        tmax_sea_stat.to_csv(index=False),  
                        file_name=f'seasonal_tmax_stat_{year}.csv', 
                        mime='text/csv')
                
    #Create a box plot of the 'mean maximum temperature' column
    st.markdown("---") 
    st.subheader('Seasonal Mean Maximum Temperature Box Plot') 
    if st.button('Generate Box Plot', key="90"):
        st.info(f"Seasonal mean maximum temperature box plot for the year {year}")

    # Create a box plot of the 'Seasonal Mean Maximum Temperature' column
        fig_tmax_sea = go.Figure()

        fig_tmax_sea.add_trace(go.Box(
            y=seasonal_data['Mean Maximum Temperature'],
            name='Mean Maximum Temperature',
            marker_color='blue',
            boxmean=True, # show mean of the data
            #boxpoints='all', # show all points
        ))

        fig_tmax_sea.update_layout(
            title='Box Plot of Seasonal Mean Maximum Temperature',
            title_x = 0.4,
            title_y = 0.9,
            yaxis_title='Mean Maximum Temperature',
            #xaxis_title=f'Month',
            boxmode='group', # group together boxes of the different traces for each value of x
            plot_bgcolor='rgba(0,0,0,0)', # set background color to transparent
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            ),
        )
        
        st.plotly_chart(fig_tmax_sea, use_container_width=True)
    

if __name__ == "__main__":
    Monthly_to_Seasonal_tmax()