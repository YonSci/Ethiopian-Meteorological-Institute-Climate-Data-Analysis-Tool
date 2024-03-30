# import streamlit as st
# import pandas as pd
# import plotly.express as px
# # from Data_Importing_Module import daily_rf


# # Access the shared month value from session state
# month = st.session_state.get('month', 'Unknown Month')
# year = st.session_state.get('year', 'Unknown Year')   
# variable_type = st.session_state.get('variable_type', None)
# timestep_analysis = st.session_state.get('timestep_analysis', None)

# # Access the shared DataFrame from session state
# daily_rf = st.session_state.get('daily_rf', None)
# daily_max = st.session_state.get('daily_max', None)
# daily_min = st.session_state.get('daily_min', None)
    
# def daily_data_miss(variable_type):
#     if variable_type == 'Rainfall':  
#         #daily_rf = daily_rf.copy()
#         st.markdown("---")
#         st.subheader("Total Missing Data Count")
#         if st.button('Count Missing Data for Rainfall', key="1"):   
#             if daily_rf is not None:
#                 missing_data_count_rf = daily_rf.iloc[:, 9:40].isnull().sum().sum()
#                 st.write(f'Missing data count in {month} is: {missing_data_count_rf}')
#                 total_data_points_rf = daily_rf.iloc[:, 9:40].size
#                 percentage_missing_rf = (missing_data_count_rf / total_data_points_rf) * 100
#                 st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_rf, 2)}%')

#                 per_miss_ideal_rf = 3
#                 if percentage_missing_rf > per_miss_ideal_rf:
#                     st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
#                 else:
#                     st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
#             else:
#                 st.write("Please Load Data in Data Importing Page 😔")
                
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day')        
#         if st.button('Tabular Report: Rainfall', key="2"):
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_rf = daily_rf.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_rf = pd.DataFrame(missing_data_col_rf)
#                 names_rf = missing_data_col_rf.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_rf.columns = names_rf
#                 missing_data_col_rf['Date'] = range(1, len(missing_data_col_rf) + 1)
#                 missing_data_col_rf = missing_data_col_rf[["Date", "Missing_Data_Count"]]
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
#                 st.write(missing_data_col_rf)
#                 st.download_button('Download data as CSV', 
#                                 missing_data_col_rf.to_csv(index=False),  
#                                 file_name=(f'rf_missing_data_by_date_{month}_{year}.csv'), 
#                                 mime='text/csv', key="3")
                
                
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day')    
#         graphical_report_button = st.button("Graphical Report: Rainfall")
#         if graphical_report_button:
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_rf = daily_rf.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_rf = pd.DataFrame(missing_data_col_rf)
#                 names_rf = missing_data_col_rf.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_rf.columns = names_rf
#                 missing_data_col_rf['Date'] = range(1, len(missing_data_col_rf) + 1)
#                 missing_data_col_rf = missing_data_col_rf[["Date", "Missing_Data_Count"]]
            
