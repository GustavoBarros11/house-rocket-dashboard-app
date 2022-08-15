import pandas as pd
import streamlit as st

from PIL import Image

def main():
    st.set_page_config(layout='wide', page_title='Dashboard de Insights da House Rocket', page_icon=':thumbsup:')

    header_img = Image.open("images/header_v2_rounded.png")

    st.image(header_img, use_column_width=True)

    # Title
    st.markdown('# Resultados de Negócio')
    st.write('Nesta seção são mostrados os ganhos experados com a COMPRA e VENDA dos imóveis recomendados nesta análise de negócio, e com os conhecimentos extraídos na validação de hipóteses de negócio.')

if __name__ == '__main__':
    main()