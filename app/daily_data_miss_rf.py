import streamlit as st
import pandas as pd
import plotly.express as px


# Access the shared DataFrame from session state
daily_rf = st.session_state.get('daily_rf', None)

def daily_data_miss_rf(variable_type, daily_rf):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Rainfall':  
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire month")
        if st.button('Count Missing Data: Rainfall', key="daily_miss1"):
            if daily_rf is not None:
                missing_data_count_rf = daily_rf.iloc[:, 9:40].isnull().sum().sum()
                st.info(f'Missing rainfall data count in {month} {year} is **_{missing_data_count_rf}_**')
                total_data_points_rf = daily_rf.iloc[:, 9:40].size
                percentage_missing_rf = (missing_data_count_rf / total_data_points_rf) * 100
                st.info(f'The percentage of missing rainfall data in {month} {year} is **_{round(percentage_missing_rf, 2)}%_**')
            else:
                st.write("Please Load Data in Data Importing Page 😔")
                
        st.markdown("---")
        st.subheader('Missing data for each day across all stations')        
        if st.button('Tabular Report: Rainfall', key="daily_miss2"):
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_rf = daily_rf.iloc[:, 9:40].isnull().sum()
                missing_data_col_rf = pd.DataFrame(missing_data_col_rf)
                names_rf = missing_data_col_rf.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missing_data_col_rf.columns = names_rf
                missing_data_col_rf['Date'] = range(1, len(missing_data_col_rf) + 1)
                missing_data_col_rf = missing_data_col_rf[["Date", "Missing_Data_Count"]]
                # st.info(f'Total number of missing {variable_type} data in {month} of the year {year} at each day.')
                st.info(f'Sum of missing rainfall data counts for each day in {month} {year}')

                st.write(missing_data_col_rf)
                st.download_button('Download data as CSV', 
                                missing_data_col_rf.to_csv(index=False),  
                                file_name=(f'rf_missing_data_by_date_{month}_{year}.csv'), 
                                mime='text/csv', key="daily_miss3")
                 
  
        graphical_report_button = st.button("Graphical Report: Rainfall")
        if graphical_report_button:
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_col_rf = daily_rf.iloc[:, 9:40].isnull().sum()
                missing_data_col_rf = pd.DataFrame(missing_data_col_rf)
                names_rf = missing_data_col_rf.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missing_data_col_rf.columns = names_rf
                missing_data_col_rf['Date'] = range(1, len(missing_data_col_rf) + 1)
                missing_data_col_rf = missing_data_col_rf[["Date", "Missing_Data_Count"]]
            
                # Plotly code
        
                st.info(f'Sum of missing rainfall data counts for each day in {month} {year}')
                fig = px.bar(missing_data_col_rf, x='Date', y='Missing_Data_Count', labels={'Missing_Data_Count': 'Missing Data Counts'},
                            title="Missing Data Counts", width=700, height=500)
                st.plotly_chart(fig)
                
                
        st.markdown("---")
        st.subheader('Sum of missing data counts by station')
        if st.button('Tabular Report: Rainfall', key="daily_miss4"):
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = daily_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_join['No'] = range(1, len(rf_join) + 1)  
                rf_miss_st = rf_join[["No","Gh id", "Sname", "Lat", "Lon", "Elev", "ELID", "Year", "Month", "Missing_Data_Count"]]
                rf_miss_st = rf_miss_st.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
                st.info(f'Sum of missing rainfall data counts for {month} {year}')
                st.write(rf_miss_st)
                st.download_button('Download data as CSV', 
                                rf_miss_st.to_csv(index=False),  
                                file_name=(f'rf_missing_data_by_station_{month}_{year}.csv'), 
                                mime='text/csv', key="daily_miss5")
                
                
        st.markdown("---")
        st.subheader('Stations Above/Below the Specified Threshold Criteria')          
        if st.button('Generate Map: Rainfall ', key="daily_miss6"):
            st.info(f'Stations with missing rainfall data that exceed/below the three-day threshold criteria')
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = daily_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                rf_miss_st = rf_miss_st_re.copy()
                rf_miss_st['Legend'] = ['< 3 days missing' if count < 3 else '>= 3 days missing' for count in rf_miss_st['Missing_Data_Count']]
                color_mapping = {'< 3 days missing': 'green', '>= 3 days missing': 'red'}
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig_rf_f1 = px.scatter_mapbox(rf_miss_st, 
                                            lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color="Legend",
                                            color_discrete_map=color_mapping, 
                                            height=600,
                                            width=800
                                            )
                # Customize the layout with the center coordinates
                fig_rf_f1.update_layout(mapbox_style="open-street-map",
                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig_rf_f1.update_layout(legend=dict(itemsizing='constant'))
                # Show the map
                st.plotly_chart(fig_rf_f1)

        
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Rainfall', key="daily_miss7"):
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = daily_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                rf_miss_st = rf_miss_st_re.copy()
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 3].copy()
                miss_rf3['No'] = range(1, len(miss_rf3) + 1) 
                miss_rf3.drop(columns=['No.'], inplace=True) 
                miss_rf3 = miss_rf3[["No", "Gh id",	"Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month",	"Missing_Data_Count"]]
                
                st.info(f'Stations without any missing values for more than three consecutive days in {month} {year}')
                st.write(miss_rf3)    
                st.download_button('Download data as CSV', 
                                miss_rf3.to_csv(index=False),  
                                file_name=(f'rf_stationsless3_missing_{month}_{year}.csv'), 
                                mime='text/csv', key="daily_miss8") 
                                  

        if st.button('Generate Map: Rainfall', key="daily_miss9"):
            st.info(f'Stations without any missing data for more than three consecutive days in {month} {year}')
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:                    
                missingdata_row_rf = daily_rf.iloc[:, 9:40].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = daily_rf.iloc[:, 0:9]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st_re = rf_join.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})                
                rf_miss_st = rf_miss_st_re.copy()
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 3].copy()
                miss_rf3['No'] = range(1, len(miss_rf3) + 1) 
                miss_rf3.drop(columns=['No.'], inplace=True) 
                miss_rf3 = miss_rf3[["No", "Gh id","Longitude", "Latitude", "Elevation", "Station Name", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                fig2_rf_f2 = px.scatter_mapbox(miss_rf3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Month", "Year", "Missing_Data_Count"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_rf_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_rf_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_rf_f2, use_container_width=True)           
if __name__ == "__main__":
    daily_data_miss_rf()