import folium
from streamlit_folium import st_folium, folium_static
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st

### Abro dataframes

camaras_final = pd.read_csv('data/camaras_final_lanus.csv')
camaras_heatmap = pd.read_csv("data/heatmap_lanus.csv")

st.title('Reporte de fotomultas en el partido de Lanús')

### Creo tabs

tab_titles2 = [
                "Mapa de ubicación",
                "Mapa de calor",
]

tabs2 = st.tabs(tab_titles2)

data=camaras_final

### Mapa de ubicación

with tabs2[0]:


    data = data.rename(columns={'Descripción de cámaras': 'Tipo_de_cámara'})
    data_filtrada = data.copy()
    st.write('**Ubicación de las cámaras de fotomultas**')

    filtro_tipo_camara2 = st.multiselect(label='Seleccione el tipo de cámara:',
                                        options=data_filtrada['Tipo_de_cámara'].unique(),
                                        default=data_filtrada['Tipo_de_cámara'].unique() )

    data_filtrada2 = data_filtrada.query('Tipo_de_cámara == @filtro_tipo_camara2')

    m = folium.Map(location=[-34.708130, -58.391759], zoom_start=13.4)

    colors = {
        "Cámara entorno y LPR": "red",
        "Cinemómetro": "green"
    }

    for index, row in data_filtrada2.iterrows():
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            icon=folium.Icon(icon= 'camera', color=colors[row["Tipo_de_cámara"]]), # customize the marker icon here
            popup=row['Ubicación'],
        ).add_to(m)

    st_data = st_folium(m, width=1600)


    columns_to_drop = ['Geolocalizacion', 'latitud', 'longitud', 'Fin de actividad', 'Número de cámaras']
    data_filtrada2 = data_filtrada2.drop(columns=columns_to_drop)

    st.dataframe(data_filtrada2)

### Mapa de calor

with tabs2[1]:

    data_heatmap = camaras_heatmap.copy()
    data_heatmap = data_heatmap.rename(columns={'Tipo de cámara': 'Tipo_de_cámara'})

    st.write('**Mapa de calor según cantidad de infracciones**')

    filtro_tipo_camara = st.multiselect(label='Seleccione tipo de cámara:',
                                        options=data_heatmap['Tipo_de_cámara'].unique(),
                                        default=data_heatmap['Tipo_de_cámara'].unique() )

    filtered_data = data_heatmap.query('Tipo_de_cámara == @filtro_tipo_camara')
    fig_heatmap = px.density_mapbox(filtered_data, lat='latitud', lon='longitud', z='Infracciones Por Mes', radius=15,
                                center=dict(lat=-34.708130, lon=-58.391759), zoom=10.5, hover_data={'Tipo_de_cámara': True, 
                                    'Infracciones Por Mes': True, 'Ubicación física': True, 'latitud': False, 'longitud': False},
                                mapbox_style='carto-positron', range_color = [0,2500])
    st.plotly_chart(fig_heatmap, use_container_width=True)

    columns_to_drop2 = ['cantidad', 'latitud', 'longitud']
    data_filtrada3 = filtered_data.drop(columns=columns_to_drop2)
    st.dataframe(data_filtrada3)

#streamlit run 01_app.py