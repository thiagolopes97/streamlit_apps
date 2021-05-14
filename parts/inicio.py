# Importação das bibliotecas
import streamlit as st
import numpy as np
import cv2
from PIL import Image

# Definição da página de início do app
def inicio_func():
    st.title("Multi App - Thiago Lopes")
    st.markdown("""Aplicativo criado utilizando a biblioteca Streamlit e Hospedada no Streamlit Sharing para 
                   compartilhar projetos/ scripts/ conhecimento. Todo conteúdo pode ser encontrado em meu 
                   **[GitHub](https://github.com/thiagolopes97)**""")
                   
    st.markdown("""O app está dividido em Projetos, que podem ser selecionados na barra lateral a esquerda. Logo abaixo
                    é apresentado quais projetos foram já desenvolvidos e uma prévia de suas funcionalidades.
                """)
    st.header("Filtro - App")
    st.markdown("""**1º** Projeto da Masterclass Introdução à Visão Computacional, do Carlos Melo (Sigmoidal).
                Para saber mais sobre a Masterclass, acesse [esta página](https://pay.hotmart.com/K44730436X?checkoutMode=10&bid=1608039415553).
                Link do [Script](https://github.com/thiagolopes97/streamlit_apps/blob/master/parts/filtro.py) no Github.""")
    st.subheader("Exemplo de funcionalidade do app")
    col1, col2 = st.beta_columns(2)

    our_image = Image.open("images/empty.jpg")
    exe_image = Image.open("images/img1.jpg")

    converted_exe = np.array(exe_image.convert('RGB'))
    gray_image = cv2.cvtColor(converted_exe, cv2.COLOR_RGB2GRAY)

    col1.header("Original")
    col1.image(converted_exe, use_column_width=True)
    col2.header("Grayscale")
    col2.image(gray_image, use_column_width=True)


    st.header("Visualização de Dados de acidente aêreo - CENIPA")
    st.markdown("""**2º** Projeto da Masterclass Introdução à Visão Computacional, do Carlos Melo (Sigmoidal).
                Para saber mais sobre a Masterclass, acesse [esta página](https://pay.hotmart.com/K44730436X?checkoutMode=10&bid=1608039415553).
                Link do [Script](https://github.com/thiagolopes97/streamlit_apps/blob/master/parts/cenipa.py) no Github.""")
    st.subheader("Exemplo de funcionalidade do app")
    img = Image.open('images/exemplo1.png')
    st.image(img, caption="Visualização dos dados do CENIPA", use_column_width=True)

    st.header("MML First App")
    st.markdown(""" Projeto de aplicação direta de modelos de Machine Learning em alguns datasets distintos.
                """)
    st.subheader("Exemplo de funcionalidade do app")
    st.markdown("# Em construção")


