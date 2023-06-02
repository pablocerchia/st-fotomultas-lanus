import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import folium
from streamlit_folium import st_folium, folium_static

### Seteo de pagina

st.set_page_config(page_title = 'Reporte de fotomultas en el partido de Lanús',
                    layout='wide',
                    initial_sidebar_state='collapsed')

st.title('Reporte de fotomultas en el partido de Lanús')

### Apertura de dataframes

df_recaudacion = pd.read_csv('data/recaudacion_lanus.csv')

# Tabs

tab_titles = [
                "Recaudación según metodo de pago",
                "Recaudación e infracciones según tipo de cámara",
]

tabs = st.tabs(tab_titles)

### Ploteo


with tabs[0]:
    col1, col2 = st.columns(2)
    ### ARMO COLUMNAS CON METRICAS
    with col1: 
        st.metric(
            label='Recaudación',
            value='$145.990.964,71'
            )
        
        fig_pie_recaudacion = px.pie(df_recaudacion, values='importes', names='tipos de pago')
        fig_pie_recaudacion.update_layout(title_text="Distribución de la recaudación por método de pago")
        st.plotly_chart(fig_pie_recaudacion)

    with col2: 
        st.metric(
                label='Infracciones',
                value=29962
            )
        
        fig_barras_recaudacion = go.Figure(go.Bar(x=df_recaudacion['importes'],y=df_recaudacion['tipos de pago'],orientation='h',text=df_recaudacion['importes'].astype(int)))
        fig_barras_recaudacion.update_layout(title="Distribución de la recaudación por método de pago")
        st.plotly_chart(fig_barras_recaudacion)

with tabs[1]:
    col_1, col_2, col_3, col_4, col_5= st.columns(5)
    col_6, col_7, col_8, col_9, col_0= st.columns(5)
    with col_1: 
        st.metric(
            label='Cantidad de presunciones captadas',
            value=33305
        )

    with col_2: 
        st.metric(
            label='Imágenes aceptadas por Auditoría Interna',
            value=33206)

    with col_3: 
        st.metric(
            label='Imágenes rechazadas por Auditoría Interna',
            value=99
        )

    with col_4: 
        st.metric(
            label='Imágenes rechazadas por el Municipio',
            value=3244
        )
    with col_5: 
        st.metric(
            label='Presunciones validadas por el Municipio',
            value=29962
        )
    with col_6: 
        st.metric(
            label='Actas de notificaciones bajo puerta',
            value=14854
        )

    with col_7: 
        st.metric(
            label='Actas de notificaciones fehacientes',
            value=10072)

    with col_8: 
        st.metric(
            label='Actas de notificaciones de audiencia',
            value='No hay'
        )

    with col_9: 
        st.metric(
            label='Actas de notificaciones de sentencia',
            value='No hay'
        )
    with col_0: 
        st.metric(
            label='Actas a títulos ejecutivos',
            value='No hay'
        )
    col_graf1, col_graf2 = st.columns(2)

    ###################GRAFICO 1A#################################
    with col_graf1:
        cantidad_tipos_camara = pd.read_csv('data/tipo_infrac.csv')
        cantidad_tipos_camara['cantidad'] = 1 

        fig_cantidad_tipos_camara = px.pie(cantidad_tipos_camara, values='cantidad', names='Tipo de cámara',  title='Tipos de cámara (Marzo 2023)')
        fig_cantidad_tipos_camara.update_layout(
                        title_text="Tipos de cámara (Marzo 2023)",
                        template="plotly_white",
                        showlegend=True)
        st.plotly_chart(fig_cantidad_tipos_camara)
