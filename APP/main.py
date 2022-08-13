from json import load
from turtle import color
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import geopandas
import pydeck as pdk

from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from PIL import Image

st.set_page_config(layout='wide', page_title='Dashboard de Insights da House Rocket', page_icon=':thumbsup:')

st.markdown("<h1 style='text-align: left; color: #5c3934;'><i>Dashboard de Insights da House Rocket</i></h1><hr>", unsafe_allow_html=True)

with st.sidebar:
    # Images used.
    sidebar_icon = Image.open('images/icon_dash.png')
    st.sidebar.image(sidebar_icon)

    selected = option_menu(menu_title="MENU PRINCIPAL",
            options= ['Página Inicial', 'Insights Gerados', 'Resultados de Negócio', 'Análise de Imóvel'],
            icons=['house','bar-chart', 'calendar2-check', 'list-ul'],
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
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )

    return data

def display_home_page(data):
    if selected == 'Página Inicial':
        st.sidebar.markdown('## Opções de Filtros:')

        col1, col2 = st.columns((1, 3))
        
        with col1:
            st.metric("Temperature", "70 °F", "1.2 °F")

            st.metric(label="Active developers", value=123, delta=123, delta_color="off")

            st.metric(label="Gas price", value=4, delta=-0.5, delta_color="inverse")

            st.metric(label="Active developers", value=123, delta=123, delta_color="off")

        with col2:
            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=47.721,
                    longitude=-122.319,
                    zoom=10,
                    pitch=50,
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
        #    draw_scatter_map(data)

        with st.expander("Visualizar dataframe com TODOS os imóveis do portfólio."):
            # st.write("""
            #    Visualizando dataframe com TODOS os imóveis do portfólio da House Rocket.
            #""")
            st.dataframe(data)
        # f_all = st.checkbox('Filtrar por imóveis recomendados', value=False)

        # c1, c2, c3, c4 = st.columns(1, 1, 1, 1)

    return None

# def draw_scatter_map(df):
#     fig = px.scatter_mapbox(
#         df,
#         lat='lat',
#         lon='long',
#         size='condition',
#         color='price',
#         color_continuous_scale=px.colors.cyclical.IceFire,
#         size_max=7,
#         zoom=10
#     )

#     fig.update_layout(mapbox_style='open-street-map')
#     fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     st.plotly_chart(fig)

#     return None
        

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
    filepath = 'resulting_data.csv'
    if st.sidebar.checkbox('Filtrar por imóveis recomendados'):
        filepath = 'report1.csv'
        
    data = get_data(filepath)

    # Transform


    # Load


    # Criando Páginas do Dashboard
    display_home_page(data)
    display_insights_page(data)
    display_results_page(data)

if __name__ == "__main__":
    main()