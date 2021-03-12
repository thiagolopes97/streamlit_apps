# Importação das bibliotecas
import streamlit as st
import sys
sys.path.append('parts')
sys.path.append('images')
sys.path.append('data')
from parts.inicio import inicio_func
from parts.about import about_func
from parts.cenipa import cenipa_func
from parts.filtro import filtro_func
#from parts.mlapp import mlapp_func
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    # Estrutura da barra lateral
    st.sidebar.header("Multi App - Streamlit Sharing")
    st.sidebar.subheader("Por Thiago Lopes")

    # Menu de Páginas
    opcoes_menu = ("Início","FILTRO","CENIPA", "MLApp","Sobre mim")
    escolha = st.sidebar.selectbox("Escolha uma opção", opcoes_menu)

    if escolha == "Início":
        inicio_func()

    elif escolha == "FILTRO":
        filtro_func()

    elif escolha == "CENIPA":
        cenipa_func()

    elif escolha == "MLApp":
        #mlapp_func()
        st.markdown("# Em construção")



    elif escolha == 'Sobre mim':
        about_func()


if __name__ == '__main__':
    main()
