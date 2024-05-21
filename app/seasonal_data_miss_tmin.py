import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
seas_min = st.session_state.get('seas_min', None)

def seasonal_data_miss_tmin(variable_type, seas_min):
    season = st.session_state.get('season', 'Unknown Season')
    year = st.session_state.get('year', 'Unknown Year')
    
    if variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire season")
        if st.button('Count Missing Data: Minimum Temperature', key="seas_miss1"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmin = seas_min.iloc[:, 9:10].isnull().sum().sum()
                st.info(f'Missing minimum temperature data count in {season} {year} is **_{missing_data_count_tmin}_**')
                total_data_points_tmin = seas_min.iloc[:, 9:10].size
                percentage_missing_tmin = (missing_data_count_tmin / total_data_points_tmin) * 100
                st.info(f'The percentage of missing minimum temperature data in {season} {year} is **_{round(percentage_missing_tmin, 2)}%_**')
                          
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Minimum Temperature', key="seas_miss2"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = seas_min.iloc[:, 9:10].isnull().sum(axis=1)        
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = seas_min.iloc[:, 0:9]                
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)                         
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Missing_Data_Count"]]
      
                st.info(f'Missing minimum temperature data counts for {season} {year}')
                st.write(tmin_miss_st)
                st.download_button('Download data as CSV', 
                                tmin_miss_st.to_csv(index=False),  
                                file_name=(f'tmin_missing_data_by_station_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="seas_miss4"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = seas_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = seas_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Missing_Data_Count"]]
                
                miss_tmin1 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1].copy()  
                miss_tmin1['No'] = range(1, len(miss_tmin1) + 1)
                
                
                st.info(f'Stations without any missing data in {season} {year}')
                st.write(miss_tmin1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmin1.to_csv(index=False),  
                                file_name=(f'tmin_stationsless1_missing_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss5")        
            
        if st.button('Generate Map: Minimum Temperature', key="seas_miss6"):
            if seas_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = seas_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = seas_min.iloc[:, 0:10]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Season", "Mean Minimum Temperature", "Missing_Data_Count"]]
                miss_tmin3 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {season} {year}')
                fig2_tmin_f2 = px.scatter_mapbox(miss_tmin3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Season", "Year", "Missing_Data_Count", "Mean Minimum Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmin_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmin_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmin_f2, use_container_width=True)
          
if __name__ == "__main__":
    seasonal_data_miss_tmin()