#                 # Plotly code
#                 st.info(f'Count of missing {variable_type} data in {month} of the year {year}.')
#                 fig = px.bar(missing_data_col_rf, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
#                             title="Missing Data Counts", width=700, height=500)
#                 st.plotly_chart(fig)
                
                
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data by Station')
#         if st.button('Tabular Report: Rainfall', key="4"):
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
#                 names_rf = missingdata_rf_df.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missingdata_rf_df.columns = names_rf
#                 sub_rf = daily_rf.iloc[:, 0:9]
#                 sub_rf_df = pd.DataFrame(sub_rf)
#                 rf_join = sub_rf_df.join(missingdata_rf_df)
#                 rf_join['No'] = range(1, len(rf_join) + 1)  
#                 rf_miss_st = rf_join[["No","Gh id", "Sname", "Lat", "Lon", "Elev", "ELID", "Year", "Month", "Missing_Data_Count"]]
#                 rf_miss_st = rf_miss_st.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
#                 st.write(rf_miss_st)
#                 st.download_button('Download data as CSV', 
#                                 rf_miss_st.to_csv(index=False),  
#                                 file_name=(f'rf_missing_data_by_station_{month}_{year}.csv'), 
#                                 mime='text/csv', key="5")
                
                
#         st.markdown("---")
#         st.subheader('Stations Above/Below the Specified Threshold Criteria')          
#         if st.button('Generate Map: Rainfall ', key="6"):
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
#                 names_rf = missingdata_rf_df.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missingdata_rf_df.columns = names_rf
#                 sub_rf = daily_rf.iloc[:, 0:9]
#                 sub_rf_df = pd.DataFrame(sub_rf)
#                 rf_join = sub_rf_df.join(missingdata_rf_df)
#                 rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 rf_miss_st = rf_miss_st_re.copy()
#                 rf_miss_st['Legend'] = ['< 3 days missing' if count < 3 else '>= 3 days missing' for count in rf_miss_st['Missing_Data_Count']]
#                 color_mapping = {'< 3 days missing': 'green', '>= 3 days missing': 'red'}
#                 # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig_rf_f1 = px.scatter_mapbox(rf_miss_st, 
#                                             lat="Latitude", lon="Longitude", 
#                                             hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
#                                             color="Legend",
#                                             color_discrete_map=color_mapping, 
#                                             height=600,
#                                             width=800
#                                             )
#                 # Customize the layout with the center coordinates
#                 fig_rf_f1.update_layout(mapbox_style="open-street-map",
#                                     margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                     mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig_rf_f1.update_layout(legend=dict(itemsizing='constant'))
#                 # Show the map
#                 st.plotly_chart(fig_rf_f1)

        
#         st.markdown("---")
#         st.subheader('Stations Without Missing Data')
#         if st.button('Tabular Report: Rainfall', key="7"):
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
#                 names_rf = missingdata_rf_df.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missingdata_rf_df.columns = names_rf
#                 sub_rf = daily_rf.iloc[:, 0:9]
#                 sub_rf_df = pd.DataFrame(sub_rf)
#                 rf_join = sub_rf_df.join(missingdata_rf_df)
#                 rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 rf_miss_st = rf_miss_st_re.copy()
#                 miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 3]
#                 miss_rf3['No'] = range(1, len(miss_rf3) + 1) 
#                 miss_rf3.drop(columns=['No.'], inplace=True) 
#                 miss_rf3 = miss_rf3[["No", "Gh id",	"Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month",	"Missing_Data_Count"]]
                
#                 st.info('Please take note that these stations have missing rainfall data that does not exceed three days.')
#                 st.write(miss_rf3)    
#                 st.download_button('Download data as CSV', 
#                                 miss_rf3.to_csv(index=False),  
#                                 file_name=(f'rf_stationsless3_missing_{month}_{year}.csv'), 
#                                 mime='text/csv', key="8") 
                                  
#         st.markdown("---")  
#         st.subheader('Stations without Missing Data')
#         if st.button('Generate Map: Rainfall', key="9"):
#             if daily_rf is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:                    
#                 missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
#                 names_rf = missingdata_rf_df.columns.tolist()
#                 names_rf[names_rf.index(0)] = 'Missing_Data_Count'
#                 missingdata_rf_df.columns = names_rf
#                 sub_rf = daily_rf.iloc[:, 0:9]
#                 sub_rf_df = pd.DataFrame(sub_rf)
#                 rf_join = sub_rf_df.join(missingdata_rf_df)
#                 rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 rf_miss_st = rf_miss_st_re.copy()
#                 miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 3]
#                 miss_rf3['No'] = range(1, len(miss_rf3) + 1) 
#                 miss_rf3.drop(columns=['No.'], inplace=True) 
#                 miss_rf3 = miss_rf3[["No", "Gh id","Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
#                 # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig2_rf_f2 = px.scatter_mapbox(miss_rf3, lat="Latitude", lon="Longitude", 
#                                             hover_name="Station Name", 
#                                             hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
#                                             color_discrete_sequence=["green"], 
#                                             zoom=5, height=500)
#                 fig2_rf_f2.update_layout(mapbox_style="open-street-map",
#                                 margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                 mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig2_rf_f2.update_layout(legend=dict(itemsizing='constant'))
                
