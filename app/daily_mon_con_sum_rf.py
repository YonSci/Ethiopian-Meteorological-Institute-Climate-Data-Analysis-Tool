
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Access the shared DataFrame from session state
daily_rf = st.session_state.get('daily_rf', None)

def daily_mon_con_sum_rf(variable_type, daily_rf):
    month = st.session_state.get('month', 'Unknown Month')
    year = st.session_state.get('year', 'Unknown Year')
    if variable_type == 'Rainfall':
        st.markdown("---")
        st.subheader("Rainfall Data Conversion: Daily to Monthly 🌧️")
        if st.button('Convert', key="convert_daily_to_monthly_rf"):
            if daily_rf is None:
                st.warning('Please Load Data in Data Importing Page 😔')
            else:
                daily_rf['Missing Data'] = daily_rf.iloc[:, :].isnull().sum(axis=1)
                daily_rf3 = daily_rf.loc[daily_rf['Missing Data'] < 3].copy()
                daily_rf3['Total Rainfall'] = daily_rf3.iloc[:, 9:40].sum(axis=1)
                daily_rf3['No'] = range(1, len(daily_rf3) + 1)
                Rainfall_mon = daily_rf3[["No", "Gh id", "Sname","Lat", "Lon", "Elev","ELID", "Year","Month", "Total Rainfall"]]
                Rainfall_mon = round(Rainfall_mon, 3)
                # #Rainfall_mon['Month'] = month_to_number[month]
                # Rainfall_mon = Rainfall_mon[["No", "Gh id", "Sname", "Lat", "Lon", "Elev","ELID", "Year","Month", "Total Rainfall"]]
                Rainfall_mon = Rainfall_mon.rename(columns={"Sname": "Station Name", "Lat": "Latitude", "Lon": "Longitude", "Elev": "Elevation"})   
                # # Reset the index
                # Rainfall_mon = Rainfall_mon.reset_index()
                # # Drop the new index column
                # Rainfall_mon = Rainfall_mon.drop(columns=["index"])
                Rainfall_mon = Rainfall_mon.iloc[:, 0:10 ]
                st.info("Monthly Total Rainfall")
                st.write(Rainfall_mon)
    
                st.download_button('Download data as CSV', 
                                   Rainfall_mon.to_csv(index=False),  
                                   file_name=f'daily_mon_rf_{month}_{year}.csv',
                                   mime='text/csv')
                
                st.session_state.Rainfall_mon = Rainfall_mon

        st.markdown("---")        
        Rainfall_mon = st.session_state.get('Rainfall_mon', 'None')
        st.subheader('Plot Monthly Total Rainfall')  
        if st.button('Generate Map', key="generate_map_rf_daily_to_monthly"): 
            st.info("Monthly Total Rainfall")
            center_coordinates = (9.5, 40.5) 
            mon_rf = px.scatter_mapbox(Rainfall_mon, lat="Latitude", lon="Longitude", hover_name="Station Name", hover_data=["Elevation", "Month", "Year", "Total Rainfall"],
            color_discrete_sequence=["green"], zoom=5, height=500)
            color="Station Name"
            mon_rf.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], lon=center_coordinates[1]), zoom=5))
            st.plotly_chart(mon_rf, use_container_width=True)
                
            
        st.markdown("---")   
        st.subheader('Monthly  Rainfall Summary Statistics') 
        if st.button('Generate statistics', key="generate_statistics_rf_daily_to_monthly"):
            rainfall_mon_stat = Rainfall_mon['Total Rainfall'].describe(include='all') 
            st.info("Summary Statistics for Monthly Total Rainfall")
            st.write(rainfall_mon_stat) 

            st.download_button('Download data as CSV', 
                            rainfall_mon_stat.to_csv(index=False),  
                            file_name=f'mon_total_rf_stat_{month}_{year}.csv', 
                            mime='text/csv')
                
        # Create a box plot of the 'Monthly Total Rainfall' column
        st.markdown("---") 
        st.subheader('Box Plot Summary Statistics') 
        if st.button('Generate Box Plot', key="90"):
            st.info("Box Plot of Monthly Total Rainfall")

        # Create a box plot of the 'Monthly Total Rainfall' column
            fig_rf_mon = go.Figure()

            fig_rf_mon.add_trace(go.Box(
                y=Rainfall_mon['Total Rainfall'],
                name='Total Rainfall',
                marker_color='blue',
                boxmean=True, # show mean of the data
                #boxpoints='all', # show all points
            ))

            fig_rf_mon.update_layout(
                title='Box Plot of Monthly Total Rainfall ',
                title_x = 0.4,
                title_y = 0.9,
                yaxis_title='Rainfall',
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
    daily_mon_con_sum_rf()
