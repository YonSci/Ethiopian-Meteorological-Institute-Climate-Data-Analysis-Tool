import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Access the shared DataFrame from session state
daily_min = st.session_state.get('daily_min', None)

def daily_mon_con_sum_tmin(variable_type, daily_min):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Minimum Temperature':
        st.markdown("---")
        st.subheader("Minimum Temperature Data Conversion: Daily to Monthly 🌡️")
        if st.button('Convert', key="convert_daily_to_monthly_tmin"):
            if daily_min is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                daily_min['Missing Data'] = daily_min.iloc[:, :].isnull().sum(axis=1)
                daily_tmin5 = daily_min.loc[daily_min['Missing Data'] < 5].copy()
                daily_tmin5['Mean Minimum Temperature'] = daily_tmin5.iloc[:, 9:40].mean(axis=1)
                daily_tmin5['No'] = range(1, len(daily_tmin5) + 1)
                Minimum_Temperature_Mon = daily_tmin5[["No", "Gh id", "Sname","Lat", "Lon", "Elev","ELID", "Year","Month", "Mean Minimum Temperature"]]
                Minimum_Temperature_Mon = round(Minimum_Temperature_Mon, 3)
                # #Rainfall_mon['Month'] = month_to_number[month]
                # Rainfall_mon = Rainfall_mon[["No", "Gh id", "Sname", "Lat", "Lon", "Elev","ELID", "Year","Month", "Total Rainfall"]]
                Minimum_Temperature_Mon = Minimum_Temperature_Mon.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Elev": "Elevation"})   
                # # Reset the index
                # Rainfall_mon = Rainfall_mon.reset_index()
                # # Drop the new index column
                # Rainfall_mon = Rainfall_mon.drop(columns=["index"])
                Minimum_Temperature_Mon = Minimum_Temperature_Mon.iloc[:, 0:10 ]
                st.info("Monthly Mean Minimum Temperature")
                st.write(Minimum_Temperature_Mon)
    
                st.download_button('Download data as CSV', 
                                   Minimum_Temperature_Mon.to_csv(index=False),  
                                   file_name=f'daily_mon_tmin_{month}_{year}.csv',
                                   mime='text/csv')
                
                st.session_state.Minimum_Temperature_Mon = Minimum_Temperature_Mon

        st.markdown("---")        
        Minimum_Temperature_Mon = st.session_state.get('Minimum_Temperature_Mon', 'None')
        st.subheader('Plot Monthly Mean Minimum Temperature')  
        if st.button('Generate Map', key="generate_map_tmin_daily_to_monthly"): 
            st.info("Monthly Mean Minimum Temperature")
            center_coordinates = (9.5, 40.5) 
            mon_tmin = px.scatter_mapbox(Minimum_Temperature_Mon, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Mean Minimum Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            color="Station Name"
            mon_tmin.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(mon_tmin, use_container_width=True)
                
            
        st.markdown("---")   
        st.subheader('Monthly Minimum Temperature Summary Statistics') 
        if st.button('Generate statistics', key="generate_statistics_tmin_daily_to_monthly"):
            tmin_mon_stat = Minimum_Temperature_Mon['Mean Minimum Temperature'].describe(include='all') 
            st.info("Summary Statistics for Monthly Mean Minimum Temperature")
            st.write(tmin_mon_stat) 

            st.download_button('Download data as CSV', 
                            tmin_mon_stat.to_csv(index=False),  
                            file_name=f'mon_total_tmin_stat_{month}_{year}.csv', 
                            mime='text/csv')
                
        # Create a box plot of the 'Monthly Total Rainfall' column
        st.markdown("---") 
        st.subheader('Box Plot Summary Statistics') 
        if st.button('Generate Box Plot', key="generate_box_plot_tmin_daily_to_monthly"):
            st.info("Box Plot of Monthly Mean Minimum Temperature")

        # Create a box plot of the 'Monthly Total Rainfall' column
            fig_rf_mon = go.Figure()

            fig_rf_mon.add_trace(go.Box(
                y=Minimum_Temperature_Mon['Mean Minimum Temperature'],
                name='Mean Minimum Temperature',
                marker_color='blue',
                boxmean=True, # show mean of the data
                #boxpoints='all', # show all points
            ))

            fig_rf_mon.update_layout(
                title='Box Plot of Monthly Mean Minimum Temperature ',
                title_x = 0.4,
                title_y = 0.9,
                yaxis_title='Minimum Temperature',
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
    daily_mon_con_sum_tmin()