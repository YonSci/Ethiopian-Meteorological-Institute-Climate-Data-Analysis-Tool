import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
seas_rf = st.session_state.get('seas_rf', None)

def seasonal_data_miss_rf(variable_type, seas_rf):
    season = st.session_state.get('season', 'Unknown Season')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Rainfall':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire season")
        if st.button('Count Missing Data: Rainfall', key="seas_miss1"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_rf = seas_rf.iloc[:, 9:10].isnull().sum().sum()
                st.info(f'Missing rainfall data count in {season} {year} is **_{missing_data_count_rf}_**')
                total_data_points_rf = seas_rf.iloc[:, 9:10].size
                percentage_missing_rf = (missing_data_count_rf / total_data_points_rf) * 100
                st.info(f'The percentage of missing rainfall data in {season} {year} is **_{round(percentage_missing_rf, 2)}%_**')
                          
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Rainfall', key="seas_miss2"):
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
                rf_miss_st = rf_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Missing_Data_Count"]]
      
                st.info(f'Missing rainfall data counts for {season} {year}')
                st.write(rf_miss_st)
                st.download_button('Download data as CSV', 
                                rf_miss_st.to_csv(index=False),  
                                file_name=(f'rf_missing_data_by_station_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Rainfall', key="seas_miss4"):
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
                rf_miss_st = rf_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Missing_Data_Count"]]
                
                miss_rf1 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1].copy()  
                miss_rf1['No'] = range(1, len(miss_rf1) + 1)
                
                st.info(f'Stations without any missing data in {season} {year}')
                st.write(miss_rf1)    
        
                st.download_button('Download data as CSV', 
                                miss_rf1.to_csv(index=False),  
                                file_name=(f'rf_stationsless1_missing_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss5")        
            
        if st.button('Generate Map: Rainfall', key="seas_miss6"):
            if seas_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_rf = seas_rf.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_rf_df = pd.DataFrame(missingdata_row_rf)
                names_rf = missingdata_rf_df.columns.tolist()
                names_rf[names_rf.index(0)] = 'Missing_Data_Count'
                missingdata_rf_df.columns = names_rf
                sub_rf = seas_rf.iloc[:, 0:10]
                sub_rf_df = pd.DataFrame(sub_rf)
                rf_join = sub_rf_df.join(missingdata_rf_df)
                rf_miss_st = rf_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Total Rainfall","Missing_Data_Count"]]
                miss_rf3 = rf_miss_st[rf_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {season} {year}')
                fig2_rf_f2 = px.scatter_mapbox(miss_rf3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Season", "Year", "Missing_Data_Count", "Total Rainfall"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_rf_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_rf_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_rf_f2, use_container_width=True)
          
if __name__ == "__main__":
    seasonal_data_miss_rf()