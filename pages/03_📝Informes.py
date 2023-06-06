import folium
from streamlit_folium import st_folium, folium_static
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import base64

st.title('Reporte de fotomultas en el partido de Lanús')

with open("data/marzolanus.pdf","rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'

with st.expander("**Visualizar Informe de Marzo 2023**"):
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.expander("**Visualizar Informe de Abril 2023**"):
    st.write("En desarrollo...")

#streamlit run 01_Recaudacion.py