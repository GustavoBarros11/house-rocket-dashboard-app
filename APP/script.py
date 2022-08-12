from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas
import folium

from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster
from datetime import datetime

@st.cache( allow_output_mutation=True )
def read_csv_file(filename):
    data = pd.read_csv(filename, index_col=0)

    return data

def build_report(cx, head, subhead, filename):
    cx.header( head )
    cx.subheader(subhead)
    cx.text(filename)
    filename = f'./{filename}'

    rel1 = read_csv_file( filename )

    cx.dataframe(rel1, height=500)

def price_density_maps( data, geofile ):
    st.title( 'Region Overview' )

    m1, m2 = st.columns( (1, 1) )

    # maps_df = data.copy()
    maps_df = data.sample( 100 )

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
    
    m1.header( 'Portfolio Density' )
    with m1:
        folium_static( density_map )

    # Region Price Map
    m2.header( 'Price Density' )

    df_m2 = maps_df[['price', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
    df_m2.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin( df_m2['ZIP'].tolist() )]

    region_price_map = folium.Map( location=[data['lat'].mean(),
            data['long'].mean()],
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

def build_multiselect( msg, filter ):
    return st.sidebar.multiselect(
        msg,
        filter
    )

def data_overview( data ):
    f_attributes = build_multiselect( 'Enter columns', data.columns )

    f_zipcode = build_multiselect( 'Enter zipcode', data.zipcode.unique() )

    if (f_attributes != []) and (f_zipcode != []):
        data = data.loc[data['zipcode'].isin( f_zipcode ), f_attributes]
    elif (f_attributes != []) and (f_zipcode == []):
        data = data.loc[:, f_attributes]
    elif (f_attributes == []) and (f_zipcode != []):
        data = data.loc[data['zipcode'].isin( f_zipcode ), :]
    else:
        data = data.copy()

    #st.dataframe( data.head() )

    return data

def main():
    st.set_page_config(layout="wide")
    st.title( 'Dashboard de Insights da House Rocket' )

    
    st.sidebar.write("Para mais informações sobre as análises performadas neste Dashboard, você pode acessar este Repositório do GitHub")

    # Primeira Seção: Relatórios
    c1, c2 = st.columns((1, 1))

    build_report(c1, 'Relatório #1', 'Quais os imóveis que a House \
Rocket deveria COMPRAR e por qual preço?', 'report1.csv')
    
    build_report(c2, 'Relatório #2', 'Uma vez comprados, \
quando será a melhor época para VENDER e por qual preço?', 'report2.csv')

    # Segunda Seção: Construindo Visualizações
    st.header( 'Hipóteses de Negócio Validadas' )
    
    # Importando o dataframe resultante das análises do arquivo 'notebook.ipynb'
    filename = f'./resulting_data.csv'
    data = read_csv_file( filename )

    # Plottando as visualizações das hipóteses H1 e H2
    c1, c2 = st.columns((1, 1))

    c1.subheader('H1) Imóveis que possuem vista para o mar, são 20% mais caros, na média.')
    
    gh1 = sns.catplot(data=data, x='waterfront', y='price', kind='box')
    gh1.set(title='Média do preço do imóvel por Vista do Mar', ylabel='Preço do imóvel (USD)', xlabel='Vista para o Mar [Sim=1, Não=0]')
    c1.pyplot(gh1, use_container_width=True, heigth=20)

    c2.subheader('H2) Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')

    fig_h2, ax = plt.subplots()

    sns.regplot(data=data, x='yr_built', y='price', ax=ax, x_estimator=np.mean)
    ax.annotate(text='1950', xy=[1950, data.loc[data['yr_built'] == 1950, 'price'].mean()], xytext=[1950, 600000], \
        arrowprops=dict(arrowstyle="->",
                                color="gray",
                                patchB=None,
                                shrinkB=0,
                                ))

    ax.set_title('Preço versus Data de Construção', fontsize=15)
    ax.set_ylabel('Preço do imóvel (USD)')
    ax.set_xlabel('Ano de construção')

    c2.pyplot(fig_h2, use_container_width=True, heigth=20)

    # Plottando as visualizações das hipóteses H3 e H4
    c3, c4 = st.columns((1, 1))
    
    c3.subheader('H3) Imóveis sem porão - possuem área total (sqft_lot) - 40% maiores do que os imóveis com porão.')
    fig_h3, ax = plt.subplots()

    ax.hist(data.loc[~(data['sqft_basement'] == 0)]['sqft_lot'], color='r', histtype='step', label='COM Porão')
    ax.hist(data.loc[data['sqft_basement'] == 0]['sqft_lot'], color='b', histtype='step', label='SEM Porão')
    ax.set_title('Distribuição do Preço dos imóveis por Porão', fontsize=15)
    ax.set_ylabel('Qtd. de imóveis')
    ax.set_xlabel('Preço do imóvel (USD)')

    ax.legend()
    c3.pyplot(fig_h3, use_container_width=True)
    
    c4.subheader('H4) O crescimento do preço dos imóveis YoY (Year over Year) é de 10%.')
    yoy = data.groupby('year').agg({'price': ['mean', 'std']})
    fig_h4, ax = plt.subplots()

    ax.bar('2014', yoy.loc[2014].price['mean'], yerr=yoy.loc[2014].price['std'])
    ax.bar('2015', yoy.loc[2015].price['mean'], yerr=yoy.loc[2015].price['std'])
    ax.set_ylabel('Preço médio (USD)')
    ax.set_xlabel('Ano')
    ax.set_title('Crescimento YoY nos preços dos Imóveis', fontsize=15)
    c4.pyplot(fig_h4, use_container_width=True)

    # Plottando as visualizações das hipóteses H5 e H6
    c5, c6 = st.columns((1, 1))

    c5.subheader('H5) Imóveis com 3 banheiros tem um crescimento de MoM (Month over Month) médio de 15%.')

    # Lógica do gráfico
    mom = data.loc[data['bathrooms'] == 3].groupby('month').agg({'price': 'mean'}).reset_index()

    fig_h5, ax = plt.subplots()

    ax.plot(mom['month'], mom['price'], marker='o', linestyle='--')
    ax.set_title('Crescimento MoM do preço dos imóveis com 3 banheiros', fontsize=15)
    ax.set_ylabel('Preço do imóvel (USD)')
    ax.set_xlabel('Mês')
    
    c5.pyplot(fig_h5, use_container_width=True)

    c6.subheader('H6) Imóveis com mais números de quarto são em média 10% mais caros do que outros imóveis.')

    # Lógica do gráfico
    gh6 = sns.catplot(data=data, x='bedrooms', y='price', kind='point')
    gh6.set(title='Média do preço dos imóveis por número de quartos', ylabel='Preço dos imóveis (USD)', \
        xlabel='Número de quartos')

    c6.pyplot(gh6, use_container_width=True)

    # Plottando as visualizações das hipóteses H7 e H8
    c7, c8 = st.columns((1, 1))

    c7.subheader('H7) A variação média no preço dos imóveis entre as categorias da variável *condition*, indicam um acréscimo médio de 20% de uma para outra.')
    
    # Lógica do gráfico
    fig_h7, ax = plt.subplots()

    sns.regplot(x=data['condition'].astype(int), y=data['price'], ax=ax)
    ax.set_title('Preço do imóvel por condição', fontsize=15)
    ax.set_ylabel('Preço do imóvel (USD)')
    ax.set_xlabel('Condição')

    c7.pyplot(fig_h7, use_container_width=True)

    c8.subheader('H8) Imóveis em más condições mas COM vista para o mar, são em média 40% mais caros do que aqueles em mesmas condições mas SEM vista para o mar.')
    
    # Lógica do gráfico
    gh8 = sns.catplot(data=data, x='condition', y='price', hue='waterfront', kind='bar', legend=False)
    gh8.set(title='Preço do imóvel por condição', xlabel='Condição', ylabel='Preço do imóvel (USD)')

    plt.legend(loc='upper right', title='Vista para o Mar')

    c8.pyplot(gh8, use_container_width=True)

    # Plottando as visualizações das hipóteses H9 e H10
    c9, c10 = st.columns((1, 1))

    c9.subheader('H9) Para cada nível da variável "grade", o preço médio dos imóveis aumenta em 18%.')

    # Lógica do gráfico
    df_h9 =  data.groupby('grade').agg({'price': 'mean'}).reset_index()
    fig_h9, ax = plt.subplots()

    sns.barplot(data=df_h9, x='grade', y='price', ax=ax)
    ax.set_title('Preço do imóvel por Grade')
    ax.set_xlabel('Grade')
    ax.set_ylabel('Preço do imóvel (USD)')

    c9.pyplot(fig_h9, use_container_width=True)

    c10.subheader('H10) O crescimento WoW (Week over Week) do preço das propriedades é de 0.1%, na média.')

    # Lógica do gráfico
    fig_h10, ax = plt.subplots()

    gh10 = sns.lineplot(data=data, x='week', y='price', markers=True, ax=ax)
    gh10.set(title='Preço do imóvel WoW (Week over Week)', xlabel='Semana', ylabel='Preço do imóvel (USD)')

    c10.pyplot(fig_h10, use_container_width=True)

    # Terceira Seção: Mapas
    st.header( 'Mapas' )



if __name__ == '__main__':
    main()