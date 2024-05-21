import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state

seas_max = st.session_state.get('seas_max', None)

def seasonal_indices_calculator_tmax(variable_type, seas_max):
    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring maximum temperature data, focusing on temperature thresholds.</p>
    
    #    <b>Maximum temperature</b>: This analysis identifies and visualizes temperature stations that recorded maximum temperature above a user-selected threshold. 
       
    #    The output includes a table of maximum temperature data, a downloadable CSV file of the data, a bar chart showing maximum temperature recorded at each station, and a map showing the locations of the stations. 

    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
        
    season = st.session_state.get('season', 'Unknown Season')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Maximum temperature recording above the selected threshold")
    
    if seas_max is not None:
        max_tmax = seas_max.loc[:, 'Mean Maximum Temperature':'Mean Maximum Temperature'].max().max()
        min_tmax = seas_max.loc[:, 'Mean Maximum Temperature':'Mean Maximum Temperature'].min().min()
        
        # Create a placeholder for the slider
        slider_placeholder = st.empty()
       
        
        # Set the slider range dynamically based on the maximum temprature value
        tmax = slider_placeholder.slider('Select maximum temperature values:', int(min_tmax), int(max_tmax), 5, key="tmax_slider1")
        st.info(f"You selected {tmax} °C")
        st.info(f"Maximum temperature  recording exceeding {tmax} °C.")            

        # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Season' columns
        df_max_temp_stations = seas_max.loc[:,['Station Name', 'Longitude', 'Latitude', 'Elevation', 'ELID', 'Year', 'Season']] 
        df_max_temp_dates = seas_max.loc[:,'Mean Maximum Temperature':'Mean Maximum Temperature']
        df_max_temp_dates_filtered = df_max_temp_dates[(df_max_temp_dates >= tmax)]
        
        
        dict_max_temp_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                'Season': [], 'Mean Maximum Temperature (°C)': []}
        
        
        for index, row in df_max_temp_dates_filtered.iterrows():
            #notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if rainfall.is_integer() and rainfall.is_float()]
            notna_max_temp_dates = [(date[3:], tmax) for date, tmax in row.items() if pd.notnull(tmax)]
            for date, max_temp in notna_max_temp_dates:  
                dict_max_temp_reports['Station Name'].append(df_max_temp_stations['Station Name'].loc[index])
                dict_max_temp_reports['Lon'].append(df_max_temp_stations['Longitude'].loc[index])
                dict_max_temp_reports['Lat'].append(df_max_temp_stations['Latitude'].loc[index])
                dict_max_temp_reports['Elev'].append(df_max_temp_stations['Elevation'].loc[index])
                dict_max_temp_reports['ELID'].append(df_max_temp_stations['ELID'].loc[index])
                dict_max_temp_reports['Year'].append(df_max_temp_stations['Year'].loc[index])
                dict_max_temp_reports['Season'].append(df_max_temp_stations['Season'].loc[index])
                dict_max_temp_reports['Mean Maximum Temperature (°C)'].append(max_temp)
                
    
                
        df_max_temp_reports = pd.DataFrame(dict_max_temp_reports)
        df_max_temp_reports = df_max_temp_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})

        st.write(df_max_temp_reports.round(2))
            
        
        st.download_button('Download data as CSV', 
                            df_max_temp_reports.to_csv(index=False),  
                            file_name=f'df_rf_{tmax}_{season}_{year}.csv', 
                            mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations exceeding the selected threshold")
                
        df_max_temp_reports['Station Name'] = df_max_temp_reports['Station Name'] 
        st.info(f'Stations that exceeding {tmax} °C in {season} {year}')

        fig = px.bar(df_max_temp_reports, x='Station Name', y='Mean Maximum Temperature (°C)', 
                    labels={'Maximum Temperature (°C)': 'Maximum Temperature (°C)'},
                    title='Maximum Temperature Recorded at Each Station', 
                    hover_data=['Station Name', 'Mean Maximum Temperature (°C)'], 
                    width=700, height=500)
        
        
        st.plotly_chart(fig)
        
        st.markdown("---")
        st.subheader("Map of stations exceeding the selected threshold")
        st.info(f'Stations that exceeding {tmax} °C in {season} {year}')
        

        center_coordinates = (9.5, 40.5)
        fig_tmax_i1 = px.scatter_mapbox(df_max_temp_reports, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Season", "Year", "Longitude", "Latitude","Mean Maximum Temperature (°C)"],
                                    height=600,
                                    width=800
                                    )

        # Set marker size to 15
        fig_tmax_i1.update_traces(marker=dict(size=10))

        # Customize the layout with the center coordinates
        fig_tmax_i1.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))

        # Show the map
        st.plotly_chart(fig_tmax_i1)      

    
    else:
        st.error("No monthly maximum temperature data provided.")
        
        
if __name__ == "__main__":
    seasonal_indices_calculator_tmax()