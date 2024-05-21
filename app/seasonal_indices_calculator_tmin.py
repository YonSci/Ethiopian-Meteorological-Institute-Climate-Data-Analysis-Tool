import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state
seas_min = st.session_state.get('seas_min', None)

def seasonal_indices_calculator_tmin(variable_type, seas_min):
    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring minimum temperature data, focusing on temperature thresholds.</p>
    
    #    <b>Minimum temperature</b>: This analysis identifies and visualizes temperature stations that recorded minimum temperature below a user-selected threshold. 
       
    #    The output includes a table of minimum temperature data, a downloadable CSV file of the data, a bar chart showing minimum temperature recorded at each station, and a map showing the locations of the stations. 

    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
    season = st.session_state.get('season', 'Unknown Season')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Minimum temperature recording above the selected threshold")
    
    if seas_min is not None:
        max_tmin = seas_min.loc[:, 'Mean Minimum Temperature':'Mean Minimum Temperature'].max().max()
        min_tmin = seas_min.loc[:, 'Mean Minimum Temperature':'Mean Minimum Temperature'].min().min()
        
        # Create a placeholder for the slider
        slider_placeholder = st.empty()
       
        
        # Set the slider range dynamically based on the minimum temprature value
        tmin = slider_placeholder.slider('Select minimum temprature values:', int(min_tmin), int(max_tmin), 5, key="tmin_slider1")
        st.info(f"You selected {tmin} °C")
        st.info(f"Minimum temperature  recording below {tmin} °C.")            

        # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Season' columns
        df_min_temp_stations = seas_min.loc[:,['Station Name', 'Longitude', 'Latitude', 'Elevation', 'ELID', 'Year', 'Season']] 
        df_min_temp_dates = seas_min.loc[:,'Mean Minimum Temperature':'Mean Minimum Temperature']
        df_min_temp_dates_filtered = df_min_temp_dates[(df_min_temp_dates <= tmin)]
        
        
        dict_min_temp_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                'Season': [], 'Mean Minimum Temperature (°C)': []}
        
        
        for index, row in df_min_temp_dates_filtered.iterrows():
            #notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if rainfall.is_integer() and rainfall.is_float()]
            notna_min_temp_dates = [(date[3:], tmin) for date, tmin in row.items() if pd.notnull(tmin)]
            for date, min_temp in notna_min_temp_dates:  
                dict_min_temp_reports['Station Name'].append(df_min_temp_stations['Station Name'].loc[index])
                dict_min_temp_reports['Lon'].append(df_min_temp_stations['Longitude'].loc[index])
                dict_min_temp_reports['Lat'].append(df_min_temp_stations['Latitude'].loc[index])
                dict_min_temp_reports['Elev'].append(df_min_temp_stations['Elevation'].loc[index])
                dict_min_temp_reports['ELID'].append(df_min_temp_stations['ELID'].loc[index])
                dict_min_temp_reports['Year'].append(df_min_temp_stations['Year'].loc[index])
                dict_min_temp_reports['Season'].append(df_min_temp_stations['Season'].loc[index])
                dict_min_temp_reports['Mean Minimum Temperature (°C)'].append(min_temp)
                
    
                
        df_min_temp_reports = pd.DataFrame(dict_min_temp_reports)
        df_min_temp_reports = df_min_temp_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})

        st.write(df_min_temp_reports.round(2))
            
        
        st.download_button('Download data as CSV', 
                            df_min_temp_reports.to_csv(index=False),  
                            file_name=f'df_rf_{tmin}_{season}_{year}.csv', 
                            mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations below the selected threshold")
                
        df_min_temp_reports['Station Name'] = df_min_temp_reports['Station Name'] 
        st.info(f'Stations below {tmin} °C in {season} {year}')

        fig = px.bar(df_min_temp_reports, x='Station Name', y='Mean Minimum Temperature (°C)', 
                    labels={'Minimum Temperature (°C)': 'Minimum Temperature (°C)'},
                    title='Minimum Temperature Recorded at Each Station', 
                    hover_data=['Station Name', 'Mean Minimum Temperature (°C)'], 
                    width=700, height=500)
        
        
        st.plotly_chart(fig)
        
        st.markdown("---")
        st.subheader("Map of stations below the selected threshold")
        st.info(f'Stations below {tmin} °C in {season} {year}')
        

        center_coordinates = (9.5, 40.5)
        fig_tmin_i1 = px.scatter_mapbox(df_min_temp_reports, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Season", "Year", "Longitude", "Latitude","Mean Minimum Temperature (°C)"],
                                    height=600,
                                    width=800
                                    )

        # Set marker size to 15
        fig_tmin_i1.update_traces(marker=dict(size=10))

        # Customize the layout with the center coordinates
        fig_tmin_i1.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))

        # Show the map
        st.plotly_chart(fig_tmin_i1)      

    
    else:
        st.error("No monthly minimum temperature data provided.")
        
        
if __name__ == "__main__":
    seasonal_indices_calculator_tmin()