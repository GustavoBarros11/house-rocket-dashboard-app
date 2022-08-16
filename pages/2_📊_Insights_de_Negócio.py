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
    st.set_page_config(layout='wide', page_title='Insights de Negócio | Dashboard de Insights da House Rocket', page_icon=':bar-chart:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    # Title
    st.markdown('# Insights de Negócio')
    st.write('Nesta seção foram levantadas hipóteses de negócio durante a análise dos dados do portfólio de imóveis da House Rocket,\
         que posteriormente foram validadas ou invalidadas tornando-se em insights acionáveis para a tomada de decisão do CEO da empresa.')

    # ETL
    ## Extract
    filepath = 'data/recommended_houses.csv'
        
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
    c1.write(':x: Inválida: Imóveis que possuem vista para o mar, são em média, 62.77% mais caros do que imóveis sem vista para o mar.')
    fig_h1 = px.box(data, x="waterfront", y="price", labels={
        'price': 'Preço do imóvel (USD)',
        'waterfront': 'Vista para o Mar (0=Sem | 1=Com)'
    }, color_discrete_sequence=["#8d3941"], height=290 )
    fig_h1.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c1.plotly_chart(fig_h1, use_container_width=True)
    # Hyphotesis 02
    c2.subheader('H2) Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    c2.write(':x: Inválida: Imóveis com data de construção menor que 1955, são em média apenas, 2.95% mais caros.')
    df_h2 = data.groupby('new_house').agg({'price': 'mean'}).reset_index()
    fig_h2 = px.pie(df_h2, values="price", names=["Velho (< 1955)", "Novo (> 1955)"], labels={
        'price': 'Preço do imóvel (USD)',
        'new_price': 'Ano de Construção (0=< 1955 | 1=>= 1955)'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h2.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c2.plotly_chart(fig_h2, use_container_width=True)

    # Hyphotesis 03
    c3.subheader('H3) Imóveis sem porão - possuem área total (sqft_lot) - são 40% maiores do que os imóveis com porão.')
    c3.write(':x: Inválida: Imóveis sem porão, são em média 2.00% maiores do que imóveis com porão.')
    fig_h3 = px.box(data, x="sqft_lot", color="has_basement", labels={
        'sqft_lot': 'Área total (m²)',
        'has_basement': 'Tem Porão',
    }, category_orders={'has_basement': ['Não', 'Sim']},color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h3.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c3.plotly_chart(fig_h3, use_container_width=True)

    # Hyphotesis 04
    c4.subheader('H4) O crescimento do preço dos imóveis YoY (Year over Year) é de 10%.')
    c4.write(':x: Inválida: Nota-se uma variação mínima negativa YoY de 0.04% no preço.')
    df_h4 = data.groupby('year').agg({'price': 'mean'}).reset_index()
    fig_h4 = px.bar(df_h4, x="year", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'year': 'Ano'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h4.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c4.plotly_chart(fig_h4, use_container_width=True)

    # Hyphotesis 05
    c5.subheader('H5) Imóveis com 3 banheiros tem um crescimento de MoM (Month over Month) médio de 15%.')
    c5.write(':x: Inválida: Imóveis com 3 banheiros obtiveram um crescimento MoM (Month over Month) de apenas 0.23%.')
    df_h5 = data.loc[data['bathrooms'] == 3].groupby('month').agg({'price': 'mean'}).reset_index()
    fig_h5 = px.line(df_h5, x="month", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'month': 'Mês'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h5.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c5.plotly_chart(fig_h5, use_container_width=True)

    # Hyphotesis 06
    c6.subheader('H6) Imóveis com mais números de quarto são em média 10% mais caros do que outros imóveis com 1 unidade de quartos a menos, em média.')
    c6.write(':x: Inválida: Imóveis com mais número de quartos, são em média 18.54% mais caros do que aqueles com uma unidade de quarto a menos.')
    df_h6 = data.groupby('bedrooms').agg({'price':'mean'}).reset_index()
    fig_h6 = px.bar(df_h6, x='bedrooms', y='price', labels={
        'price': 'Preço médio do imóvel (USD)',
        'bedrooms': 'Quartos'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h6.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c6.plotly_chart(fig_h6, use_container_width=True)

    # Hyphotesis 07
    c7.subheader('H7) A variação média no preço dos imóveis entre as categorias da variável *condition*, indicam um acréscimo médio de 20% de uma para outra.')
    c7.write(':white_check_mark: Válida: Entre as categorias da variável condition, averigou-se um acréscimo médio de 20.60% no preço do imóvel.')
    fig_h7 = px.scatter(x=data["condition"].astype(int), y=data["price"], trendline="ols", labels={
        'y': 'Preço dos imóveis (USD)',
        'x': 'Condição'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h7.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c7.plotly_chart(fig_h7, use_container_width=True)

    # Hyphotesis 08
    c8.subheader('H8) Imóveis em más condições mas COM vista para o mar, são em média 40% mais caros do que aqueles em mesmas condições mas SEM vista para o mar.')
    c8.write(':x: Inválida: Imóveis em más condições mas possuem vista para o mar, são em média 116.87% mais caros do que imóveis nas mesmas condições mas não possuem vista para o mar.')
    df_h8 = data.groupby(['waterfront', 'condition']).agg({'price':'mean'}).reset_index()
    fig_h8 = px.bar(df_h8, x='condition', y='price', color='waterfront', labels={
        'price': 'Preço médio dos imóveis (USD)',
        'condition': 'Condição',
        'waterfront': 'Vista p/ água'
    }, color_continuous_scale=["#8d3941", "#a8adba"], color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h8.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c8.plotly_chart(fig_h8, use_container_width=True)

    # Hyphotesis 09
    c9.subheader("H9) Para cada nível da variável 'grade', o preço médio dos imóveis aumenta em 25%.")
    c9.write(':white_check_mark: Válida: Para cada nível da variável "grade", o preço médio dos imóveis subiu em 25.59%.')
    df_h9 = data.groupby('grade').agg({'price': 'mean'}).reset_index()
    fig_h9 = px.bar(df_h9, x="grade", y="price", labels={
        'price': 'Preço médio dos imóveis (USD)',
        'grade': 'Grade'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h9.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c9.plotly_chart(fig_h9, use_container_width=True)

    # Hyphotesis 10
    c10.subheader('H10) O crescimento WoW (Week over Week) do preço das propriedades é de 0.1%, na média.')
    c10.write(':white_check_mark: Válida: O crescimento WoW (Week over Week) dos imóveis foi de apenas 0.1%, na média.')
    df_h10 = data.groupby('week').agg({'price': 'mean'}).reset_index()
    fig_h10 = px.line(df_h10, x='week', y='price', labels={
        'price': 'Preço médio dos imóveis (USD)',
        'week': 'Semana'
    }, color_discrete_sequence=["#8d3941", "#a8adba"], height=290 )
    fig_h8.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 40})
    c10.plotly_chart(fig_h10, use_container_width=True)

    ### Sidebar
    with st.sidebar:
        st.markdown('# Sobre')
        st.markdown('Construido por **Gustavo Barros**')
        st.markdown('Se você quiser procurar por mais informações sobre este projeto ou entrar em contato comigo, consulte meu [Portfólio de Projetos](https://gustavobarros11.github.io/) ou [Github](https://github.com/GustavoBarros11).')
        st.markdown('___')

if __name__ == '__main__':
    main()