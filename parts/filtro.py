'''
    1º Projeto da Masterclass de visão computacional do mestre Carlos Melo
    #FamíliaSigmoidal
'''

# Importação das bibliotecas
import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance

def filtro_func():
    st.sidebar.header("Thiago Lopes - App Filtro")
    st.sidebar.info("Aplicativo desenvolvido 100% em Python")
    st.sidebar.markdown("App para aplicar filtros em imagens, utilizando a bilioteca OpenCV.")

    OUTPUT_WIDTH = 450
    # Estrutura cabeçalho da página
    st.title("App Filtro - Filtro")
    st.text("por Thiago Lopes")
    # Carregamento e exibição da imagem
    st.subheader("Carregar arquivo de imagem")
    image_file = st.file_uploader("Escolha uma imagem", type=['jpg', 'jpeg', 'png'])

    col1, col2 = st.beta_columns(2)

    if image_file is not None:

        # Loading da imagem e conversão dos canais
        our_image = Image.open(image_file)
        converted_image = np.array(our_image.convert('RGB'))
        image_BGR = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)

        # Opções de filtros
        filtros = st.sidebar.radio("Filtros", ['Original', 'Grayscale', 'Desenho', 'Sépia', 'Blur',
                                               'Canny', 'Contraste', 'Brilho', 'Sharpen', 'Mexican hat'])
        if filtros == 'Grayscale':
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Grayscale")
            col2.image(gray_image, use_column_width=True)

        elif filtros == 'Desenho':
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
            inv_gray_image = 255 - gray_image
            blur_image = cv2.GaussianBlur(inv_gray_image, (21, 21), 0, 0)
            sketch_image = cv2.divide(gray_image, 255 - blur_image, scale=256)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Desenho")
            col2.image(sketch_image, use_column_width=True)

        elif filtros == 'Sépia':
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia_image = cv2.filter2D(image_BGR, -1, kernel)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Sépia")
            col2.image(sepia_image, channels="BGR", use_column_width=True)

        elif filtros == 'Blur':
            b_amount = st.sidebar.slider("Kernel (n x n)", 3, 27, 9, step=2)
            blur_image = cv2.GaussianBlur(image_BGR, (b_amount, b_amount), 0, 0)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Blur")
            col2.image(blur_image, channels="BGR", use_column_width=True)

        elif filtros == 'Canny':
            blur_image = cv2.GaussianBlur(converted_image, (11, 11), 0)
            canny = cv2.Canny(blur_image, 100, 150)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Canny Edge Detection")
            col2.image(canny, use_column_width=True)

        elif filtros == "Contraste":
            c_amount = st.sidebar.slider("Constraste", 0.0, 2.0, 1.0)
            enhancer = ImageEnhance.Contrast(our_image)
            contrast_image = enhancer.enhance(c_amount)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Contraste")
            col2.image(contrast_image, use_column_width=True)

        elif filtros == "Brilho":
            c_amount = st.sidebar.slider("Constraste", 0.0, 2.0, 1.0)
            enhancer = ImageEnhance.Brightness(our_image)
            bright_image = enhancer.enhance(c_amount)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Brilho")
            col2.image(bright_image, use_column_width=True)

        elif filtros == 'Sharpen':
            filter = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            sharpen_img = cv2.filter2D(image_BGR, -1, filter)
            sharpen_img = cv2.cvtColor(sharpen_img, cv2.COLOR_BGR2RGB)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Sharpen")
            col2.image(sharpen_img, use_column_width=True)

        elif filtros == 'Mexican hat':
            filter = np.array(
                [[0, 0, -1, 0, 0], [0, -1, -2, -1, 0], [-1, -2, 16, -2, -1], [0, -1, -2, -1, 0], [0, 0, -1, 0, 0]])
            hat_img = cv2.filter2D(image_BGR, -1, filter)
            hat_img = cv2.cvtColor(hat_img, cv2.COLOR_BGR2RGB)
            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Mexican hat")
            col2.image(hat_img, use_column_width=True)
        elif filtros == 'Original':
            st.image(our_image, width=OUTPUT_WIDTH)
        else:
            st.image(our_image, width=OUTPUT_WIDTH)
