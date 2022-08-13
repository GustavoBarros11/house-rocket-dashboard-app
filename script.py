from multiprocessing.sharedctypes import Value
from turtle import left
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import folium
import geopandas
import pydeck as pdk

from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from folium.plugins import MarkerCluster
from PIL import Image
from datetime import datetime

st.set_page_config(layout='wide')

st.markdown("<h1 style='text-align: left; color: #5c3934;'><i>Dashboard de Insights da House Rocket</i></h1><hr>", unsafe_allow_html=True)
#st.markdown(f"<span style='color: #5c3934;text-align: left;font-weight: normal;font-size: 1rem;'>{datetime.now().strftime('%d/%m/%Y')}</span><hr>", unsafe_allow_html=True)

with st.sidebar:
    # Images used.
    sidebar_icon = Image.open('images/icon_dash.png')
    st.sidebar.image(sidebar_icon)

    selected = option_menu(menu_title="MENU PRINCIPAL",
            options= ['Página Inicial', 'Insights Gerados', 'Resultados de Negócio'],
            icons=['house','bar-chart', 'calendar2-check'],
            menu_icon='cast',
            default_index = 0,
            orientation='vertical',
            styles={"container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "#087888", "font-size": "18px"},
                    "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px",
                                    "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#5c3934"},
                    "menu-title": {"text-align": "center", "color": "#5c3934"}})

# Read data
@st.cache( allow_output_mutation=True )
def load_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )

    return data

def display_home_page(data):
    if selected == 'Página Inicial':
        st.sidebar.markdown('## Opções de Filtros:')

        col1, col2, col3 = st.columns((1, 1, 2))
        col1.metric(label="Gas price", value=4, delta=-0.5, delta_color="inverse")
        
        with col2:
            st.metric("Temperature", "70 °F", "1.2 °F")

            st.metric(label="Active developers", value=123, delta=123, delta_color="off")

            st.metric(label="Gas price", value=4, delta=-0.5, delta_color="inverse")

            st.metric(label="Active developers", value=123, delta=123, delta_color="off")

        with col3:
            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=47.721,
                    longitude=-122.319,
                    zoom=10,
                    pitch=70,
                ),
                layers=[
                    pdk.Layer(
                        'HexagonLayer',
                        data=data,
                        get_position='[long, lat]',
                        radius=200,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    ),
                    #pdk.Layer(
                    #    'ScatterplotLayer',
                    #    data=data,
                    #    get_position='[long, lat]',
                    #    get_color='[200, 30, 0, 160]',
                    #    get_radius='200',
                    #),
                ],
            ))

        with st.expander("Visualizar dataframe com TODOS os imóveis do portfólio."):
            # st.write("""
            #    Visualizando dataframe com TODOS os imóveis do portfólio da House Rocket.
            #""")
            st.dataframe(data)
        # f_all = st.checkbox('Filtrar por imóveis recomendados', value=False)

        # c1, c2, c3, c4 = st.columns(1, 1, 1, 1)
        



    
    return None
        

def display_insights_page(data):
    if selected == 'Insights Gerados':
        st.write('Mostrando a Página 2')

    return None

def display_results_page(data):
    if selected == 'Resultados de Negócio':
        st.write('Mostrando a Página 3')

    return None

def main():
    # Extract
    filepath = 'kc_house_treated_data.csv'
    if st.sidebar.checkbox('Filtrar por imóveis recomendados'):
        filepath = 'report1.csv'
        
    data = load_data(filepath)

    # Transform


    # Load


    # Criando Páginas do Dashboard
    display_home_page(data)
    display_insights_page(data)
    display_results_page(data)

if __name__ == "__main__":
    main()