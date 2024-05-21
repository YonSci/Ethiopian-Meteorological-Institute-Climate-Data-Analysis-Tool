import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
an_max = st.session_state.get('an_max', None)

def annual_data_miss_tmax(variable_type, an_max):
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire year")
        if st.button('Count Missing Data: Maximum Temperature', key="yr_miss1"):
            if an_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmax = an_max.iloc[:, 8:9].isnull().sum().sum()
                st.info(f'Missing maximum temperature data count in {year} is **_{missing_data_count_tmax}_**')
                total_data_points_tmax = an_max.iloc[:, 8:9].size
                percentage_missing_tmax = (missing_data_count_tmax / total_data_points_tmax) * 100
                st.info(f'The percentage of missing maximum temperature data in {year} is **_{round(percentage_missing_tmax, 2)}%_**')
                          
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Maximum Temperature', key="yr_miss2"):
            if an_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = an_max.iloc[:, 8:9].isnull().sum(axis=1)        
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = an_max.iloc[:, 0:9]                
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)                         
                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Missing_Data_Count"]]
      
                st.info(f'Missing maximum temperature data counts for {year}')
                st.write(tmax_miss_st)
                st.download_button('Download data as CSV', 
                                tmax_miss_st.to_csv(index=False),  
                                file_name=(f'tmax_missing_data_by_station_{year}.csv'), 
                                mime='text/csv', key="yr_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Maximum Temperature', key="yr_miss4"):
            if an_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = an_max.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = an_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
  
                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Missing_Data_Count"]]
                miss_tmax1 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 1].copy()  
                
                miss_tmax1['No'] = range(1, len(miss_tmax1) + 1)
                
                st.info(f'Stations without any missing data in {year}')
                st.write(miss_tmax1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmax1.to_csv(index=False),  
                                file_name=(f'tmax_stationsless1_missing_{year}.csv'), 
                                mime='text/csv', key="yr_miss5")        
            
        if st.button('Generate Map: Maximum Temperature', key="yr_miss6"):
            if an_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = an_max.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = an_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Mean Maximum Temperature","Missing_Data_Count"]]
                miss_tmax3 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {year}')
                fig2_tmax_f2 = px.scatter_mapbox(miss_tmax3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Year", "Missing_Data_Count", "Mean Maximum Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmax_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmax_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmax_f2, use_container_width=True)
          
if __name__ == "__main__":
    annual_data_miss_tmax()