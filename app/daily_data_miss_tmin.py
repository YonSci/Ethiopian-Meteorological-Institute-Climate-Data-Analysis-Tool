import streamlit as st
import pandas as pd
import plotly.express as px


# Access the shared DataFrame from session state
daily_min = st.session_state.get('daily_min', None)

def daily_data_miss_tmin(variable_type, daily_min):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire month")
        if st.button('Count Missing Data: Minimum Temperature', key="19"):
            if daily_min is not None:
                missing_data_count_tmin = daily_min.iloc[:, 9:40].isnull().sum().sum()
                st.info(f'Missing minimum temperature data count in {month} {year} is **_{missing_data_count_tmin}_**.')
                total_data_points_tmin = daily_min.iloc[:, 9:40].size
                percentage_missing_tmin = (missing_data_count_tmin / total_data_points_tmin) * 100
                st.info(f'The percentage of missing minimum temperature data in {month} {year} is **_{round(percentage_missing_tmin, 2)}%_**.')
            else:
                st.write("Please Load Data in Data Importing Page 😔")
                
        st.markdown("---")
        st.subheader('Missing data for each day across all stations')        
        if st.button('Tabular Report: Minimum Temperature', key="20"):
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_tmin = daily_min.iloc[:, 9:40].isnull().sum()
                missing_data_col_tmin = pd.DataFrame(missing_data_col_tmin)
                names_tmin = missing_data_col_tmin.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missing_data_col_tmin.columns = names_tmin
                missing_data_col_tmin['Date'] = range(1, len(missing_data_col_tmin) + 1)
                missing_data_col_tmin = missing_data_col_tmin[["Date", "Missing_Data_Count"]]
                # st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
                st.info(f'Sum of missing minimum temperature data counts for each day in {month} {year}')

                st.write(missing_data_col_tmin)
                st.download_button('Download data as CSV', 
                                missing_data_col_tmin.to_csv(index=False),  
                                file_name=(f'tmin_missing_data_by_date_{month}_{year}.csv'), 
                                mime='text/csv', key="21")
                 
  
        graphical_report_button = st.button("Graphical Report: Minimum Temperature")
        if graphical_report_button:
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_tmin = daily_min.iloc[:, 9:40].isnull().sum()
                missing_data_col_tmin = pd.DataFrame(missing_data_col_tmin)
                names_tmin = missing_data_col_tmin.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missing_data_col_tmin.columns = names_tmin
                missing_data_col_tmin['Date'] = range(1, len(missing_data_col_tmin) + 1)
                missing_data_col_tmin = missing_data_col_tmin[["Date", "Missing_Data_Count"]]
            
                # Plotly code
        
                st.info(f'Sum of missing minimum temperature data counts for each day in {month} {year}')
                fig = px.bar(missing_data_col_tmin, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
                            title="Missing Data Counts", width=700, height=500)
                st.plotly_chart(fig)
                
                
        st.markdown("---")
        st.subheader('Sum of missing data counts by station')
        if st.button('Tabular Report: Minimum Temperature', key="22"):
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = daily_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_join['No'] = range(1, len(tmin_join) + 1)  
                tmin_miss_st = tmin_join[["No","Gh id", "Sname", "Lat", "Lon", "Elev", "ELID", "Year", "Month", "Missing_Data_Count"]]
                tmin_miss_st = tmin_miss_st.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
                st.info(f'Sum of missing minimum temperature data counts for {month} {year}')
                st.write(tmin_miss_st)
                st.download_button('Download data as CSV', 
                                tmin_miss_st.to_csv(index=False),  
                                file_name=(f'tmin_missing_data_by_station_{month}_{year}.csv'), 
                                mime='text/csv', key="23")
                
                
        st.markdown("---")
        st.subheader('Stations Above/Below the Specified Threshold Criteria')          
        if st.button('Generate Map: Minimum Temperature ', key="24"):
            st.info(f'Stations with missing minimum temperature data that exceed/below the five-day threshold criteria')
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = daily_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st_re = tmin_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmin_miss_st = tmin_miss_st_re.copy()
                tmin_miss_st['Legend'] = ['< 5 days missing' if count < 5 else '>= 5 days missing' for count in tmin_miss_st['Missing_Data_Count']]
                color_mapping = {'< 5 days missing': 'green', '>= 5 days missing': 'red'}
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig_tmin_f1 = px.scatter_mapbox(tmin_miss_st, 
                                            lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color="Legend",
                                            color_discrete_map=color_mapping, 
                                            height=600,
                                            width=800
                                            )
                # Customize the layout with the center coordinates
                fig_tmin_f1.update_layout(mapbox_style="open-street-map",
                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig_tmin_f1.update_layout(legend=dict(itemsizing='constant'))
                # Show the map
                st.plotly_chart(fig_tmin_f1)

        
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="25"):
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = daily_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st_re = tmin_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmin_miss_st = tmin_miss_st_re.copy()
                miss_tmin5 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 5].copy()
                miss_tmin5['No'] = range(1, len(miss_tmin5) + 1) 
                miss_tmin5.drop(columns=['No.'], inplace=True) 
                miss_tmin5 = miss_tmin5[["No", "Gh id",	"Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month",	"Missing_Data_Count"]]
                
                st.info('Stations without any missing values for more than five consecutive days')
                st.write(miss_tmin5)    
                st.download_button('Download data as CSV', 
                                miss_tmin5.to_csv(index=False),  
                                file_name=(f'tmin_stationsless5_missing_{month}_{year}.csv'), 
                                mime='text/csv', key="26") 
                                  

        if st.button('Generate Map: Minimum Temperature', key="27"):
            st.info('Stations without any missing values for more than five consecutive days')
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:                    
                missingdata_row_tmin = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = daily_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st_re = tmin_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                tmin_miss_st = tmin_miss_st_re.copy()
                miss_tmin5 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 5].copy()
                miss_tmin5['No'] = range(1, len(miss_tmin5) + 1) 
                miss_tmin5.drop(columns=['No.'], inplace=True) 
                miss_tmin5 = miss_tmin5[["No", "Gh id","Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig2_tmin_f2 = px.scatter_mapbox(miss_tmin5, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmin_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmin_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmin_f2, use_container_width=True)  
       
if __name__ == "__main__":
    daily_data_miss_tmin()