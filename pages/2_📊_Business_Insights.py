import pandas as pd
import streamlit as st
import plotly.express as px
import statsmodels.api as stm

from PIL import Image

# Read data
@st.cache(allow_output_mutation=True)
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )

    return data


def main():
    st.set_page_config(layout='wide', page_title='Dashboard de Insights da House Rocket', page_icon=':thumbsup:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    # Title
    st.markdown('# Business Insights')
    st.write('Nesta seção são levantadas hipóteses que podem ser úteis na tomada de decisão do CEO da empresa, ao analisar o portfólio de imóveis.')

    # ETL
    ## Extract
    filepath = 'recommended_houses.csv'
        
    data = get_data(filepath)

    ## Transform
    #data = data_transform(data)

    ## Load
    ### Plots
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    c5, c6 = st.columns(2)
    c7, c8 = st.columns(2)
    c9, c10 = st.columns(2)

    # Hyphotesis 01
    c1.subheader('H1) Imóveis que possuem vista para o mar, são 20% mais caros, na média.')
    c1.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    fig_h1 = px.box(data, x="waterfront", y="price", labels={
        'price': 'Preço do imóvel (USD)',
        'waterfront': 'Vista para o Mar (0=Sem | 1=Com)'
    }, height=290 )
    fig_h1.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c1.plotly_chart(fig_h1, use_container_width=True)
    # Hyphotesis 02
    c2.subheader('H2) Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    c2.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h2 = data.groupby('new_house').agg({'price': 'mean'}).reset_index()
    fig_h2 = px.pie(df_h2, values="price", names=["Old house (< 1955)", "New house (> 1955)"], labels={
        'price': 'Preço do imóvel (USD)',
        'new_price': 'Ano de Construção (0=< 1955 | 1=>= 1955)'
    }, height=290 )
    fig_h2.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c2.plotly_chart(fig_h2, use_container_width=True)

    # Hyphotesis 03
    c3.subheader('H3) Imóveis sem porão - possuem área total (sqf|t_lot) - são 40% maiores do que os imóveis com porão.')
    c3.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    fig_h3 = px.box(data, x="sqft_lot", color="has_basement", labels={
        'price': 'Preço do imóvel (USD)',
        'count': 'Contagem',
        'has_basement': 'Tem Porão',
    }, category_orders={'has_basement': ['Não', 'Sim']}, height=290 )
    fig_h3.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c3.plotly_chart(fig_h3, use_container_width=True)

    # Hyphotesis 04
    c4.subheader('H4) O crescimento do preço dos imóveis YoY (Year over Year) é de 10%.')
    c4.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h4 = data.groupby('year').agg({'price': 'mean'}).reset_index()
    fig_h4 = px.bar(df_h4, x="year", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h4.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c4.plotly_chart(fig_h4, use_container_width=True)

    # Hyphotesis 05
    c5.subheader('H5) Imóveis com 3 banheiros tem um crescimento de MoM (Month over Month) médio de 15%.')
    c5.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h5 = data.loc[data['bathrooms'] == 3].groupby('month').agg({'price': 'mean'}).reset_index()
    fig_h5 = px.line(df_h5, x="month", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h5.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c5.plotly_chart(fig_h5, use_container_width=True)

    # Hyphotesis 06
    c6.subheader('H6) Imóveis com mais números de quarto são em média 10% mais caros do que outros imóveis com 1 unidade de quartos a menos, em média.')
    c6.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h6 = data.groupby('bedrooms').agg({'price':'mean'}).reset_index()
    fig_h6 = px.bar(df_h6, x='bedrooms', y='price', labels={
        'price': 'Preço médio do imóvel (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h6.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c6.plotly_chart(fig_h6, use_container_width=True)

    # Hyphotesis 07
    c7.subheader('H7) A variação média no preço dos imóveis entre as categorias da variável *condition*, indicam um acréscimo médio de 20% de uma para outra.')
    c7.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    fig_h7 = px.scatter(data, x="condition", y="price", trendline="ols", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h7.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c7.plotly_chart(fig_h7, use_container_width=True)

    # Hyphotesis 08
    c8.subheader('H8) Imóveis em más condições mas COM vista para o mar, são em média 40% mais caros do que aqueles em mesmas condições mas SEM vista para o mar.')
    c8.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h8 = data.groupby(['waterfront', 'condition']).agg({'price':'mean'}).reset_index()
    fig_h8 = px.bar(df_h8, x='condition', y='price', color='waterfront', labels={
        'price': 'Preço médio do imóvel (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h8.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c8.plotly_chart(fig_h8, use_container_width=True)

    # Hyphotesis 09
    c9.subheader("H9) Para cada nível da variável 'grade', o preço médio dos imóveis aumenta em 18%.")
    c9.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h9 = data.groupby('grade').agg({'price': 'mean'}).reset_index()
    fig_h9 = px.bar(df_h9, x="grade", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h9.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c9.plotly_chart(fig_h9, use_container_width=True)

    # Hyphotesis 10
    c10.subheader('H10) O crescimento WoW (Week over Week) do preço das propriedades é de 0.1%, na média.')
    c10.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    df_h10 = data.groupby('week').agg({'price': 'mean'}).reset_index()
    fig_h10 = px.line(df_h10, x='week', y='price', labels={
        'price': 'Preço médio do imóvel (USD)',
        'year': 'Ano'
    }, height=290 )
    fig_h8.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c10.plotly_chart(fig_h10, use_container_width=True)

    ### Sidebar
    st.sidebar.write('This is the sidebar.')

if __name__ == '__main__':
    main()