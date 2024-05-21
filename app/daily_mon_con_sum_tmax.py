import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Access the shared DataFrame from session state
daily_max = st.session_state.get('daily_max', None)

def daily_mon_con_sum_tmax(variable_type, daily_max):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Maximum Temperature':
        st.markdown("---")
        st.subheader("Maximum Temperature Data Conversion: Daily to Monthly 🌡️")
        if st.button('Convert', key="convert_daily_to_monthly_tmax"):
            if daily_max is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                daily_max['Missing Data'] = daily_max.iloc[:, :].isnull().sum(axis=1)
                daily_tmax5 = daily_max.loc[daily_max['Missing Data'] < 5].copy()
                daily_tmax5['Mean Maximum Temperature'] = daily_tmax5.iloc[:, 9:40].mean(axis=1)
                daily_tmax5['No'] = range(1, len(daily_tmax5) + 1)
                Maximum_Temperature_Mon = daily_tmax5[["No", "Gh id", "Sname","Lat", "Lon", "Elev","ELID", "Year","Month", "Mean Maximum Temperature"]]
                Maximum_Temperature_Mon = round(Maximum_Temperature_Mon, 3)
                # #Rainfall_mon['Month'] = month_to_number[month]
                # Rainfall_mon = Rainfall_mon[["No", "Gh id", "Sname", "Lat", "Lon", "Elev","ELID", "Year","Month", "Total Rainfall"]]
                Maximum_Temperature_Mon = Maximum_Temperature_Mon.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Elev": "Elevation"})   
                # # Reset the index
                # Rainfall_mon = Rainfall_mon.reset_index()
                # # Drop the new index column
                # Rainfall_mon = Rainfall_mon.drop(columns=["index"])
                Maximum_Temperature_Mon = Maximum_Temperature_Mon.iloc[:, 0:10 ]
                st.info("Monthly Mean Maximum Temperature")
                st.write(Maximum_Temperature_Mon)
    
                st.download_button('Download data as CSV', 
                                   Maximum_Temperature_Mon.to_csv(index=False),  
                                   file_name=f'daily_mon_tmax_{month}_{year}.csv',
                                   mime='text/csv')
                
                st.session_state.Maximum_Temperature_Mon = Maximum_Temperature_Mon

        st.markdown("---")        
        Maximum_Temperature_Mon = st.session_state.get('Maximum_Temperature_Mon', 'None')
        st.subheader('Plot Monthly Mean Maximum Temperature')  
        if st.button('Generate Map', key="generate_map_tmax_daily_to_monthly"): 
            st.info("Monthly Mean Maximum Temperature")
            center_coordinates = (9.5, 40.5) 
            mon_tmax = px.scatter_mapbox(Maximum_Temperature_Mon, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Mean Maximum Temperature"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            color="Station Name"
            mon_tmax.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(mon_tmax, use_container_width=True)
                
            
        st.markdown("---")   
        st.subheader('Monthly Maximum Temperature Summary Statistics') 
        if st.button('Generate statistics', key="generate_statistics_tmax_daily_to_monthly"):
            tmax_mon_stat = Maximum_Temperature_Mon['Mean Maximum Temperature'].describe(include='all') 
            st.info("Summary Statistics for Monthly Mean Maximum Temperature")
            st.write(tmax_mon_stat) 

            st.download_button('Download data as CSV', 
                            tmax_mon_stat.to_csv(index=False),  
                            file_name=f'mon_mean_tmax_stat_{month}_{year}.csv', 
                            mime='text/csv')
                
        # Create a box plot of the 'Monthly Total Rainfall' column
        st.markdown("---") 
        st.subheader('Box Plot Summary Statistics') 
        if st.button('Generate Box Plot', key="generate_box_plot_tmax_daily_to_monthly"):
            st.info("Box Plot of Monthly Mean Maximum Temperature")

        # Create a box plot of the 'Monthly Total Rainfall' column
            fig_rf_mon = go.Figure()

            fig_rf_mon.add_trace(go.Box(
                y=Maximum_Temperature_Mon['Mean Maximum Temperature'],
                name='Mean Maximum Temperature',
                marker_color='blue',
                boxmean=True, # show mean of the data
                #boxpoints='all', # show all points
            ))

            fig_rf_mon.update_layout(
                title='Box Plot of Monthly Mean Maximum Temperature ',
                title_x = 0.4,
                title_y = 0.9,
                yaxis_title='Maximum Temperature',
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
    daily_mon_con_sum_tmax()