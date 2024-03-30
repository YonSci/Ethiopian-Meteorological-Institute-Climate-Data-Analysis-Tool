import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared month value from session state
month = st.session_state.get('month', 'Unknown Month')
year = st.session_state.get('year', 'Unknown Year')   
variable_type = st.session_state.get('variable_type', 'None')
timestep_analysis = st.session_state.get('timestep_analysis', 'None')

# Access the shared DataFrame from session state
mon_rf = st.session_state.get('mon_rf', 'None')
mon_max = st.session_state.get('mon_max', 'None')
mon_min = st.session_state.get('mon_min', 'None')

def monthly_data_miss(variable_type):
    if variable_type == 'Rainfall':  
        st.markdown("---")
        st.subheader("Total Missing Data Count")
        if st.button('Count Missing Data for Rainfall', key="33"):
            if mon_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_rf = mon_rf.iloc[:, 6:7].isnull().sum().sum()
                st.write(f'Missing data count in {month} is: {missing_data_count_rf}')

                total_data_points_rf = mon_rf.iloc[:, 6:7].size
                percentage_missing_rf = (missing_data_count_rf / total_data_points_rf) * 100
                st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_rf, 2)}%')

                per_miss_ideal_rf = 3
                if percentage_missing_rf > per_miss_ideal_rf:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
            
                    
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')
        if st.button('Tabular Report', key="34"):
            if mon_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = mon_rf.iloc[:, 6:7].isnull().sum(axis=1)                    
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = mon_rf.iloc[:, 0:6]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
                st.write(rf_miss_st)
                st.download_button('Download data as CSV', 
                                rf_miss_st.to_csv(index=False),  
                                file_name=(f'rf_missing_data_station_{month}.csv'), 
                                mime='text/csv', key="35")
                
                            
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Rainfall', key="36"):
            if mon_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = mon_rf.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = mon_rf.iloc[:, 0:6]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                miss_rf1 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1] 
                st.info(f'Please take note that these stations do not have not missing rainfall data in {month} of the year {year}.')
                st.write(miss_rf1)    

                
        
                st.download_button('Download data as CSV', 
                                miss_rf1.to_csv(index=False),  
                                file_name=(f'rf_stationless1_missing_{month}.csv'), 
                                mime='text/csv', key="37")        
            
        st.markdown("---")    
        st.subheader('Stations without Missing Data')
        if st.button('Generate Map: Rainfall', key="38"):
            if mon_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = mon_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = mon_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]      
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing rainfall data in {month} of the year {year}.')
                fig2_rf_f2 = px.scatter_mapbox(miss_rf3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Station Name", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_rf_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_rf_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_rf_f2, use_container_width=True)
    
    ## Monthly Maximum Temperature Data 
    elif variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Total Missing Data Count")
        if st.button('Count Missing Data for Maximum Temperature', key="39"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_max = mon_max.iloc[:, 6:7].isnull().sum().sum()
                st.write(f'Missing data count in {month} is: {missing_data_count_max}')
                total_data_points_max = mon_max.iloc[:, 6:7].size
                percentage_missing_max = (missing_data_count_max / total_data_points_max) * 100
                st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_max, 2)}%')
                per_miss_ideal_max = 5
                if percentage_missing_max > per_miss_ideal_max:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
        
    
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')               
        if st.button('Tabular Report', key="40"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = mon_max.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = mon_max.iloc[:, 0:6]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
                st.write(max_miss_st)
                st.download_button('Download data as CSV', 
                                max_miss_st.to_csv(index=False),  
                                file_name=(f'maxtemp_missing_data_station_{month}.csv'), 
                                mime='text/csv', key="41")  
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Maximum Temperature', key="42"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = mon_max.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = mon_max.iloc[:, 0:6]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 1] 
                st.info(f'Please take note that these stations do not have missing maximum temperature data in {month} of the year {year}.')
                st.write(miss_max5)    
                st.download_button('Download data as CSV', 
                                miss_max5.to_csv(index=False),  
                                file_name=(f'maxtemp_stationless1_missing_{month}.csv'), 
                                mime='text/csv', key="43")
                
        st.markdown("---")
        st.subheader('Stations without Missing Data')                        
        if st.button('Generate Map: Maximum Temperature', key="44"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_max = mon_max.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_max_df = pd.DataFrame(missingdata_row_max)
                names_max = missingdata_max_df.columns.tolist()
                names_max[names_max.index(0)] = 'Missing_Data_Count'
                missingdata_max_df.columns = names_max
                sub_max = mon_max.iloc[:, 0:6]
                sub_max_df = pd.DataFrame(sub_max)
                max_join = sub_max_df.join(missingdata_max_df)
                max_miss_st = max_join[["Station Name", "Latitude", "Longitude", "Missing_Data_Count"]]    
                miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 1] 
            # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing maximum temperature data in {month} of the year {year}.')
                fig2_max_f2 = px.scatter_mapbox(miss_max5, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Station Name", "Latitude", "Longitude", "Missing_Data_Count"],
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
        if st.button('Count Missing Data for Minimum Temperature', key="45"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_min = mon_min.iloc[:, 6:7].isnull().sum().sum()
                st.write(f'Missing data count in {month} is: {missing_data_count_min}')
                total_data_points_min = mon_min.iloc[:, 6:7].size
                percentage_missing_min = (missing_data_count_min / total_data_points_min) * 100
                st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_min, 2)}%')
                per_miss_ideal_min = 5
                if percentage_missing_min > per_miss_ideal_min:
                    st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
                else:
                    st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
                    
                
        st.markdown("---")
        st.subheader('Total Number of Missing Data by Station')                              
        if st.button('Tabular Report', key="46"):   
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = mon_min.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = mon_min.iloc[:, 0:6]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
                st.write(min_miss_st)
                st.download_button('Download data as CSV', 
                                min_miss_st.to_csv(index=False),  
                                file_name=(f'mintemp_missing_data_station_{month}.csv'), 
                                mime='text/csv', key="47")    
            
            
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="48"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = mon_min.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = mon_min.iloc[:, 0:6]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["No", "Gh id","Station Name", "Latitude", "Longitude", "Month", "Missing_Data_Count"]]
                miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 1] 
                st.info(f'Please take note that these stations do not have missing minimum temperature data in {month} of the year {year}.')
                st.write(miss_min5)    
                st.download_button('Download data as CSV', 
                                miss_min5.to_csv(index=False),  
                                file_name=(f'mintemp_stationless1_missing_{month}.csv'), 
                                mime='text/csv', key="49")
                                
        st.markdown("---")
        st.subheader('Stations without Missing Data')
        if st.button('Generate Map: Minimum Temperature', key="50"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_min = mon_min.iloc[:, 6:7].isnull().sum(axis=1)
                missingdata_min_df = pd.DataFrame(missingdata_row_min)
                names_min = missingdata_min_df.columns.tolist()
                names_min[names_min.index(0)] = 'Missing_Data_Count'
                missingdata_min_df.columns = names_min
                sub_min = mon_min.iloc[:, 0:6]
                sub_min_df = pd.DataFrame(sub_min)
                min_join = sub_min_df.join(missingdata_min_df)
                min_miss_st = min_join[["Station Name", "Latitude", "Longitude", "Missing_Data_Count"]]       
                miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Map showing stations without any missing minimum temperature data in {month} of the year {year}.')
                fig2_min_f2 = px.scatter_mapbox(miss_min5, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Station Name", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_min_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_min_f2.update_layout(legend=dict(itemsizing='constant'))
                st.plotly_chart(fig2_min_f2, use_container_width=True) 
            
        
        
        
        
            
if __name__ == "__main__":
    monthly_data_miss()