#                 st.plotly_chart(fig2_rf_f2, use_container_width=True)
                
                
#     # Daily Maximum Temperature Data 
#     elif variable_type == 'Maximum Temperature':
#         st.markdown("---")
#         st.subheader("Total Missing Data Count")
#         if st.button('Count Missing Data for Maximum Temperature', key="9"):
#             if daily_max is not None:
#                 missing_data_count_max = daily_max.iloc[:, 9:40].isnull().sum().sum()
#                 st.write(f'Missing data count in {month} is: {missing_data_count_max}')
#                 total_data_points_max = daily_max.iloc[:, 9:40].size
#                 percentage_missing_max = (missing_data_count_max / total_data_points_max) * 100
#                 st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_max, 2)}%')
#                 per_miss_ideal_max = 5
#                 if percentage_missing_max > per_miss_ideal_max:
#                     st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
#                 else:
#                     st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
#             else:
#                 st.write("Please Load Data in Data Importing Page 😔")
        
        
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day')
#         if st.button('Tabular Report: Maximum Temperature', key="10"):
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_max = daily_max.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_max = pd.DataFrame(missing_data_col_max)
#                 names_max = missing_data_col_max.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_max.columns = names_max
#                 missing_data_col_max['Date'] = range(1, len(missing_data_col_max) + 1)
#                 missing_data_col_max = missing_data_col_max[["Date", "Missing_Data_Count"]]
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
#                 st.write(missing_data_col_max)
#                 st.download_button('Download data as CSV', 
#                                 missing_data_col_max.to_csv(index=False),  
#                                 file_name=(f'tmax_missing_data_by_date_{month}_{year}.csv'),
#                                 mime='text/csv', key="11")
                
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day')
#         graphical_report_button = st.button("Graphical Report: Maximum Temperature")
#         if graphical_report_button:
#             missing_data_col_max = st.session_state.get('missing_data_col_max', pd.DataFrame())
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_max = daily_max.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_max = pd.DataFrame(missing_data_col_max)
#                 names_max = missing_data_col_max.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_max.columns = names_max
#                 missing_data_col_max['Date'] = range(1, len(missing_data_col_max) + 1)
#                 missing_data_col_max = missing_data_col_max[["Date", "Missing_Data_Count"]]
        
#                 # Plotly code
#                 st.info(f'Count of missing {variable_type} data in {month} of the year {year}.')
#                 fig = px.bar(missing_data_col_max, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
#                             title="Missing Data Counts", width=700, height=500)
#                 st.plotly_chart(fig)
    
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data by Station')
#         if st.button('Tabular Report: Maximum Temperature', key="12"):
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_max = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_max_df = pd.DataFrame(missingdata_row_max)
#                 names_max = missingdata_max_df.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missingdata_max_df.columns = names_max
#                 sub_max = daily_max.iloc[:, 0:9]
#                 sub_max_df = pd.DataFrame(sub_max)
#                 max_join = sub_max_df.join(missingdata_max_df)
#                 max_join['No'] = range(1, len(max_join) + 1)  
#                 max_miss_st = max_join[["No","Gh id", "Sname", "Lat", "Lon", "Elev", "ELID", "Year", "Month", "Missing_Data_Count"]]
#                 max_miss_st = max_miss_st.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
#                 st.write(max_miss_st)
#                 st.download_button('Download data as CSV', 
#                                 max_miss_st.to_csv(index=False),  
#                                 file_name=(f'tmax_missing_data_by_station_{month}_{year}.csv'), 
#                                 mime='text/csv', key="13")
        
        
#         st.markdown("---")
#         st.subheader('Stations Above/Below the Specified Threshold Criteria')          
#         if st.button('Generate Map: Maximum Temperature', key="14"):
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_max = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_max_df = pd.DataFrame(missingdata_row_max)
#                 names_max = missingdata_max_df.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missingdata_max_df.columns = names_max
#                 sub_max = daily_max.iloc[:, 0:9]
#                 sub_max_df = pd.DataFrame(sub_max)
#                 max_join = sub_max_df.join(missingdata_max_df)
#                 max_miss_st_re = max_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 max_miss_st = max_miss_st_re.copy()
#                 max_miss_st['Legend'] = ['< 5 days missing' if count < 5 else '>= 5 days missing' for count in max_miss_st['Missing_Data_Count']]
#                 color_mapping = {'< 5 days missing': 'green', '>= 5 days missing': 'red'}
#                 # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig_max_f1 = px.scatter_mapbox(max_miss_st, 
#                                             lat="Latitude", lon="Longitude", 
#                                             hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
#                                             color="Legend",
#                                             color_discrete_map=color_mapping, 
#                                             height=600,
#                                             width=800
#                                             )
#                 # Customize the layout with the center coordinates
#                 fig_max_f1.update_layout(mapbox_style="open-street-map",
#                                     margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                     mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig_max_f1.update_layout(legend=dict(itemsizing='constant'))
#                 # Show the map
#                 st.plotly_chart(fig_max_f1)


