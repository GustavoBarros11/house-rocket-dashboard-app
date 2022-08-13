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
def data_transform(data):
    # Convertendo variáável date de object para datetime
    data['date'] = pd.to_datetime(data['date'])

    # Convertendo variáveis do tipo numérico para categórico
    data['has_basement'] = data['has_basement'].astype('category')
    data['new_house'] = data['new_house'].astype('category')
    data['condition'] = data['condition'].astype('category')
    data['waterfront'] = data['waterfront'].astype('category')
    data['view'] = data['view'].astype('category')

    # criando variável metro quadrado
    data['valor_m2'] = data.apply(lambda x: x['price']/x['sqft_lot'], axis=1)

    return data

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    try:
        geofile = geopandas.read_file( url )

        return geofile
    except:
        return None

def plot_distribution_of_variable(df, col):
    # data plot
    fig = px.histogram( df, x=col, title='Qtd. de Imóveis por Faixa de Preço', labels={
        'price': 'Preço do imóvel (USD)',
        'count': 'Total de Imóveis (Und)'
    }, height=290 )
    fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    st.plotly_chart( fig, use_container_width=True )

def plot_bar_chart(df, col1, col2):
    df_plot = df[[col1, col2]].groupby(col1).mean()

    # data plot
    fig = px.bar( x=df_plot.index, y=df_plot['price'], title='Qtd. de Imóveis por Faixa de Preço', labels={
        'y': 'Preço médio (USD)',
        'x': 'Grade'
    }, height=290 )
    fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    st.plotly_chart( fig, use_container_width=True )

def price_density_maps( df, geofile ):
    st.header( 'Visão Geral da Região' )

    m1, m2 = st.columns( (1, 1) )

    # maps_df = data.copy()
    maps_df = df.sample( 100 )

    # Base Map - Folium
    density_map = folium.Map( location=[maps_df['lat'].mean(),
        maps_df['long'].mean()],
        default_zoom_start=15 )

    marker_cluster = MarkerCluster().add_to( density_map )

    for name, row in maps_df.iterrows():
        folium.Marker( [row['lat'], row['long']],
        popup=f"Price ${row['price']} on: {row['date']}  Features: {row['sqft_living']}" 
        + f"sqft, {row['bedrooms']} bedrooms, {row['bathrooms']}"
        + f" bathrooms, year built: {row['yr_built']}" ).add_to( marker_cluster )
    
    m1.subheader( 'Portfolio Density' )
    with m1:
        folium_static( density_map )

    # Region Price Map
    m2.subheader( 'Price Density' )

    df_m2 = maps_df[['price', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
    df_m2.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin( df_m2['ZIP'].tolist() )]

    region_price_map = folium.Map( location=[df['lat'].mean(),
            df['long'].mean()],
            default_zoom_start=15 )
    
    region_price_map.choropleth( data = df_m2,
        geo_data = geofile,
        columns=['ZIP', 'PRICE'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd',
        fill_opacity = 0.7,
        line_opacity = 0.2,
        legend_name = 'AVG PRICE' )

    with m2:
        folium_static( region_price_map )
    
    return None

def display_home_page(df, geofile):
    if selected == 'Página Inicial':
        col1_1, col1_2, col1_3, col1_4 = st.columns(4)
        
        col1_1.metric(label="Preço Médio dos Imóveis", value=f"${df['price'].mean():,.2f}")

        col1_2.metric(label="Preço Médio do M²", value=f"${df['valor_m2'].mean():,.2f}")

        col1_3.metric(label="Total de Imóveis", value=df.shape[0], delta="100% dos imóveis")
        col1_4.metric(label="Recomendados para COMPRA", value=5808, delta=f'{(5808/df.shape[0])*100:.2f}% dos imóveis', delta_color="off")

        col2_1, col2_2 = st.columns(2)

        with col2_1:
            st.markdown('#### Principais Métricas')
            plot_distribution_of_variable(df, 'price')
            plot_bar_chart(df, 'grade', 'price')
        
        with col2_2:
            st.markdown('#### Mapa de densidade: Preço x Valor M²')
            fig = px.scatter_mapbox( df,
                lat='lat',
                lon='long',
                color='price',
                size='valor_m2',
                color_continuous_scale=px.colors.sequential.dense,
                size_max=15,
                zoom=9.5 )

            fig.update_layout( mapbox_style='open-street-map' )
            fig.update_layout( height=600, margin={'r': 0, 'l': 0, 'b': 0, 't': 0})
            st.plotly_chart(fig)

        st.markdown('#### Métricas de Resumo')
        col3_1, col3_2 = st.columns((2, 1))

        with col3_1:
            st.text('Variáveis numéricas')

            data_numeric = df.select_dtypes(include=['int', 'float'])
            data_category = df.select_dtypes(exclude=['int', 'float'])
            df_num_to_describe = data_numeric.describe().T.drop(columns=['count', '25%', '75%'], \
                index=['id', 'lat', 'long', 'sqft_lot15', 'sqft_living15', \
                    'grade']) \
                    .rename(columns={
                        'index': 'Atributos',
                        '50%': 'Mediana', 
                        'max': 'Máx', 
                        'min': 'Min', 
                        'mean': 'Média', 
                        'std':'Desvio Padrão'
                    }).sort_index(ascending=False, axis=1)
            st.dataframe(df_num_to_describe, height=160)
        
        with col3_2:
            st.text('Variáveis categóricas')
            
            st.dataframe(data_category.drop(columns=['date', 'season']) \
                .rename(columns={'count':'contagem', 'unique': 'únicos'}).describe().T, height=160)

        price_density_maps(df, geofile)

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
    # ETL
    ## Extract
    filepath = 'resulting_data.csv'
        
    data = get_data(filepath)

    # get geofile
    url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    geofile = get_geofile( url )

    ## Transform
    data = data_transform(data)

    ## Load
    df_controller = st.sidebar.selectbox('Qual grupo de imóveis você deseja visualizar?', \
         options=[0, 1], \
            format_func=lambda x: 'Todos os Imóveis' if x == 0 else 'Apenas Imóveis Recomendados')

    st.sidebar.markdown('# Opções de Filtros:')

    with st.sidebar:
        price_interval = st.slider('Intervalo de Preço', min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=int(data['price'].max()))

        st.multiselect('Selecionar por Código Postal', options=data['zipcode'].unique())

    # Criando Páginas do Dashboard
    display_home_page(data, geofile)
    display_insights_page(data)
    display_results_page(data)

    st.header( 'Relatórios de Negócio' )
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


if __name__ == "__main__":
    main()