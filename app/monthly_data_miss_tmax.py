import streamlit as st
import pandas as pd
import plotly.express as px

# Access the shared DataFrame from session state
mon_max = st.session_state.get('mon_max', None)

def monthly_data_miss_tmax(variable_type, mon_max):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')

    if variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Missing data across all stations for the entire month")
        if st.button('Count Missing Data: Maximum Temperature', key="mon_miss_tmax1"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missing_data_count_tmax = mon_max.iloc[:, 9:10].isnull().sum().sum()
                st.info(f'Missing maximum temperature data count in {month} {year} is **_{missing_data_count_tmax}_**')
                total_data_points_tmax = mon_max.iloc[:, 9:10].size
                percentage_missing_tmax = (missing_data_count_tmax / total_data_points_tmax) * 100
                st.info(f'The percentage of missing maximum temperature data in {month} {year} is **_{round(percentage_missing_tmax, 2)}%_**')
                            
        
        st.markdown("---")
        st.subheader('Missing data counts by station')
        if st.button('Tabular Report: Maximum Temperature', key="mon_miss_tmax2"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = mon_max.iloc[:, 9:10].isnull().sum(axis=1)        
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = mon_max.iloc[:, 0:9]                
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)                         
                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Missing_Data_Count"]]
        
                st.info(f'Missing maximum temperature data counts for {month} {year}')
                st.write(tmax_miss_st)
                st.download_button('Download data as CSV', 
                                tmax_miss_st.to_csv(index=False),  
                                file_name=(f'tmax_missing_data_by_station_{month}_{year}_{month}.csv'), 
                                mime='text/csv', key="mon_miss3")
                
        st.markdown("---")
        st.subheader('Stations Without Missing Data')
        if st.button('Tabular Report: Maximum Temperature', key="mon_miss4"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = mon_max.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = mon_max.iloc[:, 0:9]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)
                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Missing_Data_Count"]]
                
                miss_tmax1 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 1].copy()  
                miss_tmax1['No'] = range(1, len(miss_tmax1) + 1) 
                
                st.info(f'Stations without any missing data in {month} {year}')
                st.write(miss_tmax1)    
        
                st.download_button('Download data as CSV', 
                                miss_tmax1.to_csv(index=False),  
                                file_name=(f'tmax_stationsless1_missing_{month}_{year}.csv'), 
                                mime='text/csv', key="mon_miss5")        
            
        if st.button('Generate Map: Maximum Temperature', key="mon_miss6"):
            if mon_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                missingdata_row_tmax = mon_max.iloc[:, 9:10].isnull().sum(axis=1)
                missingdata_tmax_df = pd.DataFrame(missingdata_row_tmax)
                names_tmax = missingdata_tmax_df.columns.tolist()
                names_tmax[names_tmax.index(0)] = 'Missing_Data_Count'
                missingdata_tmax_df.columns = names_tmax
                sub_tmax = mon_max.iloc[:, 0:10]
                sub_tmax_df = pd.DataFrame(sub_tmax)
                tmax_join = sub_tmax_df.join(missingdata_tmax_df)

                tmax_miss_st = tmax_join[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "ELID", "Year", "Month", "Mean Maximum Temperature","Missing_Data_Count"]]          
                miss_tmax3 = tmax_miss_st[tmax_miss_st['Missing_Data_Count'] < 1] 
                center_coordinates = (9.5, 40.5)
                st.info(f'Stations without any missing data in {month} {year}')
                fig2_tmax_f2 = px.scatter_mapbox(miss_tmax3, lat="Latitude", lon="Longitude", 
                                            hover_name="Station Name", 
                                            hover_data=["Elevation", "Month", "Year", "Missing_Data_Count", "Mean Maximum Temperature"],
                                            color_discrete_sequence=["green"], 
                                            zoom=5, height=500)
                fig2_tmax_f2.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
                # Update the legend to use markers
                fig2_tmax_f2.update_layout(legend=dict(itemsizing='constant'))
                
                st.plotly_chart(fig2_tmax_f2, use_container_width=True)
        
        
if __name__ == "__main__":
    monthly_data_miss_tmax()