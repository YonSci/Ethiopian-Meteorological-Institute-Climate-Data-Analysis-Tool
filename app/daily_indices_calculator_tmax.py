import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state
daily_max = st.session_state.get('daily_max', None)

# maximum temperature ( unit in °C) 

def daily_indices_calculator_tmax(variable_type, daily_max):    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring maximum temperature data, focusing on temperature thresholds.</p>
    
    #    <b>Maximum temperature</b>: This analysis identifies and visualizes temperature stations that recorded maximum temperature above a user-selected threshold. 
       
    #    The output includes a table of maximum temperature data, a downloadable CSV file of the data, a bar chart showing maximum temperature recorded at each station, and a map showing the locations of the stations. 

    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
    
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Stations recording above the selected threshold")
        

    # Assuming daily_max is your dataset containing maximum temperature data
    if daily_max is not None:
        max_tmax = daily_max.loc[:, 'Val01':'Val31'].max().max()
        min_tmax = daily_max.loc[:, 'Val01':'Val31'].min().min()
        
        # Create a placeholder for the slider
        slider_placeholder = st.empty()
        
        # Set the slider range dynamically based on the maximum temperature value
        tmax = slider_placeholder.slider('Select maximum temperature values:', int(min_tmax), int(max_tmax), 5, key="maximum temperature_slider1")
        st.info(f"You selected {tmax} °C")
        st.info(f"Maximum temperature recording exceeding {tmax} °C.")            

        # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Month' columns
        df_max_temp_stations = daily_max.loc[:,['Sname', 'Lon', 'Lat', 'Elev', 'ELID', 'Year', 'Month']] 
        df_max_temp_dates = daily_max.loc[:,'Val01':'Val31']
        df_max_temp_dates_filtered = df_max_temp_dates[(df_max_temp_dates >= tmax)]
        
        
        dict_max_temp_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                'Month': [], 'Maximum Temperature (°C)': [], 'Date': []}
        
        
        for index, row in df_max_temp_dates_filtered.iterrows():
            #notna_max_temp_dates = [(date[3:], max_temp) for date, max_temp in row.items() if max_temp.is_integer() and max_temp.is_float()]
            notna_max_temp_dates = [(date[3:], max_temp) for date, max_temp in row.items() if pd.notnull(max_temp)]
            for date, max_temp in notna_max_temp_dates:  
                dict_max_temp_reports['Station Name'].append(df_max_temp_stations['Sname'].loc[index])
                dict_max_temp_reports['Lon'].append(df_max_temp_stations['Lon'].loc[index])
                dict_max_temp_reports['Lat'].append(df_max_temp_stations['Lat'].loc[index])
                dict_max_temp_reports['Elev'].append(df_max_temp_stations['Elev'].loc[index])
                dict_max_temp_reports['ELID'].append(df_max_temp_stations['ELID'].loc[index])
                dict_max_temp_reports['Year'].append(df_max_temp_stations['Year'].loc[index])
                dict_max_temp_reports['Month'].append(df_max_temp_stations['Month'].loc[index])
                dict_max_temp_reports['Maximum Temperature (°C)'].append(max_temp)
                
                # Merge year, month, and date to form a full date
                full_date = f"{year}-{month}-{date}"
                dict_max_temp_reports['Date'].append(full_date)
                
                
                
        df_max_temp_reports = pd.DataFrame(dict_max_temp_reports)
        df_max_temp_reports = df_max_temp_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})


        try:
            # Convert 'Date' column to datetime format
            df_max_temp_reports['Date'] = pd.to_datetime(df_max_temp_reports['Date'], format='%Y-%B-%d', errors='coerce')

            # Format 'Date' column to display only date, month, and year
            df_max_temp_reports['Date'] = df_max_temp_reports['Date'].dt.strftime('%d-%m-%Y')

        except ValueError as e:
            st.error(f"Error converting 'Date' column to datetime: {e}")
        
        st.write(df_max_temp_reports.round(1))
            
        
        
        st.download_button('Download data as CSV', 
                            df_max_temp_reports.to_csv(index=False),  
                            file_name=f'df_tmax_{tmax}_{month}_{year}.csv', 
                            mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations exceeding the selected threshold")
                
        df_max_temp_reports['Station_Date'] = df_max_temp_reports['Station Name'] + ':' + df_max_temp_reports['Date'].astype(str)

        fig = px.bar(df_max_temp_reports, x='Station_Date', y='Maximum Temperature (°C)', 
                    labels={'Maximum Temperature (°C)': 'Maximum Temperature (°C)', 'Station_Date': 'Station Name & Date'},
                    title='Maximum Temperature Recorded at Each Station', 
                    hover_data=['Station Name', 'Maximum Temperature (°C)', 'Date'], 
                    width=700, height=500)
        st.info(f'Stations that exceeding {tmax} °C in {month} {year}')
        st.plotly_chart(fig)
        
        st.markdown("---")
        st.subheader("Map of stations exceeding the selected threshold")
        st.info(f'Stations that exceeding {tmax} °C in {month} {year}')
        

        center_coordinates = (9.5, 40.5)
        fig_tmax_i1 = px.scatter_mapbox(df_max_temp_reports, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Month", "Year", "Longitude", "Latitude","Maximum Temperature (°C)", "Date"],
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
        st.error("No daily maximum temperature  data provided.")
        
if __name__ == "__main__":
    daily_indices_calculator_tmax()