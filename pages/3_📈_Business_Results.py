from string import hexdigits
import pandas as pd
import streamlit as st
import plotly.express as px

from PIL import Image

# Read data
@st.cache(allow_output_mutation=True)
def get_data( filepath ):
    data = pd.read_csv( filepath, index_col=0 )
    data = data[data['status'] == 'Buy'].copy()

    return data

def main():
    st.set_page_config(layout='wide', page_title='Dashboard de Insights da House Rocket', page_icon=':thumbsup:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    # Title
    st.markdown('# Resultados de Negócio')
    st.write('Nesta seção são mostrados os ganhos experados com a COMPRA e VENDA dos imóveis recomendados nesta análise de negócio, e com os conhecimentos extraídos na validação de hipóteses de negócio.')

    # ETL
    ## Extract
    filepath = 'recommended_houses.csv'
        
    data = get_data(filepath)

    ## Transform
    #data = data_transform(data)

    ## Load

    c1, c2, c3, c4 = st.columns(4)

    # Preço de compra de todos os imóveis recomendados
    c1.metric(label="Imóveis Recomendados", value=data.shape[0], delta="100% dos imóveis", delta_color="off")
    # Preço total de venda dos imóveis recomendados
    c2.metric(label=f"Preço total de COMPRA dos {data.shape[0]} imóveis", value=f"${data['price'].sum():,.2f}")
    # Lucro gerado na venda dos imóveis recomendados
    c3.metric(label=f"Preço total da VENDA dos {data.shape[0]} imóveis", value=f"${data['Sell Price'].sum():,.2f}")
    # Lucro gerado na venda dos imóveis recomendados
    c4.metric(label=f"Lucro total:", value=f"${data['Profit'].sum():,.2f}", delta=f"{data['Profit'].sum()/data['price'].sum()*100:.1f}%")

    st.subheader('100 melhores negócios')
    c1, c2 = st.columns(2)

    with c1:
        df = data.sort_values(by='Profit')[:100]
        fig = px.scatter_mapbox( df,
            lat='lat',
            lon='long',
            color='price',
            size='Profit',
            color_continuous_scale=px.colors.sequential.dense,
            size_max=15,
            zoom=9.5 )

        fig.update_layout( mapbox_style='open-street-map' )
        fig.update_layout( height=600, margin={'r': 0, 'l': 0, 'b': 0, 't': 0})
        st.plotly_chart(fig)
    with c2:
        st.dataframe(df, height=600)


if __name__ == '__main__':
    main()