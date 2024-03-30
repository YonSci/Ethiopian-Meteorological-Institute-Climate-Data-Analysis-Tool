import streamlit as st
import pandas as pd
import plotly.express as px 

# Access the shared DataFrame from session state
mon_min = st.session_state.get('mon_min', None)

def monthly_data_miss_tmin(variable_type, mon_min):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    if variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire month")
        if st.button('Count Missing Data: Minimum Temperature', key="mon_miss_tmin1"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmin = mon_min.iloc[:, 9:10].isnull().sum().sum()
                st.info(f'Missing minimum temperature data count in {month} {year} is **_{missing_data_count_tmin}_**')
                total_data_points_tmin = mon_min.iloc[:, 9:10].size
                percentage_missing_tmin = (missing_data_count_tmin / total_data_points_tmin) * 100
                st.info(f'The percentage of missing minimum temperature data in {month} {year} is **_{round(percentage_missing_tmin, 2)}%_**')
                            
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Minimum Temperature', key="mon_miss_tmin2"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = mon_min.iloc[:, 9:10].isnull().sum(axis=1)        
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = mon_min.iloc[:, 0:9]                
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)                         
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Missing_Data_Count"]]
        
                st.info(f'Missing minimum temperature data counts for {month} {year}')
                st.write(tmin_miss_st)
                st.download_button('Download data as CSV', 
                                tmin_miss_st.to_csv(index=False),  
                                file_name=(f'tmin_missing_data_by_station_{month}_{year}_{month}.csv'), 
                                mime='text/csv', key="mon_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Minimum Temperature', key="mon_miss4"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = mon_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = mon_min.iloc[:, 0:9]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
                miss_tmin1 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1].copy()  
                miss_tmin1['No'] = range(1, len(miss_tmin1) + 1) 
                 
                st.info(f'Stations without any missing data in {month} {year}')
                st.write(miss_tmin1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmin1.to_csv(index=False),  
                                file_name=(f'tmin_stationsless1_missing_{month}_{year}.csv'), 
                                mime='text/csv', key="mon_miss5")        
            
        if st.button('Generate Map: Minimum Temperature', key="mon_miss6"):
            if mon_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmin = mon_min.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmin_df = pd.DataFrame(missingdata_row_tmin)
                names_tmin = missingdata_tmin_df.columns.tolist()
                names_tmin[names_tmin.index(0)] = 'Missing_Data_Count'
                missingdata_tmin_df.columns = names_tmin
                sub_tmin = mon_min.iloc[:, 0:10]
                sub_tmin_df = pd.DataFrame(sub_tmin)
                tmin_join = sub_tmin_df.join(missingdata_tmin_df)
                tmin_miss_st = tmin_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Mean Minimum Temperature", "Missing_Data_Count"]]
                miss_tmin3 = tmin_miss_st[tmin_miss_st['Missing_Data_Count'] < 1] 
                
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {month} {year}')
                fig2_tmin_f2 = px.scatter_mapbox(miss_tmin3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Month", "Year", "Missing_Data_Count", "Mean Minimum Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmin_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmin_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmin_f2, use_container_width=True)
        
        
if __name__ == "__main__":
    monthly_data_miss_tmin()