#         st.markdown("---")
#         st.subheader('Stations Without Missing Data')
#         if st.button('Tabular Report: Maximum Temperature', key="15"):
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_max = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_max_df = pd.DataFrame(missingdata_row_max)
#                 names_max = missingdata_max_df.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missingdata_max_df.columns = names_max
#                 sub_max = daily_max.iloc[:, 0:9]
#                 sub_max_df = pd.DataFrame(sub_max)
#                 max_join = sub_max_df.join(missingdata_max_df)
#                 max_miss_st_re = max_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 max_miss_st = max_miss_st_re.copy()
#                 miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 5]
#                 miss_max5['No'] = range(1, len(miss_max5) + 1) 
#                 miss_max5.drop(columns=['No.'], inplace=True) 
#                 miss_max5 = miss_max5[["No", "Gh id",	"Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month",	"Missing_Data_Count"]]
#                 st.info('Please take note that these stations have missing rainfall data that does not exceed five days.')
#                 st.write(miss_max5)    
#                 st.download_button('Download data as CSV', 
#                                 miss_max5.to_csv(index=False),  
#                                 file_name=(f'max_stationsless5_missing_{month}_{year}.csv'), 
#                                 mime='text/csv', key="16")
                
#         st.markdown("---")  
#         st.subheader('Stations without Missing Data')
#         if st.button('Generate Map: Maximum Temperature', key="17"):
#             if daily_max is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:                    
#                 missingdata_row_max = daily_max.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_max_df = pd.DataFrame(missingdata_row_max)
#                 names_max = missingdata_max_df.columns.tolist()
#                 names_max[names_max.index(0)] = 'Missing_Data_Count'
#                 missingdata_max_df.columns = names_max
#                 sub_max = daily_max.iloc[:, 0:9]
#                 sub_max_df = pd.DataFrame(sub_max)
#                 max_join = sub_max_df.join(missingdata_max_df)
#                 max_miss_st_re = max_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
#                 max_miss_st = max_miss_st_re.copy()
#                 miss_max5 = max_miss_st[max_miss_st['Missing_Data_Count'] < 5]
#                 miss_max5['No'] = range(1, len(miss_max5) + 1) 
#                 miss_max5.drop(columns=['No.'], inplace=True) 
#                 miss_max5 = miss_max5[["No", "Gh id","Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
#                 # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig2_max_f2 = px.scatter_mapbox(miss_max5, lat="Latitude", lon="Longitude", 
#                                             hover_name="Station Name", 
#                                             hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
#                                             color_discrete_sequence=["green"], 
#                                             zoom=5, height=500)
#                 fig2_max_f2.update_layout(mapbox_style="open-street-map",
#                                 margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                 mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig2_max_f2.update_layout(legend=dict(itemsizing='constant'))
                
