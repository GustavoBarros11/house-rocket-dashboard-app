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

def build_plot(c, df, title):
    return None

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

    ## Load
    ### Plots
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    c5, c6 = st.columns(2)
    c7, c8 = st.columns(2)
    c9, c10 = st.columns(2)

    # Hipótese 01
    c1.subheader('H1) Imóveis que possuem vista para o mar, são 20% mais caros, na média.')
    c1.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    fig_h1 = px.box(data, x="waterfront", y="price", labels={
        'price': 'Preço do imóvel (USD)',
        'waterfront': 'Vista para o Mar (0=Sem | 1=Com)'
    }, height=290 )
    fig_h1.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c1.plotly_chart(fig_h1, use_container_width=True)
    # Hipóteses 02
    c2.subheader('H2) Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    c2.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar impoveis e reformá-los.')
    fig_h2 = px.scatter(data, x="yr_built", y="price", trendline="ols", labels={
        'price': 'Preço do imóvel (USD)',
        'waterfront': 'Vista para o Mar (0=Sem | 1=Com)'
    }, height=290 )
    fig_h2.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c2.plotly_chart(fig_h2, use_container_width=True)

    ### Sidebar
    st.sidebar.write('This is the sidebar.')

if __name__ == '__main__':
    main()