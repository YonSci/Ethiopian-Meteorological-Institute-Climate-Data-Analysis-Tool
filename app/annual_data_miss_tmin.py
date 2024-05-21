import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
an_min = st.session_state.get('an_min', None)

def annual_data_miss_tmin(variable_type, an_min):
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire year")
        if st.button('Count Missing Data: Minimum Temperature', key="yr_miss1"):
            if an_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmin = an_min.iloc[:, 8:9].isnull().sum().sum()
                st.info(f'Missing minimum temperature data count in {year} is **_{missing_data_count_tmin}_**')
                total_data_points_tmin = an_min.iloc[:, 8:9].size
                percentage_missing_tmin = (missing_data_count_tmin / total_data_points_tmin) * 100
                st.info(f'The percentage of missing minimum temperature data in {year} is **_{round(percentage_missing_tmin, 2)}%_**')
                          
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Minimum Temperature', key="yr_miss2"):
            if an_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = an_min.iloc[:, 8:9].isnull().sum(axis=1)        
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = an_min.iloc[:, 0:9]                
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)                         
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Missing_Data_Count"]]
      
                st.info(f'Missing minimum temperature data counts for {year}')
                st.write(tmin_miss_st)
                st.download_button('Download data as CSV', 
                                tmin_miss_st.to_csv(index=False),  
                                file_name=(f'tmin_missing_data_by_station_{year}.csv'), 
                                mime='text/csv', key="yr_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="yr_miss4"):
            if an_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = an_min.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = an_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
  
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Missing_Data_Count"]]
                miss_tmin1 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1].copy()  
                
                miss_tmin1['No'] = range(1, len(miss_tmin1) + 1)
                
                st.info(f'Stations without any missing data in {year}')
                st.write(miss_tmin1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmin1.to_csv(index=False),  
                                file_name=(f'tmin_stationsless1_missing_{year}.csv'), 
                                mime='text/csv', key="yr_miss5")        
            
        if st.button('Generate Map: Minimum Temperature', key="yr_miss6"):
            if an_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = an_min.iloc[:, 8:9].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = an_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Mean Minimum Temperature","Missing_Data_Count"]]
                miss_tmin3 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1] 
                # Specify the center coordinates (e.g., latitude=your_lat, longitude=your_lon)
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {year}')
                fig2_tmin_f2 = px.scatter_mapbox(miss_tmin3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Year", "Missing_Data_Count", "Mean Minimum Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmin_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmin_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmin_f2, use_container_width=True)
          
if __name__ == "__main__":
    annual_data_miss_tmin()