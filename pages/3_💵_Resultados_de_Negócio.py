import pandas as pd
import streamlit as st
import plotly.express as px

from datetime import datetime

from PIL import Image

# Read data
@st.cache(allow_output_mutation=True)
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0, parse_dates=['date'] )
    data = data[data['status'] == 'Buy'].copy()

    return data

def main():
    st.set_page_config(layout='wide', page_title='Resultados de Negócio | Dashboard de Insights da House Rocket', page_icon=':dollar:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    # Title
    st.markdown('# Resultados de Negócio')

    # ETL
    ## Extract
    filepath = 'data/recommended_houses.csv'
        
    data = get_data(filepath)

    ## Transform
    #data = data_transform(data)

    ## Load
    st.write(f'Nesta seção são mostrados os ganhos experados com a COMPRA e VENDA dos {data.shape[0]} imóveis recomendados nesta análise de negócio, e com os conhecimentos extraídos na validação de hipóteses de negócio.')

    c1, c2, c3, = st.columns(3)

    # Preço total de venda dos imóveis recomendados
    c1.metric(label=f"Preço total de COMPRA dos {data.shape[0]} imóveis", value="USD $2,1B")
    # Lucro gerado na venda dos imóveis recomendados
    c2.metric(label=f"Preço total da VENDA dos {data.shape[0]} imóveis", value="USD $2,53B")
    # Lucro gerado na venda dos imóveis recomendados
    c3.metric(label=f"Lucro total:", value="USD $430M", delta=f"20.5%")

    st.subheader('100 melhores negócios')
    c1, c2 = st.columns(2)

    with c1:
        df = data.sort_values(by='Profit')[:100]
        fig = px.scatter_mapbox( df,
            lat='lat',
            lon='long',
            color='price',
            size='Profit',
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15,
            zoom=9.5 )

        fig.update_layout( mapbox_style='open-street-map' )
        fig.update_layout( height=600, margin={'r': 0, 'l': 0, 'b': 0, 't': 0})
        st.plotly_chart(fig)
    with c2:
        st.dataframe(df, height=600)

    st.subheader('Total de imóveis vendidos por dia e por sazonalidade')
    df_2 = data.groupby(['date', 'season']).agg({'id': 'count'})
    df_2 = df_2['2014-06-01':].reset_index()
    fig2 = px.line(df_2, x='date', y='id', color='season', labels={
        'id': 'Quantidade',
        'date': 'Data',
        'season': 'Estação do Ano'
    })
    fig2.update_layout(margin={"b": 0, "l": 0, "r": 0, "t": 0})
    st.plotly_chart(fig2, use_container_width=True)

    with st.sidebar:
        st.markdown('# Sobre')
        st.markdown('Construido por **Gustavo Barros**')
        st.markdown('Se você quiser procurar por mais informações sobre este projeto ou entrar em contato comigo, consulte meu [Portfólio de Projetos](https://gustavobarros11.github.io/) ou [Github](https://github.com/GustavoBarros11).')
        st.markdown('___')


if __name__ == '__main__':
    main()