import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared month value from session state
# month = st.session_state.get('month', 'Unknown Month')
season = st.session_state.get('season', 'Unknown Month')
year = st.session_state.get('year', 'Unknown Year')   
variable_type = st.session_state.get('variable_type', 'None')
timestep_analysis = st.session_state.get('timestep_analysis', 'None')

# Access the shared DataFrame from session state
seas_rf = st.session_state.get('seas_rf', 'None')
seas_max = st.session_state.get('seas_max', 'None')
seas_min = st.session_state.get('seas_min', 'None')

def seasonal_data_miss(variable_type):
    if variable_type == 'Rainfall':  
        st.markdown("---")
        st.subheader("Total Missing Data Count")
        if st.button('Count Missing Data for Rainfall', key="51"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_rf = seas_rf.iloc[:, 9:10].isnull().sum().sum()
                st.write(f'Missing data count in {season} is: {missing_data_count_rf}')

                total_data_points_rf = seas_rf.iloc[:, 9:10].size
                percentage_missing_rf = (missing_data_count_rf / total_data_points_rf) * 100
                st.write(f'Percentage of missing value in {season} is: {round(percentage_missing_rf, 2)}%')

                per_miss_ideal_rf = 3
                if percentage_missing_rf > per_miss_ideal_rf:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
            
                    
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')
        if st.button('Tabular Report', key="52"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = seas_rf.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = seas_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["Sname", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {season} of the year {year}.')
                st.write(rf_miss_st)
                st.download_button('Download data as CSV', 
                                rf_miss_st.to_csv(),  
                                file_name='missing_data_by_station.csv', 
                                mime='text/csv', key="53")
                
                            
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Rainfall', key="54"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = seas_rf.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = seas_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["Sname", "Missing_Data_Count"]]
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1] 
                st.info('Please take note that these stations do not have not missing rainfall data in {season} of the year {year}.')
                st.write(miss_rf3)    
                st.download_button('Download data as CSV', 
                                miss_rf3.to_csv(),  
                                file_name='stationless3_daymissing data.csv', 
                                mime='text/csv', key="55")        
            
        st.markdown("---")    
        st.subheader('Stations without Missing Data')
        if st.button('Generate Map: Rainfall', key="56"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = seas_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = seas_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["Sname", "Lat", "Lon", "Missing_Data_Count"]]      
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing rainfall data in {season} of the year {year}.')
                fig2_rf_f2 = px.scatter_mapbox(miss_rf3, lat="Lat", lon="Lon", 
                                            hover_name="Sname", 
                                            hover_data=["Sname", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_rf_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_rf_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_rf_f2, use_container_width=True)
    
    ## Daily Maximum Temperature Data 
    elif variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Total Missing Data Count")
        if st.button('Count Missing Data for Maximum Temperature', key="57"):
            if seas_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_max = seas_max.iloc[:, 9:10].isnull().sum().sum()
                st.write(f'Missing data count in {season} is: {missing_data_count_max}')
                total_data_points_max = seas_max.iloc[:, 9:10].size
                percentage_missing_max = (missing_data_count_max / total_data_points_max) * 100
                st.write(f'Percentage of missing value in {season} is: {round(percentage_missing_max, 2)}%')
                per_miss_ideal_max = 5
                if percentage_missing_max > per_miss_ideal_max:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
        
    
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')               
        if st.button('Tabular Report', key="58"):
            if seas_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = seas_max.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = seas_max.iloc[:, 0:9]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["Sname", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {season} of the year {year}.')
                st.write(max_miss_st)
                st.download_button('Download data as CSV', 
                                max_miss_st.to_csv(),  
                                file_name='missing_data_by_station.csv', 
                                mime='text/csv', key="59")  
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Maximum Temperature', key="60"):
            if seas_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = seas_max.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = seas_max.iloc[:, 0:9]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["Sname", "Missing_Data_Count"]]
                miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 1] 
                st.info(f'Please take note that these stations do not have missing maximum temperature data in {season} of the year {year}.')
                st.write(miss_max5)    
                st.download_button('Download data as CSV', 
                                miss_max5.to_csv(),  
                                file_name='stationless5_daymissing data.csv', 
                                mime='text/csv', key="61")
                
        st.markdown("---")
        st.subheader('Stations without Missing Data')                        
        if st.button('Generate Map: Maximum Temperature', key="62"):
            if seas_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = seas_max.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = seas_max.iloc[:, 0:9]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["Sname", "Lat", "Lon", "Missing_Data_Count"]]    
                miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 1] 
            # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing maximum temperature data in {season} of the year {year}.')
                fig2_max_f2 = px.scatter_mapbox(miss_max5, lat="Lat", lon="Lon", 
                                            hover_name="Sname", 
                                            hover_data=["Sname", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_max_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_max_f2.update_layout(legend=dict(itemsizing='constant'))
                st.plotly_chart(fig2_max_f2, use_container_width=True)
        
                                
    ## Daily Minimum Temperature Data      
    elif variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Total Missing Data Count")
        if st.button('Count Missing Data for Minimum Temperature', key="63"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_min = seas_min.iloc[:, 9:10].isnull().sum().sum()
                st.write(f'Missing data count in {season} is: {missing_data_count_min}')
                total_data_points_min = seas_min.iloc[:, 9:10].size
                percentage_missing_min = (missing_data_count_min / total_data_points_min) * 100
                st.write(f'Percentage of missing value in {season} is: {round(percentage_missing_min, 2)}%')
                per_miss_ideal_min = 5
                if percentage_missing_min > per_miss_ideal_min:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
                    
                
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')                              
        if st.button('Tabular Report', key="64"):   
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = seas_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = seas_min.iloc[:, 0:9]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["Sname", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {season} of the year {year}.')
                st.write(min_miss_st)
                st.download_button('Download data as CSV', 
                                min_miss_st.to_csv(),  
                                file_name='missing_data_by_station.csv', 
                                mime='text/csv', key="65")    
            
            
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="66"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = seas_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = seas_min.iloc[:, 0:9]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["Sname", "Missing_Data_Count"]]
                miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 5] 
                st.info(f'Please take note that these stations do not have missing minimum temperature data in {season} of the year {year}.')
                st.write(miss_min5)    
                st.download_button('Download data as CSV', 
                                miss_min5.to_csv(),  
                                file_name='stationless5_daymissing data.csv', 
                                mime='text/csv', key="67")
                                
        st.markdown("---")
        st.subheader('Stations without Missing Data')
        if st.button('Generate Map: Minimum Temperature', key="68"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = seas_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = seas_min.iloc[:, 0:9]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["Sname", "Lat", "Lon", "Missing_Data_Count"]]       
                miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 5] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing minimum temperature data in {season} of the year {year}.')
                fig2_min_f2 = px.scatter_mapbox(miss_min5, lat="Lat", lon="Lon", 
                                            hover_name="Sname", 
                                            hover_data=["Sname", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_min_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_min_f2.update_layout(legend=dict(itemsizing='constant'))
                st.plotly_chart(fig2_min_f2, use_container_width=True)
            
        
        
        
        
            
if __name__ == "__main__":
    seasonal_data_miss()