import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Access the shared DataFrame from session state
daily_rf = st.session_state.get('daily_rf', None)

def daily_indices_calculator_rf(variable_type, daily_rf):
    
    # info = """
    # <div style="text-align: justify; color:blue; font-family: Arial, Helvetica, sans-serif;">
    # <p>This page offers an intuitive and interactive platform for exploring rainfall data, focusing on rainfall thresholds and the number of rainy-day.</p>
    #     <ol>
    #         <li> 
    #         <b>Rainfall Threshold</b>: This analysis identifies and visualizes rainfall stations that recorded rainfall above a user-selected threshold. The output includes a table of rainfall data, a downloadable CSV file of the data, a bar chart showing rainfall recorded at each station, and a map showing the locations of the stations. 
    #         </li>
    #         <li>
    #         <b>Number of Rainy Days</b>: This analysis calculates and visualizes the number of rainy days in a selected month. The output includes a table showing the number of rainy days at each station, a downloadable CSV file of the data, and a map showing the locations of the stations.
    #         </li>   
    #     </ol>
    # </div>
    # """
    # st.markdown(info, unsafe_allow_html=True)
    
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    
    st.subheader("Select the analysis type")
    analysis_type = st.selectbox("Select the type of analysis", ["None","Rainfall Threshold", "Number of Rainy Days" ])
    st.info(f"Selected analysis type: {analysis_type}")
    
    if analysis_type == "Rainfall Threshold":
        st.markdown("---")
        st.subheader("Rainfall stations recording above the selected threshold")
        

        # Assuming daily_rf is your dataset containing rainfall data
        if daily_rf is not None:
            max_rf = daily_rf.loc[:, 'Val01':'Val31'].max().max()
            min_rf = daily_rf.loc[:, 'Val01':'Val31'].min().min()
            
            # Create a placeholder for the slider
            slider_placeholder = st.empty()
            
            # Set the slider range dynamically based on the maximum rainfall value
            rf = slider_placeholder.slider('Select rainfall values:', int(min_rf), int(max_rf), 5, key="rainfall_slider1")
            st.info(f"You selected {rf} mm")
            st.info(f"Rainfall recording exceeding {rf} mm.")            

            # Include 'Lon', 'Lat', 'Elev', 'ELID', 'Year', and 'Month' columns
            df_rainfall_stations = daily_rf.loc[:,['Sname', 'Lon', 'Lat', 'Elev', 'ELID', 'Year', 'Month']] 
            df_rainfall_dates = daily_rf.loc[:,'Val01':'Val31']
            df_rainfall_dates_filtered = df_rainfall_dates[(df_rainfall_dates >= rf)]
            
         
            dict_rainfall_reports = {'Station Name': [], 'Lon': [], 'Lat': [], 'Elev': [], 'ELID': [], 'Year': [],
                                    'Month': [], 'Rain Fall (mm)': [], 'Date': []}
            
            
            for index, row in df_rainfall_dates_filtered.iterrows():
                #notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if rainfall.is_integer() and rainfall.is_float()]
                notna_rainfall_dates = [(date[3:], rainfall) for date, rainfall in row.items() if pd.notnull(rainfall)]
                for date, rainfall in notna_rainfall_dates:  
                    dict_rainfall_reports['Station Name'].append(df_rainfall_stations['Sname'].loc[index])
                    dict_rainfall_reports['Lon'].append(df_rainfall_stations['Lon'].loc[index])
                    dict_rainfall_reports['Lat'].append(df_rainfall_stations['Lat'].loc[index])
                    dict_rainfall_reports['Elev'].append(df_rainfall_stations['Elev'].loc[index])
                    dict_rainfall_reports['ELID'].append(df_rainfall_stations['ELID'].loc[index])
                    dict_rainfall_reports['Year'].append(df_rainfall_stations['Year'].loc[index])
                    dict_rainfall_reports['Month'].append(df_rainfall_stations['Month'].loc[index])
                    dict_rainfall_reports['Rain Fall (mm)'].append(rainfall)
                    
                    # Merge year, month, and date to form a full date
                    full_date = f"{year}-{month}-{date}"
                    dict_rainfall_reports['Date'].append(full_date)
                    
                    
                    
            df_rainfall_reports = pd.DataFrame(dict_rainfall_reports)
            df_rainfall_reports = df_rainfall_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})


            try:
                # Convert 'Date' column to datetime format
                df_rainfall_reports['Date'] = pd.to_datetime(df_rainfall_reports['Date'], format='%Y-%B-%d', errors='coerce')

                # Format 'Date' column to display only date, month, and year
                df_rainfall_reports['Date'] = df_rainfall_reports['Date'].dt.strftime('%d-%m-%Y')

            except ValueError as e:
                st.error(f"Error converting 'Date' column to datetime: {e}")
            
            st.write(df_rainfall_reports)
                
            
           
            st.download_button('Download data as CSV', 
                                df_rainfall_reports.to_csv(index=False),  
                                file_name=f'df_rf_{rf}_{month}_{year}.csv', 
                                mime='text/csv')


        st.markdown("---")
        st.subheader("Bar chart of stations exceeding the selected threshold")
                
        df_rainfall_reports['Station_Date'] = df_rainfall_reports['Station Name'] + ':' + df_rainfall_reports['Date'].astype(str)

        fig = px.bar(df_rainfall_reports, x='Station_Date', y='Rain Fall (mm)', 
                    labels={'Rain Fall (mm)': 'Rainfall (mm)', 'Station_Date': 'Station Name & Date'},
                    title='Rainfall Recorded at Each Station', 
                    hover_data=['Station Name', 'Rain Fall (mm)', 'Date'], 
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
                                    hover_data=["Elevation", "Month", "Year", "Longitude", "Latitude","Rain Fall (mm)", "Date"],
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

    elif analysis_type == "Number of Rainy Days":
        st.markdown("---")
        st.subheader("Number of Rainy Days in the selected month")
        clicked = st.button("Calculate Number of Rainy Days")
        if clicked:
                df_rfst_name = daily_rf.loc[:,['Sname']]  
                df_rfst_lon = daily_rf.loc[:,['Lon']]  
                df_rfst_lat = daily_rf.loc[:,['Lat']] 
                df_rfst_Elev = daily_rf.loc[:,['Elev']]
                df_rfst_Ghid = daily_rf.loc[:,['Gh id']]
                df_rfst_ELID = daily_rf.loc[:,['ELID']]
                df_rfst_Year = daily_rf.loc[:,['Year']] 
                df_rfst_Month = daily_rf.loc[:,['Month']]  
                
                        
                df_rfst_dates = daily_rf.loc[:,'Val01':'Val31'].astype(float)
                No_rain_days = df_rfst_dates[df_rfst_dates >= 0.1].count(axis=1)
                No_rain_days = pd.DataFrame(No_rain_days)
                
                dict_no_rainy_days_reports = {'Station Name' : [], 'Lon' : [], 'Lat' : [], 'Gh id' : [],'Elev' : [], 'ELID' : [], 'Year' : [], 'Month' : [],'Rainy Day Count' : [], }  
                
                for index, row in No_rain_days.iterrows():
                        norain_date_rf = [(date, temp) for date, temp in row.items()]
                        for date, temp in norain_date_rf:  
                            dict_no_rainy_days_reports['Station Name'].append(df_rfst_name['Sname'].loc[index])
                            dict_no_rainy_days_reports['Lon'].append(df_rfst_lon['Lon'].loc[index])
                            dict_no_rainy_days_reports['Lat'].append(df_rfst_lat['Lat'].loc[index])
                            dict_no_rainy_days_reports['Elev'].append(df_rfst_Elev['Elev'].loc[index])
                            dict_no_rainy_days_reports['Gh id'].append(df_rfst_Ghid['Gh id'].loc[index])
                            dict_no_rainy_days_reports['ELID'].append(df_rfst_ELID['ELID'].loc[index])
                            dict_no_rainy_days_reports['Year'].append(df_rfst_Year['Year'].loc[index])
                            dict_no_rainy_days_reports['Month'].append(df_rfst_Month['Month'].loc[index])
                            dict_no_rainy_days_reports['Rainy Day Count'].append(temp)
                    
                df_norf_reports = pd.DataFrame(dict_no_rainy_days_reports)
                df_rainfall_reports = df_norf_reports.rename(columns={'Lon': 'Longitude', 'Lat': 'Latitude', 'Elev': 'Elevation'})
                st.write(df_rainfall_reports)  
                
                st.download_button('Download data as CSV', 
                            df_rainfall_reports.to_csv(index=False),  
                            file_name=f'norf_reports_{month}_{year}.csv', 
                            mime='text/csv')
                
                st.markdown("---")
                st.subheader("Map of stations with the number of rainy days")
                st.info(f'Number of rainy days in {month} {year}')
                

                center_coordinates = (9.5, 40.5)
                fig_rf_norf = px.scatter_mapbox(df_rainfall_reports, 
                                                lat="Latitude", lon="Longitude", 
                                                hover_name="Station Name", 
                                                hover_data=["Gh id","Elevation", "Month", "Year", "Longitude", "Latitude", "Rainy Day Count"],
                                                height=600,
                                                width=800
                                                )

                # Set marker size to 15
                fig_rf_norf.update_traces(marker=dict(size=8))

                # Customize the layout with the center coordinates
                fig_rf_norf.update_layout(mapbox_style="open-street-map",
                                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                        mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))

                # Show the map
                st.plotly_chart(fig_rf_norf)    

    else:
        st.error("No daily rainfall data provided.")
        
        
if __name__ == "__main__":
    daily_indices_calculator_rf()