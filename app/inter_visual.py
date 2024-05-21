import streamlit as st
import plotly.express as px


def inter_visual(variable_type, df_data):
    
    variable = st.session_state.get('variable', 'None')

    if df_data is not None:
        df_data = df_data.rename(columns={df_data.columns[-1]: variable})
        var_name = df_data[variable].name
        
    st.markdown("#### :blue[2) Visualize the data ]" )
    
    if st.checkbox("Visualize the spatial distribution", key="_map"):
        
        
        
        center_coordinates = (9.5, 40.5)
        fig_rf_i1 = px.scatter_mapbox(df_data, 
                                    lat="Latitude", lon="Longitude", 
                                    hover_name="Station Name", 
                                    hover_data=["Elevation", "Month", "Year", "Longitude", "Latitude", var_name],
                                    color=var_name, # Add color based on Total Rainfall
                                    color_continuous_scale=px.colors.sequential.Viridis, # Set color scale
                                    height=600,
                                    width=900
                                    )

        # Set marker size to 15
        fig_rf_i1.update_traces(marker=dict(size=10))

        # Customize the layout with the center coordinates
        fig_rf_i1.update_layout(mapbox_style="open-street-map",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                mapbox=dict(center=dict(lat=center_coordinates[0], 
                                                        lon=center_coordinates[1]),
                                            zoom=5.1))

        # Show the map
        st.plotly_chart(fig_rf_i1)  
            
    st.markdown("---")
            
if __name__ == "__main__":
    inter_visual()