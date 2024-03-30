import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
seas_mean = st.session_state.get('seas_mean', None)

def seasonal_data_miss_tmean(variable_type, seas_mean):
    season = st.session_state.get('season', 'Unknown Season')
    year = st.session_state.get('year', 'Unknown Year')
    
    if variable_type == 'Mean Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire season")
        if st.button('Count Missing Data: Mean Temperature', key="seas_miss1"):
            if seas_mean is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmean = seas_mean.iloc[:, 8:9].isnull().sum().sum()
                st.info(f'Missing mean temperature data count in {season} {year} is **_{missing_data_count_tmean}_**')
                total_data_points_tmean = seas_mean.iloc[:, 8:9].size
    
                percentage_missing_tmean = (missing_data_count_tmean / total_data_points_tmean) * 100
                st.info(f'The percentage of missing mean temperature data in {season} {year} is **_{round(percentage_missing_tmean, 2)}%_**')
                          
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Mean Temperature', key="seas_miss2"):
            if seas_mean is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmean = seas_mean.iloc[:, 8:9].isnull().sum(axis=1)        
                missingdata_tmean_df = pd.DataFrame(missingdata_row_tmean)
                names_tmean = missingdata_tmean_df.columns.tolist()
                names_tmean[names_tmean.index(0)] = 'Missing_Data_Count'
                missingdata_tmean_df.columns = names_tmean
                sub_tmean = seas_mean.iloc[:, 0:8]                
                sub_tmean_df = pd.DataFrame(sub_tmean)
                tmean_join = sub_tmean_df.join(missingdata_tmean_df)                         
                tmean_miss_st = tmean_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "Year", "Season", "Missing_Data_Count"]]
      
                st.info(f'Missing mean temperature data counts for {season} {year}')
                st.write(tmean_miss_st)
                st.download_button('Download data as CSV', 
                                tmean_miss_st.to_csv(index=False),  
                                file_name=(f'tmean_missing_data_by_station_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Mean Temperature', key="seas_miss4"):
            if seas_mean is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmean = seas_mean.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmean_df = pd.DataFrame(missingdata_row_tmean)
                names_tmean = missingdata_tmean_df.columns.tolist()
                names_tmean[names_tmean.index(0)] = 'Missing_Data_Count'
                missingdata_tmean_df.columns = names_tmean
                sub_tmean = seas_mean.iloc[:, 0:8]
                sub_tmean_df = pd.DataFrame(sub_tmean)
                tmean_join = sub_tmean_df.join(missingdata_tmean_df)
                tmean_miss_st = tmean_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "Year", "Season", "Missing_Data_Count"]]
                            
                miss_tmean1 = tmean_miss_st[tmean_miss_st['Missing_Data_Count'] < 1].copy()  
                miss_tmean1['No'] = range(1, len(miss_tmean1) + 1)
                
                st.info(f'Stations without any missing data in {season} {year}')
                st.write(miss_tmean1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmean1.to_csv(index=False),  
                                file_name=(f'tmean_stationsless1_missing_{season}_{year}.csv'), 
                                mime='text/csv', key="seas_miss5")        
            
        if st.button('Generate Map: Mean Temperature', key="seas_miss6"):
            if seas_mean is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmean = seas_mean.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmean_df = pd.DataFrame(missingdata_row_tmean)
                names_tmean = missingdata_tmean_df.columns.tolist()
                names_tmean[names_tmean.index(0)] = 'Missing_Data_Count'
                missingdata_tmean_df.columns = names_tmean
                sub_tmean = seas_mean.iloc[:, 0:9]
                sub_tmean_df = pd.DataFrame(sub_tmean)
                tmean_join = sub_tmean_df.join(missingdata_tmean_df)
                tmean_miss_st = tmean_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "Year", "Season", "Mean Temperature", "Missing_Data_Count"]]
                miss_tmean3 = tmean_miss_st[tmean_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {season} {year}')
                fig2_tmean_f2 = px.scatter_mapbox(miss_tmean3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Season", "Year", "Missing_Data_Count", "Mean Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmean_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmean_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmean_f2, use_container_width=True)
          
if __name__ == "__main__":
    seasonal_data_miss_tmean()