###################GRAFICO 2A#################################

        facturacion_tipocamara = cantidad_tipos_camara.groupby('Tipo de cámara')['Facturacion por equipo'].sum().reset_index()
        facturacion_tipocamara = facturacion_tipocamara.sort_values(by='Facturacion por equipo')
        facturacion_tipocamara['color'] = '#496595'
        facturacion_tipocamara['color'][:-2] = '#c6ccd8'

        barras_facturacion_tipocamara= go.Figure()

        barras_facturacion_tipocamara.add_trace(
            go.Bar(x=facturacion_tipocamara['Facturacion por equipo'], y=facturacion_tipocamara['Tipo de cámara'], marker=dict(color= facturacion_tipocamara['color']),
                            name='Tipo de cámara', text=facturacion_tipocamara['Facturacion por equipo'], orientation='h')
        )
        barras_facturacion_tipocamara.update_layout(
                        title_text="Facturación por tipo de cámara (Marzo 2023)",
                        template="plotly_white",
                        showlegend=False)
        st.plotly_chart(barras_facturacion_tipocamara)
    with col_graf2:
###################GRAFICO 1B#################################
        infracciones_tipos_camara = pd.read_csv('data/tipo_infrac.csv')
        fig_infracciones_tipos_camara = px.pie(infracciones_tipos_camara, values='Infracciones Por Mes', names='Tipo de cámara',  title='Infracciones por tipo de cámara (Marzo 2023)')
        fig_infracciones_tipos_camara.update_layout(
                        title_text="Infracciones por tipo de cámara (Marzo 2023)",
                        template="plotly_white",
                        showlegend=True)
        st.plotly_chart(fig_infracciones_tipos_camara)

###################GRAFICO 2B#################################

        cant_tipoinfrac = cantidad_tipos_camara[['Circular a contramano', 'Cruzar con luz roja',
            'Falta patente trasera o fuera de lugar', 'Giro indebido',
            'No detenerse en línea de frenado o sobre senda peatonal',
            'No respetar carril establecido',
            'Sin casco y/o chaleco reflectante (moto)',
            'Exceso de Velocidad',
            'Estacionamiento indebido', 'Varias']]

        cant_tipoinfrac2 = pd.melt(cant_tipoinfrac, var_name='Tipo de infracción', value_name='Cantidad de infracciones')
        cant_tipoinfrac3 = cant_tipoinfrac2.groupby('Tipo de infracción')['Cantidad de infracciones'].sum().reset_index()
        cant_tipoinfrac3 = cant_tipoinfrac3.sort_values(by='Cantidad de infracciones')
        cant_tipoinfrac3['color'] = '#496595'
        cant_tipoinfrac3['color'][:-2] = '#c6ccd8'

        barras_cant_tipoinfrac= go.Figure()

        barras_cant_tipoinfrac.add_trace(
            go.Bar(x=cant_tipoinfrac3['Cantidad de infracciones'], y=cant_tipoinfrac3['Tipo de infracción'], marker=dict(color= cant_tipoinfrac3['color']),
                            name='Tipo de infracción', text=cant_tipoinfrac3['Cantidad de infracciones'], orientation='h')
        )
        barras_cant_tipoinfrac.update_layout(
                        title_text="Distribución por tipo de infracción (Marzo 2023)",
                        template="plotly_white",
                        showlegend=False)
        st.plotly_chart(barras_cant_tipoinfrac)

###################GRAFICO 3#################################

    facturacion_ubicacion = pd.read_csv('data/facturacion_ubicacion.csv')
    facturacion_ubicacion['color'] = '#496595'
    facturacion_ubicacion['color'][:-2] = '#c6ccd8'

    barras_facturacion_ubi= go.Figure()

    barras_facturacion_ubi.add_trace(
        go.Bar(x=facturacion_ubicacion['Facturacion por equipo'], y=facturacion_ubicacion['Ubicación física'], marker=dict(color= facturacion_ubicacion['color']),
                        name='Ubicación física', text=facturacion_ubicacion['Facturacion por equipo'], orientation='h')
    )
    barras_facturacion_ubi.update_layout(bargap=0.2, height=1000,
                    title_text="Facturación por ubicación (Marzo 2023)",
                    template="plotly_white",
                    showlegend=False)
    st.plotly_chart(barras_facturacion_ubi, use_container_width=True)

#streamlit run 01_app.py
