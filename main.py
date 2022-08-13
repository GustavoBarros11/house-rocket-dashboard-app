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
@st.cache(allow_output_mutation=True)
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )

    return data

@st.cache(allow_output_mutation=True)
def data_transform(df):

    # criando variável metro quadrado
    df['valor_m2'] = df.apply(lambda x: x['price']/x['sqft_lot'], axis=1)

def plot_distribution_of_variable(df, col):
    # data plot
    fig = px.histogram ( df, x=col )
    st.plotly_chart( fig, use_container_width=True )

def display_home_page(df):
    if selected == 'Página Inicial':
        st.sidebar.markdown('## Opções de Filtros:')

        col1_1, col1_2, col1_3, col1_4 = st.columns(4)
        
        col1_1.metric(label="Preço Médio dos Imóveis", value=f"${df['price'].mean():,.2f}")

        col1_2.metric(label="Preço Médio do M²", value=f"${df['valor_m2'].mean():,.2f}")

        col1_3.metric(label="Total de Imóveis", value=df.shape[0], delta="100% dos imóveis")
        col1_4.metric(label="Recomendados para COMPRA", value=5808, delta=f'{(5808/df.shape[0])*100:.2f}% dos imóveis', delta_color="off")

        col2_1, col2_2 = st.columns(2)

        with col2_1:
            st.markdown('#### Qtd. de Imóveis por Faixa de Preço')
            plot_distribution_of_variable(df, 'price')
        
        with col2_2:
            st.markdown('#### Métricas de Resumo')
            st.text('Variáveis numéricas')
            df_to_describe = df.describe().T.drop(columns=['count', '25%', '75%'], \
                index=['id', 'lat', 'long', 'sqft_lot15', 'sqft_living15', 'has_basement', \
                    'grade', 'condition', 'view', 'waterfront', 'new_house']) \
                    .rename(columns={
                        'index': 'Atributos',
                        '50%': 'Mediana', 
                        'max': 'Máx', 
                        'min': 'Min', 
                        'mean': 'Média', 
                        'std':'Desvio Padrão'
                    }).sort_index(ascending=False, axis=1)
            st.dataframe(df_to_describe, height=300)
            st.text('Variáveis categóricas')
        
        with st.expander("Visualizar dataframe com TODOS os imóveis do portfólio."):
            # st.write("""
            #    Visualizando dataframe com TODOS os imóveis do portfólio da House Rocket.
            #""")
            st.dataframe(df)
        

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
    filepath = 'resulting_data.csv'
    if st.sidebar.checkbox('Filtrar por imóveis recomendados'):
        filepath = 'report1.csv'
        
    data = get_data(filepath)

    # Transform
    data_transform(data)

    # Load


    # Criando Páginas do Dashboard
    display_home_page(data)
    display_insights_page(data)
    display_results_page(data)

if __name__ == "__main__":
    main()