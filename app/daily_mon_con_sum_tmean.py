import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Access the shared DataFrame from session state
daily_max = st.session_state.get('daily_max', None)
daily_min = st.session_state.get('daily_min', None)


def daily_mon_con_sum_tmean(variable_type, daily_max, daily_min):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    
    if variable_type == 'Mean Temperature':
        st.markdown("---")
        st.subheader("Mean Temperature Data Conversion: Daily to Monthly 🌡️")
        if st.button('Convert', key="convert_daily_to_monthly_tmean"):
            if daily_max is None or daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                daily_max['Missing Data'] = daily_max.iloc[:, :].isnull().sum(axis=1)
                daily_min['Missing Data'] = daily_min.iloc[:, :].isnull().sum(axis=1)       
                daily_max5 = daily_max.loc[daily_max['Missing Data'] < 5].copy()
                daily_min5 = daily_min.loc[daily_min['Missing Data'] < 5].copy()    
                daily_max5['Mean Maximum Temperature'] = daily_max5.iloc[:, 9:40].mean(axis=1)
                daily_min5['Mean Minimum Temperature'] = daily_min5.iloc[:, 9:40].mean(axis=1) 
                daily_max5['No'] = range(1, len(daily_max5) + 1)
                daily_min5['No'] = range(1, len(daily_min5) + 1) 
                maxtemp_mon = daily_max5[["No", "Gh id", "Sname","Lat", "Lon", "Elev","ELID", "Year","Month", "Missing Data", "Mean Maximum Temperature"]]
                mintemp_mon = daily_min5[["No", "Gh id", "Sname","Lat", "Lon", "Elev","ELID", "Year","Month", "Missing Data", "Mean Minimum Temperature"]]
                maxtemp_mon = round(maxtemp_mon, 3)
                mintemp_mon = round(mintemp_mon, 3)
                maxtemp_mon = maxtemp_mon.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
                mintemp_mon = mintemp_mon.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Missing Data": "Missing Data (days)", "Elev":"Elevation"})
                mean_temp_mon = maxtemp_mon.merge(mintemp_mon, how='inner', on=["Gh id"])
                mean_temp_mon = mean_temp_mon.rename(columns={"No_x": "No", "Station Name_x": "Station Name", "Latitude_x": "Latitude", "Longitude_x": "Longitude", "Elevation_x":"Elevation","ELID_x":"ELID","Year_x":"Year", "Month_x":"Month", "Missing Data (days)_x": "Missing Data (days)"})
                mean_temp_mon['Mean Temperature'] = (mean_temp_mon['Mean Maximum Temperature'] + mean_temp_mon['Mean Minimum Temperature']) / 2
                mean_temp_mon = mean_temp_mon[["No", "Gh id", "Station Name", "Latitude", "Longitude", "Elevation", "Year","Month", "Mean Temperature"]]                    
                mean_temp_mon['No'] = range(1, len(mean_temp_mon) + 1)
                st.info("Monthly Mean Temperature")
                st.write(mean_temp_mon)  
    
                st.download_button('Download data as CSV', 
                                   mean_temp_mon.to_csv(index=False),  
                                   file_name=f'daily_mon_tmean_{month}_{year}.csv',
                                   mime='text/csv')
                
                st.session_state.mean_temp_mon = mean_temp_mon

        st.markdown("---")        
        mean_temp_mon = st.session_state.get('mean_temp_mon', 'None')
        st.subheader('Plot Monthly Mean Temperature')  
        if st.button('Generate Map', key="generate_map_tmean_daily_to_monthly"): 
            st.info("Monthly Mean Temperature")
            center_coordinates = (9.5, 40.5) 
            mon_tmean = px.scatter_mapbox(mean_temp_mon, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Mean Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            color="Station Name"
            mon_tmean.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(mon_tmean, use_container_width=True)
                
            
        st.markdown("---")   
        st.subheader('Monthly Mean Temperature Summary Statistics') 
        if st.button('Generate statistics', key="generate_statistics_tmean_daily_to_monthly"):
            tmean_mon_stat = mean_temp_mon['Mean Temperature'].describe(include='all') 
            st.info("Summary Statistics for Monthly Mean Temperature")
            st.write(tmean_mon_stat) 

            st.download_button('Download data as CSV', 
                            tmean_mon_stat.to_csv(index=False),  
                            file_name=f'mon_mean_tmean_stat_{month}_{year}.csv', 
                            mime='text/csv')
                
        #  Create a box plot of the 'Monthly Total Rainfall' column
        st.markdown("---") 
        st.subheader('Box Plot Summary Statistics') 
        if st.button('Generate Box Plot', key="generate_box_plot_tmean_daily_to_monthly"):
            st.info("Box Plot of Monthly Mean Temperature")

        # Create a box plot of the 'Monthly Total Rainfall' column
            fig_rf_mon = go.Figure()

            fig_rf_mon.add_trace(go.Box(
                y=mean_temp_mon['Mean Temperature'],
                name='Mean Temperature',
                marker_color='blue',
                boxmean=True, # show mean of the data
                #boxpoints='all', # show all points
            ))

            fig_rf_mon.update_layout(
                title='Box Plot of Monthly Mean Temperature ',
                title_x = 0.4,
                title_y = 0.9,
                yaxis_title='Mean Temperature',
                #xaxis_title=f'Month',
                boxmode='group', # group together boxes of the different traces for each value of x
                plot_bgcolor='rgba(0,0,0,0)', # set background color to transparent
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                ),
            )
            
            st.plotly_chart(fig_rf_mon, use_container_width=True)
            
if __name__ == "__main__":
    daily_mon_con_sum_tmean()