#                 st.plotly_chart(fig2_max_f2, use_container_width=True)
                
                
#     # Daily Minimum Temperature Data      
#     elif variable_type == 'Minimum Temperature':
#         st.markdown("---")
#         st.subheader("Total Missing Data Count")
#         if st.button('Count Missing Data for Minimum Temperature', key="18"):
#             if daily_min is not None:
#                 missing_data_count_min = daily_min.iloc[:, 9:40].isnull().sum().sum()
#                 st.write(f'Missing data count in {month} is: {missing_data_count_min}')
#                 total_data_points_min = daily_min.iloc[:, 9:40].size
#                 percentage_missing_min = (missing_data_count_min / total_data_points_min) * 100
#                 st.write(f'Percentage of missing value in {month} is: {round(percentage_missing_min, 2)}%')
#                 per_miss_ideal_min = 5
#                 if percentage_missing_min > per_miss_ideal_min:
#                     st.warning('Too many missing data points in the dataset. It is recommended to stop further analysis!')
#                 else:
#                     st.success('The dataset has no or fewer missing data points. It is recommended to continue the analysis!')
#             else:
#                 st.write("Please Load Data in Data Importing Page 😔")
                    
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day')
#         if st.button('Tabular Report: Minimum Temperature', key="19"):
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_min = daily_min.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_min = pd.DataFrame(missing_data_col_min)
#                 names_min = missing_data_col_min.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_min.columns = names_min
#                 missing_data_col_min['Date'] = range(1, len(missing_data_col_min) + 1)
#                 missing_data_col_min = missing_data_col_min[["Date", "Missing_Data_Count"]]
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
#                 st.write(missing_data_col_min)
#                 st.download_button('Download data as CSV', 
#                                 missing_data_col_min.to_csv(),  
#                                 file_name='missing_data_by_date.csv', 
#                                 mime='text/csv', key="20")
                        
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data at Each Day') 
#         graphical_report_button = st.button("Graphical Report")
#         if graphical_report_button:
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missing_data_col_min = daily_min.iloc[:, 9:40].isnull().sum()
#                 missing_data_col_min = pd.DataFrame(missing_data_col_min)
#                 names_min = missing_data_col_min.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missing_data_col_min.columns = names_min
#                 missing_data_col_min['Date'] = range(1, len(missing_data_col_min) + 1)
#                 missing_data_col_min = missing_data_col_min[["Date", "Missing_Data_Count"]]
            
