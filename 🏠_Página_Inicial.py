import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import geopandas
import pydeck as pdk

from datetime import datetime
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image

# Read data
@st.cache(allow_output_mutation=True)
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )

    return data

@st.cache(allow_output_mutation=True)
def data_transform(data):
    # Convertendo variável date de object para datetime
    data['date'] = pd.to_datetime(data['date'])

    # Convertendo variáveis do tipo numérico para categórico
    data['month'] = data['month'].astype('category')
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

@st.cache
def convert_df_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv()

@st.cache
def convert_df_excel(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_excel('data.xlsx')

@st.cache
def convert_df_json(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_json()

def plot_distribution_of_variable(df, col):
    # data plot
    fig = px.histogram( df, x=col, title='Qtd. de Imóveis por Faixa de Preço', color_discrete_sequence=["#8d3941"], labels={
        'price': 'Preço do imóvel (USD)',
        'count': 'Total de Imóveis (Und)'
    }, height=290 )
    fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    st.plotly_chart( fig, use_container_width=True )

def plot_bar_chart(df, col1, col2):
    df_plot = df[[col1, col2]].groupby(col1).mean()

    # data plot
    fig = px.bar( x=df_plot.index, y=df_plot['price'], title='Preço médio x Grade', color_discrete_sequence=["#8d3941"], labels={
        'y': 'Preço médio (USD)',
        'x': 'Grade'
    }, height=290 )
    fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    st.plotly_chart( fig, use_container_width=True )

def price_density_maps( df, geofile ):
    st.header( 'Visão Geral da Região' )

    m1, m2 = st.columns( (1, 1) )

    # maps_df = data.copy()
    maps_df = df.loc[df['status'] == 'Buy', :]

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
    
    m1.subheader( 'Densidade por Região' )
    with m1:
        folium_static( density_map )

    # Region Price Map
    m2.subheader( 'Densidade por Preço' )

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
    col1_1, col1_2, col1_3, col1_4 = st.columns(4)
    
    col1_1.metric(label="Total de Imóveis", value=df.shape[0], delta="100% dos imóveis")
    col1_2.metric(label="Recomendados para COMPRA", value=5767, delta=f'{(5767/df.shape[0])*100:.2f}% dos imóveis', delta_color="off")

    col1_3.metric(label="Preço Médio dos Imóveis", value=f"${df['price'].mean():,.2f}")

    col1_4.metric(label="Preço Médio do M²", value=f"${df['valor_m2'].mean():,.2f}")

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
            color_continuous_scale=px.colors.cyclical.IceFire,
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
        data_category = df.select_dtypes(exclude=['int', 'float', 'object'])
        df_num_to_describe = data_numeric.describe().drop(index=['count', '25%', '75%'], \
            columns=['id', 'lat', 'long', \
                'grade']) \
                .rename(index={
                    'index': 'Atributos',
                    '50%': 'Mediana', 
                    'max': 'Máx', 
                    'min': 'Min', 
                    'mean': 'Média', 
                    'std':'Desvio Padrão'
                }).sort_index(ascending=False, axis=1)
        st.dataframe(df_num_to_describe, height=180)
    
    with col3_2:
        st.text('Variáveis categóricas')
        
        st.dataframe(data_category.drop(columns=['date']) \
            .rename(columns={'count':'contagem', 'unique': 'únicos'}).describe())

    with st.expander("Portfólio de imóveis da House Rocket", expanded=True):
        st.write("""
            Tabela com todos os dados dos IMÓVEIS FILTRADOS
        """)
        f_attributes = st.multiselect('Filtro de colunas:', options=df.columns.values)

        c1, c2 = st.columns((5, 1))
        
        df_attr = df.copy()
        if f_attributes != []:
            df_attr = df_attr[f_attributes]
        
        c1.dataframe(df_attr)

        with c2:
            csv = convert_df_csv(df_attr)
            #excel = convert_df_excel(df_attr)
            #json = convert_df_json(df_attr)

            st.download_button('Download .csv', data=csv, file_name='data.csv', key=1)
            #st.download_button('Download .xlsx', data=excel, file_name='data.xlsx', key=2)
            #st.download_button('Download .json', data=json, file_name='data.json', key=3)

    price_density_maps(df, geofile)

    st.header( 'Relatórios de Negócio' )
    tab1, tab2 = st.tabs(["Relatório #1", "Relatório #2"])

    with tab1:
        df_rep1 = pd.read_csv('data/report1.csv', index_col=0)
        st.markdown("##### Visualizar dataframe dos imóveis RECOMENDADOS PARA COMPRA.")
        st.subheader("Relatório 1: Quais os imóveis que a House Rocket deveria comprar e por qual preço?")
        c1, c2, c3 = st.columns((2, 2, 1))

        c1.dataframe(df_rep1)

        df_rep1['profit'] = df_rep1['Median Price'] - df_rep1['price']
        df_rep1_2 = df_rep1.groupby('zipcode').agg({'profit': 'mean'}).reset_index().sort_values('profit', ascending=False)
        df_rep1_2['zipcode'] = df_rep1_2['zipcode'].astype(str)

        with c2:
            # data plot
            fig = px.bar(df_rep1_2[:10], x='zipcode', y='profit', title='Lucro Médio x Região', color_discrete_sequence=["#8d3941"], labels={
                'profit': 'Lucro médio (USD)',
                'zipcode': 'Região'
            }, height=400 )
            fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
            st.plotly_chart( fig, use_container_width=True )

        with c3:
            csv = convert_df_csv(df_rep1)
            #excel = convert_df_excel(df_rep1)
            #json = convert_df_json(df_rep1)

            st.download_button('Download .csv', data=csv, file_name='report1.csv', key=1)
            #st.download_button('Download .xlsx', data=excel, file_name='data.xlsx', key=2)
            #st.download_button('Download .json', data=json, file_name='data.json', key=3)

    with tab2:
        df_rep2 = pd.read_csv('data/report2.csv', index_col=0)
        st.markdown("##### Visualizar dataframe dos imóveis RECOMENDADOS PARA VENDA.")
        st.subheader("Relatório 2: Uma vez comprados, quando será a melhor época para revender e por qual preço?")
        c1, c2, c3 = st.columns((2, 2, 1))

        c1.dataframe(df_rep2)

        with c2:
            # data plot
            fig = px.bar(df_rep2, x='season', y='Buy Price', title='Preço médio de COMPRA x Estação do Ano', color_discrete_sequence=["#8d3941"], labels={
                'y': 'Preço médio de COMPRA (USD)',
                'x': 'Estação do ano'
            }, height=400 )
            fig.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
            st.plotly_chart( fig, use_container_width=True )
        
        with c3:
            csv = convert_df_csv(df_rep2)
            #excel = convert_df_excel(df_rep1)
            #json = convert_df_json(df_rep1)

            st.download_button('Download .csv', data=csv, file_name='report2.csv', key=1)
            #st.download_button('Download .xlsx', data=excel, file_name='data.xlsx', key=2)
            #st.download_button('Download .json', data=json, file_name='data.json', key=3) 
                

    return None

def main():
    st.set_page_config(layout='wide', page_title='Página Inicial | Dashboard de Insights da House Rocket', page_icon=':house:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    with st.sidebar:
        # Images used.
        sidebar_icon = Image.open('images/icon_dash.png')
        st.sidebar.image(sidebar_icon, caption=f'{datetime.now().strftime("%B %d, %Y")}')

    # ETL
    ## Extract
    filepath = 'data/recommended_houses.csv'
        
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

    if df_controller == 1:
        data = data.loc[data['status'] == 'Buy', :]

    with st.sidebar:
        st.markdown('# Opções de Filtros:')

        price_interval = st.slider('Intervalo de Preço', min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=int(data['price'].max()))

        f_zipcode = st.multiselect('Filter by Region', options=data['zipcode'].unique())
        f_season = st.multiselect('Filter by Season', options=data['season'].unique())

        if f_zipcode != []:
            data = data.loc[data['zipcode'].isin( f_zipcode ), :]
        if f_season != []:
            data = data.loc[data['season'].isin( f_season ), :]

        yr_built_interval = st.slider('Year Built', min_value=int(data['yr_built'].min()), max_value=int(data['yr_built'].max()), value=int(data['yr_built'].max()))
        data = data.loc[data['yr_built'] <= yr_built_interval]
        
        # filters
        min_date = datetime.strptime( data['date'].min().strftime( '%Y-%m-%d' ), '%Y-%m-%d' )
        max_date = datetime.strptime( data['date'].max().strftime( '%Y-%m-%d' ), '%Y-%m-%d' )

        f_date = st.sidebar.slider( 'Date', min_date, max_date, max_date )
        data = data[data['date'] <= f_date]
        

        if st.checkbox('Only waterfront houses'):
            data = data.loc[data['waterfront'] == 1]
        if st.checkbox('Only renovated houses'):
            data = data.loc[data['yr_renovated'] > 0]
        if st.checkbox('Only  houses with basement'):
            data = data.loc[data['has_basement'] == 1]

        st.markdown('___')

        st.markdown('# Sobre')
        st.markdown('Construido por **Gustavo Barros**')
        st.markdown('Se você quiser procurar por mais informações sobre este projeto ou entrar em contato comigo, consulte meu [Portfólio de Projetos](https://gustavobarros11.github.io/) ou [Github](https://github.com/GustavoBarros11).')
        st.markdown('___')

    # Criando Páginas do Dashboard
    display_home_page(data, geofile)


if __name__ == "__main__":
    main()