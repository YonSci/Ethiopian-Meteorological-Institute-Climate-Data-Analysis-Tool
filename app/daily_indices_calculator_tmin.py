import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state
daily_min = st.session_state.get('daily_min', None)

# minimum temperature ( unit in °C) 

def daily_indices_calculator_tmin(variable_type, daily_min):    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring minimum temperature data, focusing on temperature thresholds.</p>
    
    #    <b>Minimum temperature</b>: This analysis identifies and visualizes temperature stations that recorded minimum temperature below a user-selected threshold. 
       
    #    The output includes a table of minimum temperature data, a downloadable CSV file of the data, a bar chart showing minimum temperature recorded at each station, and a map showing the locations of the stations. 

    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
    
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Stations recording below the selected threshold")
        

    # Assuming daily_min is your dataset containing minimum temperature data
    if daily_min is not None:
        max_tmin = daily_min.loc[:, 'Val01':'Val31'].max().max()
        min_tmin = daily_min.loc[:, 'Val01':'Val31'].min().min()
        
        # Create a placeholder for the slider
        slider_placeholder = st.empty()
        
        # Set the slider range dynamically based on the minimum temperature value
        tmin = slider_placeholder.slider('Select minimum temperature values:', int(min_tmin), int(max_tmin), 5, key="minimum temperature_slider1")
        st.info(f"You selected {tmin} °C")
        st.info(f"Minimum temperature recording below  {tmin} °C.") 
        

        # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Month' columns
        df_min_temp_stations = daily_min.loc[:,['Sname', 'Lon', 'Lat', 'Elev', 'ELID', 'Year', 'Month']] 
        df_min_temp_dates = daily_min.loc[:,'Val01':'Val31']
        df_min_temp_dates_filtered = df_min_temp_dates[(df_min_temp_dates <= tmin)]
        
        
        dict_min_temp_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                'Month': [], 'Minimum Temperature (°C)': [], 'Date': []}
        
        
        for index, row in df_min_temp_dates_filtered.iterrows():
            #notna_min_temp_dates = [(date[3:], min_temp) for date, min_temp in row.items() if min_temp.is_integer() and min_temp.is_float()]
            notna_min_temp_dates = [(date[3:], min_temp) for date, min_temp in row.items() if pd.notnull(min_temp)]
            for date, min_temp in notna_min_temp_dates:  
                dict_min_temp_reports['Station Name'].append(df_min_temp_stations['Sname'].loc[index])
                dict_min_temp_reports['Lon'].append(df_min_temp_stations['Lon'].loc[index])
                dict_min_temp_reports['Lat'].append(df_min_temp_stations['Lat'].loc[index])
                dict_min_temp_reports['Elev'].append(df_min_temp_stations['Elev'].loc[index])
                dict_min_temp_reports['ELID'].append(df_min_temp_stations['ELID'].loc[index])
                dict_min_temp_reports['Year'].append(df_min_temp_stations['Year'].loc[index])
                dict_min_temp_reports['Month'].append(df_min_temp_stations['Month'].loc[index])
                dict_min_temp_reports['Minimum Temperature (°C)'].append(min_temp)
                
                # Merge year, month, and date to form a full date
                full_date = f"{year}-{month}-{date}"
                dict_min_temp_reports['Date'].append(full_date)
                
                
                
        df_min_temp_reports = pd.DataFrame(dict_min_temp_reports)
        df_min_temp_reports = df_min_temp_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})


        try:
            # Convert 'Date' column to datetime format
            df_min_temp_reports['Date'] = pd.to_datetime(df_min_temp_reports['Date'], format='%Y-%B-%d', errors='coerce')

            # Format 'Date' column to display only date, month, and year
            df_min_temp_reports['Date'] = df_min_temp_reports['Date'].dt.strftime('%d-%m-%Y')

        except ValueError as e:
            st.error(f"Error converting 'Date' column to datetime: {e}")
        
        st.write(df_min_temp_reports)
            
        
        
        st.download_button('Download data as CSV', 
                            df_min_temp_reports.to_csv(index=False),  
                            file_name=f'df_tmin_{tmin}_{month}_{year}.csv', 
                            mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations below  the selected threshold")
                
        df_min_temp_reports['Station_Date'] = df_min_temp_reports['Station Name'] + ':' + df_min_temp_reports['Date'].astype(str)

        fig = px.bar(df_min_temp_reports, x='Station_Date', y='Minimum Temperature (°C)', 
                    labels={'Minimum Temperature (°C)': 'Minimum Temperature (°C)', 'Station_Date': 'Station Name & Date'},
                    title='Minimum Temperature Recorded at Each Station', 
                    hover_data=['Station Name', 'Minimum Temperature (°C)', 'Date'], 
                    width=700, height=500)
        st.info(f'Stations below  {tmin} °C in {month} {year}')
        st.plotly_chart(fig)
        
        st.markdown("---")
        st.subheader("Map of stations below  the selected threshold")
        st.info(f'Stations below  {tmin} °C in {month} {year}')
        

        center_coordinates = (9.5, 40.5)
        fig_tmin_i1 = px.scatter_mapbox(df_min_temp_reports, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Month", "Year", "Longitude", "Latitude","Minimum Temperature (°C)", "Date"],
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
        st.error("No daily minimum temperature  data provided.")
        
if __name__ == "__main__":
    daily_indices_calculator_tmin()