#                 # Plotly code
#                 st.info(f'Count of missing {variable_type} data in {month} of the year {year}.')
#                 fig = px.bar(missing_data_col_min, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
#                             title="Missing Data Counts", width=700, height=500)
#                 st.plotly_chart(fig) 
        
                
#         st.markdown("---")
#         st.subheader('Total Number of Missing Data by Station')                              
#         if st.button('Tabular Report', key="27"):   
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_min = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_min_df = pd.DataFrame(missingdata_row_min)
#                 names_min = missingdata_min_df.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missingdata_min_df.columns = names_min
#                 sub_min = daily_min.iloc[:, 0:9]
#                 sub_min_df = pd.DataFrame(sub_min)
#                 min_join = sub_min_df.join(missingdata_min_df)
#                 min_miss_st = min_join[["Sname", "Missing_Data_Count"]]
#                 st.info(f'Total number of missing {variable_type} data in {month} of the year {year}.')
#                 st.write(min_miss_st)
#                 st.download_button('Download data as CSV', 
#                                 min_miss_st.to_csv(),  
#                                 file_name='missing_data_by_station.csv', 
#                                 mime='text/csv', key="28")    

                
#         st.markdown("---")
#         st.subheader('Stations Above/Below the Specified Threshold Criteria')                   
#         if st.button('Generate Map: Minimum Temperature ', key="29"):
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_min = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_min_df = pd.DataFrame(missingdata_row_min)
#                 names_min = missingdata_min_df.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missingdata_min_df.columns = names_min
#                 sub_min = daily_min.iloc[:, 0:9]
#                 sub_min_df = pd.DataFrame(sub_min)
#                 min_join = sub_min_df.join(missingdata_min_df)
#                 min_miss_st = min_join[["Sname", "Lat", "Lon", "Missing_Data_Count"]].copy()                  
#                 # Add a new column for marker color based on the condition
#                 min_miss_st['Legend'] = ['< 5 days missing' if count < 5 else '>= 5 days missing' for count in min_miss_st['Missing_Data_Count']]
#                 # Define the color mapping
#                 color_mapping = {'< 5 days missing': 'green', '>= 5 days missing': 'red'}
#                 # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig_min_f1 = px.scatter_mapbox(min_miss_st, 
#                                             lat="Lat", lon="Lon", 
#                                             hover_name="Sname", hover_data=["Sname", "Missing_Data_Count"],
#                                             color="Legend",
#                                             color_discrete_map=color_mapping, 
#                                             height=600,
#                                             width=800
#                                             )
#                 # Customize the layout with the center coordinates
#                 fig_min_f1.update_layout(mapbox_style="open-street-map",
#                                     margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                     mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig_min_f1.update_layout(legend=dict(itemsizing='constant'))
#                 # Show the map
#                 st.plotly_chart(fig_min_f1)
            
            
#         st.markdown("---")
#         st.subheader('Stations Without Missing Data')
#         if st.button('Tabular Report: Minimum Temperature', key="30"):
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_min = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_min_df = pd.DataFrame(missingdata_row_min)
#                 names_min = missingdata_min_df.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missingdata_min_df.columns = names_min
#                 sub_min = daily_min.iloc[:, 0:9]
#                 sub_min_df = pd.DataFrame(sub_min)
#                 min_join = sub_min_df.join(missingdata_min_df)
#                 min_miss_st = min_join[["Sname", "Missing_Data_Count"]]
#                 miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 5] 
#                 st.info('Please take note that these stations have missing Minimum Temperature data that does not exceed five days.')
#                 st.write(miss_min5)    
#                 st.download_button('Download data as CSV', 
#                                 miss_min5.to_csv(),  
#                                 file_name='stationless5_daymissing data.csv', 
#                                 mime='text/csv', key="31")
                                
#         st.markdown("---")
#         st.subheader('Stations without Missing Data')
#         if st.button('Generate Map: Minimum Temperature', key="32"):
#             if daily_min is None:
#                 st.warning('Please Load Data in Data Importing Page 😔')
#             else:
#                 missingdata_row_min = daily_min.iloc[:, 9:40].isnull().sum(axis=1)
#                 missingdata_min_df = pd.DataFrame(missingdata_row_min)
#                 names_min = missingdata_min_df.columns.tolist()
#                 names_min[names_min.index(0)] = 'Missing_Data_Count'
#                 missingdata_min_df.columns = names_min
#                 sub_min = daily_min.iloc[:, 0:9]
#                 sub_min_df = pd.DataFrame(sub_min)
#                 min_join = sub_min_df.join(missingdata_min_df)
#                 min_miss_st = min_join[["Sname", "Lat", "Lon", "Missing_Data_Count"]]       
#                 miss_min5 = min_miss_st[min_miss_st['Missing_Data_Count'] < 5] 
#             # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
#                 center_coordinates = (9.5, 40.5)
#                 fig2_min_f2 = px.scatter_mapbox(miss_min5, lat="Lat", lon="Lon", 
#                                             hover_name="Sname", 
#                                             hover_data=["Sname", "Missing_Data_Count"],
#                                             color_discrete_sequence=["green"], 
#                                             zoom=5, height=500)
#                 fig2_min_f2.update_layout(mapbox_style="open-street-map",
#                                 margin={"r": 0, "t": 0, "l": 0, "b": 0},
#                                 mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
#                 # Update the legend to use markers
#                 fig2_min_f2.update_layout(legend=dict(itemsizing='constant'))
#                 st.plotly_chart(fig2_min_f2, use_container_width=True)
                
#         st.markdown("---")
                    
                    
# if __name__ == "__main__":
#     daily_data_miss()