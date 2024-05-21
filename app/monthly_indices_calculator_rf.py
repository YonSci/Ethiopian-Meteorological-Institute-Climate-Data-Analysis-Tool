import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state
mon_rf = st.session_state.get('mon_rf', None)

def monthly_indices_calculator_rf(variable_type, mon_rf):
    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring rainfall data, focusing on rainfall thresholds.</p>
    # <b>Rainfall Threshold</b>: This analysis identifies and visualizes rainfall stations that recorded rainfall above a user-selected threshold. 
    
    # The output includes a table of rainfall data, a downloadable CSV file of the data, a bar chart showing rainfall recorded at each station, and a map showing the locations of the stations. 
  
    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
    
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Rainfall stations recording above the selected threshold")
    
    if mon_rf is not None:
        max_rf = mon_rf.loc[:, 'Total Rainfall':'Total Rainfall'].max().max()
        min_rf = mon_rf.loc[:, 'Total Rainfall':'Total Rainfall'].min().min()
        
        # Create a placeholder for the slider
        slider_placeholder = st.empty()
       
        
        # Set the slider range dynamically based on the maximum rainfall value
        rf = slider_placeholder.slider('Select rainfall values:', int(min_rf), int(max_rf), 5, key="rainfall_slider1")
        st.info(f"You selected {rf} mm")
        st.info(f"Rainfall recording exceeding {rf} mm.")            

        # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Month' columns
        df_rainfall_stations = mon_rf.loc[:,['Station Name', 'Longitude', 'Latitude', 'Elevation', 'ELID', 'Year', 'Month']] 
        df_rainfall_dates = mon_rf.loc[:,'Total Rainfall':'Total Rainfall']
        df_rainfall_dates_filtered = df_rainfall_dates[(df_rainfall_dates >= rf)]
        
        
        dict_rainfall_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                'Month': [], 'Rain Fall (mm)': []}
        
        
        for index, row in df_rainfall_dates_filtered.iterrows():
            #notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if rainfall.is_integer() and rainfall.is_float()]
            notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if pd.notnull(rainfall)]
            for date, rainfall in notna_rainfall_dates:  
                dict_rainfall_reports['Station Name'].append(df_rainfall_stations['Station Name'].loc[index])
                dict_rainfall_reports['Lon'].append(df_rainfall_stations['Longitude'].loc[index])
                dict_rainfall_reports['Lat'].append(df_rainfall_stations['Latitude'].loc[index])
                dict_rainfall_reports['Elev'].append(df_rainfall_stations['Elevation'].loc[index])
                dict_rainfall_reports['ELID'].append(df_rainfall_stations['ELID'].loc[index])
                dict_rainfall_reports['Year'].append(df_rainfall_stations['Year'].loc[index])
                dict_rainfall_reports['Month'].append(df_rainfall_stations['Month'].loc[index])
                dict_rainfall_reports['Rain Fall (mm)'].append(rainfall)
                
    
                
        df_rainfall_reports = pd.DataFrame(dict_rainfall_reports)
        df_rainfall_reports = df_rainfall_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})


        st.write(df_rainfall_reports)
            
        
        
        st.download_button('Download data as CSV', 
                            df_rainfall_reports.to_csv(index=False),  
                            file_name=f'df_rf_{rf}_{month}_{year}.csv', 
                            mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations exceeding the selected threshold")
                
        df_rainfall_reports['Station Name'] = df_rainfall_reports['Station Name'] 

        fig = px.bar(df_rainfall_reports, x='Station Name', y='Rain Fall (mm)', 
                    labels={'Rain Fall (mm)': 'Rainfall (mm)'},
                    title='Rainfall Recorded at Each Station', 
                    hover_data=['Station Name', 'Rain Fall (mm)'], 
                    width=700, height=500)
        st.info(f'Stations that exceeding {rf} mm in {month} {year}')
        st.plotly_chart(fig)
        
        st.markdown("---")
        st.subheader("Map of stations exceeding the selected threshold")
        st.info(f'Stations that exceeding {rf} mm in {month} {year}')
        

        center_coordinates = (9.5, 40.5)
        fig_rf_i1 = px.scatter_mapbox(df_rainfall_reports, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Month", "Year", "Longitude", "Latitude","Rain Fall (mm)"],
                                    height=600,
                                    width=800
                                    )

        # Set marker size to 15
        fig_rf_i1.update_traces(marker=dict(size=10))

        # Customize the layout with the center coordinates
        fig_rf_i1.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))

        # Show the map
        st.plotly_chart(fig_rf_i1)      

    
    else:
        st.error("No monthly rainfall data provided.")
        
        
if __name__ == "__main__":
    monthly_indices_calculator_rf()