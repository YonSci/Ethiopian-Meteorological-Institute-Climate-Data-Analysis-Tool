import streamlit as st
import pandas as pd
import plotly.express as px


# Access the shared DataFrame from session state
daily_max = st.session_state.get('daily_max', None)

def daily_data_miss_tmax(variable_type, daily_max):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire month")
        if st.button('Count Missing Data: Maximum Temperature', key="10"):
            if daily_max is not None:
                missing_data_count_tmax = daily_max.iloc[:, 9:40].isnull().sum().sum()
                st.info(f'Missing maximum temperature data count in {month} {year} is **_{missing_data_count_tmax}_**.')
                total_data_points_tmax = daily_max.iloc[:, 9:40].size
                percentage_missing_tmax = (missing_data_count_tmax / total_data_points_tmax) * 100
                st.info(f'The percentage of missing maximum temperature data in {month} {year} is **_{round(percentage_missing_tmax, 2)}%_**.')
            else:
                st.write("Please Load Data in Data Importing Page 😔")
                
        st.markdown("---")
        st.subheader('Missing data for each day across all stations')        
        if st.button('Tabular Report: Maximum Temperature', key="11"):
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_tmax = daily_max.iloc[:, 9:40].isnull().sum()
                missing_data_col_tmax = pd.DataFrame(missing_data_col_tmax)
                names_tmax = missing_data_col_tmax.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missing_data_col_tmax.columns = names_tmax
                missing_data_col_tmax['Date'] = range(1, len(missing_data_col_tmax) + 1)
                missing_data_col_tmax = missing_data_col_tmax[["Date", "Missing_Data_Count"]]
                # st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
                st.info(f'Sum of missing maximum temperature data counts for each day in {month} {year}')

                st.write(missing_data_col_tmax)
                st.download_button('Download data as CSV', 
                                missing_data_col_tmax.to_csv(index=False),  
                                file_name=(f'tmax_missing_data_by_date_{month}_{year}.csv'), 
                                mime='text/csv', key="12")
                 
  
        graphical_report_button = st.button("Graphical Report: Maximum Temperature")
        if graphical_report_button:
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_tmax = daily_max.iloc[:, 9:40].isnull().sum()
                missing_data_col_tmax = pd.DataFrame(missing_data_col_tmax)
                names_tmax = missing_data_col_tmax.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missing_data_col_tmax.columns = names_tmax
                missing_data_col_tmax['Date'] = range(1, len(missing_data_col_tmax) + 1)
                missing_data_col_tmax = missing_data_col_tmax[["Date", "Missing_Data_Count"]]
            
                # Plotly code
        
                st.info(f'Sum of missing maximum temperature data counts for each day in {month} {year}')
                fig = px.bar(missing_data_col_tmax, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
                            title="Missing Data Counts", width=700, height=500)
                st.plotly_chart(fig)
                
                
        st.markdown("---")
        st.subheader('Sum of missing data counts by station')
        if st.button('Tabular Report: Maximum Temperature', key="13"):
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = daily_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_join['No'] = range(1, len(tmax_join) + 1)  
                tmax_miss_st = tmax_join[["No","Gh id", "Sname", "Lat", "Lon", "Elev", "ELID", "Year", "Month", "Missing_Data_Count"]]
                tmax_miss_st = tmax_miss_st.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
                st.info(f'Sum of missing maximum temperature data counts for {month} {year}')
                st.write(tmax_miss_st)
                st.download_button('Download data as CSV', 
                                tmax_miss_st.to_csv(index=False),  
                                file_name=(f'tmax_missing_data_by_station_{month}_{year}.csv'), 
                                mime='text/csv', key="14")
                
                
        st.markdown("---")
        st.subheader('Stations Above/Below the Specified Threshold Criteria')          
        if st.button('Generate Map: Maximum Temperature ', key="15"):
            st.info(f'Stations with missing maximum temperature data that exceed/below the five-day threshold criteria')
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = daily_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_miss_st_re = tmax_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmax_miss_st = tmax_miss_st_re.copy()
                tmax_miss_st['Legend'] = ['< 5 days missing' if count < 5 else '>= 5 days missing' for count in tmax_miss_st['Missing_Data_Count']]
                color_mapping = {'< 5 days missing': 'green', '>= 5 days missing': 'red'}
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig_tmax_f1 = px.scatter_mapbox(tmax_miss_st, 
                                            lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color="Legend",
                                            color_discrete_map=color_mapping, 
                                            height=600,
                                            width=800
                                            )
                # Customize the layout with the center coordinates
                fig_tmax_f1.update_layout(mapbox_style="open-street-map",
                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig_tmax_f1.update_layout(legend=dict(itemsizing='constant'))
                # Show the map
                st.plotly_chart(fig_tmax_f1)

        
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Maximum Temperature', key="16"):
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = daily_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_miss_st_re = tmax_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmax_miss_st = tmax_miss_st_re.copy()
                miss_tmax5 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 5].copy()
                miss_tmax5['No'] = range(1, len(miss_tmax5) + 1) 
                miss_tmax5.drop(columns=['No.'], inplace=True) 
                miss_tmax5 = miss_tmax5[["No", "Gh id",	"Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month",	"Missing_Data_Count"]]
                
                st.info('Stations without any missing values for more than five consecutive days')
                st.write(miss_tmax5)    
                st.download_button('Download data as CSV', 
                                miss_tmax5.to_csv(index=False),  
                                file_name=(f'tmax_stationsless5_missing_{month}_{year}.csv'), 
                                mime='text/csv', key="17") 
                                  

        if st.button('Generate Map: Maximum Temperature', key="18"):
            st.info('Stations without any missing values for more than five consecutive days')
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:                    
                missingdata_row_tmax = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = daily_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_miss_st_re = tmax_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmax_miss_st = tmax_miss_st_re.copy()
                miss_tmax5 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 5].copy()
                miss_tmax5['No'] = range(1, len(miss_tmax5) + 1) 
                miss_tmax5.drop(columns=['No.'], inplace=True) 
                miss_tmax5 = miss_tmax5[["No", "Gh id","Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig2_tmax_f2 = px.scatter_mapbox(miss_tmax5, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmax_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmax_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmax_f2, use_container_width=True)  
       
             
if __name__ == "__main__":
    daily_data_miss_tmax()